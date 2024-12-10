
import mystic.romSplitter
import mystic.ippy

def romExpand():

  print('rom expanding...')

#  romExpandMBC5()

  # choose one (or none) of the following available rom expansions,
  # you can also make your own custom romExpand...()

#  romExpandMoveMaps()
#  romExpandMoveMusicBank()
  romExpandMoveMusicBankAndExpandScriptsToFourBanks()
#  romExpandIpsPatch('./roms/colorization/en_uk_256.ips')
#  romExpandIpsPatch('./roms/colorization/en_uk_kkzero.ips')

  romExpandIpsPatch('ipsFiles/patch-assembly-mana-99.ips')
  romExpandIpsPatch('ipsFiles/patch-assembly-text-speed-1.ips')
  romExpandIpsPatch('ipsFiles/patch-graphics-animation-water-jiggle.ips')
  romExpandIpsPatch('ipsFiles/patch-save-v3.ips')
  romExpandIpsPatch('ipsFiles/patch-text-window-prefer-bottom.ips')
  romExpandIpsPatch('ipsFiles/ripple-v2.ips')
  romExpandIpsPatch('ipsFiles/shutter-effect-silent.ips')
  romExpandIpsPatch('ipsFiles/skip-intro.ips')
  romExpandIpsPatch('ipsFiles/start-faded-white.ips')
  romExpandIpsPatch('ipsFiles/titlescreen-script.ips')
  romExpandIpsPatch('ipsFiles/letterbox-off.ips')
  romExpandIpsPatch('ipsFiles/broadsword.ips')

#  romExpandIpsPatch('ipsFiles/save_magic_byte_e0.ips')

#################################################
def romExpandMBC5():
  """" This patches the rom to MBC5 and expands it to 32 banks. """

  # changing the rom header, see
  # https://gbdev.gg8.se/wiki/articles/The_Cartridge_Header
  bank0 = mystic.romSplitter.banks[0]

  # Cartridge Type = MBC5+RAM+BATTERY
  bank0[0x0147] = 0x1b
  # ROM size = 32 banks
  bank0[0x0148] = 0x04
  # RAM Size = 02
  bank0[0x0149] = 0x02
  # Header Checksum
  bank0[0x014d] = 0xb8

  # we add 16 more banks
  for i in range(0,16):
    clean = [0x00] * 0x4000
    mystic.romSplitter.banks.append(clean)

#################################################
def romExpandMoveMaps():
  """" This patches the rom before encoding, to add extra capabilities. """

  bank5 = mystic.romSplitter.banks[5]
  # we clean bank5, where map 00 (the overworld) used to be. 
  # (then encode with addr_en_romexpand.txt to burn maps in bank 0x12)
  for i in range(0,0x4000):
    bank5[i] = 0xff


#################################################
def romExpandMoveMusicBank():
  """" Moving the music bank 0xF around """

  newbanknr = 0x1f

  # get the existing music bank from the assembly
  bank0 = mystic.romSplitter.banks[0x0]
  oldbanknr = bank0[0x2053]

  oldbank = mystic.romSplitter.banks[oldbanknr]
  newbank = mystic.romSplitter.banks[newbanknr]
  for i in range(0,0x4000):
    # muevo el banco old a new
    newbank[i] = oldbank[i]
    if oldbanknr != newbanknr:
      # y borro
      oldbank[i] = 0xff

  # set the music bank in asm
  bank0[0x2053] = 0x1f
  bank0[0x217c] = 0x1f

#################################################
def romExpandMoveMusicBankAndExpandScriptsToFourBanks():

  # first we move the music bank
  romExpandMoveMusicBank()

  romExpandIpsPatch('ipsFiles/script_expand.ips')
 
#################################################
def romExpandIpsPatch(pathIps):
  """ patches the rom with the ips file """

  patch = mystic.ippy.Patch()

  # the rom array
  arraySource = mystic.romSplitter.getRomArrayFromBanks()
  # the ips array
  arrayIps = mystic.util.fileToArray(pathIps)

  arrayTarget = patch._patch(arraySource, arrayIps)
#  print('arrayTarget: ' + mystic.util.strHexa(arrayTarget[:0x200]))
#  for i in range(0,0x20):
#    print('line: ' + mystic.util.strHexa(arrayTarget[0x10*i:0x10*(i+1)]))

  # load the banks
  mystic.romSplitter.loadBanksFromArray(arrayTarget)


