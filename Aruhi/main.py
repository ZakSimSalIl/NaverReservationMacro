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
chrome_driver = "/chromedriver_win32/chromedriver"
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

#todo
#chrome창 안띄워져있으면 chrome창 띄우기

def aruhi_reservation():
    #에러페이지가 아닐경우부터 로직 시작
    day_elements = driver.find_elements_by_class_name("calendar-date")
    for day in day_elements:
        # 회색 e4e4e4
        if day.find_element_by_class_name("num").value_of_css_property('color') != "rgba(228, 228, 228, 1)":
            day.click()

            time_section_list = driver.find_elements_by_class_name('lst_time') #오전 오후
            time_element_list = map(lambda time_section: time_section.find_elements_by_xpath(".//li"),
                                    time_section_list) # [['11:30'], ['1:00']]
            flatten_time_element_list = [y for x in list(time_element_list) for y in x] #['11:30', '1:00']

            is_time_available = False
            for time_element in flatten_time_element_list:
                # 색상
                time_element_color = time_element.find_element_by_tag_name('a').value_of_css_property(
                    'background-color')
                if time_element_color == "rgba(237, 251, 220, 1)":
                    #time_element.click()
                    time_element.send_keys('\n')
                    is_time_available = True
                    break

            #몇인분선택
            if is_time_available:
                # btn_plus_minus class는 방문인원, 몇인분에 모두 적용됨. 마지막 element가 몇인분의 plus에 해당함.
                meal_plus_element = driver.find_elements_by_class_name("btn_plus_minus")[-1]
                meal_plus_element.click()


aruhi_reservation()