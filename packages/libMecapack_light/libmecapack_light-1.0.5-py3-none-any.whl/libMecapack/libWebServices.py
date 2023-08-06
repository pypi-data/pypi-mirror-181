#! /usr/bin/env python
# -*- coding:Utf-8 -*-

""" WebServices system management.
    Keyword arguments:
        none
    Return self
"""

from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth
from suds.client import Client

import libMecapack.libLog as liblog


class webServices_WSDL:
    """
    _summary_

    Raises:
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """

    hshParam = {}
    __hshData = {}

    @property
    def data(self):
        return self.__hshData

    def __init__(self, phshParam={}):
        """permet la déclaration des variables de travail, et les init de variables de base
        Keyword arguments :
            phshParam -- the parameters dictionary
        Return self
        """
        # Work variables
        self.token = ""
        self.login = ""

        # Start log manager
        self.log = liblog.Log()

        # Update of parameters
        self.hshParam.update(phshParam)

    def Call(self, pqueryfilter):
        url = self.hshParam["address"].format(self.hshParam["request"][pqueryfilter]["address"])

        client = Client(url, username=self.hshParam["user"], password=self.hshParam["password"])
        request_data = self.hshParam["request"][pqueryfilter]["request_data"]

        method = getattr(client.service, self.hshParam["request"][pqueryfilter]["function"])
        result = method(**request_data)
        if result != "\n":
            self.__hshData[pqueryfilter] = result
        else:
            self.__hshData[pqueryfilter] = None


