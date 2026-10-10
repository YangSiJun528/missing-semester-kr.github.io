---
layout: lecture
title: "운영체제 사용자 설정"
lang: ko
presenter: Anish
date: 2019-01-29
order: 3
video:
  aspect: 62.5
  id: epSRVqQzeDo
special: true
---

운영체제를 원하는 대로 바꾸는 방법은 설정 메뉴에 보이는 것보다 훨씬 많습니다.

# 키보드 매핑 바꾸기
{: #keyboard-remapping}

키보드에는 자주 쓰지 않는 키가 있을 것입니다. 그대로 두는 대신 유용한 동작에 연결해보세요.

## 다른 키로 매핑하기
{: #remapping-to-other-keys}

가장 간단한 방법은 어떤 키를 다른 키로 바꾸는 것입니다. 예를 들어 Caps Lock을 거의 쓰지 않는다면 더 유용한 키로 바꿀 수 있습니다. Vim 사용자라면 Caps Lock이 Escape로 동작하게 만들고 싶을 수 있습니다.

macOS에서는 시스템 환경설정의 키보드 설정에서 일부 매핑을 바꿀 수 있습니다. 더 복잡한 매핑에는 별도 소프트웨어가 필요합니다.

## 임의의 명령으로 매핑하기
{: #remapping-to-arbitrary-commands}

키를 다른 키로 바꾸는 것만 가능한 것은 아닙니다. 키 하나나 키 조합을 임의의 명령에 연결하는 도구도 있습니다. 예를 들어 `Command-Shift-T`로 새 터미널 창을 열게 만들 수 있습니다.

# 숨겨진 운영체제 설정 바꾸기
{: #customizing-hidden-os-settings}

## macOS
{: #macos}

macOS는 `defaults` 명령으로 유용한 설정을 많이 제공합니다. 예를 들어 숨긴 앱의 Dock 아이콘을 반투명하게 표시할 수 있습니다.

```shell
defaults write com.apple.dock showhidden -bool true
```

가능한 설정을 모두 모은 단일 목록은 없지만, Mathias Bynens의 [.macos](https://github.com/mathiasbynens/dotfiles/blob/master/.macos)처럼 구체적인 설정 사례를 온라인에서 찾아볼 수 있습니다.

# 창 관리
{: #window-management}

## 타일 방식의 창 관리
{: #tiling-window-management}

[타일 방식의 창 관리](https://en.wikipedia.org/wiki/Tiling_window_manager)는 창을 서로 겹치지 않는 영역에 배치하는 방식입니다. Linux 기반 운영체제에서는 타일 창 관리자를 설치할 수 있습니다. Windows나 macOS에서는 비슷한 동작을 제공하는 앱을 설치할 수 있습니다.

## 여러 화면 관리
{: #screen-management}

키보드 단축키를 설정하면 여러 화면 사이에서 창을 옮기고 배치하기 편리합니다.

## 배치
{: #layouts}

창을 늘 일정한 방식으로 배치한다면 매번 직접 옮기지 않고 스크립트로 처리할 수 있습니다. 원하는 배치를 손쉽게 다시 적용할 수 있게 됩니다.

# 참고 자료
{: #resources}

- [Hammerspoon](https://www.hammerspoon.org/): macOS 데스크톱 자동화
- [Rectangle](https://rectangleapp.com/): macOS 창 관리자
- [Karabiner](https://karabiner-elements.pqrs.org/): 정교한 macOS 키보드 매핑
- [r/unixporn](https://www.reddit.com/r/unixporn/): 다양한 사용자 설정의 화면과 설명

# 연습 문제
{: #exercises}

1. Caps Lock을 Escape, Ctrl, Backspace처럼 더 자주 쓰는 키로 바꾸는 방법을 알아보세요.

1. 새 터미널 창이나 브라우저 창을 여는 전역 키보드 단축키를 만드세요.

{% comment %}
추가할 내용:

- Bitbar / Polybar
- 클립보드 관리자(복사 기록 쌓기와 검색)
{% endcomment %}
