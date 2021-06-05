#! Python3
# Nostalgie-Inator - Opens up images of a ceratin folder, which were created one or more years ago on the same day
import logging, os, pyperclip
from pathlib import Path
from datetime import date
from datetime import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO
import win32clipboard
from PIL.ExifTags import TAGS
import parsedatetime

#Puts out the weekday in German
def getWochentag(datum):
    weekday = datum.weekday()
    if(weekday == 0): return "Montag"
    elif(weekday == 1): return "Dienstag"
    elif(weekday == 2): return "Mittwoch"
    elif(weekday == 3): return "Donnerstag"
    elif(weekday == 4): return "Freitag"
    elif(weekday == 5): return "Samstag"
    elif(weekday == 6): return "Sonntag"
    else: return ""

#Copies the Image
def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

import module1
logging.basicConfig(filename = 'E:\\Dokumente\\TestPython\\nostalgieLog.txt', level=logging.ERROR, format=' %(asctime)s - %(levelname) s - %(message)s')
logging.debug('Start of programm')
#Path of Nostalige Folder
p = Path('E:/Bilder/Nostalgie')
#Take the current date and split it up into comparable values
datet = date.today()
day = int(datet.day)
month = int(datet.month)
year = int(datet.year)
#Create Exif List
exif={}
logging.info(f'Extracted today: "{day, month, year}"')
for filenames in p.rglob('*.*'):
    logging.debug(f'Found:"{filenames}"')
    image = Image.open(filenames)

    #All Tags
    try:
        for tag, value in image._getexif().items():
            if tag in TAGS:
                exif[TAGS[tag]] = value
    except:
        logging.error(f'"{filenames}" has a lack of Metadata')
    #Creation date
    if 'DateTimeOriginal' in exif:
        orignalTime = exif['DateTimeOriginal']
        time, clock, f = orignalTime.partition(' ')
        logging.info(f'Date and Time of current picture:"{orignalTime}"')
        yearp, f, daymonth = time.partition(':')
        #Have to sperate month and day seperatly, no clue why
        monthp, f, dayp = daymonth.partition(':')
        #Convert to int
        yearp = int(yearp)
        monthp = int(monthp)
        dayp = int(dayp)
        image.close()
        #Renames it smartly
        module1.renameSmartly(dayp, monthp, yearp, filenames, p)
        if (yearp != year) & (monthp == month) & (dayp == day):
            #Message
            difference = year - yearp
            if difference == 1:
                message = ('Heute vor einem Jahr:')
            else:
                message = (f'Heute vor {difference} Jahren:')
            logging.info(message)
            img = Image.open(filenames)
            #Draws the Text
            I1 = ImageDraw.Draw(img)
            font = ImageFont.truetype("georgia.ttf", 50)
            I1.text((30, 30), message, font=font, fill=(255, 255, 255))
            I1 = ImageDraw.Draw(img)
            #Get Wochentag
            d = datetime(yearp, monthp, dayp, 12, 00)
            print(d)
            wochentag = getWochentag(d)
            font = ImageFont.truetype("georgia.ttf", 80)
            width = img.width / 2 - 200
            height = img.height - 120
            I1.text((width, height), wochentag, font=font, fill=(255, 255, 255))
            #Shows and call copy
            img.show()
            output = BytesIO()
            img.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()
            send_to_clipboard(win32clipboard.CF_DIB, data)
logging.info('End of Program')
