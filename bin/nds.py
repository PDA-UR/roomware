#!/usr/bin/env python3

# coding: utf-8
import ldap
import sys
from getpass import getpass
from string import Template

SERVER  = "ldaps://ldap.ur.de:636"
BIND_DN = "cn=mel45452,ou=mi,ou=sprachlit,o=uni-regensburg,c=de"
BASE_DN = "o=uni-regensburg,c=de"
SCOPE   = ldap.SCOPE_SUBTREE


def print_dict(d):
    for key,val in d.items():
        if type(val) is list:
            print(str(key) + ":")
            for i in val:
                print(str(i))
        else:
            print("{}: {}".format(key, val))
        print("")

query = sys.argv[1]
if "," in query:
    surname, givenname = query.split(",")
    query = Template("(&(urrzGivenName=$givenname)(urrzSurname=$surname))").substitute(surname=surname.strip(), givenname=givenname.strip())
elif not "=" in query:
    query = Template("(|(cn=$q)(urrzFullname=$q)(urrzGivenName=$q)(urrzSurname=$q))").substitute(q=query)
print(query)

l = ldap.initialize(SERVER)
#l.simple_bind(BIND_DN, getpass())
results = l.search_s(BASE_DN, SCOPE, query)
print("%d results:" % len(results))
for result in results:
    print(result[0])
    print_dict(result[1])

