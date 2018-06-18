import pandas
import re 
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import sys
import  csv
################################################################################
colnames = ['Interface','AdminStatus','IPv4','VRF','Description','IPv6','SwitchPort']
data = pandas.read_csv('parsed_log_show_running_config.csv', names=colnames)
interface=data.Interface.tolist()
dict1={"Ethernet":0,"Ethernet_sub_Interface":0,"nve":0,"loopback":0,"mgmt":0,"Vlan":0,"Bdi":0,}
for intf in interface:
    if "." in intf:
        dict1["Ethernet_sub_Interface"]+=1
    else:
        for key,val in dict1.items():
            if(intf.startswith(key)):
                dict1[key]=dict1[key]+1;
######################################################################################
'''
THIS IS TABLE 
'''
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
doc = SimpleDocTemplate("table0.pdf", rightMargin=200,leftMargin=200, topMargin=200,bottomMargin=200)
doc.pagesize = landscape(A4)
elements = []
import pandas
import re 
from collections import Counter
import matplotlib.pyplot as plt
colnames = ['Interface','AdminStatus','IPv4','VRF','Description','IPv6','SwitchPort']
data = pandas.read_csv('parsed_log_show_running_config.csv', names=colnames)
interface=data.Interface.tolist()
x="Interface_Name"
dict2={x:"Number Of Interface", "Ethernet":0,"Ethernet_sub_Interface":0,"nve":0,"loopback":0,"mgmt":0,"Vlan":0,"Bdi":0,}
for intf in interface:
    if "." in intf:
        dict2["Ethernet_sub_Interface"]+=1
    else:
        for key,val in dict2.items():
            if(intf.startswith(key)):
                dict2[key]=dict2[key]+1;


data = dict2
style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                    ('VALIGN',(0,0),(0,-1),'TOP'),
                    ('TEXTFONT', (0, 1), (-1, 1), 'Times-Bold'), 
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                    ('GRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (1, 0), colors.lightblue),
                ])
s = getSampleStyleSheet()
s = s["BodyText"]
s.wordWrap = 'CJK'
list1 =[[key,data[key]] for key in data]
t=Table(list1,colWidths=[3.9*inch]* 50)
t.setStyle(style)
elements.append(t)
doc.build(elements)
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 20)
can.drawString(300, 430, "INTERFACE VS COUNT TABLE")
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("table0.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("table1.pdf", "wb")
output.write(outputStream)
outputStream.close()
    
#####################################################################################    
'''
THIS IS BAR GRAPH
'''

import matplotlib.pyplot as plt
D = dict1
x=D.keys()
y=D.values()
fig,ax=plt.subplots(figsize=(15, 6))
plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), list(D.keys()))
for i,v in enumerate(y):
         plt.text(i, v, str(v), color='red', fontweight='bold')
pp = PdfPages('bartable0.pdf')         
plt.savefig( pp, format='pdf')         
pp.close()
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 15)
can.drawString(50, 400, "BAR GRAPH")
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("bartable0.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("bartable1.pdf", "wb")
output.write(outputStream)
outputStream.close()                

######################################################################################
'''
THIS IS PIE CHART
'''
import matplotlib.pyplot as plt1
fig,ax=plt.subplots(figsize=(15, 6))
labels = dict1.keys()
sizes = dict1.values()
colors = ['yellowgreen', 'seagreen', 'lightskyblue', '#F0F8FF','orange','green','teal']
plt1.pie(sizes, colors=colors,autopct='%5.0f%%',shadow=True)
texts = plt1.pie(sizes, colors=colors, shadow=True, startangle=360)
plt1.legend( labels, loc="upper right")
plt1.axis('equal')
plt1.tight_layout()
from matplotlib.backends.backend_pdf import PdfPages
pp1= PdfPages('piechart0.pdf')
plt1.savefig(pp1, format='pdf')
pp1.close()

from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 15)
can.drawString(50, 400, "PIE CHART")
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("piechart0.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("piechart1.pdf", "wb")
output.write(outputStream)
outputStream.close()

###########################################################################################

from PyPDF2 import PdfFileMerger

pdfs = ['table1.pdf','bartable1.pdf','piechart1.pdf',]

merger = PdfFileMerger()

###########################################################################################
for pdf in pdfs:
    merger.append(open(pdf, 'rb'))
import glob
import os
files=glob.glob('*.pdf')
for filename in files:
        os.unlink(filename)

with open('result1.pdf', 'wb') as fout:
    merger.write(fout)
############################################################################################

import pandas as pd
import pandas
import re 
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import sys
import  csv
'''
with open('parsed_log_show_running_config.csv','rb') as csvfile:
    for line in csvfile.readlines():
        print(line)
'''
colnames = ['Interface','AdminStatus','IPv4','VRF','Description','IPv6','SwitchPort']
data = pd.read_csv('parsed_log_show_running_config.csv', names=colnames)
interface=data.Interface.tolist()
Admin=data.AdminStatus.tolist()

dict2=dict(zip(interface,Admin))
dict1={"Interface":"AdminStatus(No ShutDown)","Ethernet":0,"Ethernet_sub_Interface":0,"nve":0,"loopback":0,"mgmt":0,"Vlan":0,"Bdi":0,}
#count=0
for key2,val2 in dict2.items():
            if "." in key2 and val2==" no shutdown":
                dict1["Ethernet_sub_Interface"]+=1
            else:               
                for key1,val1 in dict1.items(): 
                        if (key2.startswith(key1) and val2==' no shutdown'):
                                dict1[key1]+=1
######################################################################################
'''
THIS IS TABLE 
'''
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
doc = SimpleDocTemplate("table0.pdf", rightMargin=200,leftMargin=200, topMargin=200,bottomMargin=200)
doc.pagesize = landscape(A4)
elements = []
data = dict1
style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                    ('VALIGN',(0,0),(0,-1),'TOP'),
                    ('TEXTFONT', (0, 1), (-1, 1), 'Times-Bold'), 
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                    ('GRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (1, 0), colors.lightblue),
                ])
