import pandas
import re 
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
try:
    os.makedirs('./PDF0')
except OSError:
    pass
##################################################################################
pp = PdfPages('bartable0.pdf')
#pp1= PdfPages('multipage2.pdf')

################################################################################
colnames = ['Interface','IP_Addr','Description','State','VRF']
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
#print(dict1)
#print ("{:<35} {:<35} ".format('Interface','Number_of_interface'))
#for k, v in dict1.items():
         #print ("{:<35} {:<35} ".format(k, v))

######################################################################################   
#table generation
                
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
#from docx import Document
from reportlab.lib.units import inch
 
doc = SimpleDocTemplate("table0.pdf", rightMargin=200,leftMargin=200, topMargin=200,bottomMargin=200)
doc.pagesize = landscape(A4)
#doc.add_heading("INTERFACE VS COUNT TABLE FOR SHOW RUNNING CONFIG COMMAND ")
elements = []
 

import pandas
import re 
from collections import Counter
import matplotlib.pyplot as plt
colnames = ['Interface','IP_Addr','Description','State','VRF']
data = pandas.read_csv('parsed_log_show_running_config.csv', names=colnames)
interface=data.Interface.tolist()
x="Interface_Name"
#x=colors.draw("Interface Name", bold=True, fg_yellow=True)
dict2={x:"Number Of Interface", "Ethernet":0,"Ethernet_sub_Interface":0,"nve":0,"loopback":0,"mgmt":0,"Vlan":0,"Bdi":0,}
for intf in interface:
    if "." in intf:
        dict2["Ethernet_sub_Interface"]+=1
    else:
        for key,val in dict2.items():
            if(intf.startswith(key)):
                dict2[key]=dict2[key]+1;


data = dict2
 
#TODO: Get this line right instead of just copying it from the docs
style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                    ('VALIGN',(0,0),(0,-1),'TOP'),
                    ('TEXTFONT', (0, 1), (-1, 1), 'Times-Bold'), 
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                    ('GRID', (0,0), (-1,-1), 0.25, colors.black),
                    #('GRID',(0,0),(-3,-3),1,colors.green),
                    #('BOX',(0,0),(1,-1),2,colors.),
                    #('LINEABOVE',(1,2),(-2,2),1,colors.blue),
                    #('LINEBEFORE',(2,1),(2,-2),1,colors.pink),
                    ('BACKGROUND', (0, 0), (1, 0), colors.lightblue),
                ])
 
#Configure style and word wrap
s = getSampleStyleSheet()
s = s["BodyText"]
s.wordWrap = 'CJK'
list1 =[[key,data[key]] for key in data]
#data2 = [[Paragraph(key, data(val))] for key in data]
t=Table(list1,colWidths=[3.9*inch]* 50)
t.setStyle(style)
 
#Send the data and build the file
elements.append(t)
doc.build(elements)

from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
#can.setFillColorRGB(1,0,0)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 20)
can.drawString(300, 430, "INTERFACE VS COUNT TABLE")
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open("table0.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open("table1.pdf", "wb")
output.write(outputStream)
outputStream.close()

    
#####################################################################################    
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize']=(15,6)
D = dict1
x=D.keys()
y=D.values()
fig,ax=plt.subplots()
plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), list(D.keys()))
#plt.annotate('(%s, %s)' % xticks, xticks=D.values, textcoords='data')
#plt.show()
for i,v in enumerate(y):
         plt.text(i, v, str(v), color='red', fontweight='bold')
plt.savefig( pp, format='pdf')         
pp.close()
plt.show()

from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
#can.setFillColorRGB(1,0,0)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 15)
can.drawString(50, 400, "BAR GRAPH")
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open("bartable0.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open("bartable1.pdf", "wb")
output.write(outputStream)
outputStream.close()                

######################################################################################
#print(dict1)


import matplotlib.pyplot as plt
#print("##############PIE CHART")
#print("\n\n\t\t\t\t\t\t\033[90m  PIE CHART")
labels = dict1.keys()
sizes = dict1.values()
colors = ['yellowgreen', 'seagreen', 'lightskyblue', '#F0F8FF','orange','green','teal']
plt.pie(sizes, colors=colors,autopct='%5.0f%%',shadow=True)
texts = plt.pie(sizes, colors=colors, shadow=True, startangle=360)
plt.legend( labels, loc="upper right")
plt.axis('equal')
plt.tight_layout()
#plt.show()
from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('piechart1.pdf')
plt.savefig(pp, format='pdf')
plt.show()
pp.close()

from reportlab.lib.colors import HexColor
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
#can.setFillColorRGB(1,0,0)
can.setFillColor(HexColor(0xff8100))
can.setFont("Helvetica", 15)
can.drawString(50, 300, "PIE CHART")
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open("piechart1.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open("table2.pdf", "wb")
output.write(outputStream)
outputStream.close()

###########################################################################################

from PyPDF2 import PdfFileMerger

pdfs = ['table1.pdf','bartable1.pdf','table2.pdf']

merger = PdfFileMerger()

###########################################################################################
for pdf in pdfs:
    merger.append(open(pdf, 'rb'))
import glob
import os
files=glob.glob('*.pdf')
for filename in files:
        os.unlink(filename)

with open('result.pdf', 'wb') as fout:
    merger.write(fout)
############################################################################################

