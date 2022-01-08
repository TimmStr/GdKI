from reportlab.pdfgen import canvas as cv
from datetime import date
import pandas as pd
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')

"""
def create(name):
    dateToday=str(date.today())
    filename = str(name) +'_'+ dateToday+'.pdf'
    canvas = cv.Canvas(filename)
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 12)
    canvas.drawString(30, 750, 'Report for ' + str(name))
    canvas.drawString(30, 735, 'OF ACME INDUSTRIES')
    canvas.drawString(500, 750, dateToday)
    canvas.line(480, 747, 580, 747)
    canvas.drawString(30, 703, 'CREATED BY:')
    canvas.line(120, 700, 580, 700)
    canvas.drawString(120, 703, "GROUP 3")


    image=name+'.png'
    canvas.save()
"""
def create(name):

    dateToday=str(date.today())
    filename = str(name) +'_'+ dateToday+'.pdf'
    doc = SimpleDocTemplate(filename,pagesize=A4,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    Story=[]
    imageName=str(name)+'.png'
    logo = imageName
    magName = "Pythonista"
    issueNum = 12
    subPrice = "99.00"
    limitedDate = "03/05/2010"
    freeGift = "tin foil hat"
    formatted_time = time.ctime()
    full_name = "Mike Driscoll"
    address_parts = ["411 State St.", "Marshalltown, IA 50158"]
    im = Image(logo, width=320, height=240)
    Story.append(im)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '%s' % formatted_time
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    # Create return address
    ptext = '%s' % full_name
    Story.append(Paragraph(ptext, styles["Normal"]))
    for part in address_parts:
        ptext = '%s' % part.strip()
        Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    ptext = 'Dear %s:' % full_name.split()[0].strip()
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    ptext = 'We would like to welcome you to our subscriber base for %s Magazine! \
            You will receive %s issues at the excellent introductory price of $%s. Please respond by\
            %s to start receiving your subscription and get the following free gift: %s.' % (magName,
                                                                                                    issueNum,
                                                                                                    subPrice,
                                                                                                    limitedDate,
                                                                                                    freeGift)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = 'Thank you very much and we look forward to serving you.'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = 'Sincerely,'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 48))
    ptext = 'Ima Sucker'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    doc.build(Story)


def getNames(df):
    names=[]
    for i in df:
        name = i
        if name == 'yyyyddd':
            continue
        liste=['0','1','2','3','4','5','6','7','8','9']
        while (name[0] == ' ' or name[0] == '(' or name[0] == ')'or name[0] in liste):
            name = name[1:]
        names.append(name)
    return names


def startPdf(df):
    names=getNames(df)
    create(names[0])
    for i in names:
        create(i)



startPdf(df)