s = getSampleStyleSheet()
s = s["BodyText"]
s.wordWrap = 'CJK'
list1 =[[key,data[key]] for key in data]
t=Table(list1,colWidths=[3.9*inch]* 50)
t.setStyle(style)
elements.append(t)
doc.build(elements)
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 20)
can.drawString(250, 430, "Interfaces V/S AdminStatus (No Shutdown) Table")
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("table0.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("table1.pdf", "wb")
output.write(outputStream)
outputStream.close()
#####################################################################################    
'''
THIS IS BAR GRAPH
'''

import matplotlib.pyplot as plt
dict3={"Ethernet":0,"Ethernet_sub_Interface":0,"nve":0,"loopback":0,"mgmt":0,"Vlan":0,"Bdi":0,}
#count=0
for key2,val2 in dict2.items():
            if "." in key2 and val2==" no shutdown":
                dict3["Ethernet_sub_Interface"]+=1
            else:               
                for key1,val1 in dict3.items(): 
                        if (key2.startswith(key1) and val2==' no shutdown'):
                                dict3[key1]+=1
D = dict3
x=D.keys()
y=D.values()
fig,ax=plt.subplots(figsize=(15, 6))
plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), list(D.keys()))
for i,v in enumerate(y):
         plt.text(i, v, str(v), color='red', fontweight='bold')
