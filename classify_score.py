SCORES = [-500, -250, -150, -75, -25, 25, 75, 150, 250, 500]

def classify_score_cp(sc):
  for i in range(len(SCORES)):
    if sc < SCORES[i]:
      return i
  return len(SCORES)

def classify_score_mate(sc):
  if sc < 0:
    return 0
  else:
    return len(SCORES)

# Classify the score into a few categories
def classify_score(score):
  if score[0] == 'cp':
    return classify_score_cp(score[1])
  else:
    return classify_score_mate(score[1])