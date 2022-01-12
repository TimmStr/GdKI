# https://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/

from datetime import date
import pandas as pd
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

df = pd.read_csv('masie_4km_allyears_extent_sqkm.csv', header=1, delimiter=',')


def create(name, adf, kpss, acf):
    dateToday = str(date.today())
    filename = str(name) + '_' + dateToday + '.pdf'
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    Story = []
    imageName = str(name) + '.png'
    logo = imageName
    formatted_time = time.ctime()
    im = Image(logo, width=320, height=240)
    Story.append(im)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '%s' % formatted_time
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    ptext = 'Dickey-Fuller Test for: %s <br /> Test Statistic: %s <br /> p-value: %s <br /> Lags used: %s <br /> Number of Observations Used: %s <br /> Critical Value 1: %s <br /> Critical Value 5: %s <br /> Critical Value 10: %s' % (str(name),
                                          adf[0],
                                          adf[1],
                                          adf[2],
                                          adf[3],
                                          adf[4],
                                          adf[5],
                                          adf[6])

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    ptext = 'KPSS Test for: %s <br /> Test Statistic: %s <br /> p-value: %s <br /> Lags used: %s <br /> Critical Value 1: %s <br /> Critical Value 2.5: %s<br /> Critical Value 5: %s <br /> Critical Value 10: %s' % (str(name),
                                          kpss[0],
                                          kpss[1],
                                          kpss[2],
                                          kpss[6],
                                          kpss[5],
                                          kpss[4],
                                          kpss[3])

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    ptext = 'Autocorrelation Test for: %s <br /> %s'% (str(name),str(acf))
    Story.append(Paragraph(ptext, styles["Normal"]))
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

