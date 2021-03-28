from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import schedule
from selenium.common.exceptions import NoSuchElementException

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
#아웃백 url = 'https://booking.naver.com/booking/6/bizes/305136/items/3700886?area=ple'

# 1. 5분마다 현재 페이지 새로고침
# 2. 정상 페이지일 경우 월 별로 로직 실행
# 2-1. 날짜선택 : 회색이 아닌 부분 다 돌기 (회색이면 disabled_day count 증가)
# 2-2. 시간선택 : 날짜 선택 후 시간이 선택이 가능(초록색)한지 확인, 가능하면 선택, 없으면 다시 2-1로
# 2-3. 인원선택 : 1명으로 고정
# 2-4. 몇인분선택 : +1 (기본이 0이라서)
# 2-5. 결제하기 버튼 클릭
# 3. 만약 월의 모든 날짜가 회색인 경우, 중단

def isErrorPage():
    try:
        driver.find_element_by_class_name("calendar-date")
        return False
    except NoSuchElementException:
        print("현재 예약 가능한 상품이 없습니다.")
        return True

def main():
    url = "https://booking.naver.com/booking/6/bizes/223362/items/3012318"
    driver.get(url)
    time.sleep(2) # 웹 로딩때까지 sleep

    if not isErrorPage():
        while True:
            is_month_disable = aruhi_monthly_reservation() # 월 별로 Aruhi 예약
            if not is_month_disable and not isReservationSuccess:
                # 다음 달 클릭 후 다시 while loop
                calender_next_element = driver.find_element_by_class_name("calendar-btn-next-mon")
                calender_next_element.click()
            else:
                break

def aruhi_monthly_reservation():
    time.sleep(1)
    day_elements = driver.find_elements_by_class_name("calendar-date")
    disabled_day = 0

    for day in day_elements:
        # 회색 e4e4e4
        if day.find_element_by_class_name("num").value_of_css_property('color') != "rgba(228, 228, 228, 1)":
            day.click()

            time.sleep(0.5) # time list 찾는데 시간이 걸리기 때문에 여기서 쉬어줘야함
            time_section_list = driver.find_elements_by_class_name('lst_time') #오전 오후
            time_element_list = map(lambda time_section: time_section.find_elements_by_xpath(".//li"),
                                    time_section_list) # [['11:30'], ['1:00']]
            flatten_time_element_list = [y for x in list(time_element_list) for y in x] #['11:30', '1:00']

            is_time_available = False
            print(len(flatten_time_element_list))
            for time_element in flatten_time_element_list:
                # 색상
                time_element_color = time_element.find_element_by_tag_name('a').value_of_css_property(
                    'background-color')
                if time_element_color == "rgba(237, 251, 220, 1)":
                    time_element.click()
                    #time_element.send_keys('\n')
                    is_time_available = True
                    break

            if is_time_available:
                # btn_plus_minus class는 방문인원, 몇인분에 모두 적용됨. 마지막 element가 몇인분의 plus에 해당함.
                # 아루히는 방문인원이 기본 1, 몇인분이 0 이기 때문에 인분..숫자를 하나 늘려줘야한다.
                meal_plus_element = driver.find_elements_by_class_name("btn_plus_minus")[-1]
                meal_plus_element.click()

                # 예약 신청하기
                reservation_element = driver.find_element_by_class_name("bottom_btn").find_element_by_tag_name('button')
                reservation_element.click()
                global isReservationSuccess
                isReservationSuccess = True
                break
        else:
            disabled_day += 1

    is_month_disable = disabled_day == len(day_elements)
    return is_month_disable

isReservationSuccess = False

#5분마다 실행
schedule.every(5).minutes.do(main)

#schedule.run_pending() 함수를 1초 주기로 호출하여 등록된 스케쥴 Job의 계획을 확인하고 계획(주기 또는 시점)에 해당되는 Job을 수행
while not isReservationSuccess:
    schedule.run_pending()
    time.sleep(1)

