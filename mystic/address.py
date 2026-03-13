import sys
import os

# import language and stock-roms realted stuff
import mystic.language


# el idioma de la rom
language = mystic.language.ENGLISH

# el romPath
romPath = './stockRoms/en.gb'
romName = 'en'
# el path a la carpeta de base
basePath = './en'


def setRomPath(romPath):

  # el romPath (ej: './roms/de.gb')
  mystic.address.romPath = romPath
  romName = os.path.basename(romPath).split('.')[0]
  # el romName (ej: 'de')
  mystic.address.romName = romName
  # el path a la carpeta de base
  mystic.address.basePath = './' + mystic.address.romName

  # configuro el romSplitter
  mystic.romSplitter.loadBanksFromFile(romPath)

  # detecto el idioma de la rom
  lang = mystic.language.detectRomLanguage(romPath)
  # y lo seteo
  mystic.address.language = lang


def _addrToInt(strAddr):
  """ converts a string 'bb:aaaa' into the tuple (bb,aaaa) """

  strBb = strAddr[0:2]
  strAaaa = strAddr[3:7]
  bb = int(strBb,16)
  aaaa = int(strAaaa,16)
  addr = (bb,aaaa)

  return addr

def decodeTxt(lines):
  mystic.address.sizeMetatile = 6
  mystic.address.spriteSheetNames = ['worldmap', 'city', 'inner', 'cave', 'title']
  mystic.address.typeMaps = 0

  for line in lines:
#    print('line: ' + line)

#    if(line.startswith('language')):
#      idx = line.index('=')
#      strLang = line[idx+1:].strip().strip('\"').strip('\'')
#      lang = mystic.language.stockRomsLang.index(strLang)
#      mystic.address.language = lang
#    elif(line.startswith('romPath')):
#      idx = line.index('=')
#      romPath = line[idx+1:].strip().strip('\"').strip('\'')
#      mystic.address.romPath = romPath
#    elif(line.startswith('romName')):
#      idx = line.index('=')
#      romName = line[idx+1:].strip().strip('\"').strip('\'')
#      mystic.address.romName = romName
#    elif(line.startswith('basePath')):
#      idx = line.index('=')
#      basePath = line[idx+1:].strip().strip('\"').strip('\'')
#      mystic.address.basePath = basePath

    if(line.startswith('addrDictionary')):
      (bank, offset) = _addrToInt(line.split('=', 1)[1].strip().strip('\"').strip('\''))
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrDictionary = (bank, offset)
    elif(line.startswith('cantDictionary')):
      string = line.split('=', 1)[1].strip().strip('\"').strip('\'')
      cantDictionary = int(string, 10)
#      print('cantDictionary: ' + str(cantDictionary))
      mystic.address.cantDictionary = cantDictionary

    elif(line.startswith('addrWindows')):
      (bank, offset) = _addrToInt(line.split('=', 1)[1].strip().strip('\"').strip('\''))
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrWindows = (bank, offset)

    elif(line.startswith('addrMagic')):
      (bank, offset) = _addrToInt(line.split('=', 1)[1].strip().strip('\"').strip('\''))
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrMagic = (bank, offset)

    elif(line.startswith('addrInitialWeapons')):
      (bank, offset) = _addrToInt(line.split('=', 1)[1].strip().strip('\"').strip('\''))
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrInitialWeapons = (bank, offset)

    elif(line.startswith('addrLoadStateStrangeBytes')):
      (bank, offset) = _addrToInt(line.split('=', 1)[1].strip().strip('\"').strip('\''))
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrLoadStateStrangeBytes = (bank, offset)

    elif(line.startswith('addrIntro')):
      (bank, offset) = _addrToInt(line.split('=', 1)[1].strip().strip('\"').strip('\''))
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrIntro = (bank, offset)

    elif(line.startswith('addrMaps')):
      (bank, offset) = _addrToInt(line.split('=', 1)[1].strip().strip('\"').strip('\''))
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrMaps = (bank, offset)
    elif(line.startswith('typeMaps ')):
      string = line.split('=', 1)[1].strip().strip('\"').strip('\'')
      mystic.address.typeMaps = int(string, 10)

    elif(line.startswith('spriteSheetNames ')):
      idx = line.index('=')
      strLista = line[idx+1:].strip().strip('\"').strip('\'').strip('[]').split(',')
      mystic.address.spriteSheetNames = [s.strip(' ').strip('\"').strip('\'') for s in strLista]

    elif(line.startswith('spriteSheetsAddr')):
      idx = line.index('=')
      strLista = line[idx+1:].strip().strip('\"').strip('\'').strip('[]').split(',')

      listado = []
      for string in strLista:
        (bank, offset) = _addrToInt(string.strip())
