#!/usr/bin/env python

import csv
import datetime
import dateutil.relativedelta
import sys, getopt


today = datetime.date.today()
d = (datetime.date(today.year,today.month,1) - dateutil.relativedelta.relativedelta(days=1))
lastMonth = d.strftime("%B")

#cols=['YUABCGEN',2,'3BC2', d.strftime("%d-%b-%Y")]

def main(argv):

    defaultIn = "nws.backups.%s.csv" % lastMonth
    defaultOut = "nws.backups.FUPLOAD.%s.csv" % lastMonth
    inputfile = defaultIn
    outputfile = defaultOut
    try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
      print 'dothething.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'dothething.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

    letsDoIt(inputfile,outputfile)


def letsDoIt(i,o):
  total=0;
  with open(i, 'rb') as csvfile:
    csvfile.next()
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
      total+=float(row[5][1:])
      




if __name__ == "__main__":
    main(sys.argv[1:])
