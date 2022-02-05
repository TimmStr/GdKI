# Grundgerüst stammt aus https://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/

from datetime import date
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os


#Funktion zum löschen der Bilder
def deleteFiles(name):
    filename=name+'_autocorr.png'
    #löschen Autokorrelationsgrafik
    os.remove(filename)
    filename=name+'_part_autocorr.png'
    #löschen Partielle-Autokorrelationsgrafik
    os.remove(filename)
    filename=name+'.png'
    #löschen STL-Decomposition Grafik
    os.remove(filename)

#Erstellen der PDF Datei
def create(name, adf, kpss):
    #Variablen für den Vergleich ob in allen Tests Stationarität festgestellt wird
    adf1=False
    adf2=False
    adf3=False
    kpss1=False
    kpss2=False

    #Abfrage ob der Ordner PDF im aktuellen Pfad existiert
    if not os.path.exists('PDF'):
        os.mkdir('PDF')

    #Datum über die date.today Funktion abspeichern
    dateToday = str(date.today())
    #PDF Dateiname setzt sich aus dem Spaltennamen und dem heutigen Datum zusammen. Bsp. Northern_Hemisphere_2022-02-01
    filename = 'PDF/'+str(name) + '_' + dateToday + '.pdf'

    #Speichern der Vorlage mit dem Dateinamen und dem Format in der doc Variable
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    #Story ist eine Liste zur Speicherung der Bestandteile des PDF Dokuments
    Story = []
    #getSampleStyleSheet bezieht vorgefertigte Schriftgrößen
    styles = getSampleStyleSheet()

    #Überschrift
    ptext = 'Bericht für die Region: '+name
    Story.append(Paragraph(ptext, styles["Title"]))
    #Spacer ist der Abstand zum nächsten Absatz
    Story.append(Spacer(1, 12))

    #Einfügen des Datums und der Uhrzeit unterhalb der Unterschrift
    formatted_time = time.ctime()
    ptext = 'Erstellt am: %s' % formatted_time +'<br /> <br /> '
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    #STL Decomposition
    ptext = 'STL Decomposition der Region : %s' % (str(name))
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))

    imageName = str(name) + '.png'
    #anhängen der STL-Decomposition Grafik in die Story
    im = Image(imageName, width=320, height=240)
    Story.append(im)

    #hinzufügen der Schriftgröße Justify
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    # <br /> steht jeweils für einen Zeilenumbruch
    ptext = '<br /> <br /> '
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    #Augmented Dickey Fuller Test an Story anhängen
    ptext = 'Augmented Dickey-Fuller Test der Region: %s' % (str(name))
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
    #Abfragen ob Werte wie Test Statistic und p-Wer grenzen überschreiten
    #Je nach Fall wird dann Stationarität oder nicht Stationarität ausgegeben
    if(adf[0]>0):
        ptext = 'Die Zeitreihe ist nicht stationär, da der Test Statistic Wert : %s größer als 0 ist.' % (adf[0])
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
    else:
        ptext = 'Die Zeitreihe ist stationär, da der Test Statistic Wert : %s kleiner als 0 ist.' % (adf[0])
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        adf1=True

    if(adf[1]>0.05):
        ptext = 'Die Zeitreihe ist nicht stationär, da der p-Wert: %s größer als 0.05 ist.' % (adf[1])
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
    else:
        ptext = 'Die Zeitreihe ist stationär, da der p-Wert: %s kleiner als 0.05 ist.' % (adf[1])
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        adf2=True

    if(adf[0]>adf[6]):
        ptext = 'Die Zeitreihe ist nicht stationär, da der Test Statistic Wert: %s größer als %s ist.' % (adf[0],adf[6])
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
    else:
        ptext = 'Die Zeitreihe ist stationär, da der Test Statistic Wert: %s kleiner als der Critical Value(10): %s ist.' % (adf[0],adf[6])
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        adf3=True

    if (adf1==True and adf2==True and adf3==True):
        ptext = 'Es ist sehr wahrscheinlich, dass der Datensatz stationär ist, da alle drei Tests auf Stationarität schließen.'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
    elif (adf1==False and adf2==False and adf3==False):
        ptext = 'Es ist sehr wahrscheinlich, dass der Datensatz nicht stationär ist, da alle drei Tests auf nicht-Stationarität schließen.'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))


    ptext = '<br /> <br /> <br /> <br />'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    #KPSS Test, Ablauf weitestgehend genauso wie der ADF Test
    ptext = '<br /> KPSS Test der Region: %s' % (str(name))
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

    #Abfragen für KPSS Test
    if(kpss[1]>0.05):
        ptext = 'Die Zeitreihe ist stationär, da der p-Wert: %s größer als 0.05 ist.' % (kpss[1])
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        kpss1=True
    else:
        ptext = 'Die Zeitreihe ist nicht stationär, da der p-Wert: %s kleiner als 0.05 ist.' % (kpss[1])
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))

    if(kpss[0]>kpss[3]):
        ptext = 'Die Zeitreihe ist wahrscheinlich nicht stationär, da der Test Statistic Wert: %s größer als %s ist.' % (kpss[0],kpss[3])
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
    else:
        ptext = 'Die Zeitreihe ist wahrscheinlich stationär, da der Test Statistic Wert: %s kleiner als der Critical Value(10): %s ist.' % (kpss[0],kpss[3])
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        kpss2=True

    if (kpss1==True and kpss2==True):
        ptext = 'Es ist sehr wahrscheinlich, dass der Datensatz stationär ist, da die beiden Tests auf Stationarität schließen.'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
    elif (kpss1==False and kpss2==False):
        ptext = 'Es ist sehr wahrscheinlich, dass der Datensatz nicht stationär ist, da die beiden Tests auf nicht-Stationarität schließen.'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))


    #Autokorrelations Plot
    ptext = 'Autocorrelation der Region : %s' % (str(name))
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))

    #Anhängen der Autokorrelationsgrafik
    imageName = str(name) + '_autocorr.png'
    im = Image(imageName, width=320, height=240)
    Story.append(im)


    #Partielle Autokorrelations Plot
    ptext = '<br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br /> <br />  <br /> <br /> Partielle Autocorrelation der Region : %s' % (str(name))
    Story.append(Paragraph(ptext, styles["Heading2"]))
    Story.append(Spacer(1, 12))

    # Anhängen der partiellen Autokorrelationsgrafik
    imageName = str(name) + '_part_autocorr.png'
    im = Image(imageName, width=320, height=240)
    Story.append(im)

    # Builden der Story (speichern des Dokuments)
    doc.build(Story)
    print(name+".pdf erstellt")

