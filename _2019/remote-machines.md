---
layout: lecture
title: "원격 컴퓨터"
lang: ko
presenter: Jose
date: 2019-01-29
order: 4
video:
  aspect: 62.5
  id: X5c2Y8BCowM
---

프로그래머가 일상적인 작업에 원격 서버를 사용하는 일이 많아졌습니다. 백엔드 소프트웨어를 배포하거나 더 높은 연산 성능이 필요하다면 보안 셸인 SSH(Secure Shell)를 사용하게 됩니다. 다른 도구들과 마찬가지로 SSH도 설정할 수 있는 항목이 많으므로 알아둘 가치가 있습니다.

## 명령 실행하기
{: id="executing-commands"}

`ssh`가 명령을 직접 실행할 수 있다는 사실은 종종 간과됩니다.

- `ssh foobar@server ls`: 원격 서버에 있는 `foobar`의 홈 디렉터리에서 `ls`를 실행합니다.
- 파이프와 함께 쓸 수도 있습니다. `ssh foobar@server ls | grep PATTERN`은 원격 `ls`의 출력을 로컬에서 검색합니다. 반대로 `ls | ssh foobar@server grep PATTERN`은 로컬 `ls`의 출력을 원격 서버에서 검색합니다.

## SSH 키
{: id="ssh-keys"}

키 기반 인증은 공개 키 암호 기술을 사용해, 클라이언트가 비밀 키를 공개하지 않고도 해당 키를 가지고 있음을 서버에 증명합니다. 덕분에 매번 계정 비밀번호를 입력하지 않아도 됩니다. 하지만 `~/.ssh/id_rsa` 같은 비밀 키는 사실상 비밀번호와 같은 역할을 하므로 그에 맞게 관리해야 합니다.

- **키 생성**: `ssh-keygen -t rsa -b 4096`으로 키 쌍을 만들 수 있습니다. 암호문구를 지정하지 않으면 비밀 키를 얻은 누구나 그 키를 허용한 서버에 접속할 수 있습니다. 암호문구를 설정하고 `ssh-agent`로 세션에서 키를 관리하는 것을 권합니다.

