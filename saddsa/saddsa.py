#! Python3
# Nostalgie-Inator - Opens up images of a ceratin folder, which were created one or more years ago on the same day
import logging, os, pyperclip
from pathlib import Path
from datetime import date
from PIL import Image
from PIL.ExifTags import TAGS

import  module1
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
        if (yearp != year)  &  (monthp == month) & (dayp == day):
            #Message
            difference = year - yearp
            if difference == 1:
                message = ('Heute vor einem Jahr:')
            else:
                message = (f'Heute vor {difference} Jahren')
            logging.info(message)
            pyperclip.copy(message)
            os.startfile(filenames)     
logging.info('End of Program')