pp = PdfPages('bartable0.pdf')         
plt.savefig( pp, format='pdf')         
pp.close()
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 15)
can.drawString(50, 400, "Interfaces V/S AdminStatus (No Shutdown) Bar Graph")
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("bartable0.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("bartable1.pdf", "wb")
output.write(outputStream)
outputStream.close()                


######################################################################################   
'''
THIS IS PIE CHART
'''
import matplotlib.pyplot as plt1
fig,ax=plt.subplots(figsize=(15, 6))
labels = dict3.keys()
sizes = dict3.values()
colors = ['yellowgreen', 'seagreen', 'lightskyblue', '#F0F8FF','orange','green','teal']
plt1.pie(sizes, colors=colors,autopct='%5.0f%%',shadow=True)
texts = plt1.pie(sizes, colors=colors, shadow=True, startangle=360)
plt1.legend( labels, loc="upper right")
plt1.axis('equal')
plt1.tight_layout()
from matplotlib.backends.backend_pdf import PdfPages
pp1= PdfPages('piechart0.pdf')
plt1.savefig(pp1, format='pdf')
pp1.close()

from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 15)
can.drawString(50, 400, "Interfaces V/S AdminStatus (No Shutdown) Pie Chart")
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("piechart0.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("piechart1.pdf", "wb")
output.write(outputStream)
outputStream.close()

###########################################################################################
from PyPDF2 import PdfFileMerger

pdfs = ['result1.pdf','table1.pdf','bartable1.pdf','piechart1.pdf',]

merger = PdfFileMerger()

###########################################################################################
for pdf in pdfs:
    merger.append(open(pdf, 'rb'))
import glob
import os
files=glob.glob('*.pdf')
for filename in files:
        os.unlink(filename)

with open('result2.pdf', 'wb') as fout:
    merger.write(fout)



    
############################################################################################
import pandas as pd
import pandas
import re 
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import sys
import  csv
'''
with open('parsed_log_show_running_config.csv','rb') as csvfile:
    for line in csvfile.readlines():
        print(line)
'''
colnames = ['Interface','AdminStatus','IPv4','VRF','Description','IPv6','SwitchPort']
data = pd.read_csv('parsed_log_show_running_config.csv', names=colnames)
interface=data.Interface.tolist()
ipv4=data.IPv4.tolist()

dict2=dict(zip(interface,ipv4))
#dict1={"Interface":"AdminStatus(No ShutDown)","Ethernet":0,"Ethernet_sub_Interface":0,"nve":0,"loopback":0,"mgmt":0,"Vlan":0,"Bdi":0,}
#count=0
dict1={}
for key2,val2 in dict2.items():
            if "." in key2 and val2!=" ":
                dict1[key2]=val2
            #else:               
             #   for key1,val1 in dict1.items(): 
            if key2!=' ' and  val2!=' ':
                dict1[key2]=val2
######################################################################################
'''
THIS IS TABLE 
'''

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
doc = SimpleDocTemplate("table0.pdf", rightMargin=200,leftMargin=200, topMargin=200,bottomMargin=200)
doc.pagesize = landscape(A4)
elements = []
data = dict1
style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                    ('VALIGN',(0,0),(0,-1),'TOP'),
                    ('TEXTFONT', (0, 1), (-1, 1), 'Times-Bold'), 
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                    ('GRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (1, 0), colors.lightblue),
                ])
s = getSampleStyleSheet()
s = s["BodyText"]
s.wordWrap = 'CJK'
list1 =[[key,data[key]] for key in data]
t=Table(list1,colWidths=[3.9*inch]* 50)
t.setStyle(style)
elements.append(t)
doc.build(elements)
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 20)
can.drawString(250, 430, "Interfaces And Corrosponding IPv4 Table")
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("table0.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("table1.pdf", "wb")
output.write(outputStream)
outputStream.close()



 #####################################################################################    
'''
THIS IS BAR GRAPH
'''

import matplotlib.pyplot as plt
D = dict1
del D['Interface']


x=D.keys()
y=D.values()
fig,ax=plt.subplots(figsize=(15, 6))
plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), list(D.keys()))
for i,v in enumerate(y):
         plt.text(i, v, str(v), color='red', fontweight='bold')
pp = PdfPages('bartable0.pdf')         
plt.savefig( pp, format='pdf')         
pp.close()
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 15)
can.drawString(50, 400, "Interfaces And Corresponding IPv4 Bar Graph")
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("bartable0.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("bartable1.pdf", "wb")
output.write(outputStream)
outputStream.close()                


######################################################################################   
'''
THIS IS PIE CHART
'''
dict2={}
for key,value in dict1.items():
            dict2[key]=1;       
import matplotlib.pyplot as plt1
fig,ax=plt.subplots(figsize=(15, 6))
labels = dict2.keys()
sizes = dict2.values()
colors = ['yellowgreen', 'seagreen', 'lightskyblue', '#F0F8FF','orange','green','teal']
plt1.pie(sizes, colors=colors,autopct='%5.0f%%',shadow=True)
texts = plt1.pie(sizes, colors=colors, shadow=True, startangle=360)
plt1.legend( labels, loc="upper right")
plt1.axis('equal')
plt1.tight_layout()
from matplotlib.backends.backend_pdf import PdfPages
pp1= PdfPages('piechart0.pdf')
plt1.savefig(pp1, format='pdf')
pp1.close()

from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 15)
can.drawString(50, 400, "Interfaces And Corresponding IPv4 Pie Chart")
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("piechart0.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("piechart1.pdf", "wb")
output.write(outputStream)
outputStream.close()

###########################################################################################
from PyPDF2 import PdfFileMerger

pdfs = ['result2.pdf','table1.pdf','bartable1.pdf','piechart1.pdf',]

merger = PdfFileMerger()

###########################################################################################
for pdf in pdfs:
    merger.append(open(pdf, 'rb'))
import glob
import os
files=glob.glob('*.pdf')
for filename in files:
        os.unlink(filename)

with open('result3.pdf', 'wb') as fout:
    merger.write(fout)
############################################################################################
            

import pandas as pd
import pandas
import re 
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import sys
import  csv
'''
with open('parsed_log_show_running_config.csv','rb') as csvfile:
    for line in csvfile.readlines():
        print(line)
'''
colnames = ['Interface','AdminStatus','IPv4','VRF','Description','IPv6','SwitchPort']
data = pd.read_csv('parsed_log_show_running_config.csv', names=colnames)
interface=data.Interface.tolist()
Vrf=data.VRF.tolist()

dict2=dict(zip(interface,Vrf))
#dict1={"Interface":"AdminStatus(No ShutDown)","Ethernet":0,"Ethernet_sub_Interface":0,"nve":0,"loopback":0,"mgmt":0,"Vlan":0,"Bdi":0,}
#count=0
#dict2=dict(zip(interface,ipv4))
#dict1={"Interface":"AdminStatus(No ShutDown)","Ethernet":0,"Ethernet_sub_Interface":0,"nve":0,"loopback":0,"mgmt":0,"Vlan":0,"Bdi":0,}
#count=0
dict1={}
for key2,val2 in dict2.items():
            if "." in key2 and val2!=" ":
                dict1[key2]=val2
            #else:               
             #   for key1,val1 in dict1.items(): 
            if key2!=' ' and  val2!=' ':
                dict1[key2]=val2
######################################################################################
'''
THIS IS TABLE 
'''

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
doc = SimpleDocTemplate("table0.pdf", rightMargin=200,leftMargin=200, topMargin=200,bottomMargin=200)
doc.pagesize = landscape(A4)
elements = []
data = dict1
style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                    ('VALIGN',(0,0),(0,-1),'TOP'),
                    ('TEXTFONT', (0, 1), (-1, 1), 'Times-Bold'), 
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                    ('GRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (1, 0), colors.lightblue),
                ])
