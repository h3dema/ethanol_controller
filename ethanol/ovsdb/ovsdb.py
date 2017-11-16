#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# ##################################
#
# Copyright 2015 Henrique Moura
#
# This file is part of Ethanol.
#
# ##################################
#
#
"""
  OVSDB calls.
  see more information in https://tools.ietf.org/html/rfc7047

@author: Henrique Duarte Moura
@organization: WINET/DCC/UFMG
@copyright: h3dema (c) 2017
@contact: henriquemoura@hotmail.com
@licence: GNU General Public License v2.0
(https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
@since: July 2015
@status: in development
"""

import sys
import socket
import json
from select import select

class Ovsdb:

    def __init__(self, server_ip, server_port=6632, buffer_size=4096):
        self.server_ip = server_ip
        self.server_port = server_port
        self.buffer_size = buffer_size
        self.socket = None
        self.__id = 0

    @property
    def id(self):
        """message id (autoincrement)"""
        _id = self.__id
        self.__id += 1
        return _id

    def connect(self):
        """connect to the openvswitch ovsdb port"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_ip, self.server_port))

    def gather_data(self):
        """receive all json data"""
        if self.socket is None:
            return None
        result = ""
        while "error" not in result or "id" not in result or "result" not in result:
            # check if we got the whole thing
            # by verifying if we've received all the fields
            reply = self.socket.recv(self.buffer_size)
            result += reply
        return json.loads(result)

    def echo(self):
        """ perform an echo (ping) to the ovsdb """
        req = json.dumps({"method":"echo",
                          "id":"echo",
                          "params":[]})
        self.socket.send(req)
        return self.gather_data()

    def list_dbs(self):
        """list all databases"""
        req = json.dumps({"method":"list_dbs",
                           "params":[], 
                           "id": 0})
        self.socket.send(req)
        return self.gather_data()

    def monitor(self, db, columns, monitor_id=None, msg_id=None):
        msg = {"method":"monitor", "params":[db, monitor_id, columns], "id":msg_id}
        return json.dumps(msg)

    def monitor_cancel(self, db, columns, monitor_id=None, msg_id=None):
        assert monitor_id is not None, 'provide the correct monitor id (same as request)'
        msg = {"method":"monitor_cancel", "params":[db, monitor_id, columns], "id":msg_id}
        return json.dumps(msg)

    def list_bridges(self, db=None):
        """

        :param db: the database name
        :return: list of bridges
        """
        assert db is not None and isinstance(db, str), 'db should be a string with the database name'
        columns = {"Port": {"columns": ["fake_bridge",
                                        "interfaces",
                                        "name",
                                        "tag"]
                            },
                   "Controller": {"columns": []},
                   "Interface": {"columns": ["name"]},
                   "Open_vSwitch": {"columns": ["bridges", 
                                                "cur_cfg"]
                                    },
                   "Bridge": {"columns": ["controller",
                                          "fail_mode",
                                          "name",
                                          "ports"]
                              }
                   }
        id = self.id
        mon = self.monitor(columns, db, monitor_id=id, msg_id = id)
        self.socket.send(mon)
        result = self.gather_data()
        # TODO: cancel the monitor after we're done !!
        mon_cancel = self.monitor_cancel(columns, db, monitor_id=id)
        self.socket.send(mon_cancel)
        return result
    
    def get_schema(self, db):
        """
        get the database schema
        :param db: the database name
        :return:  A JSON object with the following members:

           "name": <id>                            required
           "version": <version>                    required
           "cksum": <string>                       optional
           "tables": {<id>: <table-schema>, ...}   required
        """
        assert db is not None and isinstance(db, str), 'db should be a string with the database name'
        req = json.dumps({"method": "get_schema",
                          "params":[db_name],
                          "id": current_id})
        self.socket.send(req)
        return self.gather_data()

    def list_tables(self, db):
        """
        get the tables from a database
        :param db:
        :return: A JSON object with the following members:

         "columns": {<id>: <column-schema>, ...}   required
         "maxRows": <integer>                      optional
         "isRoot": <boolean>                       optional
         "indexes": [<column-set>*]                optional
        """
        assert db is not None and isinstance(db, str), 'db should be a string with the database name'
        db_schema = self.get_schema(socket, db)
        return db_schema['tables']

    def list_table_names(self, db):
        """return a list of all table names"""
        assert db is not None and isinstance(db, str), 'db should be a string with the database name'
        return self.list_tables().keys()

if __name__ == '__main__':
    ovs = Ovsdb()
    if not ovs.connect():
        print "Cannot connect to database"
        sys.exit(0)

    current_id = 0

    db_list = ovs.list_dbs()
    db_name = db_list['result'][0]
    
    bridge_list = ovs.list_bridges(db_name)
    print "list bridges:", bridge_list
        
    bridges = bridge_list['result']['Bridge']
    print "\nbridges\n"
    print bridges.values()
    for bridge in bridges.values():
        print "---"
        print bridge['new']['name']

    print ovs.list_tables(db_name)