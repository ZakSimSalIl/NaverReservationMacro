# NaverReservationMacro
## 아루히 예약 매크로

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
