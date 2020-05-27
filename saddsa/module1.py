import re, os, logging
logging.basicConfig(filename = 'E:\\Dokumente\\TestPython\\nostalgieLog.txt', level=logging.ERROR, format=' %(asctime)s - %(levelname) s - %(message)s')
logging.debug('Start of Renamer')

stuff = re.compile(r"""
                    (.+)
                    (\.)
                    (.+)
                    """, re.VERBOSE)

def renameSmartly(day,month, year ,p, c):
    base = os.path.basename(p)
    mo = stuff.search(base)
    dayS = str(day) 
    monthS = str(month)
    yearS = str(year)
    if len(dayS) < 2:
        dayS = '0'+ dayS
    if len(monthS) < 2:
        monthS = '0'+ monthS
    prefix = dayS +'-' + monthS + '-' + yearS
    point = mo.group(2)
    suffix = mo.group(3)
    newName = prefix + point + suffix
    try:
        os.rename(p, c / newName)
    except:
        logging.error(f'Already existant {newName}')
    logging.debug(f'Renamed to "{newName}"')