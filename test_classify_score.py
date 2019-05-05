import pytest
from classify_score import classify_score

def test_cp_scores():
  for sc in [-550, -501, -800]:
    assert classify_score(('cp', sc)) == 0
  for sc in [-499, -315, -251]:
    assert classify_score(('cp', sc)) == 1
  for sc in [-249, -215, -151]:
    assert classify_score(('cp', sc)) == 2
  for sc in [-149, -115, -76]:
    assert classify_score(('cp', sc)) == 3
  for sc in [-26, -65, -51]:
    assert classify_score(('cp', sc)) == 4
  for sc in [-24, 0, 24]:
    assert classify_score(('cp', sc)) == 5
  for sc in [26, 40, 74]:
    assert classify_score(('cp', sc)) == 6
  for sc in [76, 90, 149]:
    assert classify_score(('cp', sc)) == 7
  for sc in [151, 240, 249]:
    assert classify_score(('cp', sc)) == 8
  for sc in [251, 440, 499]:
    assert classify_score(('cp', sc)) == 9
  for sc in [501, 640, 874]:
    assert classify_score(('cp', sc)) == 10

def test_mate_scores():
  for sc in [-7, -4, -1]:
    assert classify_score(('mate', sc)) == 0
  for sc in [7, 4, 1]:
    assert classify_score(('mate', sc)) == 10