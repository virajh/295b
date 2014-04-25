#!/usr/bin/python

"""
By virajh

This script connects to local mysql instance and pulls the RXNORM data and formats it into a file which is then piped to django shell.
"""

dataFile = open('NDF-RT.txt', 'r')

for line in dataFile:
    data = line.split()

    ndf_id = data.pop(0)
    ndf_data = ""

    for item in data:
        ndf_data += "%s " % ( str(item) )

    outputFile = open('NDF','a')
    outputFile.write("NDF(nui='%s', data='%s').save()" % (ndf_id, ndf_data.rstrip()))
    outputFile.write('\n')
    outputFile.close()

dataFile.close()