#        print('bank {:02x} offset {:04x}'.format(bank, offset))
        listado.append( (bank, offset) )

      mystic.address.spriteSheetsAddr = listado
    elif(line.startswith('cantSpritesInSheet')):
      idx = line.index('=')
      strLista = line[idx+1:].strip().strip('\"').strip('\'').strip('[]').split(',')
      mystic.address.cantSpritesInSheet = [int(addr,16) for addr in strLista]

    elif(line.startswith('sizeMetatile')):
      string = line.split('=', 1)[1].strip().strip('\"').strip('\'')
      mystic.address.sizeMetatile = int(string, 10)

    elif(line.startswith('addrExpTable')):
      (bank, offset) = _addrToInt(line.split('=', 1)[1].strip().strip('\"').strip('\''))
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrExpTable = (bank, offset)

    elif(line.startswith('addrPersonajesStats ')):
      (bank, offset) = _addrToInt(line.split('=', 1)[1].strip().strip('\"').strip('\''))
      mystic.address.addrPersonajesStats = (bank, offset)
    elif(line.startswith('addrPersonajes ')):
      (bank, offset) = _addrToInt(line.split('=', 1)[1].strip().strip('\"').strip('\''))
      mystic.address.addrPersonajes = (bank, offset)
    elif(line.startswith('cantPersonajesAnimation')):
      string = line.split('=', 1)[1].strip().strip('\"').strip('\'')
      mystic.address.cantPersonajesAnimation = int(string, 10)
    elif(line.startswith('cantPersonajes ')):
      string = line.split('=', 1)[1].strip().strip('\"').strip('\'')
      mystic.address.cantPersonajes= int(string, 10)
    elif(line.startswith('addrGrupos ')):
      (bank, offset) = _addrToInt(line.split('=', 1)[1].strip().strip('\"').strip('\''))
      mystic.address.addrGrupos = (bank, offset)

    elif(line.startswith('addrTilesets')):
      (bank, offset) = _addrToInt(line.split('=', 1)[1].strip().strip('\"').strip('\''))
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrTilesets = (bank, offset)


    elif(line.startswith('addrScriptAddrDic')):
      (bank, offset) = _addrToInt(line.split('=', 1)[1].strip().strip('\"').strip('\''))
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrScriptAddrDic = (bank, offset)
    elif(line.startswith('addrScripts')):
      (bank, offset) = _addrToInt(line.split('=', 1)[1].strip().strip('\"').strip('\''))
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrScripts = (bank, offset)
    elif(line.startswith('cantScripts')):
      string = line.split('=', 1)[1].strip().strip('\"').strip('\'')
      cantScripts = int(string, 16)
#      print('cantScripts: {:04x}'.format(cantScripts))
      mystic.address.cantScripts = cantScripts

    elif(line.startswith('addrMusic')):
      # Music can be either a simple address or a list.
      idx = line.index('=')
      strList = line[idx+1:].strip().strip('\"').strip('\'').strip('[]').split(',')

      list = []
      for string in strList:
        (bank, offset) = _addrToInt(string.strip())
        list.append( (bank, offset) )

      mystic.address.addrMusic = list
    elif(line.startswith('addrSounds')):
      (bank, offset) = _addrToInt(line.split('=', 1)[1].strip().strip('\"').strip('\''))
#      print('bank {:02x} offset {:04x}'.format(bank, offset))
      mystic.address.addrSounds = (bank, offset)
