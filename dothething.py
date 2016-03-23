#!/usr/bin/env python

import csv
import datetime
import dateutil.relativedelta
import sys, getopt

today = datetime.date.today()
d = (datetime.date(today.year,today.month,1) - dateutil.relativedelta.relativedelta(days=1))
lastMonth = d.strftime("%B")

cols=[]
with open('cols.cfg') as f:
  cols=f.read().splitlines()

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
  total=0.00;
  newrow=[]
  with open(i, 'rb') as ifile:
    ifile.next()
    reader = csv.reader(ifile, delimiter=',')
    for row in reader:
      purpose = row[6]+' '+cols[3]
      print purpose
      money = "{0:.2f}".format(float(row[5][1:]))
      index=row[2].split(' ')
      if 1 == len(index): index.append('')
      total+=float(money)
      newrow=[cols[0],
              '',
              cols[1],
              cols[2],
              '',
              d.strftime("%d-%b-%Y"),
              money,
              purpose,
              cols[4],
              cols[5],
              cols[6],
              index[0],
              '',
              '',
              cols[7],
              '',
              index[1],
              '',
              '',
              '',
              '',
              '',
              '',
              '',
              '',
          ]
  ifile.close()
  firstrow=[cols[0],'','1',cols[2],'',d.strftime("%d-%b-%Y"), "{0:.2f}".format(total),'','','','','','','','','','','','','','','','','','']
  print newrow
      




if __name__ == "__main__":
    main(sys.argv[1:])
