import subprocess

'''
A simple class to communicate with an UCI chess engine and ask for simple analyses
'''
class UCI:
  def __init__(self, *pargs, timeout=1.0, debug=False):
    self.pargs = pargs
    self.timeout = timeout
    self.debug = debug
    self.proc = None

  def write(self, what):
    self.proc.stdin.write(what + '\n')
    if self.debug:
      print('--> engine:', what)

  def readline(self):
    line = self.proc.stdout.readline().rstrip()
    if self.debug:
      print('<-- engine:', line)
    return line

  def start(self):
    if self.debug:
      print('Start UCI with arguments:', *self.pargs)
    self.proc = subprocess.Popen(self.pargs, bufsize=1, universal_newlines=True, close_fds=True,
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    lines = self.qa('uci', lambda x: 'uciok' in x)
    return lines

  def qa(self, question, is_last_line):
    self.write(question)
    lines = []
    ended = False
    while not ended:
      line = self.readline()
      lines.append(line)
      if len(line) == 0 or is_last_line(line):
        ended = True
    return lines

  def quit(self):
    if self.debug:
      print('--> engine: quit')
    try:
      outs, errs = self.proc.communicate(input='quit', timeout=self.timeout)
    except subprocess.TimeoutExpired:
      self.proc.kill()
      outs, errs = self.proc.communicate()
      if self.debug:
        print('Engine killed')
    self.proc = None

  def analyse_time(self, fen=None, atime=5000):
    if fen:
      pos = 'fen ' + fen
      # ptm = fen.split()[1]
    else:
      pos = 'startpos'
      # ptm = 'w'
    self.write('position ' + pos)
    tm = str(atime)
    # self.qa('go movetime ' + tm, lambda x: 'bestmove' in x)
    lines = self.qa('go movestogo 1 ' + 'wtime ' + tm + ' btime ' + tm, lambda x: 'bestmove' in x)
    return lines

  def analyse_depth(self, fen=None, depth=10):
    if fen:
      pos = 'fen ' + fen
    else:
      pos = 'startpos'
    self.write('position ' + pos)
    lines = self.qa('go depth ' + str(depth), lambda x: 'bestmove' in x)
    return lines

  @classmethod
  def find_best_move(cls, lines):
    if 'bestmove' in lines[-1]:
      return lines[-1].split()[-1]
    return None

  @classmethod
  def find_score(cls, lines):
    score = None
    for line in lines:
      if 'info' in line and 'score' in line:
        words = line.split()
        for i in range(len(words)):
          if words[i] == 'score':
            i += 1
            break
        if words[i] == 'mate':
          score = ('mate', int(words[i+1]))
        elif words[i] == 'cp':
          score = ('cp', int(words[i+1]))
    return score

  @classmethod
  def find_scores(cls, lines):
    scores = []
    for line in lines:
      if 'info' in line and 'score' in line:
        words = line.split()
        for i in range(len(words)):
          if words[i] == 'score':
            i += 1
            break
        if words[i] == 'mate':
          scores.append(('mate', int(words[i+1])))
        elif words[i] == 'cp':
          scores.append(('cp', int(words[i+1])))
    return scores

  @classmethod
  def find_depth(cls, lines):
    depth = None
    for line in lines:
      if 'info' in line and 'depth' in line:
        words = line.split()
        for i in range(len(words)):
          if words[i] == 'depth':
            i += 1
            break
        depth = int(words[i])
    return depth