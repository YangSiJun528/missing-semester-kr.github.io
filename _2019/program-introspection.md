---
layout: lecture
title: "프로그램 내부 살펴보기"
lang: ko
presenter: Anish
date: 2019-01-29
order: 1
video:
  aspect: 62.5
  id: 74MhV-7hYzg
---

# 디버깅
{: id="debugging"}

`printf`로 값을 출력하는 것만으로 문제를 찾기 어렵다면 디버거를 사용하세요.

디버거를 사용하면 실행 중인 프로그램을 제어하고 관찰할 수 있습니다.

- 특정 줄에 도달하면 실행 멈추기
- 한 단계씩 실행하기
- 변수 값 살펴보기
- 그 밖의 여러 고급 기능

## GDB와 LLDB
{: id="gdblldb"}

[GDB](https://www.gnu.org/software/gdb/)와 [LLDB](https://lldb.llvm.org/)는 C 계열을 비롯한 여러 언어를 지원합니다.

[example.c](/2019/files/example.c)를 살펴봅시다. 디버그 정보를 포함해 컴파일합니다.

`gcc -g -o example example.c`

GDB를 엽니다.

`gdb example`

사용할 수 있는 명령은 다음과 같습니다.

- `run`: 프로그램 실행
- `b {함수 이름}`: 함수에 중단점 설정
- `b {파일}:{줄}`: 파일의 특정 줄에 중단점 설정
- `c`: 실행 계속하기
- `step` / `next` / `finish`: 함수 안으로 들어가며 실행 / 함수 호출을 한 단계로 처리 / 현재 함수가 끝날 때까지 실행
- `p {변수}`: 변수 값 출력
- `watch {표현식}`: 표현식의 값이 바뀌면 멈추는 감시점 설정
- `rwatch {표현식}`: 값을 읽으면 멈추는 감시점 설정
- `layout`: 화면 배치 설정

## PDB
{: id="pdb"}

[PDB](https://docs.python.org/3/library/pdb.html)는 Python 디버거입니다.

디버깅을 시작하고 싶은 위치에 `import pdb; pdb.set_trace()`를 넣으세요. GDB 같은 디버거와 Python 셸을 합쳐 놓은 도구라고 생각하면 됩니다.

## 웹 브라우저 개발자 도구
{: id="web-browser-developer-tools"}

디버거의 또 다른 예입니다. 그래픽 인터페이스를 제공합니다.

# strace
{: id="strace"}

`strace {프로그램}`으로 프로그램이 호출하는 시스템 콜을 관찰할 수 있습니다.

# 프로파일링
{: id="profiling"}

프로파일링에는 CPU 사용량 분석, 메모리 사용량 분석 등이 있습니다.

가장 간단한 프로파일러는 `time`입니다.

## Go
{: id="go"}

CPU 프로파일러를 켜고 테스트를 실행합니다. `go test -cpuprofile=cpu.out`

결과를 분석합니다. `go tool pprof -web cpu.out`

메모리 프로파일러를 켜고 테스트를 실행합니다. `go test -memprofile=mem.out`

결과를 분석합니다. `go tool pprof -web mem.out`

## Perf
{: id="perf"}

기본 성능 통계를 확인합니다. `perf stat {명령}`

프로파일러로 프로그램을 실행합니다. `perf record {명령}`

결과를 분석합니다. `perf report`
