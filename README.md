# NaverReservationMacro
## 아루히 예약 매크로

### 파일경로

`Aruhi/main.py`

### How To Start

1. chrome debug 모드 시작

   - **mac**: `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/Desktop/temp_chrome"`
   - **window**: `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/Chrome_debug_temp"`
   - **주의점** : 화면 배율 100%로 설정

2. `chrome://settings/help` 에서 크롬 버전 확인

3. [ChromeDriver - WebDriver for Chrome](https://chromedriver.chromium.org/) 에서 version 맞는 크롬 드라이버 다운로드

4. `Aruhi/main.py` 설정

   - 받은 chromedriver 경로 지정 

     `chrome_driver = "/Users/kangsujin/Desktop/chromedriver"`
     
     `chrome_driver = "/chromedriver_win32/chromedriver"`

   - 원하는 url 설정 

     `url = "https://booking.naver.com/booking/6/bizes/223362/items/3012318"`

     - 아루히 점심: https://booking.naver.com/booking/6/bizes/223362/items/3012318
     - 아루히 저녁: https://booking.naver.com/booking/6/bizes/223362/items/3020244

   - 원하는 예약 인원 지정

     `people_count = 2` => 2명 예약

   - 실행 주기 설정

     `schedule.every(10).seconds.do(main)` => 10초마다 실행

5.  `/Aruhi` 경로에서 `python3 main.py` 실행

   이때 모듈들이 깔려 있지 않아 에러가 뜬다면 install 필요

   - `pip install selenium`

   - `pip install schedule`

     등등..

6. 처음 실행 시 크롬에 네이버 로그인 페이지가 뜰텐데, `로그인` 필요

### Main Logic

1. 특정 시간 주기로 정해진 url에 접속 (ex. 10초마다 아루히 점심 url 접속)
2. 예약 가능 페이지일 때, 모든 일자가 회색(disabled) 이 아닌 월까지 월 별 로직 실행 
   1. 회색이 아닌 일자 클릭
   2. 해당 일자에 선택 가능한 시간(연두색)이 있다면 클릭
   3. 원하는 인원 수만큼 인원 + 버튼 클릭 (defualt 1)
   4. 특정 인원 수용이 가능하다면, 원하는 인원수 만큼 인분 + 버튼 클릭 (defualt 0)
   5. 결제하기 버튼 클릭

### Environment

- python 3.7.4





## 파이썬 매크로 연습 코드

### `practice_code/naver_login_macro.ipynb`

[[파이썬 매크로 만들기] 2. PYAUTOGUI로 네이버 로그인 해보기](https://www.youtube.com/watch?v=GfFzW9jt_GI&t=0s)

- 수동으로 로그인 버튼, id, 비밀번호 위치를 받아 로그인하는 코드

### `practice_code/daum_login_macro.ipynb`

[[파이썬 매크로 만들기] 3. 매크로 시작 단축키 만들기](https://www.youtube.com/watch?v=EZcy82TU6Hs&t=0s)
- trigger_key를 이용해 로그인 버튼, id 위치를 받고, 실행시키는 코드


###  `practice_code/color_checker.ipynb`

[[파이썬 매크로 만들기] 4. 화면 색깔 인식하기 (센서)](https://www.youtube.com/watch?v=RP9lwYNC1bk&t=0s)
- 마우스가 위치한 곳의 색상을 받아 빨강/초록/파랑일 경우 색상을 출력하는 코드

### `practice_code/screen_recognition_red_table.ipynb`

[[파이썬 매크로 만들기] 5. 화면 인식 기반 매크로 만들기](https://www.youtube.com/watch?v=71ind89-vvM%E2%80%8B&feature=youtu.be)
- `practice_code/html/red_table.html` : 3X3의 테이블에 특정 확률로 한칸이 빨간색이 되는 페이지
- `red_table.html` 파일에서 빨간색 칸이 나오면 해당 칸을 클릭하고, 나오지 않으면 페이지를 새로고침하는 코드

### `practice_code/screen_recognizer_naver.ipynb` 
[[파이썬 매크로 만들기] 5. 화면 인식 기반 매크로 만들기](https://www.youtube.com/watch?v=71ind89-vvM%E2%80%8B&feature=youtu.be)
- `practice_code/html/naver_button.html` : 버튼을 클릭하면 특정 확률로 네이버 페이지로 이동하거나 alert 창이 생기는 페이지
- `naver_button.html` 파일에서 '네이버 페이지로 이동' 버튼을 클릭했을 때, alert 확인버튼위치의 색상을 판단해서, 파란색일 경우 alert창을 닫고 클릭을 반복하는 코드

### `practice_code/korail_selenium.ipynb` 
[[파이썬 매크로 만들기] 7. Selenium으로 KTX 취소표를 사보자](https://www.youtube.com/watch?v=_0JGnYS2StE&t=0s)

- [코레일 페이지](http://www.letskorail.com/)에서 출발지, 도착지, 날짜, 시간을 입력해 첫번째 가능한 좌석을 예매하는 코드

###  `practice_code/naver_login_macro_selenium.ipynb` 
- selenium으로 [네이버 페이지](https://www.naver.com)를 로그인하는 코드 





## 파이썬 매크로 연습 코드

###  `naver_reservation/naver_reservation_macro.ipynb`

#### How To Start

1. `chrome://settings/help` 에서 크롬 버전 확인

2. [ChromeDriver - WebDriver for Chrome](https://chromedriver.chromium.org/) 에서 version 맞는 크롬 드라이버 다운로드

3.  환경변수 설정

   - 받은 chromedriver 경로 지정 

     `chrome_driver = "/Users/kangsujin/Desktop/chromedriver"`

     `chrome_driver = "/chromedriver_win32/chromedriver"`

   - 원하는 url 설정 

     `url = "https://map.naver.com/v5/entry/place/159330481?c=14122634.3334544,4516874.2031988,14,0,0,0,dh"`

   - 원하는 날짜 설정

     `reservation_date = '2021-03-15'`

4. jupyter notebook에서 실행

#### Main Logic

1. 받은 url로 웹페이지 실행 
2. iframe으로 포커스 이동
3. 예약 버튼 클릭  (예약 섹션으로 이동됨)
4. 첫번째 예약 버튼 클릭 (예약 페이지 2번째 place_section 클래스 하위 a tag로 접근)
5. 캘린더 클릭
6. 예약 원하는 날짜 클릭
7. 예약 가능한 가장 빠른 시간 클릭
8. 다음 단계 클릭 
9. 위 과정이 모두 성공하면 로그인 창으로 이동됨

###  `naver_reservation/naver_reservation_macro_with_default_browser.ipynb`

#### How To Start

1. chrome debug 모드 시작

   - **mac**: `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/Desktop/temp_chrome"`
   - **window**: `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/Chrome_debug_temp"`
   - **주의점** : 화면 배율 100%로 설정

2. 예약 원하는 url 띄워놓기

   - `url = "https://map.naver.com/v5/entry/place/159330481?c=14122634.3334544,4516874.2031988,14,0,0,0,dh"`

   - 미리 로그인 필요 ( 예약이 바로 가능하도록 )

3. `chrome://settings/help` 에서 크롬 버전 확인

4. [ChromeDriver - WebDriver for Chrome](https://chromedriver.chromium.org/) 에서 version 맞는 크롬 드라이버 다운로드

5.  환경변수 설정

   - 받은 chromedriver 경로 지정 

     `chrome_driver = "/Users/kangsujin/Desktop/chromedriver"`

     `chrome_driver = "/chromedriver_win32/chromedriver"`

   - 원하는 날짜 설정

     `reservation_date = '2021-03-15'`

6. jupyter notebook에서 실행

#### Main Logic

1. 디버그 모드로 실행한 크롬으로 크롬 드라이버 설정
2. iframe으로 포커스 이동
3. 예약 버튼 클릭  (예약 섹션으로 이동됨)
4. 첫번째 예약 버튼 클릭 (예약 페이지 2번째 place_section 클래스 하위 a tag로 접근)
5. 캘린더 클릭
6. 예약 원하는 날짜 클릭
7. 예약 가능한 가장 빠른 시간 클릭
8. 다음 단계 클릭 
9. 예약 확정 클릭

**주의사항** : 다음단계 버튼이 없는 페이지일 경우 예외처리가 되어있지 않아 오류가 날 수 있다.