---
layout: lecture
title: "코드 패키징과 배포"
description: >
  프로젝트 패키징, 환경, 버전 관리와 라이브러리·애플리케이션·서비스 배포를 배웁니다.
thumbnail: /static/assets/thumbnails/2026/lec6.png
date: 2026-01-20
ready: true
video:
  aspect: 56.25
  id: KBMiB-8P4Ns
---

코드를 의도대로 작동시키기도 어렵지만, 내 컴퓨터와 다른 환경에서 실행되게 하기는 더 어렵습니다.

코드를 배포한다는 것은 자신이 작성한 코드를, 내 컴퓨터와 정확히 같은 설정이 없어도 다른 사람이 실행할 수 있는 형태로 만드는 일입니다. 언어, 시스템 라이브러리, 운영체제 등에 따라 방식이 달라집니다. 라이브러리, 명령줄 도구, 웹 서비스도 각각 요구 사항과 배포 절차가 다릅니다. 공통점은 전달할 결과물, 즉 *아티팩트(artifact)*가 무엇인지와 주변 환경에 대해 무엇을 가정하는지 정의해야 한다는 것입니다.

이번 강의에서는 다음을 다룹니다.

- [의존성과 환경](#dependencies--environments)
- [아티팩트와 패키징](#artifacts--packaging)
- [릴리스와 버전 관리](#releases--versioning)
- [재현성](#reproducibility)
- [VM과 컨테이너](#vms--containers)
- [설정](#configuration)
- [서비스와 오케스트레이션](#services--orchestration)
- [공개 배포](#publishing)

이해를 돕기 위해 Python 생태계의 구체적인 예를 사용합니다. 다른 언어에서는 도구가 달라도 개념은 대체로 같습니다.

# 의존성과 환경
{: #dependencies--environments}

현대 소프트웨어는 여러 추상화 계층을 활용합니다. 프로그램은 자연스럽게 라이브러리나 서비스에 일을 맡기고, 그 결과 동작에 필요한 라이브러리와 *의존 관계*가 생깁니다. Python으로 웹사이트 내용을 가져오는 예를 보겠습니다.

```python
import requests

response = requests.get("https://missing.csail.mit.edu")
```

`requests`는 Python 런타임에 포함되지 않으므로 설치하지 않았다면 오류가 납니다.

```console
$ python fetch.py
Traceback (most recent call last):
  File "fetch.py", line 1, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
```

먼저 `pip install requests`로 설치해야 합니다. `pip`는 Python 패키지를 설치하는 명령줄 도구입니다. 이 명령은 다음 순서로 동작합니다.

1. Python Package Index([PyPI](https://pypi.org/))에서 requests를 찾습니다.
1. 실행 중인 플랫폼에 맞는 아티팩트를 찾습니다.
1. 의존성을 해결합니다. `requests`가 의존하는 패키지와 그 패키지들의 의존성까지 호환되는 버전을 찾아 먼저 설치해야 합니다.
1. 아티팩트를 내려받아 풀고 파일 시스템의 적절한 위치에 복사합니다.

```console
$ pip install requests
Collecting requests
  Downloading requests-2.32.3-py3-none-any.whl (64 kB)
Collecting charset-normalizer<4,>=2
  Downloading charset_normalizer-3.4.0-cp311-cp311-manylinux_x86_64.whl (142 kB)
Collecting idna<4,>=2.5
  Downloading idna-3.10-py3-none-any.whl (70 kB)
Collecting urllib3<3,>=1.21.1
  Downloading urllib3-2.2.3-py3-none-any.whl (126 kB)
Collecting certifi>=2017.4.17
  Downloading certifi-2024.8.30-py3-none-any.whl (167 kB)
Installing collected packages: urllib3, idna, charset-normalizer, certifi, requests
Successfully installed certifi-2024.8.30 charset-normalizer-3.4.0 idna-3.10 requests-2.32.3 urllib3-2.2.3
```

`requests`에는 `certifi`, `charset-normalizer` 등의 의존성이 있으며 먼저 설치됩니다. 설치 후에는 Python이 임포트할 라이브러리를 찾을 수 있습니다.

```console
$ python -c 'import requests; print(requests.__path__)'
['/usr/local/lib/python3.11/dist-packages/requests']

$ pip list | grep requests
requests        2.32.3
```

언어마다 라이브러리 설치·배포 도구와 관례가 다릅니다. Rust는 `cargo`가 빌드, 테스트, 의존성 관리, 배포를 통합합니다. Python은 하나의 도구보다 표준 명세로 통일합니다. 그래서 `pip`와 [`uv`](https://docs.astral.sh/uv/), `setuptools`와 [`hatch`](https://hatch.pypa.io/), [`poetry`](https://python-poetry.org/)처럼 같은 작업을 하는 여러 도구가 경쟁할 수 있습니다. LaTeX의 TeX Live나 MacTeX처럼 수천 개의 패키지를 미리 설치한 배포판도 있습니다.

의존성을 추가하면 충돌도 생깁니다. 같은 의존성의 호환되지 않는 버전을 요구할 때입니다. 예를 들어 `tensorflow==2.3.0`이 `numpy>=1.16.0,<1.19.0`을, `pandas==1.2.0`이 `numpy>=1.16.5`를 요구한다면 `numpy>=1.16.5,<1.19.0`인 버전을 사용할 수 있습니다. 하지만 다른 패키지가 `numpy>=1.19`를 요구하면 모든 조건을 만족하는 버전이 없습니다.

이처럼 공유 의존성의 상충하는 버전을 요구하는 상황을 *의존성 지옥*이라고 합니다. 대응 방법 하나는 프로그램마다 별도의 *환경*에 의존성을 격리하는 것입니다. Python의 가상 환경은 다음처럼 만듭니다.

```console
$ which python
/usr/bin/python
$ pwd
/home/missingsemester
$ python -m venv venv
$ source venv/bin/activate
$ which python
/home/missingsemester/venv/bin/python
$ which pip
/home/missingsemester/venv/bin/pip
$ python -c 'import requests; print(requests.__path__)'
['/home/missingsemester/venv/lib/python3.11/site-packages/requests']

$ pip list
Package Version
------- -------
pip     24.0
```

환경은 자신만의 설치 패키지를 가진 독립적인 언어 런타임으로 생각할 수 있습니다. 가상 환경(venv)은 설치한 의존성을 전역 Python과 격리합니다. 프로젝트마다 필요한 의존성을 담은 가상 환경을 두는 것이 좋습니다.

> 운영체제에 Python 같은 런타임이 포함되어 있더라도 직접 변경하지 않는 편이 좋습니다. 운영체제 자체 기능이 이에 의존할 수 있으므로 별도 환경을 사용하세요.

일부 언어는 설치·빌드 방식을 도구 대신 명세로 정합니다. Python의 [PEP 517](https://peps.python.org/pep-0517/)은 빌드 시스템 인터페이스를, [PEP 621](https://peps.python.org/pep-0621/)은 `pyproject.toml`의 프로젝트 메타데이터 형식을 정의합니다. 덕분에 `pip`를 개선한 `uv` 같은 도구가 나올 수 있었습니다. `pip install uv`로 설치할 수 있습니다.

`uv pip`는 비슷한 인터페이스로 훨씬 빠르게 설치합니다.

```console
$ uv pip install requests
Resolved 5 packages in 12ms
Prepared 5 packages in 0.45ms
Installed 5 packages in 8ms
 + certifi==2024.8.30
 + charset-normalizer==3.4.0
 + idna==3.10
 + requests==2.32.3
 + urllib3==2.2.3
```

> 설치 시간이 크게 줄어들므로 가능한 경우 `pip` 대신 `uv pip`를 적극 권장합니다.

환경은 의존성뿐 아니라 언어 런타임 버전도 분리합니다.

```console
$ uv venv --python 3.12 venv312
Using CPython 3.12.7
Creating virtual environment at: venv312

$ source venv312/bin/activate && python --version
Python 3.12.7

$ uv venv --python 3.11 venv311
Using CPython 3.11.10
Creating virtual environment at: venv311

$ source venv311/bin/activate && python --version
Python 3.11.10
```

여러 Python 버전에서 테스트하거나 특정 버전이 필요한 프로젝트에 유용합니다.

> 일부 언어에서는 수동으로 만들지 않아도 프로젝트마다 의존성 환경이 생깁니다. 원리는 같습니다. 요즘 대부분의 언어에는 한 시스템에서 여러 런타임 버전을 관리하고 프로젝트별로 선택하는 방법도 있습니다.

# 아티팩트와 패키징
{: #artifacts--packaging}

개발자가 읽고 쓰는 소스 코드와, 그 소스로부터 만들어 설치·배포할 수 있게 포장한 결과물인 아티팩트를 구분합니다. 아티팩트는 실행할 코드 파일 하나일 수도 있고, 애플리케이션에 필요한 모든 것을 담은 가상 머신일 수도 있습니다. 현재 디렉터리에 `greet.py`가 있다고 합시다.

```console
$ cat greet.py
def greet(name):
    print(f"Hello, {name}!")

$ python -c "from greet import greet; greet('World')"
Hello, World!

$ cd /tmp
$ python -c "from greet import greet; greet('World')"
ModuleNotFoundError: No module named 'greet'
```

다른 디렉터리로 이동하면 임포트가 실패합니다. Python은 현재 디렉터리, 설치 패키지, `PYTHONPATH` 등 정해진 위치만 검색하기 때문입니다. 패키징은 알려진 위치에 코드를 설치해 이 문제를 해결합니다.

Python 라이브러리를 패키징하면 `pip`나 `uv`가 파일을 설치할 수 있는 아티팩트가 만들어집니다. Python의 아티팩트인 *휠(wheel)*에는 코드, 이름·버전·의존성 메타데이터, 환경의 어디에 파일을 놓을지에 관한 정보가 담깁니다. 만들려면 프로젝트의 세부 정보, 의존성, 버전 등을 적은 프로젝트 파일(매니페스트)이 필요합니다. Python에서는 `pyproject.toml`을 사용합니다.

> `pyproject.toml`이 현대적인 권장 방식입니다. `requirements.txt`로 의존성을 기록하거나 `setup.py`로 패키지를 구성하는 기존 방식도 지원되지만, 가능하면 `pyproject.toml`을 사용하세요.

명령줄 도구도 제공하는 라이브러리의 최소 예입니다.

```toml
[project]
name = "greeting"
version = "0.1.0"
description = "A simple greeting library"
dependencies = ["typer>=0.9"]

[project.scripts]
greet = "greeting:cli"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

`typer`는 반복 코드가 적은 CLI를 만드는 인기 Python 패키지입니다. 대응하는 `greeting.py`는 다음과 같습니다.

```python
import typer


def greet(name: str) -> None:
    print(f"Hello, {name}!")


def cli() -> None:
    typer.run(greet)


if __name__ == "__main__":
    cli()
```

이제 휠을 빌드할 수 있습니다.

```console
$ uv build
Building source distribution...
Building wheel from source distribution...
Successfully built dist/greeting-0.1.0.tar.gz
Successfully built dist/greeting-0.1.0-py3-none-any.whl

$ ls dist/
greeting-0.1.0-py3-none-any.whl
greeting-0.1.0.tar.gz
```

`.whl`은 특정 구조의 ZIP 아카이브인 휠이고, `.tar.gz`는 소스에서 빌드해야 하는 환경을 위한 소스 배포본입니다. 휠 안에 무엇이 담겼는지 살펴볼 수도 있습니다.

```console
$ unzip -l dist/greeting-0.1.0-py3-none-any.whl
Archive:  dist/greeting-0.1.0-py3-none-any.whl
  Length      Date    Time    Name
---------  ---------- -----   ----
      150  2024-01-15 10:30   greeting.py
      312  2024-01-15 10:30   greeting-0.1.0.dist-info/METADATA
       92  2024-01-15 10:30   greeting-0.1.0.dist-info/WHEEL
        9  2024-01-15 10:30   greeting-0.1.0.dist-info/top_level.txt
      435  2024-01-15 10:30   greeting-0.1.0.dist-info/RECORD
---------                     -------
      998                     5 files
```

다른 사람에게 휠을 전달하면 다음처럼 설치할 수 있습니다.

```console
$ uv pip install ./greeting-0.1.0-py3-none-any.whl
$ greet Alice
Hello, Alice!
```

라이브러리와 `greet` CLI 도구가 그 사람의 환경에 설치됩니다.

다만 한계가 있습니다. GPU 가속을 위한 CUDA 등 플랫폼별 라이브러리에 의존한다면 해당 라이브러리가 설치된 시스템에서만 동작합니다. Linux·macOS·Windows와 x86·ARM 등 플랫폼과 아키텍처별로 휠을 따로 만들어야 할 수도 있습니다.

소스 설치와 미리 빌드한 바이너리 설치도 구분해야 합니다. 소스 설치는 원본 코드를 받아 내 컴퓨터에서 컴파일하므로 컴파일러와 빌드 도구가 필요하고, 큰 프로젝트는 오래 걸릴 수 있습니다.

미리 빌드한 바이너리는 다른 사람이 컴파일한 아티팩트를 받아 설치하므로 빠르고 간단하지만 플랫폼과 아키텍처가 맞아야 합니다. 예를 들어 [ripgrep 릴리스](https://github.com/BurntSushi/ripgrep/releases)에는 Linux(x86_64, ARM), macOS(Intel, Apple Silicon), Windows용 바이너리가 있습니다.

# 릴리스와 버전 관리
{: #releases--versioning}

코드는 계속 개발되지만 릴리스는 특정 시점에 이루어집니다. 개발 환경과 운영 환경은 구분되며, 개발 환경에서 작동을 확인한 코드를 운영 환경에 *배포*합니다. 릴리스에는 테스트, 의존성 관리, 버전 지정, 설정, 배포, 공개 등 여러 단계가 포함됩니다.

라이브러리에는 시간이 지나며 수정과 기능이 추가됩니다. 특정 시점의 상태에 버전 식별자를 붙여 변화를 추적합니다. 변경은 작은 수정부터 새 기능, 하위 호환성을 깨는 변경까지 다양합니다. 변경 이력(changelog)은 새 릴리스에서 무엇이 달라졌는지 알리는 문서입니다.

하지만 모든 의존성의 변화, 특히 의존성의 의존성인 전이 의존성까지 일일이 추적하기는 어렵습니다.

> `uv tree`로 패키지와 전이 의존성 전체를 트리로 볼 수 있습니다.

이 문제를 줄이기 위한 버전 관례 중 대표적인 것이 [유의적 버전(Semantic Versioning, SemVer)](https://semver.org/)입니다. `MAJOR.MINOR.PATCH`의 세 정수로 표현하며, 간단히 말하면 다음과 같습니다.

- PATCH(예: 1.2.3 → 1.2.4): 하위 호환되는 버그 수정만 포함합니다.
- MINOR(예: 1.2.3 → 1.3.0): 하위 호환되는 기능을 추가합니다.
- MAJOR(예: 1.2.3 → 2.0.0): 사용자 코드 수정이 필요할 수 있는 호환성 파괴 변경을 뜻합니다.

> 이는 간략한 설명입니다. 0.1.3에서 0.2.0으로 올릴 때 호환성이 깨질 수 있는 이유나 1.0.0-rc.1의 의미는 전체 명세를 읽어보세요.

Python 패키징에서는 다양한 지정자로 호환 버전 범위를 표현할 수 있습니다. `pyproject.toml`의 예입니다.

```toml
[project]
dependencies = [
    "requests==2.32.3",  # Exact version - only this specific version
    "click>=8.0",        # Minimum version - 8.0 or newer
    "numpy>=1.24,<2.0",  # Range - at least 1.24 but less than 2.0
    "pandas~=2.1.0",     # Compatible release - >=2.1.0 and <2.2.0
]
```

npm, cargo 등에도 버전 지정자가 있지만 정확한 의미는 다릅니다. Python의 `~=`는 "호환 릴리스" 연산자입니다. `~=2.1.0`은 `>=2.1.0,<2.2.0`을 뜻합니다. npm·cargo의 캐럿(`^`)도 SemVer의 호환성을 표현하는 비슷한 목적의 연산자지만, 허용 범위는 같지 않습니다.

모든 소프트웨어가 SemVer를 쓰지는 않습니다. 달력 버전(CalVer)은 릴리스 날짜를 사용합니다. Ubuntu의 `24.04`(2024년 4월), `24.10`(2024년 10월)이 예입니다. 릴리스가 얼마나 오래됐는지는 알기 쉽지만 호환성은 알려 주지 않습니다. SemVer도 완벽하지 않아 마이너·패치 릴리스에 의도치 않은 호환성 파괴가 들어갈 수 있습니다.

# 재현성
{: #reproducibility}

코드는 런타임, 외부 라이브러리, 운영체제, 하드웨어 등 여러 계층 위에서 실행됩니다. 어느 계층의 차이든 동작을 바꾸거나 실행을 막을 수 있습니다. 하드웨어 차이도 배포에 영향을 줍니다.

버전 고정(pinning)은 `requests>=2.0` 같은 범위 대신 `requests==2.32.3`처럼 정확한 버전을 지정하는 것입니다.

패키지 관리자는 직접·전이 의존성의 모든 제약을 만족하는 버전 조합을 찾습니다. 재현성을 위해 그 목록을 저장한 파일을 *잠금 파일(lock file)*이라고 합니다.

```console
$ uv lock
Resolved 12 packages in 45ms

$ cat uv.lock | head -20
version = 1
requires-python = ">=3.11"

[[package]]
name = "certifi"
version = "2024.8.30"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/...", hash = "sha256:..." }
wheels = [
    { url = "https://files.pythonhosted.org/...", hash = "sha256:..." },
]
...
```

여기서 라이브러리와 애플리케이션·서비스의 차이가 중요합니다. 라이브러리는 다른 코드가 임포트하므로 너무 엄격한 버전 제약은 사용자의 다른 의존성과 충돌할 수 있습니다. 반면 애플리케이션과 서비스는 최종 소비자로, 라이브러리처럼 임포트되는 대신 UI나 API로 기능을 제공합니다. 라이브러리는 폭넓은 호환성을 위해 버전 범위를 지정하고, 애플리케이션은 모두가 같은 의존성을 쓰도록 정확한 버전을 고정하는 것이 좋습니다.

최대한의 재현성이 필요하면 [Nix](https://nixos.org/), [Bazel](https://bazel.build/) 같은 도구로 *밀폐형(hermetic) 빌드*를 구성할 수 있습니다. 컴파일러, 시스템 라이브러리, 빌드 환경 등 모든 입력을 고정하고 내용 기반 주소로 관리하여 언제 어디서 실행해도 비트 단위로 동일한 결과를 얻는 것을 목표로 합니다.

> NixOS로 컴퓨터 설치 전체를 관리하면 버전 관리되는 설정 파일로 전체 구성을 관리하고 같은 환경을 쉽게 새로 만들 수 있습니다.

새 버전은 의도적·비의도적 문제를 일으킬 수 있고, 오래된 버전에는 시간이 지나며 보안 취약점이 발견됩니다. 이 긴장은 끝이 없습니다. [코드 품질과 CI 강의](/2026/code-quality/)에서 볼 CI로 새 버전을 테스트하고, [Dependabot](https://github.com/dependabot) 등으로 의존성의 새 릴리스를 감지할 수 있습니다.

CI가 있어도 개발·운영 환경 차이 때문에 업그레이드 문제가 생깁니다. 이때는 업그레이드를 되돌리고 정상 동작이 확인된 버전을 다시 배포하는 *롤백* 계획이 필요합니다.

# VM과 컨테이너
{: #vms--containers}

의존성이 복잡해지면 언어의 패키지 관리자가 다룰 수 있는 범위를 벗어납니다. 특정 시스템 라이브러리나 하드웨어 드라이버가 흔한 이유입니다. 과학 계산이나 AI 프로그램은 GPU를 쓰기 위해 전용 라이브러리와 드라이버가 필요합니다. GPU 드라이버, 특정 컴파일러, OpenSSL 같은 공유 라이브러리는 여전히 시스템 전체 설치가 필요한 경우가 많습니다.

전통적으로는 가상 머신(VM)으로 해결했습니다. 컴퓨터 전체를 추상화하여 자체 운영체제를 가진 완전히 격리된 환경을 제공합니다. 컨테이너는 애플리케이션, 의존성, 라이브러리, 파일 시스템을 묶되 컴퓨터 전체를 가상화하지 않고 호스트 커널을 공유합니다. 그래서 VM보다 가볍고 시작과 실행이 효율적입니다.

대표적인 플랫폼은 [Docker](https://www.docker.com/)입니다. 컨테이너를 빌드·배포·실행하는 표준화된 방식을 도입했으며, 내부 런타임으로 Kubernetes 등도 쓰는 업계 표준인 containerd를 사용합니다.

컨테이너 안에서 Python을 실행하려면 `docker run`을 사용합니다. `-it`는 터미널을 연결한 대화형 실행이며, 인터프리터를 종료하면 컨테이너도 멈춥니다.

```console
$ docker run -it python:3.12 python
Python 3.12.7 (main, Nov  5 2024, 02:53:25) [GCC 12.2.0] on linux
>>> print("Hello from inside a container!")
Hello from inside a container!
```

프로그램이 사실상 파일 시스템 전체에 의존할 수도 있습니다. 애플리케이션의 파일 시스템 전체를 아티팩트로 묶은 컨테이너 이미지로 대응할 수 있습니다. 이미지는 프로그램으로 정의합니다. Dockerfile에 의존성, 시스템 라이브러리, 설정을 지정합니다.

```dockerfile
FROM python:3.12
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y libpq-dev
RUN pip install numpy
RUN pip install pandas
COPY . /app
WORKDIR /app
RUN pip install .
```

Docker **이미지**는 템플릿 같은 패키징 결과물이고, **컨테이너**는 그 이미지의 실행 인스턴스입니다. 이미지 하나로 여러 컨테이너를 실행할 수 있습니다. 이미지는 계층으로 구성되며 `FROM`, `RUN`, `COPY` 등 Dockerfile의 각 지시가 빌드 단계를 만듭니다. Docker는 이를 캐시하므로 한 줄을 바꾸면 해당 단계와 그 이후만 다시 빌드합니다.

앞의 예제에는 문제가 여럿 있습니다. slim 대신 전체 Python 이미지를 쓰고, `RUN`을 나눠 불필요한 계층을 만들며, 버전을 고정하지 않았고, 패키지 관리자 캐시를 지우지 않아 불필요한 파일이 포함됩니다. root 실행이나 계층에 비밀 정보를 실수로 넣는 것도 흔한 문제입니다.

다음은 개선한 예입니다.

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project
COPY . .
RUN uv sync --locked --no-dev
```

여기서는 `uv`를 소스에서 설치하지 않고 `ghcr.io/astral-sh/uv:latest` 이미지의 미리 빌드한 바이너리를 복사합니다. 이런 *빌더(builder)* 패턴을 쓰면 컴파일 도구 전체를 담지 않고 실행에 필요한 최종 바이너리만 가져올 수 있습니다. 이 예에서는 `uv`가 해당합니다.

Docker에도 한계가 있습니다. 첫째, 이미지는 흔히 플랫폼별입니다. `linux/amd64` 이미지는 Apple Silicon의 `linux/arm64` 환경에서 느린 에뮬레이션 없이 네이티브로 실행되지 않습니다. 둘째, Linux 컨테이너는 Linux 커널이 필요하므로 macOS와 Windows에서는 내부의 경량 Linux VM 때문에 추가 비용이 생깁니다. 셋째, 호스트 커널을 공유하므로 격리가 VM보다 약하며 다중 사용자 환경에서 보안을 고려해야 합니다.

> 최근에는 [Nix flakes](https://serokell.io/blog/practical-nix-flakes)로 시스템 수준 라이브러리와 애플리케이션까지 프로젝트별로 관리하는 경우도 늘고 있습니다.

# 설정
{: #configuration}

소프트웨어에는 설정이 필요합니다. [명령줄 환경 강의](/2026/command-line-environment/)에서 플래그, 환경 변수, 닷파일을 봤습니다. 복잡한 애플리케이션도 마찬가지이며 대규모 설정 관리에도 정해진 패턴이 있습니다. 설정은 코드에 박아 넣기보다 실행 시 제공해야 합니다. 흔한 방식은 환경 변수와 설정 파일입니다.

환경 변수로 설정하는 예입니다.

```python
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///local.db")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
API_KEY = os.environ["API_KEY"]  # Required - will raise if not set
```

설정 파일을 읽는 방식도 있습니다. 예를 들어 Python 프로그램이 YAML을 읽어 다음 `config.yaml`을 사용할 수 있습니다.

```yaml
database:
  url: "postgresql://localhost/myapp"
  pool_size: 5
server:
  host: "0.0.0.0"
  port: 8080
  debug: false
```

좋은 기준은 같은 코드베이스를 코드 변경 없이 설정만 바꿔 개발·스테이징·운영 환경에 배포할 수 있어야 한다는 것입니다.

설정에는 API 키 같은 민감한 정보도 있습니다. 실수로 노출하지 않도록 주의하고 버전 관리에 포함하지 마세요.

# 서비스와 오케스트레이션
{: #services--orchestration}

현대 애플리케이션은 홀로 동작하는 경우가 드뭅니다. 웹 앱에는 영구 저장용 데이터베이스, 성능 개선용 캐시, 백그라운드 작업용 메시지 큐 등이 필요할 수 있습니다. 이를 하나의 거대한 애플리케이션으로 묶기보다, 독립적으로 개발·배포·확장할 수 있는 서비스로 나누는 구조가 흔합니다.

예를 들어 캐시가 필요하다면 직접 만들기보다 [Redis](https://redis.io/), [Memcached](https://memcached.org/) 같은 검증된 도구를 사용할 수 있습니다. Redis를 앱 컨테이너에 함께 넣을 수도 있지만 양쪽의 모든 의존성을 맞추기 어렵거나 불가능할 수 있습니다. 각각 별도 컨테이너로 배포하면 이 문제를 피할 수 있습니다. 각 구성 요소가 독립된 서비스로 실행되고 보통 HTTP API 등 네트워크로 통신하는 구조를 마이크로서비스 아키텍처라고 합니다.

[Docker Compose](https://docs.docker.com/compose/)는 여러 컨테이너로 된 앱을 정의하고 실행합니다. 컨테이너를 개별 관리하는 대신 YAML 하나에 서비스를 선언하고 함께 조정합니다.

```yaml
# docker-compose.yml
services:
  web:
    build: .
    ports:
      - "8080:8080"
    environment:
      - REDIS_URL=redis://cache:6379
    depends_on:
      - cache

  cache:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

`docker compose up`으로 두 서비스가 함께 시작됩니다. Docker 내부 DNS가 서비스 이름을 해석하므로 웹 앱은 `cache`라는 호스트로 Redis에 연결합니다. Compose는 서비스 실행, 네트워크 연결, 데이터 영속성을 위한 공유 볼륨 관리를 담당합니다.

운영 환경에서는 부팅 시 자동 시작과 장애 시 재시작이 필요합니다. Compose 배포를 systemd로 관리하는 것이 흔한 방법입니다.

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down

[Install]
WantedBy=multi-user.target
```

이 유닛 파일은 부팅 후 Docker가 준비되면 앱을 시작하고, `systemctl start myapp`, `systemctl stop myapp`, `systemctl status myapp` 같은 표준 제어를 제공합니다.

여러 머신으로 확장하고, 서비스 장애에 대응하며, 고가용성을 보장해야 한다면 Kubernetes(k8s) 같은 오케스트레이션 플랫폼을 사용합니다. 머신 클러스터에 걸친 수천 개 컨테이너를 관리할 수 있지만 학습·운영 비용이 커서 작은 프로젝트에는 과한 경우가 많습니다.

이 구성이 가능한 이유 중 하나는 서비스가 HTTP REST API 같은 표준 방식으로 통신하기 때문입니다. 예를 들어 OpenAI나 Anthropic 같은 LLM 서비스에 요청하는 프로그램은 내부적으로 HTTP 요청을 보내고 응답을 파싱합니다.

```console
$ curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "content-type: application/json" \
    -H "anthropic-version: 2023-06-01" \
    -d '{"model": "claude-sonnet-4-20250514", "max_tokens": 256,
         "messages": [{"role": "user", "content": "Explain containers vs VMs in one sentence."}]}'
```

# 공개 배포
{: #publishing}

코드의 동작을 확인했다면 다른 사람이 내려받아 설치하도록 배포할 수 있습니다. 방식은 언어와 환경에 따라 다양합니다.

가장 단순한 방식은 아티팩트를 올리고 사용자가 내려받아 설치하게 하는 것입니다. 지금도 흔하며, [Ubuntu 패키지 아카이브](http://archive.ubuntu.com/ubuntu/pool/main/)도 본질적으로 `.deb` 파일을 나열하는 HTTP 디렉터리입니다.

GitHub는 소스 코드와 아티팩트를 공개하는 대표적인 플랫폼입니다. 소스 공개와 함께 GitHub Releases로 태그가 붙은 버전에 빌드된 바이너리 등을 첨부할 수 있습니다.

일부 패키지 관리자는 GitHub 소스나 휠에서 직접 설치하는 것도 지원합니다.

```console
# Install from source (will clone and build)
$ pip install git+https://github.com/psf/requests.git

# Install from a specific tag/branch
$ pip install git+https://github.com/psf/requests.git@v2.32.3

# Install a wheel directly from a GitHub release
$ pip install https://github.com/user/repo/releases/download/v1.0/package-1.0-py3-none-any.whl
```

Go처럼 분산 배포 모델을 쓰는 언어도 있습니다. 중앙 저장소에만 의존하지 않고 소스 저장소를 기준으로 모듈을 배포합니다. `github.com/gorilla/mux` 같은 모듈 경로가 위치를 나타내고 `go get`으로 가져옵니다. 반면 `pip`, `cargo`, `brew` 등은 배포·설치를 돕는 중앙 인덱스를 사용합니다. 다음을 실행하면 `requests` 휠을 어디서 가져오는지 볼 수 있습니다.

```console
$ uv pip install requests --verbose --no-cache 2>&1 | grep -F '.whl'
DEBUG Selecting: requests==2.32.5 [compatible] (requests-2.32.5-py3-none-any.whl)
DEBUG No cache entry for: https://files.pythonhosted.org/packages/1e/db/4254e3eabe8020b458f1a747140d32277ec7a271daf1d235b70dc0b4e6e3/requests-2.32.5-py3-none-any.whl.metadata
DEBUG No cache entry for: https://files.pythonhosted.org/packages/1e/db/4254e3eabe8020b458f1a747140d32277ec7a271daf1d235b70dc0b4e6e3/requests-2.32.5-py3-none-any.whl
```

파일명의 `py3-none-any`는 Python 3용이며 특정 ABI나 플랫폼에 묶이지 않은 휠이라는 뜻입니다. 컴파일된 코드가 있는 패키지는 플랫폼별 휠을 사용합니다.

```console
$ uv pip install numpy --verbose --no-cache 2>&1 | grep -F '.whl'
DEBUG Selecting: numpy==2.2.1 [compatible] (numpy-2.2.1-cp312-cp312-macosx_14_0_arm64.whl)
```

`cp312-cp312-macosx_14_0_arm64`는 macOS 14 이상, ARM64(Apple Silicon)의 CPython 3.12용입니다. 다른 플랫폼에서는 해당 플랫폼용 휠을 받거나 소스에서 빌드합니다.

반대로 우리가 만든 패키지를 다른 사람이 찾게 하려면 레지스트리에 공개해야 합니다. Python의 대표 레지스트리는 [PyPI](https://pypi.org)입니다. 방법은 여러 가지이며, `uv publish`는 현대적인 업로드 인터페이스를 제공합니다.

```console
$ uv publish --publish-url https://test.pypi.org/legacy/
Publishing greeting-0.1.0.tar.gz
Publishing greeting-0.1.0-py3-none-any.whl
```

여기서는 실제 PyPI에 연습용 패키지를 올리지 않도록 별도의 [TestPyPI](https://test.pypi.org)를 사용합니다. 업로드 후 다음처럼 설치할 수 있습니다.

```console
$ uv pip install --index-url https://test.pypi.org/simple/ greeting
```

공개할 때는 신뢰도 중요합니다. 사용자는 내려받은 패키지가 정말 작성자의 것이고 변조되지 않았음을 어떻게 확인할까요? 레지스트리는 체크섬으로 무결성을 확인하며, 일부 생태계는 작성자를 암호학적으로 증명하는 패키지 서명도 지원합니다.

Rust의 [crates.io](https://crates.io), JavaScript의 [npm](https://www.npmjs.com), Ruby의 [RubyGems](https://rubygems.org), 컨테이너 이미지의 [Docker Hub](https://hub.docker.com)처럼 생태계마다 레지스트리가 있습니다. 조직 내부 패키지는 비공개 PyPI·Docker 레지스트리를 직접 운영하거나 클라우드 관리형 서비스를 쓰기도 합니다.

웹 서비스를 인터넷에 배포하려면 도메인 등록, 도메인을 서버로 연결하는 DNS, HTTPS와 트래픽 라우팅을 담당하는 nginx 같은 리버스 프록시가 추가로 필요합니다. 문서나 정적 사이트처럼 단순한 경우에는 [GitHub Pages](https://pages.github.com/)가 저장소에서 바로 무료 호스팅을 제공합니다.

<!--
## 문서화

지금까지 배포 결과물인 아티팩트를 강조했지만, 기능·설치법·사용 예제 문서도 필요합니다.
[Sphinx](https://www.sphinx-doc.org/)(Python), [MkDocs](https://www.mkdocs.org/)는 독스트링과 Markdown에서 탐색 가능한 문서를 생성하며 [Read the Docs](https://readthedocs.org/) 등에 호스팅할 수 있습니다.
HTTP API의 [OpenAPI 명세](https://www.openapis.org/)(이전 이름 Swagger)는 엔드포인트 설명의 표준 형식이며, 도구로 대화형 문서와 클라이언트 라이브러리를 자동 생성할 수 있습니다.
-->

# 연습문제
{: #exercises}

1. `printenv`를 파일에 저장하고 venv를 생성·활성화한 뒤 다시 저장하여 `diff before.txt after.txt`로 비교하세요. 무엇이 달라졌나요? 셸은 왜 venv를 먼저 찾나요? 힌트: 활성화 전후 `$PATH`. `which deactivate`를 실행하고 `deactivate` bash 함수의 동작을 생각해 보세요.
1. `pyproject.toml`이 있는 Python 패키지를 만들고 가상 환경에 설치하세요. 잠금 파일을 만들고 내용을 살펴보세요.
1. Docker를 설치하고 Docker Compose로 Missing Semester 사이트를 로컬 빌드하세요.
1. 간단한 Python 앱의 Dockerfile을 쓰고, Redis 캐시와 함께 실행하는 `docker-compose.yml`도 작성하세요.
1. Python 패키지를 TestPyPI에 공개하세요. 공유할 가치가 없다면 실제 PyPI에는 올리지 마세요. 해당 패키지가 포함된 Docker 이미지를 만들고 `ghcr.io`에 푸시하세요.
1. [GitHub Pages](https://docs.github.com/en/pages/quickstart)로 사이트를 만드세요. 추가 과제: 사용자 지정 도메인을 설정하세요.
