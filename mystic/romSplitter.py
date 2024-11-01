import os
import shutil

import mystic.address
import mystic.tileset
import mystic.spriteSheet
import mystic.romStats
import mystic.spritePersonaje
import mystic.personaje
import mystic.bosses
import mystic.projectiles
import mystic.inventory
import mystic.scripts
import mystic.maps
import mystic.music
import mystic.audio
import mystic.sounds
import mystic.ippy

# la rom
#self.rom = []
# los bancos
banks = []
# los cinco tilesets
tilesets = []
# los cinco spriteSheets
spriteSheets = []
# los mapas
#mapas = None


def getVal(bank, offset):
  hexa = self.banks[bank][offset]
  return hexa

def setVal(bank, offset, hexa):
  self.banks[bank][offset] = hexa


#def configure():
def loadBanksFromFile(romPath):
  """ lo preparo para splitear la rom indicada """

#  romPath = mystic.address.romPath

  mystic.romSplitter.banks = []

  f = open(romPath, 'rb')
  while True:
    piece = f.read(0x4000)

    listPiece = list(piece)

    if(len(piece) == 0):
      break

    # lo agrego a la lista de bancos
    mystic.romSplitter.banks.append(listPiece)

  f.close()


def loadBanksFromArray(romArray):
  """ load the banks from the rom array """

  mystic.romSplitter.banks = []

  subArray = romArray
  while(True):

    banco = subArray[:0x4000]
#    print('len banco: ' + str(len(banco)))

    if(len(banco) == 0):
      break

    # lo agrego a la lista de bancos
    mystic.romSplitter.banks.append(banco)

    subArray = subArray[0x4000:]

def getRomArrayFromBanks():
  """ returns the rom array by joining the banks """

  hexs = []

  for bank in mystic.romSplitter.banks:
    hexs.extend(bank)

  return hexs

def clean():
  """ borro la carpeta de split de la rom indicada """

  romName = mystic.address.romName

  # si el directorio existía
  if os.path.exists(romName):
    # lo borro 
    shutil.rmtree(romName)

def cleanBank(banco):
  """ pone un banco en 0x00 """

  clean = [0x00] * 0x4000
  mystic.romSplitter.banks[banco] = clean


def exportRom(filepath):
  """ vuelve a juntar los bancos en una rom """

  hexs = mystic.romSplitter.getRomArrayFromBanks()

  f = open(filepath, 'wb')
  f.write( bytes(hexs) )
  f.close()

def exportBank(nroBank, filepath):

  # creo el archivo binario del banco
  g = open(filepath, 'wb')
  bank = mystic.romSplitter.banks[nroBank]
  bytesbank = bytes(bank)
  g.write(bytesbank)
  g.close()

def exportIps(pathStock, pathNew, pathIps):
  """ exports the .ips file """

  patch = mystic.ippy.Patch()
  patch.buildIpsFromFiles(pathStock, pathNew, pathIps)

def gameGenieHacks():
  """ cambia un par de bytes para que no reste HP """

  # gamegenie hacks!
  bank0 = mystic.romSplitter.banks[0]
  val = bank0[0x3e3a]
#  print('val1: {:02x}'.format(val))
  # cambio la resta 'sub l' por un nop (no resta hp los golpes, si el veneno)
  bank0[0x3e3a] = 0x00

  bank2 = mystic.romSplitter.banks[2]
  val = bank2[0x396c]
#  print('val2: {:02x}'.format(val))
  # cambio la resta 'sub l' por 'sub h' para que reste 0x00 el daño por veneno
  bank2[0x396c] = 0x94


def exportSongsRom(filepath):
  """ exporta a una rom musical gbs """

  # cargo el gbs rom
#  gbsRom = mystic.util.fileToArray('./roms/audio.gb')
  # me quedo con el bank00
#  gbsRom = gbsRom[0:0x4000]
  gbsRom = mystic.util.fileToArray('./gbsBank00.bin')
  # agarro el bank0f
  bank0f = mystic.romSplitter.banks[0x0f]
  # los concateno
  gbsRom.extend(bank0f)
  # creo la rom gbs de salida
  mystic.util.arrayToFile(gbsRom, filepath)


def exportSoundsRom(filepath):
  """ exporta a una rom con efectos de sonido """

  # cargo el gbs rom
#  gbsRom = mystic.util.fileToArray('./roms/audio.gb')
  # me quedo con el bank00
#  gbsRom = gbsRom[0:0x4000]
  gbsRom = mystic.util.fileToArray('./gbsBank00.bin')

#  titulo = 'Final Fantasy Adventure'
  titulo = 'Mystic Sounds'
  listTitulo = list(titulo.encode())
  listTitulo.extend([0x00 for i in range(0, 32-len(listTitulo))])

#  autor = 'Kenji Ito'
  autor = ''
  listAutor = list(autor.encode())
  listAutor.extend([0x00 for i in range(0, 32-len(listAutor))])

#  date = '1991 Square'
  date = ''
  listDate = list(date.encode())
  listDate.extend([0x00 for i in range(0, 32-len(listDate))])

  for i in range(0, 32):
    gbsRom[0x3F74 + i] = listTitulo[i]
    gbsRom[0x3F94 + i] = listAutor[i]
    gbsRom[0x3FB4 + i] = listDate[i]

  cantSounds = 37
  # seteo los números de efectos
  for i in range(0,cantSounds):
    gbsRom[0x3F00+i] = i+1
  # cambio 1E por 25 para setear la cantidad de efectos de sonido
  gbsRom[0x3F68] = 0x25
  # cambio E2 por 00 para que los números de efectos los busque a partir del 3F00
  gbsRom[0x3FD5] = 0x00
  # cambio 90 por 92 para cambiar música por efectos de sonido
  gbsRom[0x3FE0] = 0x92

  # agarro el bank0f
  bank0f = mystic.romSplitter.banks[0x0f]
  # los concateno
  gbsRom.extend(bank0f)
  # creo la rom gbs de salida
  mystic.util.arrayToFile(gbsRom, filepath)



def testRom(filepath, emulator):
  """ ejecuta la rom indicada con el emulador vba de linux """

  # si es vba (sudo apt install visualboyadvance)
  if(emulator == 'vba'):
    comando = 'vba ' + filepath
    os.system(comando)

  # si es el mgba (sudo apt install mgba-sdl)
  elif(emulator == 'mgba'):
    comando = 'mgba -3 ' + filepath
    os.system(comando)

  elif(emulator == 'vba-m'):
    # para instalar vba-m
    #sudo snap install visualboyadvance-m --beta

    # cambio dir para evitar bug de vba-m
    os.chdir('/home/arathron/')

    comando = 'visualboyadvance-m ' + filepath
    os.system(comando)

  # si es el vba-m compilado
  elif(emulator == 'vba-m2'):
#    comando = 'vba ' + filepath
    comando = '../visualboyadvance-m/build/visualboyadvance-m ' + filepath
    os.system(comando)


def split():
  """ parte una rom en banks """

  basePath = mystic.address.basePath
  romPath = mystic.address.romPath
  romName = mystic.address.romName

  # si el directorio no existía
  if not os.path.exists(romName):
    # lo creo
    os.makedirs(romName)

  # copio la rom
  shutil.copyfile(romPath, basePath + '/' + romName + '.gb')

#  for i in range(0, 0x10):
  i = 0x00
  for bank in mystic.romSplitter.banks:
    bank = mystic.romSplitter.banks[i]

#    banco = 'bank_' + hex(i)[2:].zfill(2)
    banco = 'bank_' + str(i).zfill(2)
    folderName = romName + '/banks/' + banco 

    # si el directorio no existía
    if not os.path.exists(folderName):
      # creo la carpeta del banco
      os.makedirs(folderName)

    # creo el archivo binario del banco
    filepath = romName + '/banks/' + banco + '/' + banco + '.bin'
    mystic.romSplitter.exportBank(i, filepath)
    i += 1



def pattern():

#  pattern = 'abbba'
  pattern = 'ababbbbaba'
  pattern = 'abccba'
  pattern = 'babaabab'
  pattern = 'bbbaabbb'
  pattern = 'abcdabcdcdcdcdabcdab'
  pattern = 'abcd1234abcd1234'
  pattern = 'abababcdcdababab'
  pattern = 'aaaaaaaaaaaaaa'
  pattern = 'ab**ba'
  pattern = 'b*****a*****b*****a*****a*****a*****a*****b*****a*****b'
  pattern = 'a*b*a*b*a'
  pattern = 'ab*cd*ab*cd*cd'
  pattern = 'b*a*b*a*a*a*a*b'

  pattern = 'ababababababab'

  iPat = 0
  dic = {}

  array = mystic.romSplitter.rom

  iArr = 0
  for byty in array:

#    print('byty: ' + hex(byty))

    # agarro la letra del pattern que toca
    patKey = pattern[iPat]
#    print('patKey: ' + patKey)

    if(patKey == '*'):
      iPat += 1
    else:

      # si la letra ya estaba en el dic
      if(patKey in dic.keys()):
        # agarro el byty pattern
        bytyPat = dic[patKey]
#        print('tenia bytyPat: ' + hex(bytyPat))
      # sino
      else:

        # si el byty no estaba en los values anteriores
        if(byty not in dic.values()):
          # creo el byty pattern
          bytyPat = byty
          # lo seteo a la letra
          dic[patKey] = bytyPat
#          print('creamos bytyPat: ' + hex(bytyPat))
        # sino, el key ya estaba
        else:
          bytyPat = None
#          print('poniendo noneee!')


      # si el byty pattern coincide con el byty
      if(bytyPat == byty):
        # incremento la cuenta
        iPat += 1
      else:
        iPat = 0
        dic = {}

    if(iPat == len(pattern)):
#      print(' --- byty: ' + hex(byty)[2:].zfill(2) + ' - key: ' + pattern[0:iPat+1])
      patron = array[iArr - iPat + 1: iArr+1]
#      print('patron: ' + str(patron))

      strhex = ''
      for num in patron:
        strhex += hex(num)[2:].zfill(2) + ' '
#      strhex = mystic.romSplitter.bytesDecode(patron)
      print('addr: ' + hex(iArr)[2:].zfill(6) + ' - strhex: ' + strhex)
      iPat = 0
      dic = {}

    iArr += 1
   

def pattern2():

#  pattern = 'ababababababab'

  array = mystic.romSplitter.rom

  iArr = 0
  for i in range(10,len(array)):
    a0 = array[i-10]
    a1 = array[i-9]
    a2 = array[i-8]
    a3 = array[i-7]
    a4 = array[i-6]
    a5 = array[i-5]
    a6 = array[i-4]
    a7 = array[i-3]
    a8 = array[i-2]
    a9 = array[i-1]
    a10 = array[i-0]

    strhex = ''
    if(a1 == 0x00 and a2 == 0x03 and a3 == 0x01):

      strhex += hex(a0)[2:].zfill(2) + ' '
      strhex += hex(a1)[2:].zfill(2) + ' '
      strhex += hex(a2)[2:].zfill(2) + ' '
      strhex += hex(a3)[2:].zfill(2) + ' '
      strhex += hex(a4)[2:].zfill(2) + ' '
      strhex += hex(a5)[2:].zfill(2) + ' '
      strhex += hex(a6)[2:].zfill(2) + ' '
      strhex += hex(a7)[2:].zfill(2) + ' '
      strhex += hex(a8)[2:].zfill(2) + ' '
      strhex += hex(a9)[2:].zfill(2) + ' '
      strhex += hex(a10)[2:].zfill(2) + ' '


#      strhex = mystic.romSplitter.bytesDecode(patron)
      print('addr: ' + hex(iArr)[2:].zfill(6) + ' - strhex: ' + strhex)
 
    iArr += 1

def exportGfx():
  """ convierte los banks .bin en .png """

  basePath = mystic.address.basePath

  i = 0x00
  for bank in mystic.romSplitter.banks:
    # para cada una de las 4 paletas del banko
    for nroTileset in range(0,4):
      # creo el tileset
      tileset = mystic.tileset.Tileset(16,16)

      array = bank[0x1000*nroTileset:0x1000*(nroTileset+1)]        

      tileset.decodeRom(array)

      filepath = basePath + '/banks/bank_{:02}/tileset_{:02}_{:02}.png'.format(i, i, nroTileset)
