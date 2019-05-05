import pytest
import chess.uci
from os.path import join, normpath

def test_uci_sas():
  engdir = normpath(join('c:', '/', 'Engines', 'Barbarossa'))
  exefile = join(engdir, 'Barbarossa-0.6.0-lts6.exe')
  fens = [
    '3r2r1/1p2qp1k/1Q4n1/2ppp2p/6P1/1P1R1PBP/P1P1R3/7K w - - 0 31',
    '6r1/1p1r1p1k/5R2/2pp4/P3p1P1/1P2R2P/2P5/7K w - - 1 38',
    '4BQ2/1r3P2/4Pk2/5P1q/8/p7/P7/K7 w - - 0 1',
    '3k4/2p5/2p5/K1P4p/3P1p1P/5P2/8/8 w - - 0 1'
  ]
  uci = chess.uci.UCI(exefile, '-l', '5', debug=True)
  uci.start()
  for fen in fens:
    uci.analyse_time(fen=fen, atime=1000)
    uci.analyse_depth(fen=fen, depth=5)
  uci.quit()

def test_uci_fens():
  engdir = normpath(join('c:', '/', 'Engines', 'Barbarossa'))
  exefile = join(engdir, 'Barbarossa-0.6.0-lts6.exe')
  fenfile = join(engdir, 'fens1.fen')
  uci = chess.uci.UCI(exefile, '-l', '5', debug=False)
  uci.start()
  with open(fenfile, mode='r', encoding='ascii') as f:
    i = 0
    while i < 4:
      line = f.readline().rstrip()
      if line == '':
        break
      i += 1
      uci.analyse_depth(fen=line, depth=4)
  uci.quit()

def test_uci_ani():
  engdir = normpath(join('c:', '/', 'Engines', 'Barbarossa'))
  exefile = join(engdir, 'Barbarossa-0.6.0-lts6.exe')
  fen = '3k4/2p5/2p5/K1P4p/3P1p1P/5P2/8/8 w - - 0 1'
  uci = chess.uci.UCI(exefile, '-l', '5', debug=True)
  uci.start()
  lines = uci.analyse_depth(fen=fen, depth=5)
  uci.quit()
  depth = chess.uci.UCI.find_depth(lines)
  scoreinfo = chess.uci.UCI.find_score(lines)
  bm = chess.uci.UCI.find_best_move(lines)
  assert depth == 5
  assert scoreinfo is not None
  assert scoreinfo[0] == 'cp'
  assert bm is not None