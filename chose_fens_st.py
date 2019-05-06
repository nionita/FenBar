# Chose fens by analysing them with many engines and favour
# those which give high variance between engines

# This is the single threaded version

import logging
from os.path import join, normpath
import re
from chose_engines import engines_data
from chess.uci import UCI
# from classify_score import classify_score

# If we analyse with fixed depth, we get 3 problems:
# - positions of different game phases are treated differently from normal play
# (where end game position reach more quickly a given depth)
# - tactical positions are treated differently because of check extensions
# - engines with more than 1 thread, which are stronger, cannot expose theyr advantage
# DEPTH=6
TIME=500
logger = None
engines = None

'''
Generate a possibly bounded number of fen batches
of the given size from the given fen file
'''
def batch_generator(fenfile, batch_size=100, max_batches=None):
  lastsl = re.compile(r'/ ')
  zero2f = re.compile(r' \d+ \d+$')
  with open(fenfile, mode='r', encoding='ascii') as f:
    batches = 0
    batch = []
    for line in f.readlines():
      fen = re.sub(lastsl, ' ', line.rstrip())
      fen = re.sub(zero2f, ' 0 0', fen)
      batch.append(fen)
      if len(batch) >= batch_size:
        batches += 1
        yield batch
        batch = []
        if max_batches is not None and batches >= max_batches:
          break
    if len(batch) > 0:
      yield batch

'''
The results consumer
Results come also in batches
'''
def result_writer(resfile, results):
  with open(resfile, mode='a', encoding='utf-8') as f:
    for fen, short, depth, score, bm in results:
      # Our fen contains in last 3 chars the counters, which we don't want in the epd
      # For the engine (short) name we use tcsi (telecommunication sender identification)
      f.write('{}tcsi {};acd {};bm {};'.format(fen[:-3], short, depth, bm))
      if score[0] == 'mate':
        f.write('dm {}\n'.format(score[1]))
      else:
        f.write('ce {}\n'.format(score[1]))
      # logger.debug('{} -> {} -> {} -> {}'.format(short, fen, score, cat))

'''
The worker gets tasks in form of pairs (shortname, fen batch)
and analyses all fens with the given engine,
returning a batch of results
'''
def worker(short, fens):
  logger.info('Engine {}'.format(short))

  exefile = engines[short]
  logger.debug('executable is {}'.format(exefile))

  uci = UCI(exefile, '-l', '5')
  uci.start()

  results = []
  for fen in fens:
    # lines = uci.analyse_depth(fen=fen, depth=DEPTH)
    lines = uci.analyse_time(fen=fen, atime=TIME)
    score = uci.find_score(lines)
    # cat = classify_score(score)
    depth = uci.find_depth(lines)
    bm = uci.find_best_move(lines)
    results.append((fen, short, depth, score, bm))
  uci.quit()
  return results

if __name__ == '__main__':
  logger = logging.getLogger(__name__)
  logging.basicConfig(level=logging.INFO)

  # Take engines data
  logger.info('Reading engines data')
  engines, rate, errb = engines_data()

  fenfile = normpath(join('c:', '/', 'Engines', 'Barbarossa', 'fens1.fen'))
  resfile = 'results.txt'
  i = 0

  for batch in batch_generator(fenfile, batch_size=10, max_batches=2):
    i += 1
    logger.info('Processing batch {}'.format(i))
    for short in engines:
      res = worker(short, batch)
      result_writer(resfile, res)