#      print(filepath)
      tileset.exportPngFile(filepath)
    i += 1


def exportFont():

  basePath = mystic.address.basePath
  bank = mystic.romSplitter.banks[8]
  # creo el tileset
  tileset = mystic.tileset.Tileset(16,9)

  array = bank[0x1000*2+7*0x100:0x1000*(2+1)]

  tileset.decodeRom(array)
  tileset.exportPngFile(basePath + '/font.png')

def burnFont():

  basePath = mystic.address.basePath

  tileset = mystic.tileset.Tileset(16,9)
  tileset.importPngFile(basePath + '/font.png')
  array = tileset.encodeRom()

  mystic.romSplitter.burnBank(8, 0x1000*2+7*0x100, array)

def exportTilesets():
  """ exporta los cinco tilesets """

  basePath = mystic.address.basePath
  path = basePath + '/tilesets'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  mystic.romSplitter.tilesets = []
  # para cada uno de los cinco tilesets
  for nroTileset in range(0,5):

    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)

    # para los primeros 4 tilesets
    if(nroTileset < 4):
      tileset = mystic.tileset.Tileset(16,16)
      banco12 = mystic.romSplitter.banks[12]
      array = banco12[0x1000*nroTileset:0x1000*(nroTileset+1)]
      tileset.decodeRom(array)

      # agrego info al stats
      mystic.romStats.appendDato(0x0c, 0x1000*nroTileset, 0x1000*(nroTileset+1) , (rr, gg, bb), 'un tileset')

    # sino, para el 5to tileset
    else:
      tileset = mystic.tileset.Tileset(16,13)
      banco11 = mystic.romSplitter.banks[11]
      array = banco11[0x0000:0x0d00]
      tileset.decodeRom(array)

      # agrego info al stats
      mystic.romStats.appendDato(0x0b, 0x0000, 0x0d00, (rr, gg, bb), 'un tileset')

    tileset.exportPngFile(path + '/tileset_{:02}.png'.format(nroTileset))

    mystic.romSplitter.tilesets.append(tileset)

def burnTilesets():

  basePath = mystic.address.basePath
  path = basePath + '/tilesets'
 
  # para cada uno de los cinco tilesets
  for nroTileset in range(0,5):

    # para los primeros 4 tilesets
    if(nroTileset < 4):
      tileset = mystic.tileset.Tileset(16,16)
      tileset.importPngFile(path + '/tileset_{:02}.png'.format(nroTileset))
      array = tileset.encodeRom()
      mystic.romSplitter.burnBank(12, 0x1000*nroTileset, array)

    # sino, para el 5to tileset
    else:
      tileset = mystic.tileset.Tileset(16,13)
      tileset.importPngFile(path + '/tileset_{:02}.png'.format(nroTileset))
      array = tileset.encodeRom()
      mystic.romSplitter.burnBank(11, 0x0000, array)

def burnSpriteSheets():

  basePath = mystic.address.basePath
  path = basePath + '/spriteSheets'

  sheetNames = ['worldmap', 'city', 'inner', 'cave', 'title']
  spriteSheets = []
  # para cada una de los cinco spriteSheets 
  for nroSpriteSheet in range(0,5):

    sheet = mystic.spriteSheet.SpriteSheet(16,8,nroSpriteSheet,sheetNames[nroSpriteSheet])

    filepath = path + '/sheet_{:02x}.txt'.format(nroSpriteSheet)
#    print('filepath: ' + filepath)

    f = open(filepath, 'r', encoding="utf-8")
    lines = f.readlines()
    f.close()

    sheet.decodeTxt(lines)

    array = sheet.encodeRom()
#    strArray = mystic.util.strHexa(array)
#    print('array: ' + strArray)

    nroBank,addr = mystic.address.spriteSheetsAddr[nroSpriteSheet]
    cant = mystic.address.cantSpritesInSheet[nroSpriteSheet]
#    bank08 = mystic.romSplitter.banks[8]
#    array = bank08[addr:addr+6*cant]

    mystic.romSplitter.burnBank(nroBank, addr, array)
 

def exportSpriteSheets():
  """ exporta los spritesheets """

  basePath = mystic.address.basePath
  path = basePath + '/spriteSheets'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  sheetNames = ['worldmap', 'city', 'inner', 'cave', 'title']
  mystic.romSplitter.spriteSheets = []
  # para cada una de los cinco spriteSheets 
  for nroSpriteSheet in range(0,5):

    sheet = mystic.spriteSheet.SpriteSheet(16,8,nroSpriteSheet,sheetNames[nroSpriteSheet])

    nroBank,addr = mystic.address.spriteSheetsAddr[nroSpriteSheet]
    cant = mystic.address.cantSpritesInSheet[nroSpriteSheet]
    bank08 = mystic.romSplitter.banks[nroBank]

    array = bank08[addr:addr+6*cant]
    sheet.decodeRom(array)
    # lo agrego a la lista
    mystic.romSplitter.spriteSheets.append(sheet)

    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    mystic.romStats.appendDato(nroBank, addr, addr+6*cant, (rr, gg, bb), 'sprite sheet')

    lines = sheet.encodeTxt()
    string = '\n'.join(lines)
    f = open(basePath + '/spriteSheets/sheet_{:02}.txt'.format(nroSpriteSheet), 'w', encoding="utf-8")
    f.write(string)
    f.close()

    sheet.exportPngFile(basePath + '/spriteSheets/sheet_{:02}.png'.format(nroSpriteSheet))

    sheet.exportTiled(basePath + '/spriteSheets/sheet_{:02}.tsx'.format(nroSpriteSheet))


def exportWindows():
  """ exporta las ventanas """

#  print('--- 2:1baa')

  basePath = mystic.address.basePath
  path = basePath + '/items'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  f = open(path + '/windows.txt', 'w', encoding="utf-8")
  nroBank,addr = mystic.address.addrWindows
  bank = mystic.romSplitter.banks[nroBank]

  # recorro las 34 ventanas
  for i in range(0,34):
    subArray = bank[addr + i*10: addr + (i+1)*10]
#    strArray = mystic.util.strHexa(subArray)
#    print('window: ' + strArray)

    win = mystic.inventory.Window(i)
    win.decodeRom(subArray)
#    print('win: --- ' + str(win))

    lines = win.encodeTxt()

    strWin = '\n'.join(lines)

    f.write(strWin)

  f.close()

def burnWindows(filepath):
  """ quema las ventanas en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  i = 0
  windows = []
  primero = True
  subLines = []
  for line in lines:
#    print('line: ' + line)
    if('------------ window' in line):
      if(not primero):
        win = mystic.inventory.Window(i)
        win.decodeTxt(subLines)
        windows.append(win)
        i += 1
        subLines = []
      else:
        primero = False

    subLines.append(line)
  win = mystic.inventory.Window(i)
  win.decodeTxt(subLines)

  array = []
  for win in windows:
#    print('win: ' + str(win))
    subArray = win.encodeRom()
    array.extend(subArray)

  nroBank,addr = mystic.address.addrWindows
  mystic.romSplitter.burnBank(nroBank, addr, array)


def exportPersonajeStats(personajes):
  """ exporta los stat de los personajes """

#  print('--- 3:19fe')

  basePath = mystic.address.basePath
  path = basePath + '/personajes'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  f = open(path + '/personajeStats.txt', 'w', encoding="utf-8")

  bank = mystic.romSplitter.banks[0x03]

  personajeStatuses = []
  for i in range(0,0x62):
    subArray = bank[0x19fe + i*14: 0x19fe + (i+1)*14]
#    strArray = mystic.util.strHexa(subArray)
#    print('strArray: ' + strArray)

    stats = mystic.personaje.PersonajeStats(i)
    stats.decodeRom(subArray)
    personajeStatuses.append(stats)

#    print('stats: nro={:02x} '.format(stats.nroStats) + str(stats))

    lines = stats.encodeTxt(personajes)
    strStats = '\n'.join(lines)

    f.write(strStats)
 
  f.close()

  length = 14*len(personajeStatuses)
  import random
  rr = random.randint(0,0xff)
  gg = random.randint(0,0xff)
  bb = random.randint(0,0xff)
  mystic.romStats.appendDato(0x03, 0x19fe, 0x19fe+length, (rr, gg, bb), 'personajes stats')


def burnPersonajeStats(filepath):
  """ quema las stats de los personajes en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  i = 0
  personajeStatuses = []
  primero = True
  subLines = []
# Quick hack so the final entry isn't skipped.
  lines.append('------------ stats')
  for line in lines:
#    print('line: ' + line)
    if('------------ stats' in line):
      if(not primero):
        stats = mystic.personaje.PersonajeStats(i)
        stats.decodeTxt(subLines)
        personajeStatuses.append(stats)
        i += 1
        subLines = []
      else:
        primero = False

    subLines.append(line)
  stats = mystic.personaje.PersonajeStats(i)
  stats.decodeTxt(subLines)

  array = []
  for stats in personajeStatuses:
#    print('stats: ' + str(stats)) 
    subArray = stats.encodeRom()
    array.extend(subArray)

  mystic.romSplitter.burnBank(0x3, 0x19fe, array)

  return personajeStatuses


def exportPersonajes():
  """ exporta los personajes """

#  print('--- 3:1f5a')

  basePath = mystic.address.basePath
  path = basePath + '/personajes'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  f = open(path + '/personajes.txt', 'w', encoding="utf-8")

  bank = mystic.romSplitter.banks[0x03]

  array = []
  personajes = []
#  for i in range(0,10):
  for i in range(0,191):
    subArray = bank[0x1f5a + i*24 : 0x1f5a + (i+1)*24]
    array.extend(subArray)
    strSubarray = mystic.util.strHexa(subArray)
#    print('strSub: {:02x} {:03} {:04x} = '.format(i,i, 0x1f5a+i*24) + strSubarray)

    pers = mystic.personaje.Personaje(i)
    pers.decodeRom(subArray)
    personajes.append(pers)
#    print('personaje: ' + str(pers))

    lines = pers.encodeTxt()
    strPersona = '\n'.join(lines)

    f.write(strPersona)

#      print('pers {:02x} {:03} {:04x} := '.format(i, i, 0x1f5a+i*24) + str(pers))
#      personajes.append( (i,pers) )

#    for i,pers in personajes:
#      if(pers.amistad != 0x81):
#        print('pers {:02x} {:03} {:04x} := '.format(i, i, 0x1f5a+i*24) + str(pers))
#    print('----')
#    for i,pers in personajes:
#      if(pers.amistad == 0x81):
#        print('pers {:02x} {:03} {:04x} := '.format(i, i, 0x1f5a+i*24) + str(pers))
#    print('----')


  f.close()

#    ies = [0x7b, 0x7c]
#    ies = [0x12, 0x13]
#    ies = [0x12, 0x13, 0x7b, 0x7c]
#    for i in ies:
#    i = 0x7b  #nena
#    i = 0x7c  #nene
#      array = bank[0x1f5a:]
#      nene = array[24*i:]
#      subArray = nene[:24]
#      strSubarray = mystic.util.strHexa(subArray)
#      print('strSub: {:02x} {:03} {:04x} = '.format(i,i, 0x1f5a+i*24) + strSubarray)

#      pers = Personaje(i)
#      pers.decodeRom(subArray)
#      print('pers {:02x} {:03} {:04x} := '.format(i, i, 0x1f5a+i*24) + str(pers))

  length = 24*len(personajes)
  import random
  rr = random.randint(0,0xff)
  gg = random.randint(0,0xff)
  bb = random.randint(0,0xff)
  mystic.romStats.appendDato(0x03, 0x1f5a, 0x1f5a+length, (rr, gg, bb), 'personajes')

  # exporto una imagen con los sprites de cada personaje!

  bank = mystic.romSplitter.banks[8]
  # leo el tileset del font
  tileset = mystic.tileset.Tileset(16,9)
  array = bank[0x1000*2+7*0x100:0x1000*(2+1)]
  tileset.decodeRom(array)

  # obtengo los tiles de los números 0,1,...,F
  numberTile = []
  for i in range(0,16):
    tile = tileset.tiles[16*4 + i]
    numberTile.append(tile)

  # un tile en blanco
#  blankTile = tileset.tiles[16*2]
  blankTile = mystic.tileset.Tile()
  blankTile.decodeRom([0x00]*16)

  extraTiles = []
