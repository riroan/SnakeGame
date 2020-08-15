SnakeGame
=========

Simple Console Snake Game

## 특이사항
### C
- 콘솔
- 하드코딩 인공지능

### python
- by pygame with AI
- 트리탐색 알고리즘 사용

## 적용방법
1. 현재방향에서 행동할 수 있는 모든 방향의 행동을 취한다.
2. 점수를 계산한다.(유효하지 않은 행동일 경우 점수는 -1, 낮을수록 좋음)

  score = 2 * (|x1 - x2| + |y1 - y2|)
  
3. 점수가 0이면 먹이를 먹은 경우이므로 끝내고 현재까지의 행동들을 리턴한다.(행동 수행)
4. 그 외의 경우 1번으로 돌아가 다시 수행한다.

5. 모든 방향의 점수가 -1점일 경우 죽는 경우이므로 이전 행동을 제거한 후 다른 행동을 찾아본다.
