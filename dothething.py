#!/usr/bin/env python


import csv
import datetime
import dateutil.relativedelta
import sys, getopt,os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

today = datetime.date.today()
d = (datetime.date(today.year,today.month,1) - dateutil.relativedelta.relativedelta(days=1))
lastMonth = d.strftime("%B")

cols=[]
wd=os.path.dirname(os.path.realpath(__file__))
f = open(wd+'/cols.cfg')
cols=f.read().splitlines()

def letsWriteIt(rows,o):
    csvfile = open(o, 'wb')
    outwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in rows:
      print row
      outwriter.writerow(row)
    csvfile.close()


def letsDoIt(i,o):
    total=0.00
    rows=[]
    ifile = open(i, 'rb')
    ifile.next()
    reader = csv.reader(ifile, delimiter=',')
    for row in reader:
      purpose = row[6]+' '+cols[3]
      money = "%.2f" % float(row[5][1:])
      if(float(money) <= 0):
        continue
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
      rows.append(newrow)
    ifile.close()
    t1 = "%.2f" % float(total)
    t2 = "%.2f" % float(total+total)



    rows.insert(0,[cols[0],'','1',cols[2],'',d.strftime("%d-%b-%Y"),t2,'','','','','','','','','','','','','','','','','',''])
    rows.append([cols[0],'',cols[1],cols[2],'',d.strftime("%d-%b-%Y"),t1,'IT Infrastructure Server Backups',cols[6],cols[5],cols[6],cols[11],'','',cols[12],'','','','','','','','','',''])
    rows.append([cols[0],'','4','','','','','','','','','','','','','','','','','','','','','',cols[8]])
    rows.append([cols[0],'','4','','','','','','','','','','','','','','','','','','','','','',cols[9]])
    rows.append([cols[0],'','4','','','','','','','','','','','','','','','','','','','','','',cols[10]])
    letsWriteIt(rows,o)


def send_message(ofile):
  msg = MIMEMultipart('alternative')
  s = smtplib.SMTP(cols[13],25)
  msg['Subject'] = "%s Backups FUPLOAD" %lastMonth
  msg['From'] = 'nobody@nsr1.nws.oregonstate.edu'
  msg['To'] = cols[14]
  body = 'Attached is the FUPLOAD file for Backups for %s' %lastMonth
  content = MIMEText(body, 'plain')
  msg.attach(content)
  f=file(ofile)
  attachment=MIMEText(f.read())
  attachname='%s-NWSBCKUPS-FUPLOAD.csv' %lastMonth
  attachment.add_header('Content-Disposition', 'attachment', filename=attachname)
  msg.attach(attachment)
  recip = cols[14].split(',')
  s.sendmail('nobody@nsr1.nws.oregonstate.edu',recip,msg.as_string())

def main(argv):
    defaultIn = "/tmp/nws.backups.%s.csv" % lastMonth
    defaultOut = "/tmp/nws.backups.FUPLOAD.%s.csv" % lastMonth
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
    send_message(outputfile)




if __name__ == "__main__":
    main(sys.argv[1:])
