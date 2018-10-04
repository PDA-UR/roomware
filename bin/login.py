#!/usr/bin/python3
# -*- coding: utf-8 -*-

# novell eDirectory access
# https://www.novell.com/coolsolutions/feature/15853.html last access: 20.09.2018
# nds.py (Raphael Wimmer)

import ldap


class LDAPConnection:
    __port = 0
    def __init__( self):
        self.__host = 'ldaps://ldap3.ur.de'
        self.__port = '636'
        self.user = ''
        self.__binddn = 'cn=mel45452,ou=mi,ou=sprachlit,o=uni-regensburg,c=de'
        #self.__password = password
        scope = "sub"
        if scope.upper() == "SUB":
            self.__scope = ldap.SCOPE_SUBTREE
        elif scope.upper() == "ONE":
            self.__scope = ldap.SCOPE_ONE
        else:
            self.__scope = ldap.SCOPE_BASE
            
    @property
    def get_username(self):
        return self.user
        
    @get_username.setter
    def get_username(self, username):
        self.user = username
            
    def __connect( self, host, binddn, password, port=636 ):
        handle = ldap.initialize(host)
        return handle
    
    def __search( self, handle, basedn, filter, scope=ldap.SCOPE_SUBTREE):
        if not handle:
            return False
        results = handle.search_s( basedn, scope, filter )
        self.__binddn = results[0][0]
        print(self.__binddn)
        return handle.search_s( basedn, scope, filter )
        
    def authenticate(self, handle, user, password):
        if not handle:
            return False

        try:
            results = handle.simple_bind_s(self.__binddn, password)
            return True
        except:
            return False
       
    def print_dict(self, d):
        for key,val in d.items():
            #print(key, val)
            if key == 'urrzSurname':
                print(str(key) + ":")
                for i in val:
                    print(str(i))
            #else:
                #print("{}: {}".format(key, val))
            #print("")
            
    def logout(self, connection):
        connection.unbind()
      
                
    def TestConnection(self, user, password):
        # Create a test connection.
        # This will try to connect and search based on the
        # input given to the class.  If the connection fails,
        # it will return False.  If the connection succeeds
        # but there is nothing in the tree at the search base,
        # it will return False; so it is important to provide
        # real search data.
        self.user = user
        basedn = "o=uni-regensburg,c=de"
        filter = '(&(uid=' + self.user + ')(objectClass=inetorgperson))'
        self.ldap_connection = self.__connect(self.__host, self.__binddn, password, self.__port)
        self.__search(self.ldap_connection, basedn, filter, self.__scope)
        connection = self.authenticate(self.ldap_connection, self.user, password)
        print(self.ldap_connection)
        conn_ldap = [connection, self.ldap_connection]
        return conn_ldap
        

#LDAPConnection('raa', '').TestConnection()
#'mel45452', "d1ll.dapp
