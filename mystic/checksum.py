# Handle checksums for the header. This was added in ME 0.95.8 into romSplitter.py

import mystic.romSplitter

def fixChecksums():
  """ fixes the checksums for allowing playing on original hardware """

  bank0 = mystic.romSplitter.banks[0]

  # first we fix the header checksum
  prevHeaderChecksum = bank0[0x014d]
  checksum = 0
  for i in range(0x0134,0x014d):
    c = bank0[i]
    checksum -= c + 1
  headerChecksum = checksum & 0xFF
  print('setting headerChecksum (previous: {:02x}   now: {:02x})'.format(prevHeaderChecksum, headerChecksum))
  bank0[0x014d] = headerChecksum

  globalChecksum = 0
  # now we fix the global checksum
  prevGlobalChecksum = bank0[0x014E]*0x100 + bank0[0x014F]
  # zero out the checksum before calculating it.
  bank0[0x014E] = 0
  bank0[0x014F] = 0
  for bank in mystic.romSplitter.banks:
    globalChecksum = (globalChecksum + sum(bank)) & 0xFFFF

  print('setting globalChecksum (previous: {:04x} now: {:04x})'.format(prevGlobalChecksum, globalChecksum))
#  bank0[0x014E] = globalChecksum >> 8
#  bank0[0x014F] = globalChecksum & 0xFF
  bank0[0x014E] = globalChecksum // 0x100
  bank0[0x014F] = globalChecksum % 0x100
