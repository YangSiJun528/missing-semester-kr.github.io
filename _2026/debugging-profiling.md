---
layout: lecture
title: "디버깅과 프로파일링"
description: >
  로그와 디버거로 오류를 찾고, 프로파일러로 코드의 성능을 분석합니다.
thumbnail: /static/assets/thumbnails/2026/lec4.png
date: 2026-01-15
ready: true
translation_status: ai-draft
human_review: pending
translation_source: 1d695c94ccafdce3f06d6b9dfe3e6f106097693a
panopto: "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=a72c48e3-5eb2-46fa-aa03-b3b700e1ca8d"
video:
  aspect: 56.25
  id: 8VYT9TcUmKs
---

프로그래밍의 중요한 원칙은 코드가 여러분의 기대가 아니라 명령한 대로 동작한다는 것입니다. 그 차이를 메우기는 때로 어렵습니다. 이번 강의에서는 버그가 있거나 자원을 많이 쓰는 코드를 다루는 기법인 디버깅과 프로파일링을 배웁니다.

# 디버깅
{: #debugging}

## 출력문 디버깅과 로깅
{: #printf-debugging-and-logging}

> "가장 효과적인 디버깅 도구는 여전히 신중한 사고와 적절한 위치에 배치한 출력문이다." — Brian Kernighan, *Unix for Beginners*.

가장 먼저 시도할 방법은 문제가 발견된 곳 주변에 출력문을 넣고, 원인을 이해할 만큼 정보가 모일 때까지 반복하는 것입니다.

두 번째 방법은 임시 출력문 대신 로깅을 사용하는 것입니다. 로깅은 좀 더 체계적인 출력이며, 보통 다음 기능이 있는 프레임워크를 사용합니다.

- 전체 로그나 일부를 다른 출력 위치로 보냅니다.
- INFO, DEBUG, WARN, ERROR 같은 심각도 수준을 지정하고 필터링합니다.
- 로그와 관련된 데이터를 구조화하여 나중에 쉽게 추출합니다.

로그는 보통 개발 중에 미리 넣으므로, 디버깅에 필요한 정보가 이미 남아 있을 수도 있습니다. 출력문으로 문제를 찾아 고쳤다면 곧바로 지우기보다 적절한 로그로 바꾸는 것도 좋습니다. 비슷한 버그가 다시 생겼을 때 코드를 고치지 않고도 진단 정보를 얻을 수 있습니다.

> **외부 프로그램의 로그**: 많은 프로그램은 `-v`나 `--verbose`로 자세한 출력을 제공합니다. 명령 실패 원인을 찾을 때 유용하며, 플래그를 반복하면 더 자세해지는 프로그램도 있습니다. 데이터베이스나 웹 서버 같은 서비스는 로그를 확인하세요. Linux에서는 흔히 `/var/log/`에 있고, systemd 서비스는 `journalctl -u <service>`로 확인합니다. 외부 라이브러리도 환경 변수나 설정으로 디버그 로깅을 지원하는지 살펴보세요.

## 디버거
{: #debuggers}

무엇을 출력할지 알고 코드를 쉽게 수정·재실행할 수 있다면 출력문 디버깅이 효과적입니다. 반면 필요한 정보가 불분명하거나, 재현하기 어려운 조건에서만 버그가 생기거나, 긴 초기화나 복잡한 상태 때문에 수정·재시작 비용이 클 때는 디버거가 유용합니다.

디버거는 실행 중인 프로그램과 상호작용하며 다음 작업을 할 수 있게 합니다.

- 특정 줄에 도달하면 실행을 멈춥니다.
- 명령을 하나씩 실행합니다.
- 충돌 후 변수의 값을 확인합니다.
- 지정한 조건을 만족할 때만 멈춥니다.
- 이 밖에도 여러 고급 기능을 제공합니다.

대부분의 언어는 디버거를 제공하거나 지원합니다. [`gdb`](https://www.gnu.org/software/gdb/)(GNU Debugger), [`lldb`](https://lldb.llvm.org/)(LLVM Debugger) 같은 **범용 디버거**는 네이티브 바이너리를 디버깅합니다. Python의 pdb나 Java의 jdb처럼 런타임과 더 밀접하게 통합된 **언어 전용 디버거**도 있습니다.

`gdb`는 C, C++, Rust 등 컴파일 언어에서 사실상의 표준 디버거입니다. 거의 모든 프로세스의 레지스터, 스택, 프로그램 카운터 등 현재 상태를 조사할 수 있습니다.

유용한 GDB 명령은 다음과 같습니다.

- `run`: 프로그램을 시작합니다.
- `b {function}` 또는 `b {file}:{line}`: 중단점을 설정합니다.
- `c`: 계속 실행합니다.
- `step` / `next` / `finish`: 함수 안으로 들어가며 한 단계 실행 / 함수 호출을 건너뛰며 한 단계 실행 / 현재 함수를 빠져나올 때까지 실행합니다.
- `p {variable}`: 변수 값을 출력합니다.
- `bt`: 호출 스택을 표시합니다.
- `watch {expression}`: 값이 바뀌면 멈춥니다.

> `gdb -tui`나 GDB 안에서 `Ctrl-x a`로 TUI 모드를 켜면 소스 코드와 명령 프롬프트를 분할 화면으로 볼 수 있습니다.

### 기록·재생 디버깅
{: #record-replay-debugging}

특히 까다로운 버그는 관찰하려고 하면 사라지거나 동작이 달라지는 *하이젠버그(Heisenbug)*입니다. 경쟁 조건, 타이밍에 민감한 버그, 특정 시스템 상태에서만 나타나는 문제가 여기에 해당합니다. 다시 실행할 때 동작이 달라져 일반적인 디버깅이 통하지 않기도 합니다. 출력문이 코드를 느리게 만들어 경쟁 조건이 사라지는 경우가 한 예입니다.

**기록·재생 디버깅**은 실행을 기록한 뒤 같은 실행을 원하는 만큼 결정적으로 재생합니다. 실행을 *거꾸로* 따라가며 문제가 생긴 정확한 지점을 찾을 수도 있습니다.

Linux의 [rr](https://rr-project.org/)은 실행을 기록하고 완전한 디버깅 기능으로 재생하는 도구입니다. GDB를 사용하므로 익숙한 인터페이스를 그대로 쓸 수 있습니다.

기본 사용법은 다음과 같습니다.

```bash
# Record a program execution
rr record ./my_program

# Replay the recording (opens GDB)
rr replay
```

재생 중에는 실행이 결정적이므로 **역방향 디버깅** 명령을 사용할 수 있습니다.

- `reverse-continue`(`rc`): 중단점을 만날 때까지 거꾸로 실행합니다.
- `reverse-step`(`rs`): 한 줄 뒤로 갑니다.
- `reverse-next`(`rn`): 함수 호출을 건너뛰며 한 단계 뒤로 갑니다.
- `reverse-finish`: 현재 함수에 진입한 지점까지 거슬러 올라갑니다.

프로그램이 충돌했다면 버그 위치를 추측해 중단점을 놓는 대신 다음과 같이 할 수 있습니다.

1. 충돌 지점까지 실행합니다.
2. 손상된 상태를 확인합니다.
3. 손상된 변수에 감시점을 설정합니다.
4. `reverse-continue`로 손상된 정확한 지점을 찾습니다.

**rr을 쓰기 좋은 경우:**

- 간헐적으로 실패하는 테스트
- 경쟁 조건과 스레드 버그
- 재현하기 어려운 충돌
- "시간을 되돌리고 싶은" 모든 버그

> rr은 Linux에서만 동작하며 하드웨어 성능 카운터가 필요합니다. 대부분의 AWS EC2 인스턴스처럼 이 카운터를 노출하지 않는 VM에서는 작동하지 않고, GPU 접근도 지원하지 않습니다. macOS에서는 [Warpspeed](https://warpspeed.dev/)를 살펴보세요.

> **rr과 동시성**: rr은 결정적 기록을 위해 스레드 스케줄링을 직렬화합니다. 특정 타이밍에 의존하는 경쟁 조건은 기록 중 나타나지 않을 수도 있습니다. 실패한 실행만 확보하면 안정적으로 재생할 수 있지만, 간헐적 버그를 잡으려면 여러 번 기록해야 할 수 있습니다. 동시성과 무관한 버그에서는 정확한 실행을 재현하고 역방향으로 손상 원인을 찾을 수 있어 특히 유용합니다.

## 시스템 호출 추적
{: #system-call-tracing}

프로그램과 운영체제의 상호작용을 알아야 할 때도 있습니다. 프로그램은 [시스템 호출](https://en.wikipedia.org/wiki/System_call)로 파일 열기, 메모리 할당, 프로세스 생성 등을 커널에 요청합니다. 이를 추적하면 왜 멈춰 있는지, 어떤 파일에 접근하려는지, 어디에서 기다리는지 알 수 있습니다.

### strace(Linux)와 dtruss(macOS)
{: #strace-linux-and-dtruss-macos}

[`strace`](https://www.man7.org/linux/man-pages/man1/strace.1.html)는 프로그램의 모든 시스템 호출을 보여 줍니다.

```bash
# Trace all system calls
strace ./my_program

# Trace only file-related calls
strace -e trace=file ./my_program

# Follow child processes (important for programs that start other programs)
strace -f ./my_program

# Trace a running process
strace -p <PID>

# Show timing information
strace -T ./my_program
```

> macOS와 BSD에서는 `dtrace`를 감싸는 [`dtruss`](https://www.manpagez.com/man/1/dtruss/)로 비슷한 기능을 사용할 수 있습니다.

> 더 알아보려면 Julia Evans의 [strace 소책자](https://jvns.ca/strace-zine-unfolded.pdf)를 참고하세요.

### bpftrace와 eBPF
{: #bpftrace-and-ebpf}

[eBPF](https://ebpf.io/)(extended Berkeley Packet Filter)는 Linux 커널 안에서 샌드박스 프로그램을 실행하는 강력한 기술입니다. [`bpftrace`](https://github.com/iovisor/bpftrace)는 eBPF 프로그램을 작성하는 고수준 문법을 제공합니다. 커널 안에서 프로그램을 실행하므로 표현력이 크지만, awk와 비슷한 문법은 다소 낯설 수 있습니다. 주로 시스템 호출을 조사하며 호출 수나 지연 통계를 집계하고, 호출 인자를 살펴보거나 조건으로 필터링합니다.

```bash
# Trace file opens system-wide (prints immediately)
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_openat { printf("%s %s\n", comm, str(args->filename)); }'

# Count system calls by name (prints summary on Ctrl-C)
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_* { @[probe] = count(); }'
```

[`bcc`](https://github.com/iovisor/bcc) 같은 도구 모음으로 eBPF 프로그램을 C로 직접 작성할 수도 있습니다. 디스크 작업의 지연을 살펴보는 `biosnoop`, 열린 파일을 출력하는 `opensnoop` 등 [유용한 도구](https://www.brendangregg.com/blog/2015-09-22/bcc-linux-4.3-tracing.html)도 함께 제공됩니다.

`strace`는 바로 시작하기 편합니다. 더 낮은 오버헤드, 커널 함수 추적, 집계가 필요하면 `bpftrace`를 사용하세요. 다만 `root` 권한이 필요하며 보통 특정 프로세스가 아니라 커널 전체를 관찰합니다. 명령 이름이나 PID로 대상을 좁힐 수 있습니다.

```bash
# Filter by command name (prints summary on Ctrl-C)
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_* /comm == "bash"/ { @[probe] = count(); }'

# Trace a specific command from startup using -c (cpid = child PID)
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_* /pid == cpid/ { @[probe] = count(); }' -c 'ls -la'
```

`-c`는 명령을 실행하고 그 PID를 `cpid`에 설정합니다. 시작 순간부터 추적할 때 유용하며, 대상 명령이 종료되면 집계 결과가 출력됩니다.

### 네트워크 디버깅
{: #network-debugging}

[`tcpdump`](https://www.man7.org/linux/man-pages/man1/tcpdump.1.html)와 [Wireshark](https://www.wireshark.org/)로 패킷을 캡처하고 분석할 수 있습니다.

```bash
# Capture packets on port 80
sudo tcpdump -i any port 80

# Capture and save to file for Wireshark analysis
sudo tcpdump -i any -w capture.pcap
```

HTTPS는 암호화되어 있어 tcpdump만으로 얻는 정보가 제한됩니다. [mitmproxy](https://mitmproxy.org/) 같은 도구는 중간 프록시로 암호화된 트래픽을 조사합니다. 웹 애플리케이션의 HTTPS 요청은 브라우저 개발자 도구의 Network 탭으로 디버깅하는 것이 가장 간단한 경우가 많습니다. 복호화된 요청·응답 데이터, 헤더, 소요 시간을 보여 줍니다.

## 메모리 디버깅
{: #memory-debugging}

버퍼 오버플로, 해제 후 사용, 메모리 누수는 위험하고 디버깅하기 어려운 버그입니다. 즉시 충돌하지 않고 메모리를 손상시켰다가 훨씬 나중에 문제를 일으키기도 합니다.

### 새니타이저
{: #sanitizers}

**새니타이저(sanitizer)**는 코드에 검사 기능을 넣어 실행 중 오류를 탐지하는 컴파일러 기능입니다. 널리 쓰이는 **AddressSanitizer(ASan)**는 다음을 탐지합니다.

- 스택·힙·전역 버퍼 오버플로
- 해제 후 사용(use-after-free)
- 함수 반환 후 해당 스택 메모리 사용(use-after-return)
- 메모리 누수

```bash
# Compile with AddressSanitizer
gcc -fsanitize=address -g program.c -o program
./program
```

다른 새니타이저도 유용합니다.

- **ThreadSanitizer(TSan)**: 멀티스레드 코드의 데이터 경쟁을 탐지합니다(`-fsanitize=thread`).
- **MemorySanitizer(MSan)**: 초기화하지 않은 메모리 읽기를 탐지합니다(`-fsanitize=memory`).
- **UndefinedBehaviorSanitizer(UBSan)**: 정수 오버플로 같은 정의되지 않은 동작을 탐지합니다(`-fsanitize=undefined`).

다시 컴파일해야 하지만, CI 파이프라인과 평소 개발에 사용할 수 있을 만큼 빠릅니다.

### Valgrind: 다시 컴파일할 수 없을 때
{: #valgrind-when-you-cant-recompile}

[Valgrind](https://valgrind.org/)는 가상 머신과 비슷한 환경에서 프로그램을 실행해 메모리 오류를 탐지합니다. 새니타이저보다 느리지만 다시 컴파일할 필요가 없습니다.

```bash
valgrind --leak-check=full ./my_program
```

다음과 같은 경우에 사용하세요.

- 소스 코드가 없을 때
- 외부 라이브러리 등 다시 컴파일할 수 없는 코드가 있을 때
- 새니타이저에 없는 특정 도구가 필요할 때

Valgrind는 강력한 실행 제어 환경이며, 뒤의 프로파일링에서도 다시 다룹니다.

## AI를 이용한 디버깅
{: #ai-for-debugging}

대규모 언어 모델은 기존 도구를 보완하는 디버깅 보조 수단으로 유용해졌습니다. 특히 다음 작업에 강점이 있습니다.

- **난해한 오류 메시지 설명**: C++ 템플릿이나 Rust 빌림 검사기의 오류를 쉬운 말로 풀고 수정안을 제안합니다.
- **언어와 추상화 경계 탐색**: Python 바인딩으로 드러나는 C 라이브러리 버그처럼 여러 언어에 걸친 문제에서 계층을 따라가도록 돕습니다. FFI 경계, 빌드 시스템, 의존 라이브러리의 버그 등 언어 간 문제를 조사하는 데 유용합니다.
- **증상과 원인 연결**: "프로그램은 작동하지만 예상보다 메모리를 10배 쓴다" 같은 모호한 증상에서 가능한 원인과 확인할 사항을 제안합니다.
- **크래시 덤프와 스택 추적 분석**: 스택 추적을 붙여 넣고 가능한 원인을 물어볼 수 있습니다.

> **디버그 심볼**: 의미 있는 스택 추적과 디버깅을 위해 바이너리와 연결하는 라이브러리를 디버그 심볼(`-g`)과 함께 컴파일하세요. 디버그 정보는 보통 DWARF 형식입니다. 프레임 포인터를 유지하는 `-fno-omit-frame-pointer`도 특히 프로파일링 도구의 스택 추적을 더 신뢰할 수 있게 합니다. 그렇지 않으면 주소만 나오거나 일부가 빠질 수 있습니다. Python·Java보다 C++·Rust 같은 네이티브 컴파일 프로그램에서 더 중요합니다.

한계도 기억하세요.

- 그럴듯하지만 틀린 설명을 만들어 낼 수 있습니다.
- 버그를 고치는 대신 증상만 숨기는 수정을 제안할 수 있습니다.
- 실제 디버깅 도구로 제안을 검증하세요.
- 코드 이해를 대신하기보다 보완할 때 가장 효과적입니다.

> 개발 환경 강의의 [일반적인 AI 코딩 기능](/2026/development-environment/#ai-powered-development)과는 구별됩니다. 여기서는 디버깅 보조 용도에 집중합니다.

# 프로파일링
{: #profiling}

코드가 기대한 기능을 수행해도 CPU나 메모리를 모두 차지한다면 충분하지 않습니다. 알고리즘 수업은 빅 *O* 표기법을 가르치지만 프로그램의 병목을 찾는 법은 잘 가르치지 않습니다. [성급한 최적화는 모든 악의 근원](https://wiki.c2.com/?PrematureOptimization)이라는 말처럼, 먼저 프로파일러와 모니터링 도구를 익히세요. 시간과 자원을 많이 쓰는 부분을 알아야 그곳에 최적화를 집중할 수 있습니다.

## 시간 측정
{: #timing}

가장 간단한 성능 측정은 소요 시간을 재는 것입니다. 두 지점 사이의 경과 시간을 출력하는 것만으로 충분한 경우도 많습니다.

하지만 다른 프로세스가 실행 중이거나 이벤트를 기다릴 수 있어 실제 경과 시간만으로는 오해할 수 있습니다. `time`은 *Real*, *User*, *Sys*를 구분합니다.

- **Real**: 대기를 포함한 시작부터 종료까지의 실제 경과 시간.
- **User**: 사용자 코드를 CPU에서 실행한 시간.
- **Sys**: 커널 코드를 CPU에서 실행한 시간.

```bash
$ time curl https://missing.csail.mit.edu &> /dev/null
real	0m0.272s
user	0m0.079s
sys	    0m0.028s
```

요청에 약 300ms가 걸렸지만 CPU 사용 시간은 107ms(user + sys)뿐입니다. 나머지는 네트워크 대기입니다.

## 자원 모니터링
{: #resource-monitoring}

성능 분석의 첫 단계는 실제 자원 사용량을 파악하는 것일 수 있습니다. 자원이 부족하면 프로그램이 느려지곤 합니다.

- **전반적인 모니터링**: [`htop`](https://htop.dev/)은 실행 중 프로세스의 통계를 보여 주는 개선된 `top`입니다. `<F6>`로 정렬하고, `t`로 트리 구조를 보고, `h`로 스레드 표시를 전환합니다. 더 많은 항목을 감시하는 [`btop`](https://github.com/aristocratos/btop)도 있습니다.
- **입출력**: [`iotop`](https://www.man7.org/linux/man-pages/man8/iotop.8.html)은 실시간 I/O 사용량을 보여 줍니다.
- **메모리**: [`free`](https://www.man7.org/linux/man-pages/man1/free.1.html)는 전체 여유·사용 메모리를 표시합니다.
- **열린 파일**: [`lsof`](https://www.man7.org/linux/man-pages/man8/lsof.8.html)는 프로세스가 연 파일의 정보를 보여 줍니다. 특정 파일을 누가 열었는지 찾을 때 유용합니다.
- **네트워크 연결**: [`ss`](https://www.man7.org/linux/man-pages/man8/ss.8.html)는 연결을 감시합니다. `ss -tlnp | grep :8080`으로 포트를 사용하는 프로세스를 찾을 수 있습니다.
- **네트워크 사용량**: [`nethogs`](https://github.com/raboof/nethogs), [`iftop`](https://pdw.ex-parrot.com/iftop/)은 네트워크 사용량을 대화형 CLI로 살펴보는 데 유용합니다.

## 성능 데이터 시각화
{: #visualizing-performance-data}

사람은 숫자 표보다 그래프에서 패턴을 빨리 찾습니다. 성능 데이터를 그리면 원시 숫자로는 잘 보이지 않던 추세, 급등, 이상을 발견할 수 있습니다.

**그리기 쉬운 데이터 만들기**: 출력문이나 로그를 추가할 때 나중에 그래프로 만들기 쉬운 형식을 고려하세요. CSV의 타임스탬프·값(`1705012345,42.5`)은 문장보다 다루기 쉽습니다. JSON 구조 로그도 쉽게 파싱해 그릴 수 있습니다. 즉, [정돈된 방식](https://vita.had.co.nz/papers/tidy-data.pdf)으로 기록하세요.

**gnuplot으로 빠르게 그리기**: [`gnuplot`](http://www.gnuplot.info/)은 명령줄에서 데이터 파일로 바로 그래프를 만듭니다.

```bash
# Plot a simple CSV with timestamp,value
gnuplot -e "set datafile separator ','; plot 'latency.csv' using 1:2 with lines"
```

**matplotlib과 ggplot2로 반복 탐색**: Python의 [`matplotlib`](https://matplotlib.org/)과 R의 [`ggplot2`](https://ggplot2.tidyverse.org/)는 데이터를 나누고 변환하며 가설을 조사하는 데 좋습니다. ggplot2의 패싯 그래프는 데이터를 범주별 작은 그래프로 나눕니다. 예를 들어 엔드포인트나 시간대별로 요청 지연을 나누면 숨은 패턴을 발견할 수 있습니다.

활용 예는 다음과 같습니다.

- 시간에 따른 요청 지연을 그리면 백분위수만으로는 숨겨지는 주기적 지연을 찾을 수 있습니다. 가비지 컬렉션, cron 작업, 트래픽 패턴 등이 원인일 수 있습니다.
- 커지는 자료구조의 삽입 시간을 그리면 복잡도 문제를 찾을 수 있습니다. 벡터의 내부 배열 크기가 두 배가 될 때 나타나는 지연 급등이 한 예입니다.
- 요청 유형, 사용자 집단, 서버별로 나누면 "시스템 전체" 문제로 보이던 것이 특정 범주에 한정된 문제임을 발견할 수 있습니다.

## CPU 프로파일러
{: #cpu-profilers}

보통 *프로파일러*라고 하면 *CPU 프로파일러*를 뜻합니다. 크게 두 종류입니다.

- **추적 프로파일러**: 모든 함수 호출을 기록합니다.
- **샘플링 프로파일러**: 일정 간격(보통 1ms)으로 프로그램의 스택을 기록합니다.

샘플링 방식은 오버헤드가 낮아 운영 환경에서 보통 더 적합합니다.

### perf: 샘플링 프로파일러
{: #perf-the-sampling-profiler}

[`perf`](https://www.man7.org/linux/man-pages/man1/perf.1.html)는 Linux의 표준 프로파일러로, 다시 컴파일하지 않고 프로그램을 분석할 수 있습니다. `perf stat`은 시간이 어디에 쓰이는지 개괄적으로 보여 줍니다.

```bash
$ perf stat ./slow_program

 Performance counter stats for './slow_program':

         3,210.45 msec task-clock                #    0.998 CPUs utilized
               12      context-switches          #    3.738 /sec
                0      cpu-migrations            #    0.000 /sec
              156      page-faults               #   48.587 /sec
   12,345,678,901      cycles                    #    3.845 GHz
    9,876,543,210      instructions              #    0.80  insn per cycle
    1,234,567,890      branches                  #  384.532 M/sec
       12,345,678      branch-misses             #    1.00% of all branches
```

실제 프로그램의 결과에는 많은 정보가 담깁니다. 사람은 많은 숫자를 읽는 데 능숙하지 않으므로 [플레임 그래프](https://www.brendangregg.com/flamegraphs.html)가 이해를 돕습니다.

플레임 그래프는 Y축에 함수 호출 계층을, X축의 폭에 소요 시간에 비례하는 값을 표시합니다. 대화형 그래프에서는 클릭해 특정 부분을 확대할 수 있습니다.

[![플레임 그래프](https://www.brendangregg.com/FlameGraphs/cpu-bash-flamegraph.svg)](https://www.brendangregg.com/FlameGraphs/cpu-bash-flamegraph.svg)

`perf` 데이터로 만드는 방법은 다음과 같습니다.

```bash
# Record profile
perf record -g ./my_program

# Generate flame graph (requires flamegraph scripts)
perf script | stackcollapse-perf.pl | flamegraph.pl > flamegraph.svg
```

> 웹 기반 대화형 뷰어 [Speedscope](https://www.speedscope.app/), 시스템 전반의 분석 도구 [Perfetto](https://perfetto.dev/)도 살펴보세요.

### Valgrind의 Callgrind: 추적 프로파일러
{: #valgrinds-callgrind-the-tracing-profiler}

[`callgrind`](https://valgrind.org/docs/manual/cl-manual.html)는 함수 호출 이력과 명령 수를 기록합니다. 샘플링 방식과 달리 정확한 호출 횟수와 호출자·피호출자 관계를 보여 줍니다.

```bash
# Run with callgrind
valgrind --tool=callgrind ./my_program

# Analyze with callgrind_annotate (text) or kcachegrind (GUI)
callgrind_annotate callgrind.out.<pid>
kcachegrind callgrind.out.<pid>
```

샘플링보다 느리지만 정확한 호출 수를 얻고, 필요하면 `--cache-sim=yes`로 캐시 동작도 시뮬레이션할 수 있습니다.

> 언어 전용 도구도 있습니다. Python에는 [`cProfile`](https://docs.python.org/3/library/profile.html), [`py-spy`](https://github.com/benfred/py-spy), Go에는 [`go tool pprof`](https://pkg.go.dev/cmd/pprof), Rust에는 [`cargo-flamegraph`](https://github.com/flamegraph-rs/flamegraph)가 있습니다. 마지막 도구는 다른 컴파일 프로그램에도 사용할 수 있습니다.

## 메모리 프로파일러
{: #memory-profilers}

메모리 프로파일러는 시간에 따른 메모리 사용을 이해하고 누수를 찾도록 돕습니다.

### Valgrind의 Massif
{: #valgrinds-massif}

[`massif`](https://valgrind.org/docs/manual/ms-manual.html)는 힙 메모리 사용을 분석합니다.

```bash
valgrind --tool=massif ./my_program
ms_print massif.out.<pid>
```

시간에 따른 힙 사용량으로 누수와 과도한 할당을 찾을 수 있습니다.

> Python의 [`memory-profiler`](https://pypi.org/project/memory-profiler/)는 줄별 메모리 사용량을 제공합니다.

## 벤치마킹
{: #benchmarking}

구현이나 도구의 성능을 비교할 때 [`hyperfine`](https://github.com/sharkdp/hyperfine)은 명령줄 프로그램 벤치마킹에 유용합니다.

```bash
$ hyperfine --warmup 3 'fd -e jpg' 'find . -iname "*.jpg"'
Benchmark #1: fd -e jpg
  Time (mean ± σ):      51.4 ms ±   2.9 ms    [User: 121.0 ms, System: 160.5 ms]
  Range (min … max):    44.2 ms …  60.1 ms    56 runs

Benchmark #2: find . -iname "*.jpg"
  Time (mean ± σ):      1.126 s ±  0.101 s    [User: 141.1 ms, System: 956.1 ms]
  Range (min … max):    0.975 s …  1.287 s    10 runs

Summary
  'fd -e jpg' ran
   21.89 ± 2.33 times faster than 'find . -iname "*.jpg"'
```

> 웹 개발에서는 브라우저 개발자 도구에도 좋은 프로파일러가 있습니다. [Firefox Profiler](https://profiler.firefox.com/docs/)와 [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools/rendering-tools) 문서를 참고하세요.

# 연습문제
{: #exercises}

## 디버깅
{: #debugging-1}

1. **정렬 알고리즘 디버깅**: 다음 병합 정렬 의사 코드에는 버그가 있습니다. 원하는 언어로 구현하고 gdb, lldb, pdb 또는 IDE 디버거로 찾아 고치세요.

   ```
   function merge_sort(arr):
       if length(arr) <= 1:
           return arr
       mid = length(arr) / 2
       left = merge_sort(arr[0..mid])
       right = merge_sort(arr[mid..end])
       return merge(left, right)

   function merge(left, right):
       result = []
       i = 0, j = 0
       while i < length(left) AND j < length(right):
           if left[i] <= right[j]:
               append result, left[i]
               i = i + 1
           else:
               append result, right[i]
               j = j + 1
       append remaining elements from left and right
       return result
   ```

   `merge_sort([3, 1, 4, 1, 5, 9, 2, 6])`은 `[1, 1, 2, 3, 4, 5, 6, 9]`를 반환해야 합니다. 중단점을 놓고 merge 함수를 단계별 실행하여 잘못된 원소를 선택하는 지점을 찾으세요.

1. [`rr`](https://rr-project.org/)을 설치하고 역방향 디버깅으로 데이터 손상 버그를 찾으세요. 다음을 `corruption.c`로 저장합니다.

   ```c
   #include <stdio.h>

   typedef struct {
       int id;
       int scores[3];
   } Student;

   Student students[2];

   void init() {
       students[0].id = 1001;
       students[0].scores[0] = 85;
       students[0].scores[1] = 92;
       students[0].scores[2] = 78;

       students[1].id = 1002;
       students[1].scores[0] = 90;
       students[1].scores[1] = 88;
       students[1].scores[2] = 95;
   }

   void curve_scores(int student_idx, int curve) {
       for (int i = 0; i < 4; i++) {
           students[student_idx].scores[i] += curve;
       }
   }

   int main() {
       init();
       printf("=== Initial state ===\n");
       printf("Student 0: id=%d\n", students[0].id);
       printf("Student 1: id=%d\n", students[1].id);

       curve_scores(0, 5);

       printf("\n=== After curving ===\n");
       printf("Student 0: id=%d\n", students[0].id);
       printf("Student 1: id=%d\n", students[1].id);

       if (students[1].id != 1002) {
           printf("\nERROR: Student 1's ID was corrupted! Expected 1002, got %d\n",
                  students[1].id);
           return 1;
       }
       return 0;
   }
   ```

   `gcc -g corruption.c -o corruption`으로 컴파일하고 실행하세요. 학생 0만 다루는 함수에서 학생 1의 ID가 손상됩니다. `rr record ./corruption`, `rr replay`로 원인을 찾으세요. `students[1].id`에 감시점을 놓고 손상 후 `reverse-continue`를 실행하여 값을 덮어쓴 정확한 줄을 찾으세요.

1. AddressSanitizer로 메모리 오류를 디버깅하세요. 다음을 `uaf.c`로 저장합니다.

   ```c
   #include <stdlib.h>
   #include <string.h>
   #include <stdio.h>

   int main() {
       char *greeting = malloc(32);
       strcpy(greeting, "Hello, world!");
       printf("%s\n", greeting);

       free(greeting);

       greeting[0] = 'J';
       printf("%s\n", greeting);

       return 0;
   }
   ```

   먼저 `gcc uaf.c -o uaf && ./uaf`로 실행하세요. 겉보기에는 작동할 수 있습니다. 이번에는 `gcc -fsanitize=address -g uaf.c -o uaf && ./uaf`로 실행하고 보고서를 읽으세요. ASan이 어떤 버그를 찾았나요? 해당 문제를 고치세요.

1. `strace`(Linux)나 `dtruss`(macOS)로 `ls -l` 같은 명령의 시스템 호출을 추적하세요. 어떤 호출을 하나요? 더 복잡한 프로그램도 추적해 어떤 파일을 여는지 보세요.
1. LLM에 난해한 오류 메시지를 설명하고 고치도록 요청하세요. 특히 C++ 템플릿이나 Rust의 컴파일 오류, `strace`나 AddressSanitizer 출력을 사용해 보세요.

## 프로파일링
{: #profiling-1}

1. 원하는 프로그램을 `perf stat`으로 분석하세요. 각 카운터는 무엇을 뜻하나요?
1. `perf record`로 프로파일링하세요. 다음을 `slow.c`로 저장합니다.

   ```c
   #include <math.h>
   #include <stdio.h>

   double slow_computation(int n) {
       double result = 0;
       for (int i = 0; i < n; i++) {
           for (int j = 0; j < 1000; j++) {
               result += sin(i * j) * cos(i + j);
           }
       }
       return result;
   }

   int main() {
       double r = 0;
       for (int i = 0; i < 100; i++) {
           r += slow_computation(1000);
       }
       printf("Result: %f\n", r);
       return 0;
   }
   ```

   `gcc -g -O2 slow.c -o slow -lm`으로 디버그 심볼과 함께 컴파일합니다. `perf record -g ./slow` 다음 `perf report`로 시간이 쓰이는 곳을 찾으세요. flamegraph 스크립트로 그래프도 만들어 보세요.

1. `hyperfine`으로 같은 작업의 두 구현을 비교하세요. `find`와 `fd`, `grep`과 `ripgrep`, 또는 자신의 코드 두 버전을 비교할 수 있습니다.
1. 자원을 많이 쓰는 프로그램을 실행하며 `htop`으로 관찰하세요. `taskset --cpu-list 0,2 stress -c 3`으로 사용 가능한 CPU를 제한해 보세요. 왜 `stress`가 CPU 세 개를 사용하지 못하나요?
1. 사용하려는 포트를 다른 프로세스가 점유한 상황을 조사하세요. `python -m http.server 4444`로 웹 서버를 열고 다른 터미널에서 `ss -tlnp | grep 4444`로 프로세스를 찾은 뒤 `kill <PID>`로 종료하세요.
