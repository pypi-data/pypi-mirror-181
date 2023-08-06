#! /usr/bin/env python
# -*- coding:Utf-8 -*-

""" Excel system management.
    Keyword arguments:
        none
    Return self
"""
# ============================================================
#    Linux python path and Library import
# ============================================================
import pypyodbc as pyodbc
from sortedcontainers import SortedDict

from . import libLog

# ============================================================
#    Variables and Constants
# ============================================================

# None

# ============================================================
#    Class
# ============================================================


# ||||||||||||||||||||||||||||||||||||||||||||||||||
#    Sql
# ||||||||||||||||||||||||||||||||||||||||||||||||||
class Sql:
    """Class to manage the Sql system.
    Keyword arguments :
        none
    Return self
    """

    # //////////////////////////////////////////////////
    #    Variables and Constants
    # //////////////////////////////////////////////////

    # Variables
    hshParam = {}
    hshParam["Connections"] = {}
    hshParam["Dataname"] = SortedDict()
    hshParam["Queries"] = SortedDict()
    hshData = {}

    @property
    def data(self):
        return self.hshData

    # //////////////////////////////////////////////////
    #     INITIALIZATION
    # //////////////////////////////////////////////////
    def __init__(self, phshParam={}):
        """Initialization of the class
        Keyword arguments :
            phshParam -- the parameters dictionary
        Return self
        """

        # Work variables
        self.connections = {}
        self.cursors = {}
        self._last_count = None
        self._data_flag = False
        self._at_least_one_change = False

        # Start log manager
        self.log = libLog.Log()

        # Update of parameters
        self.hshParam.update(phshParam)

    # //////////////////////////////////////////////////
    #     Connections_Load
    # //////////////////////////////////////////////////
    def Connections_Load(self, penv=None, pconnectionfilter=None, **kw):
        """Loading connexion
        Keyword arguments :
            penv -- environment define. Ex : prod, dev, test...
            pconnectionfilter -- filter string in connection dictionary
        OPTIONS
            plogconnect -- Log level display for connect. "None" for no display (default=DEBUG)
        Return self
        """

        hshOption = {"plogconnect": "DEBUG"}

        # Setting dictionary option
        if isinstance(kw, dict):
            hshOption.update(kw)

        # Connection
        for k, v in self.hshParam["Connections"][penv].items():
            self.log.setStep = k
            if (pconnectionfilter or k) == k:
                self.connections[k] = pyodbc.connect(v)
                if hshOption["plogconnect"]:
                    self.log.Write(
                        self.log.LEVEL[hshOption["plogconnect"]],
                        "Connection to %s successfully",
                        self.log.setStep,
                    )

    # //////////////////////////////////////////////////
    #     Execute_Request
    # //////////////////////////////////////////////////
    def Execute_Request(self, pqueryfilter, pbind=None, ptransaction=None, **kw):
        """loading data in excel template
        Keyword arguments :
            pqueryfilter -- filter string in queries dictionary
            pbind -- the bind variables of queries (default=None)
            ptransaction -- Validation of transaction : "commit", "rollback", "standby" and, "None" (default) for select statement
        OPTIONS
            pcnxname -- Name of connection (default=value between point in query key)
            pcursorname -- Name of cursor (default=value between point in query key)
            pfetchtype -- Type of data fetch ; "fetchall" (default), fetchone
            plogrequest -- Log level display for request. "None" for no display (default=DEBUG)
            plogcolumn -- Log level display for column. "None" for no display (default=DEBUG)
            plogrow -- Log level display for row. "None" for no display (default=DEBUG)
            plogcount -- Log level display for count. "None" for no display (default=DEBUG)
            perrnochange -- Raise exception if no change with the request. Value expected, message or CustomException code. "None" for no display (default=None)
            perrrequest -- Log level display for request in error. "None" for no display (default=INFO)
        Return self
        """

        hshOption = {
            "pcnxname": None,
            "pcursorname": None,
            "pfetchtype": "fetchall",
            "plogrequest": "DEBUG",
            "plogcolumn": "DEBUG",
            "plogrow": "DEBUG",
            "plogcount": "DEBUG",
            "perrnochange": None,
            "perrrequest": "INFO",
        }
        _transaction = {
            "commit": "commit",
            "rollback": "rollback",
            "standby": "standby",
        }
        _fetchtype = {"fetchall": "fetchall", "fetchone": "fetchone"}

        # Setting dictionary option
        if isinstance(kw, dict):
            hshOption.update(kw)

        self._last_count = None
        self._data_flag = False
        self._at_least_one_change = False

        for k, v in filter(
            lambda x: pqueryfilter == x[0][: len(pqueryfilter)],
            self.hshParam["Queries"].items(),
        ):
            self.log.setStep = "Q[%s]" % k
            cnxname = hshOption["pcnxname"] or k.split(".")[1]
            cursorname = hshOption["pcursorname"] or k.split(".")[1]
            if pbind:
                SQL0 = v.format(**pbind)
            else:
                SQL0 = v
            if hshOption["plogrequest"]:
                self.log.Write(
                    self.log.LEVEL[hshOption["plogrequest"]],
                    "Request %s : %s",
                    k,
                    " ".join(SQL0.split()),
                )
            cnx0 = self.connections[cnxname]
            curs0 = self.cursors.setdefault(cursorname, cnx0.cursor())
            try:
                curs0.execute(SQL0)
            except Exception as e:
                if hshOption["perrrequest"]:
                    self.log.Write(
                        self.log.LEVEL[hshOption["perrrequest"]],
                        "Request %s : %s has problem : %s",
                        k,
                        " ".join(SQL0.split()),
                        str(e),
                    )
                raise
            count0 = curs0.rowcount
            if ptransaction:
                if count0 <= 0 and hshOption["perrnochange"]:
                    raise self.log.CustomException(hshOption["perrnochange"])
                if not ptransaction == "standby":
                    getattr(cnx0, _transaction[ptransaction])()
                if hshOption["plogcount"]:
                    self.log.Write(self.log.LEVEL[hshOption["plogcount"]], "Rowcount : %s", count0)
                if not count0 == 0:
                    self._at_least_one_change = True
            else:
                column0 = curs0.description
                rows0 = getattr(curs0, _fetchtype[hshOption["pfetchtype"]])()
                count0 = len(rows0 or [])
                if hshOption["plogcount"]:
                    self.log.Write(self.log.LEVEL[hshOption["plogcount"]], "Rowcount : %s", count0)
                if hshOption["plogcolumn"]:
                    self.log.Write(self.log.LEVEL[hshOption["plogcolumn"]], "Columns : %s", column0)
                if hshOption["plogrow"]:
                    self.log.Write(self.log.LEVEL[hshOption["plogrow"]], "Rows : %s", rows0)
                self.hshData["%s.H" % self.hshParam["Dataname"].get(k, k)] = column0
                self.hshData["%s.R" % self.hshParam["Dataname"].get(k, k)] = rows0
                if not count0 == 0:
                    self._data_flag = True
            self._last_count = count0
            self.log.setStep = ""
