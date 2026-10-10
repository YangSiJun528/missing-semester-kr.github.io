---
layout: lecture
title: "웹과 브라우저"
lang: ko
presenter: Jose
date: 2019-01-31
order: 1
video:
  aspect: 62.5
  id: XpZO3S8odec
special: true
---

터미널 외에 많은 시간을 보내는 도구가 웹 브라우저입니다. 따라서 브라우저를 효율적으로 활용하는 방법을 익힐 가치가 있습니다.

## 단축키
{: #shortcuts}

브라우저에서 마우스로 클릭하는 것이 항상 가장 빠른 방법은 아닙니다. 자주 쓰는 단축키에 익숙해지면 장기적으로 시간을 많이 아낄 수 있습니다.

- 링크를 `마우스 가운데 버튼`으로 클릭하면 새 탭에서 엽니다.
- `Ctrl+T`: 새 탭을 엽니다.
- `Ctrl+Shift+T`: 최근에 닫은 탭을 다시 엽니다.
- `Ctrl+L`: 주소·검색창의 내용을 선택합니다.
- `Ctrl+F`: 웹페이지 안에서 검색합니다. 자주 사용한다면 정규 표현식 검색을 지원하는 확장 프로그램도 유용할 수 있습니다.

## 검색 연산자
{: #search-operators}

Google이나 DuckDuckGo 같은 검색 엔진은 더 정교하게 검색할 수 있는 연산자를 제공합니다.

- `"bar foo"`: `bar foo`와 정확히 일치하는 구문을 검색합니다.
- `foo site:bar.com`: `bar.com` 안에서 `foo`를 검색합니다.
- `foo -bar`: `foo`를 검색하되 `bar`가 들어간 결과를 제외합니다.
- `foobar filetype:pdf`: 해당 확장자의 파일을 검색합니다.
- `(foo|bar)`: `foo` 또는 `bar`가 들어간 결과를 검색합니다.

[Google](https://ahrefs.com/blog/google-advanced-search-operators/)과 [DuckDuckGo](https://duck.co/help/results/syntax)의 더 자세한 연산자 목록도 참고하세요.

## 주소·검색창
{: #searchbar}

주소·검색창 자체도 강력한 도구입니다. 많은 브라우저가 웹사이트의 검색 엔진을 인식해 저장합니다. 검색 엔진에 할당된 키워드를 수정할 수 있습니다.

- Google Chrome: [chrome://settings/searchEngines](chrome://settings/searchEngines)
- Firefox: [about:preferences#search](about:preferences#search)

예를 들어 `y 검색할 단어`를 입력하면 YouTube에서 바로 검색하도록 설정할 수 있습니다.

도메인을 갖고 있다면 도메인 등록업체를 통해 하위 도메인의 전달 설정을 만들 수도 있습니다. 강사는 `https://ht.josejg.com`을 이 수업 웹사이트로 연결해 두었습니다. 주소창에 `ht.`만 입력하면 나머지가 자동 완성됩니다. 북마크와 달리 어떤 브라우저에서든 사용할 수 있다는 장점도 있습니다.

## 개인정보 보호 확장 프로그램
{: #privacy-extensions}

광고는 웹 탐색을 방해하고, 추적기는 개인정보를 침해할 수 있습니다. 좋은 광고 차단기는 광고 대부분을 차단할 뿐 아니라 공통 차단 목록에 포함된 의심스럽거나 악성인 사이트도 차단합니다. 요청 수를 줄여 페이지 로딩을 빠르게 만들기도 합니다. 추천하는 확장 프로그램은 다음과 같습니다.

- **uBlock Origin**([Chrome](https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm), [Firefox](https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/)): 미리 정의한 규칙에 따라 광고와 추적기를 차단합니다. 설정에서 활성화된 차단 목록을 살펴보세요. 지역이나 탐색 습관에 맞는 목록을 추가할 수 있습니다. [다른 곳에서 제공하는 필터](https://github.com/gorhill/uBlock/wiki/Filter-lists-from-around-the-web)를 설치할 수도 있습니다.
- **[Privacy Badger](https://privacybadger.org/)**: 추적기를 자동으로 감지하고 차단합니다. 광고 회사가 여러 사이트에서 방문 기록을 수집해 사용자 프로필을 만드는 것이 추적의 한 예입니다.
- **[HTTPS Everywhere](https://www.eff.org/https-everywhere)**: HTTPS 버전이 있는 사이트를 자동으로 HTTPS로 연결해 주는 훌륭한 확장 프로그램입니다.

비슷한 확장 프로그램은 [이 목록](https://www.privacytools.io/privacy-browser-addons/)에서도 찾아볼 수 있습니다.

## 스타일 바꾸기
{: #style-customization}

웹 브라우저도 *여러분의 컴퓨터*에서 실행되는 소프트웨어입니다. 무엇을 표시하고 어떻게 동작할지 최종적으로 사용자가 정할 수 있는 경우가 많습니다. 사용자 정의 스타일이 한 가지 예입니다. 브라우저는 CSS(Cascading Style Sheets)를 사용해 웹페이지를 어떻게 표시할지 결정합니다.

개발자 도구로 웹사이트의 소스를 살펴보고 내용이나 스타일을 임시로 바꿀 수 있습니다. 웹페이지 스크린샷만으로 내용을 무조건 믿어서는 안 되는 이유이기도 합니다.

특정 페이지의 스타일을 계속 덮어쓰게 하려면 확장 프로그램이 필요합니다. 저희는 **[Stylus](https://github.com/openstyles/stylus)**([Firefox](https://addons.mozilla.org/en-US/firefox/addon/styl-us/), [Chrome](https://chrome.google.com/webstore/detail/stylus/clngdbkpkpeebahjckkjfobafhncgmne?hl=en))를 추천합니다.

예를 들어 수업 웹사이트에 다음 스타일을 적용할 수 있습니다.

```css

body {
    background-color: #2d2d2d;
    color: #eee;
    font-family: Fira Code;
    font-size: 16pt;
}

a:link {
    text-decoration: none;
    color: #0a0;
}
```

Stylus에서는 다른 사용자가 [userstyles.org](https://userstyles.org/)에 공개한 스타일도 찾을 수 있습니다. 널리 쓰이는 사이트에는 보통 하나 이상의 어두운 테마가 있습니다. 참고로 이름이 비슷한 Stylish는 사용자 데이터를 유출한 사실이 드러났으므로 사용하지 마세요. [관련 보도](https://arstechnica.com/information-technology/2018/07/stylish-extension-with-2m-downloads-banished-for-tracking-every-site-visit/)를 참고하세요.

## 동작 바꾸기
{: #functionality-customization}

스타일을 수정하듯 웹사이트의 동작도 바꿀 수 있습니다. JavaScript를 직접 작성하고 [Tampermonkey](https://tampermonkey.net/) 같은 브라우저 확장 프로그램으로 실행하면 됩니다.

예를 들어 다음 스크립트는 J와 K 키로 Vim처럼 페이지를 위아래로 이동하게 합니다.

```js
// ==UserScript==
// @name         VIM HT
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Vim JK for our website
// @author       You
// @match        https://hacker-tools.github.io/*
// @grant        none
// ==/UserScript==


(function() {
    'use strict';

    window.onkeyup = function(e) {
        var key = e.keyCode ? e.keyCode : e.which;

        if (key == 74) { // J is key 74
            window.scrollBy(0,500);;
        }else if (key == 75) { // K is key 75
            window.scrollBy(0,-500);;
        }
    }
})();
```

[OpenUserJS](https://openuserjs.org/)나 [Greasy Fork](https://greasyfork.org/en)처럼 스크립트를 모아 둔 사이트도 있습니다. 다만 다른 사람이 작성한 사용자 스크립트는 신용카드 번호를 훔치는 등 여러 위험한 동작을 할 수 있습니다. 설치하기 전에 전체 내용을 직접 읽고 동작을 이해하며 의심스러운 행동이 없다고 확신해야 합니다. 읽을 수 없게 축소되거나 난독화된 코드는 설치하지 마세요.

## 웹 API
{: #web-apis}

웹 요청으로 서비스와 상호작용할 수 있도록 프로그래밍 인터페이스, 즉 웹 API를 제공하는 서비스가 늘고 있습니다. 자세한 입문 설명은 [MDN](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Introduction)을 참고하세요. [공개 API 목록](https://github.com/toddmotto/public-apis)도 있습니다. 웹 API는 여러 용도로 활용할 수 있습니다.

- **정보 가져오기**: 지도, 날씨, 공인 IP 주소 등의 정보를 쉽게 얻을 수 있습니다. 예를 들어 `curl ipinfo.io`는 공인 IP, 지역, 위치 등의 정보가 담긴 JSON 객체를 반환합니다. 응답을 적절히 파싱하면 명령줄 도구와도 결합할 수 있습니다. 다음 Bash 함수는 Google 자동 완성 API에 요청을 보내 처음 10개 결과를 반환합니다.

```bash
function c() {
    url='https://www.google.com/complete/search?client=hp&hl=en&xhr=t'
    # NB: user-agent must be specified to get back UTF-8 data!
    curl -H 'user-agent: Mozilla/5.0' -sSG --data-urlencode "q=$*" "$url" |
        jq -r ".[1][][0]" |
        sed 's,</\?b>,,g'
}
```

- **동작 실행하기**: 웹 API 엔드포인트로 작업을 실행할 수도 있습니다. 보통 서비스에서 발급받은 인증 토큰이 필요합니다. 예를 들어 `curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' "https://hooks.slack.com/services/$SLACK_TOKEN"`은 채널에 `Hello, World!` 메시지를 보냅니다.
- **서비스 연결하기**: 널리 쓰이는 서비스의 API를 서로 연결하는 기능은 이미 구현되어 서버와 함께 제공되기도 합니다. [If This Then That](https://ifttt.com/)과 [Zapier](https://zapier.com/)가 이런 서비스입니다.

## 웹 자동화
{: #web-automation}

웹 API만으로 충분하지 않을 때도 있습니다. 내용을 읽기만 하면 된다면 `pup` 같은 HTML 파서나 Python의 BeautifulSoup 같은 라이브러리를 사용할 수 있습니다. 하지만 사용자 동작을 재현하거나 JavaScript를 실행해야 한다면 이런 도구만으로는 부족합니다.

- **WebDriver**: 예를 들어 다음 스크립트는 웹사이트 주소를 입력하는 동작을 흉내 내 지정한 URL을 Wayback Machine에 저장합니다.

```python
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys


def snapshot_wayback(driver, url):

    driver.get("https://web.archive.org/")
    elem = driver.find_element_by_class_name('web-save-url-input')
    elem.clear()
    elem.send_keys(url)
    elem.send_keys(Keys.RETURN)
    driver.close()


driver = Firefox()
url = 'https://hacker-tools.github.io'
snapshot_wayback(driver, url)
```

## 연습 문제
{: #exercises}

1. 자주 사용하는 검색 엔진에 브라우저 검색 키워드를 설정하세요.
1. 소개한 확장 프로그램을 설치해보세요. 특정 사이트에서 uBlock Origin이나 Privacy Badger를 끄는 방법을 알아보세요. 무엇이 달라지나요? YouTube처럼 광고가 많은 사이트에서 비교해보세요.
1. Stylus를 설치하고 제공된 CSS로 수업 웹사이트의 스타일을 바꾸세요. `=   ==   ===   >=   =>   ++   /=   ~=` 같은 프로그래밍 기호가 있습니다. 글꼴을 Fira Code로 바꾸면 어떻게 보이나요? 더 알고 싶다면 프로그래밍 글꼴의 합자(ligature)를 검색해보세요.
1. 거주하는 도시나 지역의 날씨를 가져올 웹 API를 찾아보세요.
1. [Selenium](https://www.selenium.dev/documentation/) 같은 WebDriver 도구로 브라우저에서 자주 반복하는 작업을 자동화해보세요.