s = getSampleStyleSheet()
s = s["BodyText"]
s.wordWrap = 'CJK'
list1 =[[key,data[key]] for key in data]
t=Table(list1,colWidths=[3.9*inch]* 50)
t.setStyle(style)
elements.append(t)
doc.build(elements)
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 20)
can.drawString(250, 430, "Interfaces And Corrosponding VRF Table")
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("table0.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("table1.pdf", "wb")
output.write(outputStream)
outputStream.close()

 #####################################################################################    
'''
THIS IS BAR GRAPH
'''

import matplotlib.pyplot as plt
D = dict1
del D['Interface']


x=D.keys()
y=D.values()
fig,ax=plt.subplots(figsize=(15, 6))
plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), list(D.keys()))
for i,v in enumerate(y):
         plt.text(i, v, str(v), color='red', fontweight='bold')
pp = PdfPages('bartable0.pdf')         
plt.savefig( pp, format='pdf')         
pp.close()
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 15)
can.drawString(50, 400, "Interfaces And Corrosponding VRF Table")
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("bartable0.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("bartable1.pdf", "wb")
output.write(outputStream)
outputStream.close()                

######################################################################################   
'''
THIS IS PIE CHART
'''
dict2={}
for key,value in dict1.items():
            dict2[key]=1;       
import matplotlib.pyplot as plt1
fig,ax=plt.subplots(figsize=(15, 6))
labels = dict2.keys()
sizes = dict2.values()
colors = ['yellowgreen', 'seagreen', 'lightskyblue', '#F0F8FF','orange','green','teal']
plt1.pie(sizes, colors=colors,autopct='%5.0f%%',shadow=True)
texts = plt1.pie(sizes, colors=colors, shadow=True, startangle=360)
plt1.legend( labels, loc="upper right")
plt1.axis('equal')
plt1.tight_layout()
from matplotlib.backends.backend_pdf import PdfPages
pp1= PdfPages('piechart0.pdf')
plt1.savefig(pp1, format='pdf')
pp1.close()

from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 15)
can.drawString(50, 400, "Interfaces And Corrosponding VRF Table")
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("piechart0.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("piechart1.pdf", "wb")
output.write(outputStream)
outputStream.close()

###########################################################################################
from PyPDF2 import PdfFileMerger

pdfs = ['result3.pdf','table1.pdf','bartable1.pdf','piechart1.pdf',]

merger = PdfFileMerger()

###########################################################################################
for pdf in pdfs:
    merger.append(open(pdf, 'rb'))
import glob
import os
files=glob.glob('*.pdf')
for filename in files:
        os.unlink(filename)

with open('result4.pdf', 'wb') as fout:
    merger.write(fout)
############################################################################################

import pandas as pd
import pandas
import re 
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import sys
import  csv
'''
with open('parsed_log_show_running_config.csv','rb') as csvfile:
    for line in csvfile.readlines():
        print(line)
'''
colnames = ['Interface','AdminStatus','IPv4','VRF','Description','IPv6','SwitchPort']
data = pd.read_csv('parsed_log_show_running_config.csv', names=colnames)
interface=data.Interface.tolist()
IPv6=data.IPv6.tolist()

dict2=dict(zip(interface,IPv6))
#dict1={"Interface":"AdminStatus(No ShutDown)","Ethernet":0,"Ethernet_sub_Interface":0,"nve":0,"loopback":0,"mgmt":0,"Vlan":0,"Bdi":0,}
#count=0
#dict2=dict(zip(interface,ipv4))
#dict1={"Interface":"AdminStatus(No ShutDown)","Ethernet":0,"Ethernet_sub_Interface":0,"nve":0,"loopback":0,"mgmt":0,"Vlan":0,"Bdi":0,}
#count=0
dict1={}
for key2,val2 in dict2.items():
            if "." in key2 and val2!=" ":
                dict1[key2]=val2
            #else:               
             #   for key1,val1 in dict1.items(): 
            if key2!=' ' and  val2!=' ':
                dict1[key2]=val2
######################################################################################
'''
THIS IS TABLE 
'''

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
doc = SimpleDocTemplate("table0.pdf", rightMargin=200,leftMargin=200, topMargin=200,bottomMargin=200)
doc.pagesize = landscape(A4)
elements = []
data = dict1
style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                    ('VALIGN',(0,0),(0,-1),'TOP'),
                    ('TEXTFONT', (0, 1), (-1, 1), 'Times-Bold'), 
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                    ('GRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (1, 0), colors.lightblue),
                ])
