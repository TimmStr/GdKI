# https://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/

from datetime import date
import pandas as pd
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os

df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')

def deleteFiles(name):
    filename=name+'_autocorr.png'
    os.remove(filename)
    filename=name+'_part_autocorr.png'
    os.remove(filename)
    filename=name+'.png'
    os.remove(filename)

def create(name, adf, kpss):
    dateToday = str(date.today())
    filename = str(name) + '_' + dateToday + '.pdf'
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    Story = []
    styles = getSampleStyleSheet()

    ptext = 'Bericht für die Region: '+name
    Story.append(Paragraph(ptext, styles["Title"]))
    Story.append(Spacer(1, 12))


    formatted_time = time.ctime()
    ptext = 'Erstellt am: %s' % formatted_time +'<br /> <br /> '
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    ptext = 'STL Decomposition der Region : %s' % (str(name))
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))

    imageName = str(name) + '.png'
    logo = imageName
    im = Image(logo, width=320, height=240)
    Story.append(im)

    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    ptext = '<br /> <br /> '
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    ptext = 'Dickey-Fuller Test der Region: %s' % (str(name))
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))
    ptext = 'Test Statistic: %s <br /> p-value: %s <br /> Lags used: %s <br /> Number of Observations Used: %s <br /> Critical Value 1: %s <br /> Critical Value 5: %s <br /> Critical Value 10: %s' % (adf[0],
                                          adf[1],
                                          adf[2],
                                          adf[3],
                                          adf[4],
                                          adf[5],
                                          adf[6])

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    ptext = '<br /> <br /> '
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    ptext = 'KPSS Test der Region: %s' % (str(name))
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))


    ptext = 'Test Statistic: %s <br /> p-value: %s <br /> Lags used: %s <br /> Critical Value 1: %s <br /> Critical Value 2.5: %s<br /> Critical Value 5: %s <br /> Critical Value 10: %s' % (kpss[0],
                                          kpss[1],
                                          kpss[2],
                                          kpss[6],
                                          kpss[5],
                                          kpss[4],
                                          kpss[3])


    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    ptext = 'Autocorrelation der Region : %s' % (str(name))
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))

    imageName = str(name) + '_autocorr.png'
    logo = imageName
    im = Image(logo, width=320, height=240)
    Story.append(im)

    ptext = 'Thank you very much and we look forward to serving you.'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    ptext = 'Partielle Autocorrelation der Region : %s' % (str(name))
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))

    imageName = str(name) + '_part_autocorr.png'
    logo = imageName
    im = Image(logo, width=320, height=240)
    Story.append(im)
    ptext = 'Sincerely,'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 48))

    doc.build(Story)
    print(name+".pdf erstellt")
    deleteFiles(name)

