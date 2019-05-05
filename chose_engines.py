import glob
from os.path import join, normpath
import re

'''
Read the ratings file and return the ratings and error bars of
all engines by short name
'''
def read_ratings(rfile):
  rate = {}
  errb = {}
  with open(rfile, mode='r', encoding='ascii') as f:
    head = False
    for line in f.readlines():
      fields = line.rstrip().split()
      if len(fields) == 9:
        if head:
          rate[fields[1]] = int(fields[2])
          errb[fields[1]] = int(fields[3])
        elif fields[1] == 'Name' and fields[2] == 'Elo':
          head = True
  return rate, errb

'''
Find engines in the given directory and return a map
of short names to full names of the engines
Consider only engines which have short names in the given
rating dictionary
'''
def read_engines(engdir, rate):
  pat = join(engdir, '*.exe')
  short_2_full = {}
  # Regex to find the engine short name from the full name
  short_re = re.compile(r'.+-0\.\d\.0-(.*)\.exe$')
  for f in glob.glob(pat):
    match = short_re.match(f)
    if match:
      short = match.group(1)
      if short in rate:
        short_2_full[short] = f
    else:
      print('Not matching:', f)
  return short_2_full
  #exefile = join(engdir, 'Barbarossa-0.6.0-lts6.exe')

'''
Take all necessary engines data: short name to full name map, rating and error bars
'''
def engines_data():
  ratefile = normpath(join('c:', '/', 'astra', 'rating-20190417.txt'))
  engdir = normpath(join('c:', '/', 'Engines', 'Barbarossa'))

  rate, errb = read_ratings(ratefile)
  short_2_full = read_engines(engdir, rate)

  # print(len(short_2_full))
  return short_2_full, rate, errb