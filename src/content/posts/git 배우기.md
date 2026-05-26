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

원격 파트는 솔직히 처음에 왜 이게 필요한지 잘 몰랐다. `git push` 하면 알아서 올라가는 거 아닌가 했는데, fetch*(원격 저장소의 변경사항을 가져오기만 하고 합치지는 않는 명령어)*랑 pull*(가져오면서 바로 내 브랜치에 합치는 명령어)* 차이도 있고, remote tracking branch*(원격 저장소의 브랜치 상태를 로컬에서 추적하는 브랜치)* 같은 개념도 있고 생각보다 할 게 많았다.

Push Main! 문제에서 한 번 막혔는데 뭔가 main 브랜치가 원격이랑 달라서 그냥 push가 안 되는 상황이었다. 결국 force push*(강제로 덮어씌우는 push, 근데 위험해서 함부로 쓰면 안 됨)* 쓰는 게 맞나 싶었는데 아니었고, rebase*(내 커밋들을 다른 브랜치의 최신 상태 위에 다시 쌓는 것)* 를 먼저 해야 했다.

---

## 지금까지 써본 명령어 정리

공부하면서 실제로 쓴 것들 모아봤다.

### 기본 작업 흐름

```bash
git status                  # 현재 변경된 파일 확인
git add 파일명              # 특정 파일 스테이징
git add .                   # 변경된 파일 전부 스테이징
git commit -m "메시지"      # 커밋 (스냅샷 저장)
git push origin main        # 원격 저장소에 올리기
git pull                    # 원격 변경사항 가져와서 합치기
```

### 로그 & 상태 확인

```bash
git log                     # 커밋 히스토리 보기
git log --oneline           # 한 줄씩 간략하게 보기
git diff                    # 스테이징 안 된 변경사항 확인
git diff --staged           # 스테이징된 변경사항 확인
```

### 브랜치

```bash
git branch                  # 브랜치 목록 확인
git branch 이름             # 새 브랜치 만들기
git checkout 이름           # 브랜치 이동
git checkout -b 이름        # 만들면서 바로 이동
git merge 브랜치명          # 현재 브랜치에 다른 브랜치 합치기
```

### 되돌리기

```bash
git reset HEAD~1            # 마지막 커밋 취소 (변경사항은 유지)
git reset --hard HEAD~1     # 마지막 커밋 완전히 되돌리기 (위험)
git revert 커밋해시         # 커밋을 되돌리는 새 커밋 만들기
```

### 원격 관련

```bash
git fetch                   # 원격 변경사항 가져오기만 (합치지 않음)
git push -u origin 브랜치명 # 처음 push 할 때 upstream 설정
```

### 임시 저장

```bash
git stash                   # 작업 중인 변경사항 임시 저장
git stash pop               # 저장해둔 변경사항 꺼내기
```

### learngitbranching에서 배운 것들

```bash
# rebase & cherry-pick
git rebase 브랜치명              # 내 커밋들을 다른 브랜치 위에 다시 쌓기
git rebase main bugFix           # bugFix를 main 위에 리베이스
git rebase -i HEAD~3             # 인터랙티브 리베이스 (순서 변경·삭제 등)
git cherry-pick 커밋해시          # 원하는 커밋만 골라서 가져오기
git cherry-pick C3 C4 C7         # 여러 커밋 한번에 가져오기
```

```bash
# 상대 참조 & 브랜치 이동
git checkout HEAD~2              # HEAD에서 2단계 전 커밋으로 이동
git checkout 브랜치명^           # 브랜치의 부모 커밋으로 이동
git branch -f main HEAD~3        # 브랜치를 특정 커밋으로 강제 이동
```

```bash
# 커밋 수정 & 되돌리기
git commit --amend               # 가장 최근 커밋 수정
git revert HEAD                  # 커밋을 되돌리는 새 커밋 만들기 (원격에 안전)
```

```bash
# 태그
git tag v1 C2                    # 특정 커밋에 태그 달기
git tag v1                       # 현재 HEAD에 태그 달기
```

```bash
# 원격 고급
git push origin foo:main         # 로컬 foo를 원격 main으로 push
git push origin :foo             # 원격 foo 브랜치 삭제
git fetch origin c3:foo          # 원격 c3을 로컬 foo로 fetch
git fetch origin :bar            # 로컬 bar 브랜치 생성
git pull --rebase                # fetch 후 merge 대신 rebase
git pull origin c3:foo           # fetch + merge, refspec 지정
git checkout -b side o/main      # 원격 브랜치 추적하는 새 브랜치 만들기
```

`rebase`랑 `cherry-pick`은 개념은 이해했는데 실제로 언제 쓰는지 감을 잡는 게 좀 걸렸다. 특히 `cherry-pick`은 커밋 해시*(각 커밋에 붙는 고유 ID)* 를 직접 지정해야 해서 처음엔 헷갈렸다.

---

## 느낀 점

솔직히 말하면 git을 1년 넘게 쓰면서 브랜치*(작업을 독립적으로 나눠서 진행할 수 있는 줄기)* 를 제대로 써본 적이 거의 없었다. 그냥 main 하나에 다 올렸었는데, 이번에 공부하면서 왜 브랜치를 쓰는지, rebase랑 merge*(두 브랜치를 합치는 것)* 가 어떻게 다른지 조금은 감이 온 것 같다.

게임처럼 만들어놔서 그런지 질리지 않고 할 수 있는 것 같다.

다음엔 실제 프로젝트에서 브랜치 제대로 나눠서 써보는 걸 목표로 해봐야겠다