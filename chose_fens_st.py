# Chose fens by analysing them with many engines and favour
# those which give high variance between engines

# This is the single threaded version

import logging
from os.path import join, normpath
from chose_engines import engines_data
from chess.uci import UCI
from classify_score import classify_score

DEPTH=6

# The worker gets tasks in the form of pairs (shortname, fen)
def worker(short, fenfile):
  global logger, short_2_full
  logger.info('Analyse with {}'.format(short))

  exefile = short_2_full[short]
  logger.debug('executable is {}'.format(exefile))
  uci = UCI(exefile, '-l', '5')
  uci.start()

  with open(fenfile, mode='r', encoding='ascii') as f:
    i = 0
    for line in f.readlines():
      i += 1
      fen = line.rstrip()
      lines = uci.analyse_depth(fen=fen, depth=DEPTH)
      score = uci.find_score(lines)
      cat = classify_score(score)
      logger.debug('{} -> {} -> {} -> {}'.format(short, fen, score, cat))
      if i >= 3:
        break

if __name__ == '__main__':
  logger = logging.getLogger(__name__)
  logging.basicConfig(level=logging.DEBUG)

  # Take engines data
  logger.info('Reading engines data')
  short_2_full, rate, errb = engines_data()

  fenfile = normpath(join('c:', '/', 'Engines', 'Barbarossa', 'fens1.fen'))


  for short in short_2_full:
    worker(short, fenfile)