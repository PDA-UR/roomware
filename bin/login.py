#!/usr/bin/python3
# -*- coding: utf-8 -*-

# novell eDirectory access
# https://www.novell.com/coolsolutions/feature/15853.html last access: 20.09.2018
# nds.py (Raphael Wimmer)

import ldap

class LDAPConnection:
    __port = 0
    def __init__( self, user, password ):
        self.__host = 'ldaps://ldap3.ur.de'
        self.__port = '636'
        self.user = user
        self.__binddn = 'cn=' + self.user + ',ou=mi,ou=sprachlit,o=uni-regensburg,c=de'
        self.__password = password
        scope = "sub"
        if scope.upper() == "SUB":
            self.__scope = ldap.SCOPE_SUBTREE
        elif scope.upper() == "ONE":
            self.__scope = ldap.SCOPE_ONE
        else:
            self.__scope = ldap.SCOPE_BASE
            
    def __connect( self, host, binddn, password, port=636 ):
        print('connect')
        handle = ldap.initialize('ldaps://ldap3.ur.de:636')
        if handle:
            print('handle')
            handle.simple_bind_s( binddn, password )
            print('connected')
            return handle
        print('not connected')
        return False
    
    def __search( self, handle, basedn, filter, scope=ldap.SCOPE_SUBTREE):
        print('search')
        if not handle:
            print('search not found')
            return False
        print('search found')
        results = handle.search_s( basedn, scope, filter )
        for result in results:
            #print(result[0])
            self.print_dict(result[1])
        return handle.search_s( basedn, scope, filter )
        
    def print_dict(self, d):
        for key,val in d.items():
            #if type(val) is list:
            if key == 'urrzSurname':
                print(str(key) + ":")
                for i in val:
                    print(str(i))
            #else:
                #print("{}: {}".format(key, val))
            #print("")
                
    def TestConnection( self ):
        # Create a test connection.
        # This will try to connect and search based on the
        # input given to the class.  If the connection fails,
        # it will return False.  If the connection succeeds
        # but there is nothing in the tree at the search base,
        # it will return False; so it is important to provide
        # real search data.
        basedn = "o=uni-regensburg,c=de"
        filter = '(&(uid=' + self.user + ')(objectClass=inetorgperson))'
        self.__ldap_connection_handle = self.__connect( self.__host, self.__binddn, self.__password, self.__port )
        if not self.__ldap_connection_handle:
            return False
        return len( self.__search( self.__ldap_connection_handle, basedn, filter, self.__scope ) ) != 0

LDAPConnection('raa26335', '2Raumwohnung').TestConnection()