GitHub에 SSH 키로 푸시하도록 설정했다면, [연결 안내](https://help.github.com/articles/connecting-to-github-with-ssh/)에 따라 이미 키 쌍을 만들었을 가능성이 큽니다. 암호문구가 있는지, 입력한 암호문구가 맞는지 확인하려면 `ssh-keygen -y -f /path/to/key`를 실행하세요.

- **키 기반 인증 설정**: 서버는 `.ssh/authorized_keys`에서 접속을 허용할 공개 키를 확인합니다. 공개 키는 다음처럼 복사할 수 있습니다.

```bash
cat .ssh/id_dsa.pub | ssh foobar@remote 'cat >> ~/.ssh/authorized_keys'
```

`ssh-copy-id`가 설치돼 있다면 더 간단하게 할 수 있습니다.

```bash
ssh-copy-id -i .ssh/id_dsa.pub foobar@remote
```

## SSH로 파일 복사하기
{: id="copying-files-over-ssh"}

SSH를 통해 파일을 복사하는 방법에는 여러 가지가 있습니다.

- **`ssh`와 `tee`**: 가장 간단하게는 SSH의 명령 실행과 표준 입력을 이용합니다. `cat localfile | ssh remote_server tee serverfile`
- **`scp`**: 파일이나 디렉터리를 많이 복사할 때 편리합니다. 디렉터리를 재귀적으로 복사할 수 있습니다. 기본 문법은 `scp path/to/local_file remote_host:path/to/remote_file`입니다.
- **`rsync`**: 로컬과 원격에 같은 파일이 있으면 다시 복사하지 않습니다. 심볼릭 링크와 권한도 더 세밀하게 제어할 수 있습니다. `--partial`로 전송이 중단됐을 때 일부 데이터를 남겨 다음 전송에 활용하는 등의 기능도 제공합니다. 문법은 `scp`와 비슷합니다.

## 프로세스를 백그라운드에서 유지하기
{: id="backgrounding-processes"}

SSH 연결이 끊어지면 셸과 그 자식 프로세스도 종료될 수 있습니다. 이를 피하는 몇 가지 방법이 있습니다.

- **`nohup`**: 터미널 연결이 끊어져도 프로세스가 계속 실행되도록 합니다. `&`와 `disown`으로 해결할 수도 있지만, `nohup`은 이런 목적에 바로 사용할 수 있습니다. [차이에 관한 설명](https://unix.stackexchange.com/questions/3886/difference-between-nohup-disown-and)을 참고하세요.
- **`tmux`, `screen`**: `nohup`만으로는 대화형 셸 세션을 다루기 불편합니다. 이때는 터미널 멀티플렉서를 사용하면 셸에서 연결을 끊었다가 다시 연결하기 쉽습니다.

이미 `disown`으로 분리한 프로그램을 현재 터미널에 다시 연결하고 싶다면 [reptyr](https://github.com/nelhage/reptyr)를 살펴보세요. `reptyr PID`는 해당 프로세스를 현재 터미널에 연결합니다.

## 포트 포워딩
{: id="port-forwarding"}

네트워크 포트에서 요청을 기다리는 소프트웨어를 사용할 일이 많습니다. 로컬 컴퓨터에서 실행한다면 `localhost:PORT`나 `127.0.0.1:PORT`로 접속하면 됩니다. 하지만 원격 서버의 포트가 네트워크나 인터넷에 직접 열려 있지 않다면 어떻게 할까요? 포트 포워딩을 사용할 수 있습니다. 로컬 포트 포워딩과 원격 포트 포워딩 두 가지가 있습니다. 아래 그림을 참고하세요. 그림의 출처는 [이 Stack Overflow 게시물](https://unix.stackexchange.com/questions/115897/whats-ssh-port-forwarding-and-whats-the-difference-between-ssh-local-and-remot)입니다.

**로컬 포트 포워딩**
![로컬 포트 포워딩](https://i.stack.imgur.com/a28N8.png)

**원격 포트 포워딩**
![원격 포트 포워딩](https://i.stack.imgur.com/4iK3b.png)

가장 흔한 경우는 로컬 포트 포워딩입니다. 원격 컴퓨터에서 서비스가 사용하는 포트에 로컬 포트를 연결합니다. 예를 들어 원격 서버에서 `jupyter notebook`을 실행해 `8888` 포트를 사용한다면, `ssh -L 9999:localhost:8888 foobar@remote_server`로 로컬의 `9999` 포트에 연결할 수 있습니다. 그런 다음 로컬 브라우저에서 `localhost:9999`를 엽니다.

## 그래픽 포워딩
{: id="graphics-forwarding"}

서버에서 GUI 프로그램을 실행하고 싶다면 포트 포워딩만으로는 부족할 수 있습니다. RealVNC나 TeamViewer처럼 데스크톱 전체를 전달하는 원격 데스크톱 프로그램도 있지만, GUI 도구 하나를 사용할 때는 SSH의 그래픽 포워딩이 좋은 대안입니다.

SSH에 `-X` 플래그를 주면 X11 포워딩을 사용합니다. 신뢰된 X11 포워딩에는 `-Y`를 사용할 수 있습니다.

서버의 `sshd_config`에는 다음과 같은 설정이 필요합니다.

```bash
X11Forwarding yes
X11DisplayOffset 10
```

## 네트워크가 바뀌어도 연결 유지하기
{: id="roaming"}

컴퓨터를 끄거나 잠자기 모드로 전환하거나 네트워크를 바꿀 때 원격 연결이 끊어지는 일은 흔합니다. 지연이 큰 연결에서 SSH를 사용하는 것도 답답할 수 있습니다. 모바일 셸인 [Mosh](https://mosh.org/)는 네트워크 변경과 일시적인 연결 끊김을 처리하고, 로컬에서 입력을 예측해 보여 줍니다.

Mosh는 주요 배포판과 패키지 관리자에서 설치할 수 있습니다. 서버에는 동작하는 SSH 서버가 필요합니다. Mosh를 설치하는 데 관리자 권한은 필요하지 않지만, 서버의 60000번부터 60010번까지 포트가 열려 있어야 합니다. 이 포트들은 특권 포트 범위에 속하지 않으므로 대개 열려 있습니다.

Mosh의 단점은 네트워크를 옮겨 다니면서 포트 포워딩이나 그래픽 포워딩을 사용할 수 없다는 것입니다. 이런 기능을 자주 사용한다면 Mosh가 큰 도움이 되지 않을 것입니다.

## SSH 설정
{: id="ssh-configuration"}

### 클라이언트
{: id="client"}

지금까지 여러 옵션을 살펴봤습니다. `alias my_server="ssh -X -i ~/.ssh/id_rsa -L 9999:localhost:8888 foobar@remote_server"` 같은 셸 별칭을 만들 수도 있지만, `~/.ssh/config`를 사용하는 편이 더 좋습니다.

```bash
Host vm
    User foobar
    HostName 172.16.174.141
    Port 22
    IdentityFile ~/.ssh/id_rsa
    RemoteForward 9999 localhost:8888

# Configs can also take wildcards
Host *.mit.edu
    User foobaz
```

설정 파일을 쓰면 `scp`, `rsync`, `mosh` 같은 프로그램도 SSH 설정을 활용할 수 있다는 장점이 있습니다.

`~/.ssh/config`도 dotfile이므로 다른 설정 파일과 함께 관리할 수 있습니다. 다만 공개할 때는 서버 주소, 사용자 이름, 열린 포트 등의 정보를 외부에 알리게 된다는 점을 고려하세요. 이런 정보가 일부 공격에 활용될 수 있습니다.

**주의: RSA 키(`~/.ssh/id_rsa*`)는 공개 저장소에 절대 넣지 마세요!**

### 서버
{: id="server-side"}

서버 설정은 보통 `/etc/ssh/sshd_config`에 있습니다. 비밀번호 인증 비활성화, SSH 포트 변경, X11 포워딩 활성화 등을 설정할 수 있습니다. 사용자별로 다른 설정을 적용할 수도 있습니다.

## 원격 파일 시스템
{: id="remote-filesystem"}

원격 디렉터리를 로컬에 마운트하면 편리할 때가 있습니다. [sshfs](https://github.com/libfuse/sshfs)로 원격 서버의 디렉터리를 마운트하면 로컬 편집기로 파일을 수정할 수 있습니다.

## 연습 문제
{: id="exercises"}

1. SSH 접속을 받는 컴퓨터에는 SSH 서버가 실행 중이어야 합니다. 나머지 실습을 위해 가상 머신에 OpenSSH 같은 SSH 서버를 설치하세요. `ip addr` 출력에서 `inet` 항목으로 IP 주소를 확인하세요. 루프백 인터페이스인 `127.0.0.1`은 제외합니다.
1. `~/.ssh/`에 SSH 키 쌍이 있는지 확인하세요. 없다면 `ssh-keygen -t rsa -b 4096`으로 만드세요. 암호문구와 `ssh-agent`를 사용하길 권합니다. [에이전트 설명](https://www.ssh.com/ssh/agent)을 참고하세요.
1. `ssh-copy-id`로 공개 키를 가상 머신에 복사하고, 계정 비밀번호 없이 접속되는지 확인하세요. 그다음 서버의 `sshd_config`에서 `PasswordAuthentication` 값을 바꿔 비밀번호 인증을 끄고, `PermitRootLogin`을 바꿔 root 로그인을 끄세요.
1. 서버의 `sshd_config`에서 SSH 포트를 바꾼 뒤 여전히 접속되는지 확인하세요. 공개 서버를 운영할 때 기본값과 다른 포트를 사용하고 키 인증만 허용하면 악의적인 공격을 상당수 줄일 수 있습니다.
1. 서버나 가상 머신에 Mosh를 설치해 접속한 다음 네트워크 어댑터를 분리해 보세요. 다시 연결했을 때 Mosh가 복구하나요?
1. 로컬 포트 포워딩으로 특정 호스트에 대한 요청을 서버를 거쳐 보낼 수도 있습니다. 네트워크에서 `reddit.com` 같은 사이트를 차단한다면 다음과 같이 서버를 통해 터널링할 수 있습니다.
    - `ssh remote_server -L 80:reddit.com:80`을 실행합니다.
    - `/etc/hosts`에서 `reddit.com`과 `www.reddit.com`을 `127.0.0.1`에 대응시킵니다.
    - 서버를 거쳐 사이트에 접속하는지 확인합니다.
    - 확실하지 않다면 호스트의 공인 IP에 따라 결과가 달라지는 [ipinfo.io](https://ipinfo.io/) 같은 사이트로 확인하세요.
1. 플래그 몇 개를 더하면 포트 포워딩을 백그라운드에서 유지할 수 있습니다. SSH의 `-N`과 `-f`를 조사하고 `ssh -N -f -L 9999:localhost:8888 foobar@remote_server`가 무엇을 하는지 설명해 보세요.

## 참고 자료
{: id="references"}

- [SSH 활용법](https://matt.might.net/articles/ssh-hacks/)
- [Secure Secure Shell](https://stribika.github.io/2015/01/04/secure-secure-shell.html)

{% comment %}
Lecture notes will be available by the start of lecture.
{% endcomment %}
