from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import date

# mac
# chrome 드라이버 저장소 - "/Users/sujikang/Desktop/chromedriver"
# chrome debug 모드 시작 - /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/Desktop/temp_chrome" (참고- https://developer.mozilla.org/en-US/docs/Tools/Remote_Debugging/Chrome_Desktop)

# window
# chrome 드라이버 저장소 - "/chromedriver_win32/chromedriver"
# chrome debug 모드 시작 - C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/Chrome_debug_temp"

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "/Users/sujikang/Desktop/chromedriver"
driver = webdriver.Chrome(chrome_driver, options=chrome_options)

# 예약 하려는 웹 페이지 주소 띄워놓기
#url lunch = 'https://booking.naver.com/booking/6/bizes/223362/items/3012318'
#url dinner = 'https://booking.naver.com/booking/6/bizes/223362/items/3020244'

# 1. 5분마다 현재 페이지 새로고침
# 2. 페이지가 에러페이지일 경우 return
# 3. 정상 페이지일 경우 로직 실행
# 3-1. 날짜선택 : 회색이 아닌 부분 다 돌기
# 3-2. 시간선택 : 날짜 선택 후 시간이 선택이 가능(초록색)한지 확인, 가능하면 선택, 없으면 다시 3-1로
# 3-3. 인원선택 : 1명으로 고정
# 3-4. 몇인분선택 : +1 (기본이 0이라서)
# 3-5. 결제하기 버튼 클릭
# 3-6. return~!

#todo - 만약 reservation_button 찾을 수 없으면 새로 고침 후 다시 시도 (아루히 등은 예약이 다 차면 reservation 버튼이 없어지기 때문)
#예약 버튼 클릭 (예약 섹션으로 이동됨)
reservation_button = driver.find_element_by_class_name('_3wP2G').find_element_by_xpath('.//a')
reservation_button.click()
#reservation_button.send_keys("\n")

#첫번째 예약 버튼 클릭 (예약 페이지 2번째 place_section 클래스 하위 a tag로 접근)
time.sleep(1)
place_section_list = driver.find_elements_by_class_name('place_section')
reservation_item_button = place_section_list[1].find_element_by_xpath(".//a")
reservation_item_button.click()
#reservation_item_button.send_keys("\n")

# 캘린더 클릭
#todo - 나중에 sleep 을 수동으로 거는게 아니라 page loading 이 다 됐나 파악한다음에 다음 코드 진행시켜야함
time.sleep(6)
calendar_status = driver.find_element_by_class_name('section_date_time').find_element_by_xpath('.//a').get_attribute("title")
if calendar_status == "펼쳐보기":
    calendar_button = driver.find_element_by_class_name('fn-calendar1')
    calendar_button.click()
#     calendar_button.send_keys('\n')


# 예약 원하는 날짜 클릭
time.sleep(2)
reservation_date = '2021-03-23'
day_element = driver.find_element_by_xpath("//td[@data-cal-datetext='" + reservation_date + "']")
day_element.click()
# day_element.send_keys('\n')

# 예약 가능한 가장 빠른 시간 클릭
time.sleep(1)
time_section_list = driver.find_elements_by_class_name('list_time')
time_element_list = map(lambda time_section: time_section.find_elements_by_xpath(".//li"), time_section_list)
flatten_time_element_list = [y for x in list(time_element_list) for y in x]

for time_element in flatten_time_element_list:
    # 색상
    time_element_color = time_element.find_element_by_tag_name('a').value_of_css_property('background-color')
    if time_element_color == "rgba(237, 251, 220, 1)":
        time_element.click()
        #time_element.send_keys('\n')
        break


#todo - 최고다손짬뽕 같은 경우 다음단계가 없고 예약 신청하기 버튼이 바로 나온다. 이런 경우의 예외처리도 필요하다.
# 다음 단계 클릭
time.sleep(1)
next_button = driver.find_element_by_xpath('//*[@id="ct"]/div/div[1]/booking-summary-floating-middle-step/div/div/booking-button-next/div/div/button')
next_button.click()
#next_button.send_keys('\n')

# 예약 신청하기 (확정) 클릭
time.sleep(0.5)
submit_reservation_button = driver.find_element_by_xpath('//*[@id="ct"]/div/div[1]/booking-button-submit/div[1]/div/button')
# submit_reservation_button.click() -> 진짜 예약할때만 주석 풀자
