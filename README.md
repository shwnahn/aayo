![aayo_logo_yellow](https://github.com/user-attachments/assets/736920e6-068a-4a5d-8f2d-f808b2fb7cd4)

# 📰 AAYO
##### 🏆 피로그래밍 21기 최종 프로젝트 작품

### 📜 Contents
 1. [Overview](#-overview)
 2. [서비스 화면](#-서비스-화면)
 3. [주요 기능](#-주요-기능)
 4. [개발 환경](#%EF%B8%8F-개발-환경)
 5. [UserFlow](#-UserFlow)
 6. [기획 및 설계 산출물](#-기획-및-설계-산출물)
 7. [팀원 소개](#-팀원-소개)
 
## ✨ Overview

> 단체 커피 메뉴 주문 시 효율적인 메뉴 취합을 도와주는 서비스

## ✨ AAYO의 배포 사이트
##### 🏆 [사이트](https://aayo.kr/)



## ✨ AAYO의 소통 플랫폼 
##### 🏆 [노션](https://ahnsh.notion.site/76c36ea84a464b1dad4e8c8d0eb935fa)
##### 🏆 [ZEP](https://zep.us/)
##### 🏆 [Discord](https://discord.com/)



## 👀 서비스 화면
### ✨ 모든 페이지 `Mobile First(웹뷰 기준 max-width: 500px)` 지원


### 홈
- AAYO 로고
- 서비스 목적을 간단하게 설명해주는 랜딩 문구
- '10초만에 메뉴 모으기' 버튼을 통해 시작
  
![image.jpg1](https://github.com/user-attachments/assets/96eeae02-5e3b-4f0b-a14c-998bfcd8b8eb)
--- |


### 카페 선택 & 방 이름 생성
- 카페 메뉴 취합을 위해 사람들을 초대할 방 이름 입력
- 카페 목록에서 메뉴를 주문할 카페를 선택
- 방 생성

![image.jpg1](https://github.com/user-attachments/assets/8cd6a796-60a3-46bb-904a-225b823136c8) |![image.jpg2](https://github.com/user-attachments/assets/bafeb4c4-8038-4b77-b465-1f457a9aae55)
--- | --- | 

### 방 상세 페이지(메인 페이지)
- 좌상단에 생성한 방 이름, 우상단에 선택된 카페 로고를 보여줌
- 링크 공유하기 버튼
  - 카카오톡 공유 또는 클립보드에 링크를 복사하는 옵션을 가지는 모달창을 생성
- 메뉴 주문하기 버튼
  - 해당 카페 메뉴들이 나열되고, 원하는 메뉴 및 커스텀을 선택할 수 있음
- 주문 모아보기 버튼
  - 해당 방에 들어온 게스트들이 주문한 내역을 한번에 볼 수 있음
- 🖤
  - 서비스에 대한 리뷰 설문과 후원을 할 수 있는 모달창을 생성함

![image.jpg3](https://github.com/user-attachments/assets/fb9c6d2d-7d83-488c-aae1-85282f0eb8ef) |![image.jpg1](https://github.com/user-attachments/assets/6fac058f-3ee9-4af1-89f1-6d347cfefda5) |![image.jpg2](https://github.com/user-attachments/assets/a465843b-5bd1-4a5f-a41b-5e81f9024096)
--- | --- | --- |


### 메뉴 주문하기 페이지
- 메뉴 검색 기능
- 카테고리 필터링 기능
- 메뉴 선택 시 상세 커스텀 기능(아이스/핫, 사이즈, 얼음 양, 기타 상세 내용)
- 메뉴를 선택하고 '주문 확정하기' 버튼을 누르면 메뉴 취합 절차가 완료되었음을 알려주는 가이드 페이지로 넘어감

![image.jpg4](https://github.com/user-attachments/assets/f3010b38-aedb-4054-9432-8dfee9a38f05) |![image.jpg1](https://github.com/user-attachments/assets/39dcc944-156b-4dac-a629-bfb7b22b01f7) |![image.jpg2](https://github.com/user-attachments/assets/99bb98d8-728b-4a44-9e46-658be6b4572c) |![image.jpg3](https://github.com/user-attachments/assets/08c33b82-d744-4877-a808-91b50310a805)
--- | --- | --- | --- |


### 주문 완료 페이지
- 유저에게 메뉴 취합이 끝났음을 명시적으로 알림
- 전체 주문 보기 / 홈으로 돌아가기 중 선택 가능

![image.jpg1](https://github.com/user-attachments/assets/6919dc0c-7997-4e23-affd-4ebaa3b698e3)
--- |

### 주문 모아보기 페이지
- 해당 방에 초대된 모든 게스트들이 주문한 메뉴를 확인할 수 있음
- 메뉴 이름, 옵션, 주문한 사람, 수량이 표시되는 아이템 카드가 나열되는 형식
- '메뉴 변경이 필요하신가요?' 버튼
  - 현재 주문자가 본인이 주문한 메뉴를 수정할 수 있음(초기화 후 다시 고르는 방식)
- '앗! 놓치신 분이 계신가요?' 버튼
  - 메뉴 주문자를 추가로 초대할 수 있음, 링크 공유하기 버튼과 동일한 모달 생성

![image.jpg1](https://github.com/user-attachments/assets/9f0539eb-ffa7-4953-831c-7b52ed7cd3e8)

## ✨ 주요 기능

- `방 생성 기능`
  - 특정 카페에서 메뉴를 취합할 사람들을 초대하는 방을 생성한다
  - 방 생성 시 랜덤한 8자리 unique id를 부여하여 각 방을 구분한다
  
- `방 링크 공유 기능`
  - 기본적으로는 클립보드에 방 링크를 복사하여 공유한다
  - 카카오톡 SDK를 활용하여 방 링크 복사 및 공유를 더 편리하게 할 수 있다
  
- `카페 메뉴 크롤링`
  - 각 카페별 크롤링 코드를 작성하여 메뉴 이름, 메뉴 사진, 카테고리, 상세 설명을 주기적으로 긁어온다
  - 긁어온 데이터들은 json 형식으로 DB에 미리 저장하여 페이지 로드 시간을 단축하였다

- `유저(게스트) 생성`
  - 유저 이름만 입력하면 되는 간단한 로그인 과정을 구현하였다 
  - 브라우저 세션 단에서 정보를 저장하여 뒤로가기나 새로고침을 하여도 유저 정보가 남아 있도록 하였다
   
- `메뉴 검색 및 카테고리 필터링`
  - 메뉴 주문 시 검색 기능을 통해 원하는 메뉴를 빠르게 찾을 수 있다
  - 크롤링 시 긁어온 카테고리 정보를 활용하여 해당 카테고리의 메뉴들만 볼 수도 있다


## 🖥️ 개발 환경

**Management Tool**
- 형상 관리 : Git
- 커뮤니케이션 : Zep, Notion, Discord
- 디자인 : Figma

**🐳 Backend**
- Python `3.12.4`
- Django `4.2.x`
- pipenv or poetry (패키지 관리 도구)
- PostgreSQL  `16.3`
- Gunicorn `20.1.0` (배포용 WSGI 서버)

**🦊 Frontend**
- lang: HTML5, CSS3, JAVASCRIPT

**🖼️ Requirements.txt**
```plaintext
asgiref            3.8.1
attrs              23.2.0
certifi            2024.7.4
charset-normalizer 3.3.2
Django             5.0.7
django-environ     0.11.2
h11                0.14.0
idna               3.7
outcome            1.3.0.post0
packaging          24.1
pillow             10.4.0
pip                24.0
psycopg            3.2.1
PySocks            1.7.1
python-dotenv      1.0.1
requests           2.32.3
selenium           4.23.1
setuptools         72.1.0
sniffio            1.3.1
sortedcontainers   2.4.0
sqlparse           0.5.1
trio               0.26.0
trio-websocket     0.11.1
typing_extensions  4.12.2
urllib3            2.2.2
webdriver-manager  4.0.2
websocket-client   1.8.0
wsproto            1.2.0
```

**🗝️ SDK**
- [카카오톡 SDK - 메시지](https://developers.kakao.com/product/message)   

**🗂️ DB**
- PostgreSQL `16.3`

**🌐 Server**
- AWS EC2 (Ubuntu `20.04`)
- Nginx `1.23` (Reverse Proxy)
- Gunicorn `20.1.0` (WSGI Application Server)
- HTTPS (TLS `1.2`)

**🔨 IDE**
- VSCode `1.92.1`
- pgAdmin `8.3`

## 💫 UserFlow

![image](https://github.com/user-attachments/assets/86b9e86c-9da0-4300-8f17-fab66a3e5d49)

## 📂 기획 및 설계 산출물

### [💭 요구사항 정의 및 기능 명세](https://ahnsh.notion.site/f8cec91e8fb64611a40f6558eaa3cfc2?v=566aabe803bf48b087a700f38aa24c8b)

### [🎨 화면 설계서](https://www.figma.com/design/7vG5sJUBdX44xBhu0uT6Q1/aayo_2nd-FE?node-id=0-1&t=CkVkcoi24cAQW8MD-1)

# 💞 팀원 소개
##### ❤️‍🔥 AAYO를 개발한 `피로그래밍 21기` 팀원들을 소개합니다!

| **[안시환](https://github.com/shwnahn)** | **[이지현](https://github.com/ljh130334)** | **[이송민](https://github.com/songmin0111)** | **[김민수](https://github.com/devkev00)** |
| :---------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------: |
| <img src="https://github.com/user-attachments/assets/66969d42-e4df-4849-b4bb-4851b057664c" width="400"> | <img src="https://github.com/user-attachments/assets/5e639a86-554e-4f33-b809-dcf233f8547d" width="400"> | <img src="https://github.com/user-attachments/assets/68a08750-ffc4-432d-a343-1b449979a20e" width="400"> | <img src="https://github.com/user-attachments/assets/2a0bec5f-203a-403d-b298-ba0db69efefc" width="400"> |
| PM | FE LEADER | PR LEADER | BE LEADER |
