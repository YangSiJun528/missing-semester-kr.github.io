# The Missing Semester of Your CS Education

[![Build Status](https://github.com/missing-semester/missing-semester/actions/workflows/build.yml/badge.svg)](https://github.com/missing-semester/missing-semester/actions/workflows/build.yml) [![Links Status](https://github.com/missing-semester/missing-semester/actions/workflows/links.yml/badge.svg)](https://github.com/missing-semester/missing-semester/actions/workflows/links.yml)

[The Missing Semester of Your CS Education](https://missing.csail.mit.edu/)의 웹사이트입니다!

기여를 환영합니다! 수정하거나 추가할 내용이 있다면 이슈나 풀 리퀘스트를 보내 주세요.

## 개발

사이트를 로컬에서 빌드하고 보려면 다음 명령을 실행하세요.

```bash
bundle exec jekyll serve -w
```

호스트 컴퓨터에 Ruby와 의존성을 설치하고 싶지 않다면 Docker 컨테이너에서 개발할 수도 있습니다.

```bash
docker compose up --build
```

브라우저에서 <http://localhost:4000>을 엽니다. 파일을 수정하면 Jekyll이 사이트를 다시 빌드합니다.

## 라이선스

웹사이트 소스 코드, 강의 노트, 연습문제, 강의 영상을 포함한 이 수업의 모든 콘텐츠에는 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 라이선스가 적용됩니다. 기여 및 번역에 관한 자세한 내용은 [여기](https://missing.csail.mit.edu/license)를 참고하세요.
