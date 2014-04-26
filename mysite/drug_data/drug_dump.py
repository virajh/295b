#!/usr/bin/python

"""
By virajh

This script connects to local mysql instance and pulls the RXNORM data and formats it into a file which is then piped to django shell.
"""
import MySQLdb

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="x", # your password
                      db="erx") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

# Use all the SQL you like
cur.execute("SELECT str FROM RXNCONSO")

def writeToFile(divider, row):
    arr = row[0].split()
    try:
        drugFile = open('drug', 'a')
        k = arr.index(divider)
        i = 0
        if arr[0][0].isalpha():
            data = ""
            while (i <= k):
                data += "%s " %(arr[i])
                i += 1
            if len(data) < 50:
                print data
                word = "Drug(name='%s').save()" % (data.rstrip())
                drugFile.write(word)
                drugFile.write('\n')
                drugFile.close()
            else:
                pass
        else:
            pass
    except:
        pass


# print all the first cell of all the rows
for row in cur.fetchall():
    if 'MG/ML' in row[0]:
        writeToFile('MG/ML', row)

#    if 'MG' in row[0]:
#        writeToFile('MG', row)

#    if 'ML' in row[0]:
#        writeToFile('ML', row)