class webServices_Sylob:
    """Class to manage the webServices system.
    Keyword arguments :
        none
    Return self
    """

    # Variables
    hshParam = {}
    hshParam["auth_cognito"] = {}
    hshParam["auth"] = {}
    hshParam["request"] = {}
    __hshData = {}

    @property
    def data(self):
        return self.__hshData

    def __init__(self, phshParam={}):
        """permet la déclaration des variables de travail, et les init de variables de base
        Keyword arguments :
            phshParam -- the parameters dictionary
        Return self
        """
        # Work variables
        self.token = ""
        self.login = ""
        self.auth = None
        self.session = requests.Session()
        # Start log manager
        self.log = liblog.Log()

        # Update of parameters
        self.hshParam.update(phshParam)

    def __Authentification(self, **kw):
        """fonction appelée si l'appel au webservice renvoi un problème d'authentification
            ( accès forbidden error = 401, 403)
        OPTIONS
            plogconnect -- Log level display for connect. "None" for no display (default=DEBUG)
        Return self
        """
        hshOption = {"plogconnect": "DEBUG"}
        # Setting dictionary option
        if isinstance(kw, dict):
            hshOption.update(kw)
        address = self.hshParam["auth_cognito"]["address"]
        params = {
            "grant_type": "client_credentials",
            "scope": "ClientExterne/rest_read",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        auth = HTTPBasicAuth(
            self.hshParam["auth_cognito"]["login"],
            self.hshParam["auth_cognito"]["pwd"],
        )
        resp = self.session.post(
            address,
            headers=headers,
            params=params,
            auth=auth,
        )
        if resp.status_code != 200:
            raise Exception(f"POST /auth/ {resp.status_code}")
        if hshOption["plogconnect"]:
            self.log.Write(
                self.log.LEVEL[hshOption["plogconnect"]],
                f"Connection {self.log.setStep} successfully",
            )
        self.token = resp.json().get("access_token")
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        self.auth = HTTPBasicAuth(
            f"{self.hshParam['auth_cognito']['login']}@@{self.hshParam['auth']['societe']}@@{now}",
            f"oauth.clientcredentials.{self.token}",
        )

    # //////////////////////////////////////////////////
    #     Call
    # //////////////////////////////////////////////////
    def Call(self, pqueryfilter, pbind=None, pparameters=None, **kw):
        # def Call(self, pqueryfilter, pbind=None, pparameters=None, phisto=False, **kw):
        """
        Lancement du web services avec infos à passer et résultats stockés dans data

        Args:
            pqueryfilter (str): filter string in queries dictionary
            pbind (str, optional): the bind variables of queries. Defaults to None.
            pparameters (dict, optional): dict of key, value to send. Defaults to None.
            phisto (bool, optional): save into history or not. Defaults to False.

        Options:
            piteration (int): First launch function for authentication problems(not to be changed)
            plimit (int): Number of elements to load (default=99999)
            plogrequest (LOG_LEVEL): Log level display for request. "None" for no display (default=DEBUG)
        Raises:
            Exception: No connection

        Returns:
            cls: Self
        """
        hshOption = {"piteration": 0, "plogrequest": "DEBUG", "plimit": 99999}
        # Setting dictionary option
        if isinstance(kw, dict):
            hshOption.update(kw)

        for k, v in filter(
            lambda x: pqueryfilter == x[0][: len(pqueryfilter)],
            self.hshParam["request"].items(),
        ):
            self.log.setStep = f"R[{k}]"
            if pbind:
                req = v.format(**pbind)
            else:
                req = v
            site = f"{self.hshParam['auth']['address']}/query/{req}/resultat?limite={hshOption['plimit']}"
            if pparameters is not None:
                site = site + "&" + "&".join(f"{k}={v}" for (k, v) in pparameters.items())
            if hshOption["plogrequest"]:
                self.log.Write(
                    self.log.LEVEL[hshOption["plogrequest"]],
                    f"Request {k} : {site}",
                )

            resp = self.session.get(
                site,
                headers={"accept": "application/json"},
                auth=self.auth,
            )
            if resp.status_code in (401, 403, 500) and hshOption["piteration"] < 2:
                self.__Authentification()
                self.Call(
                    pqueryfilter,
                    pbind=pbind,
                    pparameters=pparameters,
                    **{
                        "piteration": hshOption["piteration"] + 1,
                        "plimit": hshOption["plimit"],
                    },
                )
                return None
            if resp.status_code != 200:
                raise Exception(f"get /{pqueryfilter}/ {resp.status_code}")
            self.__hshData[k] = self._mef_data_s9(resp.json())
            self.log.setStep = ""

    # //////////////////////////////////////////////////
    #     Action
    # //////////////////////////////////////////////////
    def Action(self, pcode, pbody=None, pparameters=None, **kw):
        """
        Lancement du web services avec infos à passer et résultats stockés dans data

        Args:
            pcode (str): Sylob9 Code Action
            pbody (dict, optional): dict question, answser for scenario. Defaults to None.
            pparameters (dict, optional): dict of key, value to send. Defaults to None.

        Options:
            piteration (int): First launch function for authentication problems(not to be changed)
            plogrequest (LOG_LEVEL): Log level display for request. "None" for no display (default=DEBUG)
            pcarriagereturn (str) : Carriage return used for multiples infos. (default="\n")

        Raises:
            Exception: No connection
            Exception: Returned Error
        Returns:
            cls: Self
        """
        hshOption = {"piteration": 0, "plogrequest": "DEBUG", "pcarriagereturn": "\n"}
        if isinstance(kw, dict):
            hshOption.update(kw)

        self.log.setStep = f"R[{pcode}]"
        site = f"{self.hshParam['auth']['address']}/v2/action/{pcode}/execute"
        if pparameters is not None:
            site = site + "&" + "&".join(f"{k}={v}" for (k, v) in pparameters.items())
        if hshOption["plogrequest"]:
            self.log.Write(
                self.log.LEVEL[hshOption["plogrequest"]],
                f"Request {pcode} : {site} = {pbody}",
            )

        resp = self.session.post(site, headers={"accept": "application/json"}, auth=self.auth, json=pbody)
        resp.encoding = "utf-8"
        if resp.status_code in (401, 403, 500) and hshOption["piteration"] < 2:
            self.__Authentification()
            hshOption["piteration"] += 1
            self.Action(
                pcode,
                pbody=pbody,
                pparameters=pparameters,
                **hshOption,
            )
            return None
        self.__hshData[pcode] = self._analyse_reponse_s9(resp.json(), hshOption["pcarriagereturn"])
        if hshOption["plogrequest"]:
            self.log.Write(
                self.log.LEVEL[hshOption["plogrequest"]],
                f"Response {pcode} : {resp.json()}",
            )
        self.log.setStep = ""

    def _analyse_reponse_s9(self, reponse, CR):
        retour = {}
        if not isinstance(reponse["status"], dict):
            # Erreur
            self.log.Error(f"Erreur {reponse['status']} : {reponse['errors']}")
            retour["status"] = "ERREUR"
            retour["info"] = CR.join([e["message"] + " : " + e["help"] for e in reponse["errors"]])
        elif "schema" in reponse:
            # saisie incomplète
            self.log.Error(f"Saisie incompète : {str(reponse['schema'])}")
            retour["status"] = "INCOMPLET"
            retour["info"] = reponse["schema"]
        elif reponse["status"]["success"]:
            retour["status"] = "OK"
            retour["info"] = "Traitement OK"
        elif not reponse["status"]["success"]:
            retour["status"] = "WARNING"
            retour["info"] = CR.join(reponse["status"]["messages"]) + " : " + CR.join(reponse["status"]["warnings"])

        else:
            self.log.Error(f"unknown response : {reponse}")
            retour["status"] = "ERREUR"
            retour["info"] = reponse
        return retour

    def _mef_data_s9(self, data):
        """
        Permet de créer un dictionnaire des éléments retournés par Sylob 9

        Args:
            data (json): Données json transmises par Sylob 9

        Returns:
            lst(dict): Tous les éléments mis en forme
        """
        ordre_colonne = []
        format = {}
        modele = {}
        retour = []
        # Déclaration des colonnes dans l'ordre
        ordre_colonne = data["colonne"]
        # Récupération des types attendus
        for col in data["colonneQueryWS"]:
            format[col["libelle"]] = col["type"]
        # enregistrement d'un dictionnaire modèle
        for k in ordre_colonne:
            modele[k] = ""
        # enregistrement de toutes les lignes
        for lig in data["ligneResultatWS"]:
            val = modele.copy()
            for idx, e in enumerate(lig["valeur"]):
                k = ordre_colonne[idx]
                if format[k] == "Boolean":
                    val[k] = True if e == "Vrai" else False
                else:
                    val[k] = e
            retour.append(val)
        return retour