s = getSampleStyleSheet()
s = s["BodyText"]
s.wordWrap = 'CJK'
list1 =[[key,data[key]] for key in data]
t=Table(list1,colWidths=[3.9*inch]* 50)
t.setStyle(style)
elements.append(t)
doc.build(elements)
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 20)
can.drawString(250, 430, "Interfaces And Corrosponding IPv6 Table")
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("table0.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("table1.pdf", "wb")
output.write(outputStream)
outputStream.close()

 #####################################################################################    
'''
THIS IS BAR GRAPH
'''

import matplotlib.pyplot as plt
D = dict1
del D['Interface']


x=D.keys()
y=D.values()
fig,ax=plt.subplots(figsize=(15, 6))
plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), list(D.keys()))
for i,v in enumerate(y):
         plt.text(i, v, str(v), color='red', fontweight='bold')
pp = PdfPages('bartable0.pdf')         
plt.savefig( pp, format='pdf')         
pp.close()
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 15)
can.drawString(50, 400, "Interfaces And Corrosponding IPv6 Table")
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("bartable0.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("bartable1.pdf", "wb")
output.write(outputStream)
outputStream.close()                

######################################################################################   
'''
THIS IS PIE CHART
'''
dict2={}
for key,value in dict1.items():
            dict2[key]=1;       
import matplotlib.pyplot as plt1
fig,ax=plt.subplots(figsize=(15, 6))
labels = dict2.keys()
sizes = dict2.values()
colors = ['yellowgreen', 'seagreen', 'lightskyblue', '#F0F8FF','orange','green','teal']
plt1.pie(sizes, colors=colors,autopct='%5.0f%%',shadow=True)
texts = plt1.pie(sizes, colors=colors, shadow=True, startangle=360)
plt1.legend( labels, loc="upper right")
plt1.axis('equal')
plt1.tight_layout()
from matplotlib.backends.backend_pdf import PdfPages
pp1= PdfPages('piechart0.pdf')
plt1.savefig(pp1, format='pdf')
pp1.close()

from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 15)
can.drawString(50, 400, "Interfaces And Corrosponding IPv6 Table")
can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(open("piechart0.pdf", "rb"))
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
outputStream = open("piechart1.pdf", "wb")
output.write(outputStream)
outputStream.close()

###########################################################################################
from PyPDF2 import PdfFileMerger

pdfs = ['result4.pdf','table1.pdf','bartable1.pdf','piechart1.pdf',]

merger = PdfFileMerger()

###########################################################################################
for pdf in pdfs:
    merger.append(open(pdf, 'rb'))
import glob
import os
files=glob.glob('*.pdf')
for filename in files:
        os.unlink(filename)

with open('parsed_log_show_running_config_report.pdf', 'wb') as fout:
    merger.write(fout)
############################################################################################

import time

time.sleep(1)
