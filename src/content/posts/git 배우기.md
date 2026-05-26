---
title: git 배우기
published: 2026-05-22
description: 'learngitbranching으로 git 공부하면서 느낀 점 정리'
image: ''
tags: ['git']
category: 'git'
draft: false 
lang: ''
---

# git을 처음 제대로 배워봤다

사실 git은 그냥 `git add .` 하고 `git commit -m "수정"` 하고 `git push` 하면 끝인 줄 알았다. 그게 다인 줄 알고 쭉 써왔는데, 수업에서 제대로 공부해보라는 말에 **learngitbranching.js.org** 라는 사이트를 써봤다.

처음엔 그냥 게임 같아서 별로 안 어려울 거라고 생각했는데 생각보다 빡셌다.

---

## 메인 파트 진행 현황

![learngitbranching 메인 탭 진행 현황](/images/git-main.png)

git 기본이랑 HEAD*(현재 내가 작업 중인 위치를 가리키는 포인터)* 분리하기까지는 그래도 금방 풀었는데, Cherry-pick*(여러 커밋 중에서 원하는 것만 골라서 가져오는 명령어)* 부터 살짝 막히기 시작했다. Cherry-pick은 이름부터 뭔가 있어 보여서 어렵겠다 했는데 역시나 개념 자체는 이해가 됐는데 실제로 커밋 해시*(각 커밋에 붙는 고유 ID값)* 골라서 쓰는 게 좀 헷갈렸다.

종합선물세트는 이름이 귀여운데 내용은 하나도 안 귀여웠다. 고급 문제는... 일단 시작은 했다.

---

## 원격 파트 진행 현황

![learngitbranching 원격 탭 진행 현황](/images/git-remote.png)

원격 파트는 솔직히 처음에 왜 이게 필요한지 잘 몰랐다. `git push` 하면 알아서 올라가는 거 아닌가 했는데, fetch랑 pull 차이도 있고, remote tracking branch 같은 개념도 있고 생각보다 할 게 많았다.

Push Main! 문제에서 한 번 막혔는데 뭔가 main 브랜치가 원격이랑 달라서 그냥 push가 안 되는 상황이었다. 결국 force push 쓰는 게 맞나 싶었는데 아니었고, rebase를 먼저 해야 했다.

---

## 느낀 점

솔직히 말하면 git을 1년 넘게 쓰면서 브랜치를 제대로 써본 적이 거의 없었다. 그냥 main 하나에 다 올렸었는데, 이번에 공부하면서 왜 브랜치를 쓰는지, rebase랑 merge가 어떻게 다른지 조금은 감이 온 것 같다.

게임처럼 만들어놔서 그런지 질리지 않고 할 수 있는 것 같다.

다음엔 실제 프로젝트에서 브랜치 제대로 나눠서 써보는 걸 목표로 해봐야겠다.