#  cantPers = 0x02
  cantPers = 0xbe+1
  # para cada personaje
  for q in range(0,cantPers):
    # lo obtengo
    pers = personajes[q]
#    print('--- pers: ' + str(pers))

    addr = 0x20000 + pers.offsetBank8

    nroBank = addr // 0x4000
    offset = addr % 0x4000

    bank = mystic.romSplitter.banks[nroBank]

    primer = q // 0x10
    segund = q % 0x10

    tiles = []
    # agrego el número de personaje
    tiles.extend([numberTile[primer], numberTile[segund], blankTile, blankTile])
#    tiles.extend([numberTile[5], numberTile[1], numberTile[2], numberTile[3]])

    # agrego los sprites del personaje
    for j in range(0, 2*pers.cantDosTiles):
      data = bank[offset + j*0x10: offset + (j+1)*0x10]
      tile = mystic.tileset.Tile()
      tile.decodeRom(data)
      tiles.append(tile)

    # completo en negro hasta formar 6 imagenes en cada fila
    for k in range(2*(pers.cantDosTiles+1)+2,2*2*7):
      tile = mystic.tileset.Tile()
      tiles.append(tile)

    w = 2*7 #pers.cantDosTiles
    h = 2

    # creo un array de tiles vacío 
    sortTiles = [None for k in range(0, w*h)]

    k = 0
    for k in range(0, len(tiles)):

      modk = k%4

      if(modk == 0):
        dx,dy = 0,0
      elif(modk == 1):
        dx,dy = 1,0
      elif(modk == 2):
        dx,dy = 0,1
      elif(modk == 3):
        dx,dy = 1,1

      idx = 2*(k//4) + w*dy + dx
      sortTiles[idx] = tiles[k]

    extraTiles.extend(sortTiles)

#      tileset = mystic.tileset.Tileset(w,h)
#      tileset.tiles = sortTiles
#      tileset.exportPngFile(path + 'personaje_{:03}.png'.format(q))


  tileset = mystic.tileset.Tileset(2*7,2*cantPers)
  tileset.tiles = extraTiles
  tileset.exportPngFile(path + '/personajes_NOEDIT.png')

  return personajes

def burnPersonajes(filepath):
  """ quema los personajes en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  i = 0
  personajes = []
  primero = True
  subLines = []
  for line in lines:
#    print('line: ' + line)
    if('------------ personaje' in line):
      if(not primero):
        p = mystic.personaje.Personaje(i)
        p.decodeTxt(subLines)
        personajes.append(p)
        i += 1
        subLines = []
      else:
        primero = False

    subLines.append(line)
  p = mystic.personaje.Personaje(i)
  p.decodeTxt(subLines)
  personajes.append(p)

  array = []
  for p in personajes:
#    print('p: ' + str(p)) 
    subArray = p.encodeRom()
    array.extend(subArray)

#    mystic.util.arrayToFile(array, './game/personajes/p.bin')
#    iguales = mystic.util.compareFiles('./game/banks/bank_03/bank_03.bin', './game/personajes/p.bin', 0x1f5a, len(array))
#    print('iguales = ' + str(iguales))

  mystic.romSplitter.burnBank(0x3, 0x1f5a, array)

  return personajes
 

def exportBosses():
  """ exporta los monstruos grandes """

#  print('--- 4:0739')

  bank = mystic.romSplitter.banks[0x04]
  bosses = mystic.bosses.Bosses()
  bosses.decodeRom(bank)

  return bosses.bosses


def burnBosses(pathBosses, pathBossesDamage, pathBehaviour, pathActions, pathMiniActions, pathPositions, pathSortTiles, pathAnimations):
  """ quema los monstruos grandes en la rom """

  bosses = mystic.bosses.Bosses()

  f = open(pathBosses, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodeTxt(lines)

  f = open(pathBossesDamage, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodeDamageTxt(lines)

  f = open(pathBehaviour, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodeBehaviourTxt(lines)

  f = open(pathActions, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodeActionsTxt(lines)

  f = open(pathMiniActions, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodeMiniActionsTxt(lines)

  f = open(pathPositions, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodePositionsTxt(lines)

  f = open(pathSortTiles, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodeSortTilesTxt(lines)

  f = open(pathAnimations, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  bosses.decodeAnimationsTxt(lines)


  array = bosses.encodeRom()
  mystic.romSplitter.burnBank(0x4, 0x0739, array)

def exportProjectiles():
  """ exporta las explosiones y cosas que arrojan los enemigos """

#  print('--- 9:0479')

  bank = mystic.romSplitter.banks[0x09]
  projs = mystic.projectiles.Projectiles()
  projs.decodeRom(bank)

  return projs.projectiles


def burnProjectiles(filepath):
  """ quema los proyectiles en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  i = 0
  projectiles = []
  primero = True
  subLines = []
  for line in lines:
#    print('line: ' + line)
    if('------------ projectile' in line):
      if(not primero):
        p = mystic.projectiles.Projectile(i)
        p.decodeTxt(subLines)
        projectiles.append(p)
        i += 1
        subLines = []
      else:
        primero = False

    subLines.append(line)
  p = mystic.projectiles.Projectile(i)
  p.decodeTxt(subLines)
  projectiles.append(p)

  array = []
  for p in projectiles:
#    print('p: ' + str(p)) 
    subArray = p.encodeRom()
    array.extend(subArray)

  mystic.romSplitter.burnBank(0x9, 0x0479, array)
 
  return projectiles


def exportGrupos3Personajes():
  """ exporta grupos de 3 personajes a cargar """

  # 3:4456  ld de,$7142
#  print('--- 3:3142')

  basePath = mystic.address.basePath
  path = basePath + '/personajes'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  vaPorAddr = 0x3142
  bank = mystic.romSplitter.banks[0x03]
  array = bank[0x3142:]

  grupos = mystic.personaje.GruposPersonajes(0x3142)
  grupos.decodeRom(array)

  lines = grupos.encodeTxt()

  strGrupos = '\n'.join(lines)

  f = open(path + '/grupos3Personajes.txt', 'w', encoding="utf-8")
  f.write(strGrupos)
  f.close()


def burnGrupos3Personajes(filepath, personajes, stats, projectiles):
  """ quema los grupos de 3 personajes """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  grupos = mystic.personaje.GruposPersonajes(0x3142)
  grupos.decodeTxt(lines)

  # Check for overlap in sprite memory.
  # If an aparicione actually uses multiple values this will give a false positive.
  for grupo in grupos.grupos:
   addrs = [grupo.addrA, grupo.addrB, grupo.addrC]
   values = []
   for apa in grupos.apariciones:
     if apa.addr in addrs:
       values.extend(apa.values)
   # Remove duplicates from the list without changing the ordering.
   values = list(dict.fromkeys(values))
   for i,v in enumerate(values[:-1]):
     for personaje in personajes:
       if(personaje.nroPersonaje == v):
         base = personaje
         break
     # Check for invisiblity
     if(base.cantDosTiles == 1):
       continue
     for j,u in enumerate(values[i+1:]):
       for personaje in personajes:
         if(personaje.nroPersonaje == u):
           comp = personaje
           break
       if(base.offsetBank8 == comp.offsetBank8):
         continue
       if(base.vramTileOffset < comp.vramTileOffset):
         low = base
         high = comp
       else:
         low = comp
         high = base
       if(low.vramTileOffset + 2 * low.cantDosTiles > high.vramTileOffset):
         print('WARNING: Personajes {:02x} and {:02x} overlap in grupo {:02x}'.format(base.nroPersonaje, comp.nroPersonaje, grupo.nro))

       # Check for overlap of projectiles in sprite memory.
       stats_base = stats[base.stats]
       stats_comp = stats[comp.stats]
       if(stats_base.projectile != stats_comp.projectile):
         if ((stats_base.projectile != 0xff) and (stats_comp.projectile != 0xff)):
           projectile_base = projectiles[stats_base.projectile]
           projectile_comp = projectiles[stats_comp.projectile]
           if(projectile_base.vramTileOffset < projectile_comp.vramTileOffset):
             low = projectile_base
             high = projectile_comp
           else:
             low = projectile_comp
             high = projectile_base
           if(low.vramTileOffset + 2 * low.cantDosTiles > high.vramTileOffset):
             print('WARNING: Projectiles {:02x} and {:02x} of personajes {:02x} and {:02x} overlap in grupo {:02x}'.format(projectile_base.nroProjectile, projectile_comp.nroProjectile, base.nroPersonaje, comp.nroPersonaje, grupo.nro))

  array = grupos.encodeRom()

  mystic.romSplitter.burnBank(0x3, 0x3142, array)

#  mystic.util.arrayToFile(array, './game/personajes/grupos.bin')
#  iguales = mystic.util.compareFiles('./game/banks/bank_03/bank_03.bin', './game/personajes/grupos.bin', 0x3142, len(array))
#  print('iguales = ' + str(iguales))
   

def exportCosasRarasPersonajes():
  """ exporta cosas raras del banco 3 """

  print('--- 3:3b56')
  bank = mystic.romSplitter.banks[0x03]
  array = bank[0x3b56:]

  line = array[:4]
  strLine = mystic.util.strHexa(line)
  print('header?     : ' + strLine)

  array = array[4:]
  line = array[:16]
  strLine = mystic.util.strHexa(line)
  print('cosasTiles? : ' + strLine)

  array = array[16:]
  line = array[:8]
  strLine = mystic.util.strHexa(line)
  print('masCositas? : ' + strLine)


def exportPersonajesAnimations():
  """ exporta las animaciones doble tiles de los personajes """

#  print('--- 3:3b72')

  bank = mystic.romSplitter.banks[0x03]

  # obtengo la lista de personajes
  personajes = []
  for i in range(0,191):
    subArray = bank[0x1f5a + i*24 : 0x1f5a + (i+1)*24]
    strSubarray = mystic.util.strHexa(subArray)
    pers = mystic.personaje.Personaje(i)
    pers.decodeRom(subArray)
    personajes.append(pers)

  # creo la lista de animaciones
  animations = []
  # recorro los personajes
  for pers in personajes:
    anim = pers.addrDosTiles
    # y agrego su animación a la lista
    animations.append(anim)

  # remuevo duplicados y ordeno
  animAddrs = sorted(set(animations))

  basePath = mystic.address.basePath
  path = basePath + '/personajes'

  f = open(path + '/personajesAnimations.txt', 'w', encoding="utf-8")

  animCounter = 1
  tiles = []
  for i in range(0,371):

    addr = 0x3b72+i*3

    if(addr + 0x4000 in animAddrs):
#      print('---animation' + str(animCounter))
      f.write('---animation' + str(animCounter) + '\n')
      animCounter += 1

    subArray = bank[0x3b72 + i*3 : 0x3b72 + (i+1)*3]
    dosTiles = mystic.tileset.DosTiles(addr)
    tiles.append(dosTiles)
    dosTiles.decodeRom(subArray)
#    print('dosTiles: ' + str(dosTiles))
    lines = dosTiles.encodeTxt()
    strDosTiles = '\n'.join(lines)
    f.write(strDosTiles + '\n')

  f.close()

  length = 3*len(tiles)
  import random
  rr = random.randint(0,0xff)
  gg = random.randint(0,0xff)
  bb = random.randint(0,0xff)
  mystic.romStats.appendDato(0x03, 0x3b72, 0x3b72+length, (rr, gg, bb), 'personajes animations dosTiles')


def burnPersonajesAnimations(filepath):
  """ quema las animaciones doble tiles de los personajes en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  addr = 0x3b72
  tiles = []
  for line in lines:
#    print('line: ' + line)
    if('(attr,tile1,tile2)' in line):
       dosTiles = mystic.tileset.DosTiles(addr)
       addr += 3
       dosTiles.decodeTxt([line])
       tiles.append(dosTiles)

  array = []
  for dosTiles in tiles:
#    print('dosTiles: ' + str(dosTiles)) 
    subArray = dosTiles.encodeRom()
    array.extend(subArray)

  mystic.romSplitter.burnBank(0x3, 0x3b72, array)

      
def exportGolpes():
  """ exporta base de cuanto lastima golpes dados/recibidos ? """

  print('--- 4:0931')
  bank = mystic.romSplitter.banks[0x04]
  array = bank[0x0931:]

  for i in range(0,152):

    line = array[:8]

    strLine = mystic.util.strHexa(line)
    print('strGolpes: ' + strLine)

    array = array[8:]


def exportMonstruoGrandeDosTiles():
  """ exporta los doble tiles de los boss """

#  print('--- 4:3ba7')

  bank = mystic.romSplitter.banks[0x04]
  array = bank[0x3ba7:]

  for i in range(0,326):

    line = array[:3]

    modo = line[0]   # 10 = normal, 30 = espejo, ??? (attribute)
    left = line[1]   # 0:8000 + left                 (tile number)
    right = line[2]  # 0:8000 + right                (tile number)

    print('(modo, left, right) = ({:02x}, {:02x}, {:02x})'.format(modo,left,right))
    strLine = mystic.util.strHexa(line)
#    print('strLinePers: ' + strLine)

    array = array[3:]


def exportAudioJson():
  """ exporta el audio en formato json """

  basePath = mystic.address.basePath
  path = basePath + '/audio'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  nroBank,addrMusic = mystic.address.addrMusic
  # cargo el banco 16 con las canciones
  bank = mystic.romSplitter.banks[nroBank]

  canciones = mystic.music.Canciones()
  canciones.decodeRom(bank,addrMusic)

  songsData = {}

  for i in range(0,30):
    cancion = canciones.canciones[i]

    lines = cancion.encodeTxt()
    strCancion = '\n'.join(lines)
#    print('strCancion: ' + strCancion)

#    songsData[i] = lines

    songsData[i+1] = {}

    subLines = cancion.melody2.encodeTxt()
    songsData[i+1][2] = subLines[2:] # (salteo header)
    subLines = cancion.melody1.encodeTxt()
    songsData[i+1][1] = subLines[2:]
    subLines = cancion.melody3.encodeTxt()
    songsData[i+1][3] = subLines[2:]



  import json
  # exporto a json
  strJson = json.dumps(songsData, indent=2)
#  strJson = json.dumps(data)
  f = open(path + '/audio_noedit.js', 'w', encoding="utf-8")
  f.write('audio = \n' + strJson)
  f.close()

def exportSongsXml():
  """ exporta las canciones en formato xml """

  basePath = mystic.address.basePath
  path = basePath + '/audio'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  nroBank,addrMusic = mystic.address.addrMusic
  # cargo el banco 16 con las canciones
  bank = mystic.romSplitter.banks[nroBank]

  canciones = mystic.music.Canciones()
  canciones.decodeRom(bank,addrMusic)


  import xml.etree.cElementTree as ET
  root = ET.Element("songs")

  for i in range(0,30):
    cancion = canciones.canciones[i]

    lines = cancion.encodeTxt()
    strCancion = '\n'.join(lines)
#    print('strCancion: ' + strCancion)

    song = ET.SubElement(root, "song")
    song.text = strCancion

  tree = ET.ElementTree(root)
#  printed_xml = tree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=True)
  ET.indent(root, space=" ", level=0)
  tree.write('./en/audio/songs.xml', xml_declaration=True, encoding='utf-8')
#  print('ET: ' + str(ET.tostring(root, encoding='UTF-8')))



def exportSongs(exportLilypond=False):
  """ exporta las canciones """

  basePath = mystic.address.basePath
  path = basePath + '/audio'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  nroBank,addrMusic = mystic.address.addrMusic
  # cargo el banco 16 con las canciones
  bank = mystic.romSplitter.banks[nroBank]

  canciones = mystic.music.Canciones()
  canciones.decodeRom(bank,addrMusic)

  lines = canciones.encodeTxt()
  strCanciones = '\n'.join(lines)
  f = open(path + '/01_songs.txt', 'w', encoding="utf-8")
  f.write(strCanciones)
  f.close()

  for i in range(0,30):
    cancion = canciones.canciones[i]

    lines = cancion.encodeTxt()
    strCancion = '\n'.join(lines)
    f = open(path + '/song_{:02}.txt'.format(i), 'w', encoding="utf-8")
    f.write(strCancion)
    f.close()

    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    addr = cancion.melody2.addr
    length = len(cancion.melody2.encodeRom())
    # agrego info al stats
    mystic.romStats.appendDato(0x0f, addr-0x4000, addr-0x4000 + length , (rr, gg, bb), 'una canción')

    addr = cancion.melody1.addr
    length = len(cancion.melody1.encodeRom())
    # agrego info al stats
    mystic.romStats.appendDato(0x0f, addr-0x4000, addr-0x4000 + length , (rr, gg, bb), 'una canción')

    addr = cancion.melody3.addr
    length = len(cancion.melody3.encodeRom())
    # agrego info al stats
    mystic.romStats.appendDato(0x0f, addr-0x4000, addr-0x4000 + length , (rr, gg, bb), 'una canción')

    # si quiere que compile lilypond
    if(exportLilypond):
      # exporto lilypond!
      cancion.exportLilypond()

def burnSongs(filepath, nroBank, addrMusic):
  """ burn the songs into the rom """

  canciones = mystic.music.Canciones()

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # decode the songs from the txt
  canciones.decodeTxt(lines)

  # export to lilypond
  canciones.exportLilypond()

  # address of the pointer table
#  nroBank,addrMusic = mystic.address.addrMusic
  arrayMusic = canciones.encodeRom(addrMusic)

  # burn into the rom
  mystic.romSplitter.burnBank(nroBank, addrMusic, arrayMusic)

  vaPorAddr = addrMusic + len(arrayMusic)

  addrAudio = 0x3a4f
  if(vaPorAddr > addrAudio):
    raise Exception("ERROR: Music overlaps audio by {:04x} bytes.".format(vaPorAddr - addrAudio))

  return vaPorAddr

def exportAudio():
  """ exports audio settings """

  basePath = mystic.address.basePath
  path = basePath + '/audio'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

#  nroBank,addrAudio = mystic.address.addrAudio
  nroBank,addrAudio = 0x0f, 0x3a4f
  # cargo el banco 16 con los sonidos
  bank = mystic.romSplitter.banks[nroBank]
  vaPorAddr = addrAudio

  vibratos = mystic.audio.Vibratos()
  vibratos.decodeRom(bank, addrAudio)

  lines = vibratos.encodeTxt()
#  lines.append('')
#  lines.append('')

  strVibrato = '\n'.join(lines)
  f = open(path + '/02_vibrato.txt', 'w', encoding="utf-8")
  f.write(strVibrato)
  f.close()

  array = vibratos.encodeRom(vaPorAddr)
  vaPorAddr += len(array)
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))

  volumes = mystic.audio.Volumes()
  volumes.decodeRom(bank, vaPorAddr)
  lines = volumes.encodeTxt()

  strVolume = '\n'.join(lines)
  f = open(path + '/03_volume.txt', 'w', encoding="utf-8")
  f.write(strVolume)
  f.close()

  array = volumes.encodeRom(vaPorAddr)
  vaPorAddr += len(array)
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))

  waves = mystic.audio.Waves()
  waves.decodeRom(bank, vaPorAddr)
  lines = waves.encodeTxt()

  strWaves = '\n'.join(lines)
  f = open(path + '/04_waves.txt', 'w', encoding="utf-8")
  f.write(strWaves)
  f.close()

#  array = waves.encodeRom(vaPorAddr)
#  vaPorAddr += len(array)
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))



def burnAudio(pathVibrato, pathVolume, pathWaves):
  """ burn the audio settings """

  array = []

  vibratos = mystic.audio.Vibratos()

  f = open(pathVibrato, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # decode the audio from the txt
  vibratos.decodeTxt(lines)

#  lines = vibratos.encodeTxt()
#  strVibratos = '\n'.join(lines)
#  print('strVibratos: ' + strVibratos)

  # address of the pointer table
#  nroBank,addrAudio = mystic.address.addrAudio
  nroBank,addrAudio = 0x0f, 0x3a4f
  vaPorAddr = addrAudio

  arrayVibrato = vibratos.encodeRom(vaPorAddr)
  array.extend(arrayVibrato)
  vaPorAddr += len(arrayVibrato)
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))



  volumes = mystic.audio.Volumes()

  f = open(pathVolume, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # decode the audio from the txt
  volumes.decodeTxt(lines)

  arrayVolume = volumes.encodeRom(vaPorAddr)
#  print('arrayVolume: ' + mystic.util.strHexa(arrayVolume))
  array.extend(arrayVolume)
  vaPorAddr += len(arrayVolume)
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))



  waves = mystic.audio.Waves()

  f = open(pathWaves, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # decode the audio from the txt
  waves.decodeTxt(lines)

  arrayWaves = waves.encodeRom(vaPorAddr)
#  print('arrayWaves: ' + mystic.util.strHexa(arrayWaves))
  array.extend(arrayWaves)
  vaPorAddr += len(arrayWaves)
#  print('vaPorAddr: {:04x}'.format(vaPorAddr))

  # burn into the rom
  mystic.romSplitter.burnBank(0xf, addrAudio, array)



def exportSounds():
  """ exports the sound effects """

  basePath = mystic.address.basePath
  path = basePath + '/audio'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  nroBank,addrSounds = mystic.address.addrSounds
  # cargo el banco 16 con los sonidos
  bank = mystic.romSplitter.banks[nroBank]

  sounds = mystic.sounds.Sounds()
  sounds.decodeRom(bank,addrSounds)

  lines = sounds.encodeTxt()
#  lines.append('')
#  lines.append('')

  strSFX = '\n'.join(lines)
  f = open(path + '/05_sounds.txt', 'w', encoding="utf-8")
  f.write(strSFX)
  f.close()

def burnSounds(filepath):
  """ burn the SFX into the rom """

  sounds = mystic.sounds.Sounds()

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  # decode the songs from the txt
  sounds.decodeTxt(lines)

#  lines = sounds.encodeTxt()
#  strSFX = '\n'.join(lines)
#  print('strSFX: ' + strSFX)

  # address of the pointer table
  nroBank,addrSounds = mystic.address.addrSounds
  arraySounds = sounds.encodeRom(addrSounds)

#  print('arraySounds: ' + mystic.util.strHexa(arraySounds))
  # burn into the rom
  mystic.romSplitter.burnBank(nroBank, addrSounds, arraySounds)


def exportSpriteSheetHero():
  """ exporta sprite sheet del heroe """

  basePath = mystic.address.basePath
  path = basePath + '/spriteSheetHero'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  bank08 = mystic.romSplitter.banks[0x08]

  import random
  rr = random.randint(0,0xff)
  gg = random.randint(0,0xff)
  bb = random.randint(0,0xff)
  # agrego info al stats
  mystic.romStats.appendDato(0x08, 0x1a00, 0x4000, (rr, gg, bb), 'tiles del hero')

  tiles = []
  for i in range(0,96 + 16*7):
    data = bank08[0x1a00 + i*0x10:0x1a00 + (i+1)*0x10]
    tile = mystic.tileset.Tile()
    tile.decodeRom(data)
    tiles.append(tile)

  extraTiles = []
  for i in range(0,8):
    extraTiles.append(tiles[i])
  extraTiles.append(tiles[4])
  extraTiles.append(tiles[5])
  for i in range(8,14):
    extraTiles.append(tiles[i])
  extraTiles.append(tiles[10])
  extraTiles.append(tiles[11])
  for i in range(14,64):
    extraTiles.append(tiles[i])
  extraTiles.append(tiles[28]) # estos dos no se si estan bien
  extraTiles.append(tiles[29]) #
  extraTiles.append(tiles[64])
  extraTiles.append(tiles[65])

  extraTiles.append(tiles[66]) # estos dos tampoco se
  extraTiles.append(tiles[67]) #
  extraTiles.append(tiles[68])
  extraTiles.append(tiles[69])

  extraTiles.append(tiles[70])
  extraTiles.append(tiles[71])
  extraTiles.append(tiles[72])
  extraTiles.append(tiles[73])

#  extraTiles.append(tiles[74]) # estos dos nose para que se usan
#  extraTiles.append(tiles[75]) #

  extraTiles.append(tiles[76])
  extraTiles.append(tiles[77])
  extraTiles.append(tiles[78])
  extraTiles.append(tiles[79])

  extraTiles.append(tiles[80])
  extraTiles.append(tiles[81])
  extraTiles.append(tiles[82])
  extraTiles.append(tiles[83])

  extraTiles.append(tiles[84])
  extraTiles.append(tiles[85])
  extraTiles.append(tiles[82])
  extraTiles.append(tiles[83])

  extraTiles.append(tiles[86])
  extraTiles.append(tiles[87])
  extraTiles.append(tiles[88])
  extraTiles.append(tiles[89])

  extraTiles.append(tiles[86])
  extraTiles.append(tiles[90])
  extraTiles.append(tiles[88])
  extraTiles.append(tiles[89])

  extraTiles.append(tiles[91])
  extraTiles.append(tiles[92])
  extraTiles.append(tiles[93])
  extraTiles.append(tiles[94]) # el tile 95 está en blanco?
 
  for i in range(96,96+16*7):
    extraTiles.append(tiles[i])

  tileset = mystic.tileset.Tileset(2,2*(26+28))
#  tileset = mystic.tileset.Tileset(2,48)
#  tileset.tiles = [tile0, tile1, tile2, tile3]
#  tileset.tiles = tiles
  tileset.tiles = extraTiles
  tileset.exportPngFile(path + '/hero.png')


def exportSpriteSheetMonster():
  """ exporta sprite sheet de los monstruos """

  basePath = mystic.address.basePath
  path = basePath + '/spriteSheetMonster'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  bank0b = mystic.romSplitter.banks[0x0b]

  tiles = []
  for i in range(0,16*2):
    data = bank0b[0x3e00 + i*0x10:0x3e00 + (i+1)*0x10]
    tile = mystic.tileset.Tile()
    tile.decodeRom(data)
    tiles.append(tile)

#  for i in range(0,16):
#    extraTiles.append(tiles[i])


  extraTiles = []
  for j in range(0,2):
    extraTiles.append(tiles[0 + 16*j])
    extraTiles.append(tiles[1 + 16*j])
    extraTiles.append(tiles[8 + 16*j])
    extraTiles.append(tiles[9 + 16*j])

    extraTiles.append(tiles[2 + 16*j])
    extraTiles.append(tiles[3 + 16*j])
    extraTiles.append(tiles[10 + 16*j])
    extraTiles.append(tiles[11 + 16*j])

    extraTiles.append(tiles[4 + 16*j])
    extraTiles.append(tiles[5 + 16*j])
    extraTiles.append(tiles[12 + 16*j])
    extraTiles.append(tiles[13 + 16*j])

    extraTiles.append(tiles[6 + 16*j])
    extraTiles.append(tiles[7 + 16*j])
    extraTiles.append(tiles[14 + 16*j])
    extraTiles.append(tiles[15 + 16*j])

  tileset = mystic.tileset.Tileset(4,8)
#  tileset = mystic.tileset.Tileset(2,48)
#  tileset.tiles = [tile0, tile1, tile2, tile3]
#  tileset.tiles = tiles
  tileset.tiles = extraTiles
  tileset.exportPngFile(path + '/monster_10.png')

  bank04 = mystic.romSplitter.banks[0x04]
  # tabla de los 21 monstruos grandes
  for i in range(0,21):
    # 24 bytes por monstruo
    array = bank04[0x0739 + 24*i:0x0739 + 24*(i+1)]

#    print('{:02} | '.format(i) + mystic.util.strHexa(array))


  bank = mystic.romSplitter.banks[0x04]
  bosses = mystic.bosses.Bosses()
  bosses.decodeRom(bank)

  boss = bosses.bosses[0x10]
  print('boss: ' + str(boss))

  print('offset: {:04x}'.format(boss.offsetBank8))
  offset = 8*0x4000 + boss.offsetBank8
  print('offset2: {:04x}'.format(offset))

  nroBank = offset//0x4000
  off = offset%0x4000

  # cada tile ocupa 0x10 bytes
  byteSize = 0x10*2*boss.cantDosTiles

  print('bank {:04x} off {:04x} fin {:04x}'.format(nroBank, off, off + byteSize))

  bank = mystic.romSplitter.banks[nroBank]

  # creo el tileset
  tileset = mystic.tileset.Tileset(0x10,2*boss.cantDosTiles//0x10)

#  array = bank[offset:offset + 0x200]
  array = bank[off: off + byteSize]

  tileset.decodeRom(array)

  tileset.exportPngFile(path + '/monster_10_tiles.png')

  print('addr sort {:04x}'.format(boss.addrSortTiles)) 
#  for sortTiles in bosses.bossesSortTiles:
#    strHexa = mystic.util.strHexa(sortTiles)
#    print('hexa: ' + strHexa)
  sortTiles = bosses.bossesSortTiles[2]
  strHexa = mystic.util.strHexa(sortTiles)


  vramTiles = []
  for i in range(0, 0x10*8):
    tile = mystic.tileset.Tile()
    vramTiles.append(tile)

  for i in range(0, 2*boss.cantDosTiles):
    sort = sortTiles[i]

#    print('off+sort*0x10 {:04x}'.format(off+sort*0x10))

    data = bank[off + sort*0x10:off + (sort+1)*0x10]
    tile = mystic.tileset.Tile()
    tile.decodeRom(data)
    vramTiles[boss.vramTileOffset+i] = tile


#  tileset = mystic.tileset.Tileset(0x10,2*boss.cantDosTiles//0x10)
#  tileset = mystic.tileset.Tileset(2,48)
#  tileset.tiles = [tile0, tile1, tile2, tile3]
#  tileset.tiles = tiles
#  tileset.exportPngFile(path + '/monster_10_sorted.png')

  vramTileset = mystic.tileset.Tileset(0x10, 8)
  vramTileset.tiles = vramTiles
  vramTileset.exportPngFile(path + '/monster_10_vram.png')



  dosTiles = bosses.dosTiles[4]
#  print('dosTiles: ' + str(dosTiles))

  catSprites = []
  i = 0
  for dosTile in dosTiles: 
    print('dosTile: ' + str(dosTile))

    tiles = []
    # si hay que reflejar la imagen X-flip
    if(dosTile.attr == 0x30):
      vramTileset.tiles[dosTile.tile1].flipX()
      vramTileset.tiles[dosTile.tile2].flipX()
      vramTileset.tiles[dosTile.tile1+1].flipX()
      vramTileset.tiles[dosTile.tile2+1].flipX()

    tiles.append(vramTileset.tiles[dosTile.tile1])
    tiles.append(vramTileset.tiles[dosTile.tile2])
    tiles.append(vramTileset.tiles[dosTile.tile1+1])
    tiles.append(vramTileset.tiles[dosTile.tile2+1])

    tileset = mystic.tileset.Tileset(2,2)
    tileset.tiles = tiles
#    tileset.exportPngFile(path + '/monster_sprite_{:02}.png'.format(i))
    catSprites.append(tileset)

    i += 1

  screenSprites = []
  for j in range(0,8):
    row = []
    for i in range(0,10):
      tileset = mystic.tileset.Tileset(2,2)
      tile = mystic.tileset.Tile()
#      tile.tileData = [0x02]*16
      tileset.tiles.append(tile)
      tileset.tiles.append(tile)
      tileset.tiles.append(tile)
      tileset.tiles.append(tile)
#      tileset.tiles.append(mystic.tileset.Tile())
#      tileset.tiles.append(mystic.tileset.Tile())
#      tileset.tiles.append(mystic.tileset.Tile())

      row.append(tileset)
    screenSprites.append(row)


  # head
  sprite = catSprites[0x0a]
  sprite.exportPngFile(path + '/monster_sprite_0a.png')
  screenSprites[2][2] = sprite
  # body
  sprite = catSprites[0x08]
  sprite.exportPngFile(path + '/monster_sprite_08.png')
  screenSprites[1][1] = sprite

  sprite = catSprites[0x0b]
  sprite.exportPngFile(path + '/monster_sprite_0b.png')
  screenSprites[1][2] = sprite

  sprite = catSprites[0x09]
  sprite.exportPngFile(path + '/monster_sprite_09.png')
  screenSprites[2][1] = sprite

  tileset = mystic.tileset.Tileset(10*2,8*2)

  data = [mystic.tileset.Tile()]*10*8*4
  for j in range(0,8):
    for i in range(0,10):

      tile0 = screenSprites[j][i].tiles[0]
      tile1 = screenSprites[j][i].tiles[1]
      tile2 = screenSprites[j][i].tiles[2]
      tile3 = screenSprites[j][i].tiles[3]

      data[2*(2*j*10)+2*(0*10)+2*i+0] = tile0
      data[2*(2*j*10)+2*(0*10)+2*i+1] = tile1
      data[2*(2*j*10)+2*(1*10)+2*i+0] = tile2
      data[2*(2*j*10)+2*(1*10)+2*i+1] = tile3





  print('len data: ' + str(len(data)))
  tileset.tiles = data
  tileset.exportPngFile(path + '/monster_loco.png')
  
    

def exportSpriteSheetPersonajes():
  """ exporta los spriteSheet de personajes """

  basePath = mystic.address.basePath
  path = basePath + '/spriteSheetPersonajes'

  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  for banco in range(0,0x10):
    for nro in range(0,4):

      bank = mystic.romSplitter.banks[banco]
      array = bank[0x1000*nro:0x1000*(nro+1)]

      w, h = 8,8
#      w, h = 4,16
      sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)

      sheetPers.decodeRom(array)
      sheetData = sheetPers.encodePng()

      filepath = basePath + '/banks/bank_{:02}/sheetPers_{:02}_{:02}.png'.format(banco, banco, nro)
      # lo exporto a png
      mystic.util.arrayToPng(sheetData, 16*w, 16*h, filepath)

  i = 1
  banco = 8
  bank = mystic.romSplitter.banks[banco]
  array = bank[0x1a00:0x2000]
  w, h = 8,3
  sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
  sheetPers.decodeRom(array)
  sheetData = sheetPers.encodePng()
  filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
  mystic.util.arrayToPng(sheetData, 16*w, 16*h, filepath)

  i = 2
  banco = 8
  bank = mystic.romSplitter.banks[banco]
  array = bank[0x2000:0x3000]
  w, h = 4,7
  sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
  sheetPers.decodeRom(array)
  sheetData = sheetPers.encodePng()
  filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
  mystic.util.arrayToPng(sheetData, 16*w, 16*h, filepath)

  i = 3
  banco = 8
  bank = mystic.romSplitter.banks[banco]
  array = bank[0x3000:0x4000]
  w, h = 8,8
  sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
  sheetPers.decodeRom(array)
  sheetData = sheetPers.encodePng()
  filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
  mystic.util.arrayToPng(sheetData, 16*w, 16*h, filepath)

  bancoAddrPosta = [                 (0x09, 0x1000), (0x09, 0x2000), (0x09,0x3000),
                     (0x0a, 0x0000), (0x0a, 0x1000), (0x0a, 0x2000), (0x0a,0x3000) ]

  i = 5
  # para cada spriteSheetPersonaje posta
  for banco, addr in bancoAddrPosta:

    bank = mystic.romSplitter.banks[banco]
    array = bank[addr:]
    w, h = 8,8
#    w, h = 4,16
    sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
    sheetPers.decodeRom(array)
    sheetData = sheetPers.encodePng()
    filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
    mystic.util.arrayToPng(sheetData, 16*w, 16*h, filepath)

    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    # agrego info al stats
    mystic.romStats.appendDato(banco, addr, addr + 0x1000, (rr, gg, bb), 'un spriteSheetPersonaje')

    i += 1

def burnSpriteSheetPersonajes():

  basePath = mystic.address.basePath
  path = basePath + '/spriteSheetPersonajes'

  i = 1
  banco = 8
  addr = 0x1a00
  w, h = 8,3
  sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
  filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
  array = mystic.util.pngToArray(filepath)
  sheetPers.decodePng(array)
  array = sheetPers.encodeRom()
  mystic.romSplitter.burnBank(banco, addr, array)

  i = 2
  banco = 8
  addr = 0x2000
  w, h = 4,7
  sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
  filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
  array = mystic.util.pngToArray(filepath)
  sheetPers.decodePng(array)
  array = sheetPers.encodeRom()
  mystic.romSplitter.burnBank(banco, addr, array)

  i = 3
  banco = 8
  addr = 0x3000
  w, h = 8,8
  sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
  filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
  array = mystic.util.pngToArray(filepath)
  sheetPers.decodePng(array)
  array = sheetPers.encodeRom()
  mystic.romSplitter.burnBank(banco, addr, array)


  bancoAddrPosta = [                 (0x09, 0x1000), (0x09, 0x2000), (0x09,0x3000),
                     (0x0a, 0x0000), (0x0a, 0x1000), (0x0a, 0x2000), (0x0a,0x3000) ]

  i = 5
  # para cada spriteSheetPersonaje posta
  for banco, addr in bancoAddrPosta:

    bank = mystic.romSplitter.banks[banco]
    array = bank[addr:]
    w, h = 8,8
#    w, h = 4,16
    sheetPers = mystic.spritePersonaje.SpriteSheetPersonaje(w,h)
    filepath = path + '/sheetPers_{:02}_{:02}.png'.format(banco, i)
    array = mystic.util.pngToArray(filepath)
    sheetPers.decodePng(array)
    array = sheetPers.encodeRom()
    mystic.romSplitter.burnBank(banco, addr, array)

    i += 1


def exportMapas(exportPngFile):
  """ genera los mapa-wrappers """

  basePath = mystic.address.basePath
  path = basePath + '/mapas'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  mapas = mystic.maps.Mapas()
  # decodifico los scripts
  mapas.decodeRom()
  # los codifico en txt
  lines = mapas.encodeTxt()
  # lo grabo
  filepath = path + '/mapas.txt'
  f = open(filepath, 'w', encoding="utf-8")
  strTxt = '\n'.join(lines)
  f.write(strTxt)
  f.close()

  # para cada mapa
  for mapa in mapas.mapas:

    print('mapa: {:02x}'.format(mapa.nroMapa))

    # lo exporto a .txt
    lines = mapa.encodeTxt()
    strMapa = '\n'.join(lines)
    f = open(path + '/mapa_{:02}_{:02x}.txt'.format(mapa.nroMapa, mapa.nroMapa), 'w', encoding="utf-8")
    f.write(strMapa + '\n')
    f.close()

    # exporto a formato .tmx para Tiled
    mapa.exportTiled(path + '/mapa_{:02}_{:02x}.tmx'.format(mapa.nroMapa, mapa.nroMapa))

    if(exportPngFile):
      mapa.exportPngFile(path + '/mapa_{:02}_{:02x}.png'.format(mapa.nroMapa, mapa.nroMapa))

    # verifico volviendo a encodearlo
    subArray = mapa.encodeRom(mapa.mapAddr)
#    filepath = path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa)
#    mystic.util.arrayToFile(subArray, filepath)
#    iguales = mystic.util.compareFiles(basePath + '/banks/bank_{:02x}/bank_{:02x}.bin'.format(mapa.mapBank, mapa.mapBank), path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa), mapa.mapAddr, len(subArray))
#    print('mapa {:02x} iguales = '.format(mapa.nroMapa) + str(iguales))

    import random
    rr = random.randint(0,0xff)
    gg = random.randint(0,0xff)
    bb = random.randint(0,0xff)
    length = len(subArray)
    # agrego info al stats
    mystic.romStats.appendDato(mapa.mapBank, mapa.mapAddr, mapa.mapAddr+length, (rr, gg, bb), 'un mapa')


def burnMapas(filepath):

  basePath = mystic.address.basePath
  path = basePath + '/mapas'

  mapas = mystic.maps.Mapas()
  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  mapas.decodeTxt(lines)


  # donde va el addr en cada uno de los bancos de mapas (5,6,7)
#  vaPorBank = 0x05
#  vaPorAddr = 0x0000
  vaPorBank, vaPorAddr = mystic.address.addrMaps
#  print('vaPorBank: {:02x} vaPorAddr: {:04x}'.format(vaPorBank, vaPorAddr))

  sortMapas = [0,9, 1,15,14,10,8, 3,2,13,4,5,11,12,6,7]

  # por cada mapa
  for i in range(0,0x10):

    sortedNro = sortMapas[i]
    # lo agarro en el orden a quemar en la rom
    mapa = mapas.mapas[sortedNro]

#    print('mapa: ' + str(mapa))
#    mapa.exportPngFile('./game/mapas/mapa_{:02x}.png'.format(mapa.nroMapa))

    # lo codifico para calcular el tamaño que ocupa
    subArray = mapa.encodeRom(mapa.mapAddr)

#    filepath = path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa)
#    mystic.util.arrayToFile(subArray, filepath)
#    iguales = mystic.util.compareFiles(basePath + '/banks/bank_{:02x}/bank_{:02x}.bin'.format(mapa.mapBank, mapa.mapBank), path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa), mapa.mapAddr, len(subArray))
#    print('mapa {:02x} iguales = '.format(mapa.nroMapa) + str(iguales))

    if(vaPorAddr + len(subArray) >= 0x4000):
      vaPorBank += 1
      vaPorAddr = 0x0000

    # actualizo el addr !!
    mapa.mapBank = vaPorBank
    mapa.mapAddr = vaPorAddr
    # vuelvo a encodearlo para ajustar los punteros addr de los bloques !!
    subArray = mapa.encodeRom(mapa.mapAddr)
    # lo quemo en la rom
    mystic.romSplitter.burnBank(mapa.mapBank, mapa.mapAddr, subArray)

#    print('i: {:02x} vaPorAddr: {:02x}:{:04x} mapAddr: {:02x}:{:04x}'.format(sortedNro, vaPorBank, vaPorAddr, mapa.mapBank, mapa.mapAddr))

    vaPorAddr += len(subArray)

#    print('quedó en: {:04x}'.format(vaPorAddr))



  array = []
  # para cada mapa
  for nroMapa in range(0,0x10):

    mapa = mapas.mapas[nroMapa]
    subArray = []
    subArray.append(0x00) 
    subArray.append(mapa.nroSpriteSheet*0x10)
    subArray.append(mapa.nose)
    subArray.extend([mapa.spriteAddr%0x100,mapa.spriteAddr//0x100])
    subArray.append(mapa.cantSprites)
    subArray.append(mapa.mapBank)
    subArray.extend([(mapa.mapAddr+0x4000)%0x100,(mapa.mapAddr+0x4000)//0x100])
    subArray.extend([mapa.noseAddr%0x100,mapa.noseAddr//0x100])

#    print('mapa: ' + str(mapa.nroMapa))
#    strHex = mystic.util.strHexa(subArray)
#    print('strHex: ' + strHex + '\n')

    array.extend(subArray)

  mystic.romSplitter.burnBank(0x08, 0x0000, array)

def burnMapasTiled():
  """ quema los mapas usando los .tmx del Tiled """

  basePath = mystic.address.basePath
  path = basePath + '/mapas'

  # donde va el addr en cada uno de los bancos de mapas (5,6,7)
#  vaPorBank = 0x05
#  vaPorAddr = 0x0000
  vaPorBank, vaPorAddr = mystic.address.addrMaps
#  print('vaPorBank: {:02x} vaPorAddr: {:04x}'.format(vaPorBank, vaPorAddr))

  sortMapas = [0,9, 1,15,14,10,8, 3,2,13,4,5,11,12,6,7]

#  mystic.romSplitter.cleanBank(5)

  mapas = mystic.maps.Mapas()

  # por cada mapa
  for i in range(0,0x10):
#  for i in range(0,2):
#  for i in range(0,3):

    filepath = path + '/mapa_{:02}_{:02x}.tmx'.format(i,i)
    f = open(filepath, 'r', encoding="utf-8")
    lines = f.readlines()
    f.close()

    for line in lines:
      if('property name="nroMapa"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        nroMapa = int(strLine, 16)
      elif('property name="nroSpriteSheet"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        nroSpriteSheet = int(strLine, 16)
      elif('property name="nose"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        nose = int(strLine, 16)
      elif('property name="spriteAddr"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        spriteAddr = int(strLine, 16)
      elif('property name="cantSprites"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        cantSprites = int(strLine, 16)
      elif('property name="mapBank"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        mapBank = int(strLine, 16)
      elif('property name="mapAddr"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        mapAddr = int(strLine, 16)
      elif('property name="noseAddr"' in line):
        idx = line.index('value=')
        subLine = line[idx:]
        strLine = subLine.split('"')[1]
        noseAddr = int(strLine, 16)
 
    print('nroMapa {:02x}, nroSpriteSheet {:02x}, nose {:02x}, spriteAddr {:04x}, cantSprites {:02x}, mapBank {:02x}, mapAddr {:04x}, noseAddr {:04x}'.format(nroMapa, nroSpriteSheet, nose, spriteAddr, cantSprites, mapBank, mapAddr, noseAddr)) 

    mapa = mystic.maps.Mapa(nroMapa, nroSpriteSheet, nose, spriteAddr, cantSprites, mapBank, mapAddr, noseAddr)
    mapa.importTiled(filepath)
    mapas.mapas.append(mapa)

  # por cada mapa
  for i in range(0,0x10):
#  for i in range(0,1):

    sortedNro = sortMapas[i]
    # lo agarro en el orden a quemar en la rom
    mapa = mapas.mapas[sortedNro]

#    print('mapa: ' + str(mapa))
#    mapa.exportPngFile('./game/mapas/mapa_{:02x}.png'.format(mapa.nroMapa))

    # lo codifico para calcular el tamaño que ocupa
    subArray = mapa.encodeRom(mapa.mapAddr)

#    filepath = path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa)
#    mystic.util.arrayToFile(subArray, filepath)
#    iguales = mystic.util.compareFiles(basePath + '/banks/bank_{:02x}/bank_{:02x}.bin'.format(mapa.mapBank, mapa.mapBank), path + '/mapa_{:02}_{:02x}.bin'.format(mapa.nroMapa, mapa.nroMapa), mapa.mapAddr, len(subArray))
#    print('mapa {:02x} iguales = '.format(mapa.nroMapa) + str(iguales))

    if(vaPorAddr + len(subArray) >= 0x4000):
      vaPorBank += 1
      vaPorAddr = 0x0000

    # actualizo el addr !!
    mapa.mapBank = vaPorBank
    mapa.mapAddr = vaPorAddr
    # vuelvo a encodearlo para ajustar los punteros addr de los bloques !!
    subArray = mapa.encodeRom(mapa.mapAddr)
    # lo quemo en la rom
    mystic.romSplitter.burnBank(mapa.mapBank, mapa.mapAddr, subArray)

#    print('i: {:02x} vaPorAddr: {:02x}:{:04x} mapAddr: {:02x}:{:04x}'.format(sortedNro, vaPorBank, vaPorAddr, mapa.mapBank, mapa.mapAddr))

    vaPorAddr += len(subArray)

#    print('quedó en: {:04x}'.format(vaPorAddr))



  array = []
  # para cada mapa
  for nroMapa in range(0,0x10):
#  for nroMapa in range(0,1):

    mapa = mapas.mapas[nroMapa]
    subArray = []
    subArray.append(0x00) 
    subArray.append(mapa.nroSpriteSheet*0x10)
    subArray.append(mapa.nose)
    subArray.extend([mapa.spriteAddr%0x100,mapa.spriteAddr//0x100])
    subArray.append(mapa.cantSprites)
    subArray.append(mapa.mapBank)
    subArray.extend([(mapa.mapAddr+0x4000)%0x100,(mapa.mapAddr+0x4000)//0x100])
    subArray.extend([mapa.noseAddr%0x100,mapa.noseAddr//0x100])

#    print('mapa: ' + str(mapa.nroMapa))
#    strHex = mystic.util.strHexa(subArray)
#    print('strHex: ' + strHex + '\n')

    array.extend(subArray)

  mystic.romSplitter.burnBank(0x08, 0x0000, array)




def exportTexto():
  """ convierte los banks .bin en .txt """

  basePath = mystic.address.basePath
#  romName = mystic.address.romName
#  filePath = basePath + '/hex_texto.txt'
#  rom = mystic.romSplitter.rom
   # lo exporto a texto
#  mystic.romSplitter._exportTexto(rom, filePath)

  # para cada banco
  for i in range(0,0x10):

    filePath = basePath + '/banks/bank_{:02}/bank_{:02}.txt'.format(i,i)
    bank = mystic.romSplitter.banks[i]
    # lo exporto a texto
    mystic.romSplitter._exportTexto(bank, filePath)

def _exportTexto(array, filePath):

  g = open(filePath, 'w', encoding="utf-8")

  i = 1
  renglon = []
  for hexa in array:
    renglon.append(hexa)

    if(i % 16 == 0):
      strhexs = ''
      traduc = ''
      for hexy in renglon:
        strhexs += '{:02x}'.format(hexy) + ' '
        chars = mystic.dictionary.decodeByte(hexy)
        traduc += chars
      addr = '{:04x}'.format(i - 0x10)
      g.write(addr + ' | ' + strhexs + '| ' + traduc + '\n')
      renglon = []

    i+=1

  g.close()



def scriptDecode(addr):
  script = Script(addr)

  banco = 0x0d
  if(addr >= 0x4000):
    banco = 0x0e
    addr -= 0x4000
  array = mystic.romSplitter.banks[banco]
  # creo un array desde donde empieza el script
  array = array[addr:]

  script.decodeRom(array)
  return script


def exportIntro():
  """ exporta el intro.txt """

  nroBank,address = mystic.address.addrIntro
  bank02 = mystic.romSplitter.banks[nroBank]

  array = bank02[address:]
#  strHexa = mystic.util.strHexa(array)
#  print('strHexa: ' + strHexa)

  string = ''
  # para cada byte del array
  for code in array:

    # lo decodifico
    if(code in [0x00, 0x1a]):
      # 'en' and 'en_uk' rom uses 0x00, but 'fr' and 'de' roms use 0x1a for <enter>
      char = '\n'
    elif(code == 0xff):
      char = ' '
    elif(code == 0x01):
      break
    else:
      char = mystic.dictionary.decodeByte(code)

    # y lo agrego al string
    string += char

#  print('string: ' + string)

  romName = mystic.address.romName
  path = './' + romName + '/intro.txt'
  # lo exporto al intro.txt
  f = open(path, 'w', encoding="utf-8")
  f.write(string)
  f.close()

def burnIntro():
  """ quema el intro.txt en la rom """

  romName = mystic.address.romName
  path = './' + romName + '/intro.txt'
  f = open(path, 'r', encoding="utf-8")
  string = f.read()
  f.close()

  array = []
  # para cada char del string
  for char in string:
    # lo codifico con el byte correspondiente
    if(char == '\n'):

      lang = mystic.address.language
      if(lang in [mystic.language.ENGLISH, mystic.language.ENGLISH_UK, mystic.language.JAPAN]):
        code = 0x00
      else: 
        code = 0x1a

    elif(char == ' '):
      code = 0xff
    else:
      code = mystic.dictionary.encodeChars(char)

    # y lo agrego al array
    array.append(code)

  # agrego el byte de cierre
  array.append(0x01)

#  strHexa = mystic.util.strHexa(array)
#  print('strHexa: ' + strHexa)

  nroBank,address = mystic.address.addrIntro
  # lo quemo en el banco
  mystic.romSplitter.burnBank(nroBank, address, array)


def burnInitialScript(nroScript):
  """ setea el script inicial a ejecutar cuando inicia el juego sin battery """

  bank02 = mystic.romSplitter.banks[0x02]
#  address = mystic.address.addrScriptAddrDic
  address = 0x3cfe

  byte1 = nroScript // 0x100
  byte2 = nroScript % 0x100
  array = [byte2, byte1]
  # lo quemo en el banco
  mystic.romSplitter.burnBank(0x02, address, array)
 
     
def exportScripts():

  basePath = mystic.address.basePath
  path = basePath + '/scripts'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  scripts = mystic.scripts.Scripts()
  # decodifico los scripts
  scripts.decodeRom()
  # los codifico en txt
  lines= scripts.encodeTxt()
  # lo grabo
  filepath = path + '/scripts.txt'
  f = open(filepath, 'w', encoding="utf-8")
  strTxt = '\n'.join(lines)
  f.write(strTxt)
  f.close()




def burnScripts(filepath):
  """ compila el script.txt indicado y quema los scripts en los bancos 0x0d y 0x0e, y el dicionario de addrs en banco 0x08 """

  scripts = mystic.scripts.Scripts()

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()
  scripts.decodeTxt(lines)

  # encode script banks
  encodedBanks = scripts.encodeRom()

  basePath = mystic.address.basePath
  # creo los binarios para comparar
#  mystic.util.arrayToFile(array0d, basePath+'/scripts/scripts0d.bin')
#  mystic.util.arrayToFile(array0e, basePath+'/scripts/scripts0e.bin')
#  iguales = mystic.util.compareFiles(basePath+'/banks/bank_13/bank_13.bin', basePath+'/scripts/scripts0d.bin', 0, len(array0d))
#  print('iguales 0d: ' + str(iguales))
#  iguales = mystic.util.compareFiles(basePath+'/banks/bank_14/bank_14.bin', basePath+'/scripts/scripts0e.bin', 0, len(array0e))
#  print('iguales 0e: ' + str(iguales))

  vaPorBank = 0x0d
  for encodedBank in encodedBanks:

#    print('va por bank: {:02x}'.format(vaPorBank))
#    print('len(bank): {:04x}'.format(len(encodedBank)))

     # Creates .bin files for each script bank for debugging.
#    mystic.util.arrayToFile(encodedBank, basePath+'/scripts/scripts{:02x}.bin'.format(vaPorBank))

    # quemo los banks 0x0d y 0x0e
    mystic.romSplitter.burnBank(vaPorBank, 0x0000, encodedBank)
    vaPorBank += 1


  bank,addr = mystic.address.addrScriptAddrDic
  array = []
  # por cada script
  for script in scripts.scripts:

#    print('script addr: {:04x}'.format(script.addr))

    # agarro su addr
    byte1 = script.addr // 0x100
    byte2 = script.addr % 0x100
    # y la agrego al array
    array.extend([byte2, byte1])

  # quemo el diccionario de addr en el bank08
  mystic.romSplitter.burnBank(bank, addr, array)

#  mystic.util.arrayToFile(array, './de/scripts/dic.bin')
#  iguales = mystic.util.compareFiles('./de/banks/bank_08/bank_08.bin', './de/scripts/dic.bin', addr, len(array))
#  print('iguales dic: ' + str(iguales))


def burnBank(bank, idx0, hexs):

  i = idx0
  for hexa in hexs:

    if(i >= 0x4000):
      return False

    banco = mystic.romSplitter.banks[bank]
#    print('banco: ' + str(banco))

#    print('grabando hexa {:02x} en i {:04x}'.format(hexa, i))

    banco[i] = hexa
    i += 1

  return True


def exportExpTable():
  """ exporta la tabla de experiencia para subir de nivel """

  nroBank, addr = mystic.address.expTable
  bank = mystic.romSplitter.banks[nroBank]
  array = bank[addr:]

  lines = []
  for i in range(0,101):
    hexExp = array[3*i:3*(i+1)]

    exp = hexExp[0]*0x100**2 + hexExp[1]*0x100 + hexExp[2] 
    lines.append('level {:03}: {:06x} '.format(i+1, exp))

  string = '\n'.join(lines)

  romName = mystic.address.romName
  path = './' + romName + '/exp.txt'
  # lo exporto al exp.txt
  f = open(path, 'w', encoding="utf-8")
  f.write(string)
  f.close()

  import random
  rr = random.randint(0,0xff)
  gg = random.randint(0,0xff)
  bb = random.randint(0,0xff)
  length = 3*101
  # agrego info al stats
  mystic.romStats.appendDato(0x08, addr, addr+length, (rr, gg, bb), 'exp table')


def burnExpTable(filepath):
  """ quema el exp.txt en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  array = []
  for line in lines:
    idx0 = line.index(':')
    strHexa = line[idx0+1:].strip()
    exp = int(strHexa, 16)

    byte1 = exp//0x10000
    byte2 = (exp % 0x010000)//0x100
    byte3 = (exp % 0x000100)

    array.extend([byte1, byte2, byte3])

#    print('exp: {:06x}: {:02x} {:02x} {:02x}'.format(exp, byte1, byte2, byte3))

  nroBank,addr = mystic.address.expTable
#  print('current addr: {:04x}'.format(addr))

  strArray = mystic.util.strHexa(array)
#  print('strArray: ' + strArray)

  # lo quemo en el banco
  mystic.romSplitter.burnBank(nroBank, addr, array)



def exportItems():
  """ exporta los items """

  basePath = mystic.address.basePath
  path = basePath + '/items'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  nroBank,addr = mystic.address.addrMagic
  data = mystic.romSplitter.banks[nroBank]

  string = ''
  # para cada magia
  for i in range(0,8):
    magicOffset = addr + i*0x10
    magicArray = data[magicOffset:magicOffset+0x10]
#    magic = Magic()
    magic = mystic.inventory.Item('magic')
    # la decodifico
    magic.decodeRom(magicArray)
#    Cosas.instance().addMagic(magic)

    lines = magic.encodeTxt()
    subString = '\n'.join(lines)
    string += subString

  filePath = path + '/00_magic.txt'
  # lo exporto al magic.txt
  f = open(filePath, 'w', encoding="utf-8")
  f.write(string)
  f.close()

  addr = magicOffset + 0x10
  string = ''
  # para cada item
  for i in range(0,57):
    itemOffset = addr + i*0x10
    itemArray = data[itemOffset:itemOffset+0x10]
    item = mystic.inventory.Item('item')
    # lo decodifico
    item.decodeRom(itemArray)
#    Cosas.instance().addItem(item)

    lines = item.encodeTxt()
    subString = '\n'.join(lines)
    string += subString

  filePath = path + '/01_items.txt'
  # lo exporto al items.txt
  f = open(filePath, 'w', encoding="utf-8")
  f.write(string)
  f.close()

  addr = itemOffset + 0x10
  string = ''
  # para cada weapon
  for i in range(0,46):
    weaponOffset = addr + i*0x10
    weaponArray = data[weaponOffset:weaponOffset+0x10]
    weapon = mystic.inventory.Item('weapon')
    # la decodifico
    weapon.decodeRom(weaponArray)
#    Cosas.instance().addWeapon(weapon)

    lines = weapon.encodeTxt()
    subString = '\n'.join(lines)
    string += subString

  filePath = path + '/02_weapons.txt'
  # lo exporto al weapons.txt
  f = open(filePath, 'w', encoding="utf-8")
  f.write(string)
  f.close()


  lines = []

  # apdp
  addr = weaponOffset + 0x10
  ap = mystic.inventory.Apdp()
  ap.decodeRom(data[addr:])
  subLines = ap.encodeTxt()
  lines.extend(subLines)

  lines.append('')

  addr += 0x10
  dp = mystic.inventory.Apdp()
  dp.decodeRom(data[addr:])
  subLines = dp.encodeTxt()
  lines.extend(subLines)

  string = '\n'.join(lines)

  filePath = path + '/03_apdp.txt'
  # lo exporto al apdp.txt
  f = open(filePath, 'w', encoding="utf-8")
  f.write(string)
  f.close()

  lines = []
  addr += 0x10
  for i in range(0,17):
    subArray = data[addr:addr+16]
#    strHexa = mystic.util.strHexa(subArray)
#    print('vendor: ' + strHexa)
    vendor = mystic.inventory.Vendor()
    vendor.decodeRom(subArray)
#    print(str(vendor))
    subLines = vendor.encodeTxt()
    lines.extend(subLines)

    addr += 0x10

  string = '\n'.join(lines)

  filePath = path + '/04_vendor.txt'
  # lo exporto al vendor.txt
  f = open(filePath, 'w', encoding="utf-8")
  f.write(string)
  f.close()

  # exporto las weapons iniciales
  mystic.romSplitter.exportInitialWeapons()

  # exporto los items especiales
  mystic.romSplitter.exportSpecialItems()

def exportInitialWeapons():
  """ exporta las weapons con que inicia el juego """

  basePath = mystic.address.basePath
  path = basePath + '/items'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  nroBank, addr = mystic.address.addrInitialWeapons
  data = mystic.romSplitter.banks[nroBank]
#  print('bank, addr: {:02x} {:04x}'.format(nroBank, addr))
#  strHexa = mystic.util.strHexa(data[addr:addr+6])
#  print('hexa: ' + strHexa)

  lines = []
  lines.append('weapon: {:02x}'.format(data[addr+0]))
  lines.append('helmet: {:02x}'.format(data[addr+1]))
  lines.append('ap:     {:02x}'.format(data[addr+2]))
  lines.append('armor:  {:02x}'.format(data[addr+3]))
  lines.append('dp:     {:02x}'.format(data[addr+4]))
  lines.append('shield: {:02x}'.format(data[addr+5]))

  string = '\n'.join(lines)

  filePath = path + '/06_initialWeapons.txt'
  # lo exporto al initialWeapons.txt
  f = open(filePath, 'w', encoding="utf-8")
  f.write(string)
  f.close()

def burnInitialWeapons(filepath, nroBank, offset):
  """ quema el specialItems.txt en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  for line in lines:
    if(line.startswith('weapon:')):
      weapon = int(line[len('weapon:'):].strip(),16)
    elif(line.startswith('helmet:')):
      helmet = int(line[len('helmet:'):].strip(),16)
    elif(line.startswith('ap:')):
      ap = int(line[len('ap:'):].strip(),16)
    elif(line.startswith('armor:')):
      armor = int(line[len('armor:'):].strip(),16)
    elif(line.startswith('dp:')):
      dp = int(line[len('dp:'):].strip(),16)
    elif(line.startswith('shield:')):
      shield = int(line[len('shield:'):].strip(),16)

  array = []
  array.append(weapon)
  array.append(helmet)
  array.append(ap)
  array.append(armor)
  array.append(dp)
  array.append(shield)
 
  # lo quemo en el banco
  mystic.romSplitter.burnBank(nroBank, offset, array)

def exportSpecialItems():
  """ exporta los listados de items especiales """

  basePath = mystic.address.basePath
  path = basePath + '/items'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)


  nroBank, vaPorAddr = mystic.address.addrLoadStateStrangeBytes
  data = mystic.romSplitter.banks[nroBank]

  lines = []

  for i in range(0,4):
    lines.append('-------strangeBytes' + str(i))
    num = 0xffff
    while(num != 0x0000):
      num0 = data[vaPorAddr]
      num1 = data[vaPorAddr+1]
      num = num1*0x100 + num0
      lines.append('{:04x}'.format(num))
      vaPorAddr += 2
   
  specialItems = ['curative items', 'healing items', 'levelup items', 'sleep items', 'mute items', 'japan items', 'crystal items', 'fire items' ]

  for i in range(0,8):
 
    lines.append('-------' + specialItems[i])
    nroItem = 0xff
    while(nroItem != 0x00):
      nroItem = data[vaPorAddr]
#      print('nroItem: {:02x}'.format(nroItem))
      vaPorAddr += 1

      if(nroItem <= 8):
        itemName = mystic.variables.magias[nroItem-1]
      else:
        itemName = mystic.variables.items[nroItem-9]
#      print('item: ' + str(item))

      if(nroItem != 0x00):
        lines.append('{:02x}    # '.format(nroItem) + str(itemName))
      else:
        lines.append('{:02x}'.format(nroItem))


  string = '\n'.join(lines)

  filePath = path + '/10_specialItems.txt'
  # lo exporto al specialItems.txt
  f = open(filePath, 'w', encoding="utf-8")
  f.write(string)
  f.close()



def burnItems(tipo, filepath, nroBank, offset):
  """ quema el magic.txt en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  items = []
  primerItem = True
  subLines = []
  for line in lines:

    if('nro:' in line):
      if(not primerItem):
        item = mystic.inventory.Item(tipo)
        item.decodeTxt(subLines)
        items.append(item)
      else:
        primerItem = False

      subLines = []
    subLines.append(line)
  item = mystic.inventory.Item(tipo)
  item.decodeTxt(subLines)
  items.append(item)

  array = []
  for item in items:
#    print('item: ' + str(item))
    subArray = item.encodeRom()
    array.extend(subArray)

  # lo quemo en el banco
  mystic.romSplitter.burnBank(nroBank, offset, array)

  vaPorAddr = offset + len(array)
  return vaPorAddr

def burnApdp(filepath, nroBank, offset):
  """ quema el apdp.txt en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  array = []

  ap = mystic.inventory.Apdp()
  ap.decodeTxt(lines[0:3])
  subArray = ap.encodeRom()
  array.extend(subArray)
 
  dp = mystic.inventory.Apdp()
  dp.decodeTxt(lines[4:7])
  subArray = dp.encodeRom()
  array.extend(subArray)

#  strHexa = mystic.util.strHexa(array)
#  print('strHexa: ' + strHexa)

  # lo quemo en el banco
  mystic.romSplitter.burnBank(nroBank, offset, array)

  vaPorAddr = offset + len(array)
  return vaPorAddr

def burnVendor(filepath, nroBank, offset):
  """ quema el vendor.txt en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  array = []

#  print('lines: ' + str(lines))

  vendors = []
  primerVendor = True
  subLines = []
  for line in lines:

    if('--- vendor:' in line):
      if(not primerVendor):
        vend = mystic.inventory.Vendor()
        vend.decodeTxt(subLines)
        vendors.append(vend)
      else:
        primerVendor = False

      subLines = []
    subLines.append(line)

  vend = mystic.inventory.Vendor()
  vend.decodeTxt(subLines)
  vendors.append(vend)
 
  array = []
  for vend in vendors:
#    print('vend: ' + str(vend))
    subArray = vend.encodeRom()
#    strHexa = mystic.util.strHexa(subArray)
#    print('strHexa: ' + strHexa)
    array.extend(subArray)

  # lo quemo en el banco
  mystic.romSplitter.burnBank(nroBank, offset, array)

  vaPorAddr = offset + len(array)
  return vaPorAddr

def burnSpecialItems(filepath, nroBank, offset):
  """ quema el specialItems.txt en la rom """

  f = open(filepath, 'r', encoding="utf-8")
  lines = f.readlines()
  f.close()

  cambio = False
  strangeLines = []
  specialLines = []
  for line in lines:

    if(line.startswith('-------curative items')):
      cambio = True

    if(not cambio):
      strangeLines.append(line)
    else:
      specialLines.append(line)


  array = []

  listados = []
  listado = [] 
  primerListado = True 
  for line in strangeLines:
#    print('line: ' + line)

    if(line.startswith('-------')):
      if(not primerListado):
#        print('encontro listado: ' + str(listado))
        listados.append(listado)
        listado = []
      primerListado = False
    else:
      num = int(line.strip()[0:5],16)
#      print('num: {:04x}'.format(num))
      listado.append(num)

#  print('encontro listado: ' + str(listado))
  listados.append(listado)


  for listado in listados:
#    print('listado----')
    for num in listado:
#      print('num: {:04x}'.format(num))
      byte0 = num // 0x100
      byte1 = num % 0x100

#      print('byte0: {:02x}'.format(byte0))
#      print('byte1: {:02x}'.format(byte1))

      array.extend([byte1, byte0])

  specials = []
  special = [] 
  primerSpecial = True 
  for line in specialLines:
#    print('line: ' + line)

    if(line.startswith('-------')):
      if(not primerSpecial):
#        print('encontro special: ' + str(special))
        specials.append(special)
        special = []
      primerSpecial = False
    else:
      num = int(line.strip()[0:5],16)
#      print('num: {:04x}'.format(num))
      special.append(num)

#  print('encontro special: ' + str(special))
  specials.append(special)


  for special in specials:
#    print('special----')
    for num in special:
#      print('num: {:02x}'.format(num))
      array.append(num)
 
  # lo quemo en el banco
  mystic.romSplitter.burnBank(nroBank, offset, array)

  vaPorAddr = offset + len(array)
  return vaPorAddr


def exportSolarus():

  print('exportando a solarus...')

#  basePath = mystic.address.basePath
#  path = basePath + '/scripts'
  path = './solarusQuest'
  # si el directorio no existía
  if not os.path.exists(path):
    # lo creo
    os.makedirs(path)

  # exporto los spriteSheets
  for k in range(0,5):
    sheet = mystic.romSplitter.spriteSheets[k]

    lines = []
    lines.append('background_color{ 255, 255, 255 }')
    sheet.exportPngFile('./solarusQuest/data/tilesets/sheet_{:02}.tiles.png'.format(k))
    i = 0
    for sprite in sheet.sprites:
#      print('sprite: {:02x}'.format(sprite.bloqueo))

      x = (i%16)
      y = (i//16)

      lines.append('tile_pattern{')
      lines.append(' id = "' + str(i) + '",')
      ground = 'traversable'
#      ground = 'traversable' if sprite.bloqueo == 0x30 else 'wall'
      lines.append(' ground = "' + ground + '",')
      lines.append(' default_layer = 0,')
      lines.append(' x = ' + str(16*x) + ',')
      lines.append(' y = ' + str(16*y) + ',')
      lines.append(' width = 16,')
      lines.append(' height = 16,')
      lines.append('}')

      i += 1

    f = open('./solarusQuest/data/tilesets/sheet_{:02}.dat'.format(k), 'w', encoding="utf-8")
    f.write('\n'.join(lines))
    f.close()

  mapas = Mapas()
  # decodifico los scripts
  mapas.decodeRom()

  for m in range(0, 0x10):
    mapa = mapas.mapas[m]

    width = mapa.mapa.sizeX
    height = mapa.mapa.sizeY
    nroSpriteSheet = mapa.nroSpriteSheet
    for k in range(0, width*height):
      bloque = mapa.mapa.bloques[k]

      bloquex = k % width
      bloquey = k // width

      lines = []

      lines.append('properties{')
      lines.append('  x = 0,')
      lines.append('  y = 0,')
      lines.append('  width = 160,')
      lines.append('  height = 128,')
      lines.append('  min_layer = 0,')
      lines.append('  max_layer = 2,')
      lines.append('  tileset = "sheet_{:02}",'.format(nroSpriteSheet))
      lines.append('}\n')


      for j in range(0,8):
        for i in range(0,10):
          nro = bloque.getSprites()[j][i]
          print('sprite: ' + str(nro))

 
          lines.append('tile{')
          lines.append('  layer = 0,')
          lines.append('  x = ' + str(16*i) + ',')
          lines.append('  y = ' + str(16*j) + ',')
          lines.append('  width = 16,')
          lines.append('  height = 16,')
          lines.append('  pattern = "' + str(nro) + '",')
          lines.append('}\n')

      lines.append('teletransporter{')
      lines.append('  layer = 0,')
      lines.append('  x = 160,')
      lines.append('  y = 0,')
      lines.append('  width = 16,')
      lines.append('  height = 128,')
      lines.append('  transition = "scrolling",')
      lines.append('  destination_map = "mapa_{:02x}_{:02}_{:02}_map",'.format( m, (width+bloquex+1)%width, bloquey ))
      lines.append('  destination = "_side",')
      lines.append('}\n')

      lines.append('teletransporter{')
      lines.append('  layer = 0,')
      lines.append('  x = -16,')
      lines.append('  y = 0,')
      lines.append('  width = 16,')
      lines.append('  height = 128,')
      lines.append('  transition = "scrolling",')
      lines.append('  destination_map = "mapa_{:02x}_{:02}_{:02}_map",'.format( m, (width+bloquex-1)%width, bloquey ))
      lines.append('  destination = "_side",')
      lines.append('}\n')

      lines.append('teletransporter{')
      lines.append('  layer = 0,')
      lines.append('  x = 0,')
      lines.append('  y = -16,')
      lines.append('  width = 160,')
      lines.append('  height = 16,')
      lines.append('  transition = "scrolling",')
      lines.append('  destination_map = "mapa_{:02x}_{:02}_{:02}_map",'.format( m, bloquex, (height+bloquey-1)%height ))
      lines.append('  destination = "_side",')
      lines.append('}\n')

      lines.append('teletransporter{')
      lines.append('  layer = 0,')
      lines.append('  x = 0,')
      lines.append('  y = 128,')
      lines.append('  width = 160,')
      lines.append('  height = 16,')
      lines.append('  transition = "scrolling",')
      lines.append('  destination_map = "mapa_{:02x}_{:02}_{:02}_map",'.format( m, bloquex, (height+bloquey+1)%height ))
      lines.append('  destination = "_side",')
      lines.append('}\n')

      f = open('./solarusQuest/data/maps/mapa_{:02x}_{:02}_{:02}_map.dat'.format(m, bloquex, bloquey), 'w', encoding="utf-8")
      f.write('\n'.join(lines))
      f.close()

