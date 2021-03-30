from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import schedule
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import os


# Main Logic
#
# 1. 특정 시간 주기로 정해진 url 에 접속 (ex. 10초마다 아루히 점심 url 접속)
# 2. 예약 가능 페이지일 때, 모든 일자가 회색(disabled) 이 아닌 월까지 월 별 로직 실행
#    2-1. 회색이 아닌 일자 클릭
#    2-2. 해당 일자에 선택 가능한 시간(연두색)이 있다면 클릭
#    2-3. 원하는 인원 수만큼 인원 + 버튼 클릭 (default 1)
#    2-4. 특정 인원 수용이 가능하다면, 원하는 인원수 만큼 인분 + 버튼 클릭 (default 0)
#    2-5. 결제하기 버튼 클릭

def is_element_exist(class_name):
    try:
        driver.find_element_by_class_name(class_name)
        return True
    except NoSuchElementException:
        return False


def log_with_voice_alert(message):
    os.system('say {}'.format(message))
    print(message)


def aruhi_reservation(url, people_count):
    # 현재 시간 출력
    print("Current Time =", datetime.now().strftime("%I:%M:%S %p"))

    # url 접속
    driver.get(url)
    # 웹 로딩때까지 sleep
    time.sleep(2)

    # 에러 페이지가 아닐때 (캘린더 element 를 찾을 수 있을때) 로직 실행
    is_error_page = not is_element_exist("calendar-date")
    if not is_error_page:
        while True:
            # 월 별로 아루히 예약
            is_month_disable = aruhi_monthly_reservation(people_count)

            # 월 별 로직을 돌았을때, disable 상태(모든 일자가 회색인 경우)가 아니고 예약이 안되어있다면 다음 달 클릭한 후 위의 while loop 재실행
            if not is_month_disable and not is_reservation_success:
                calender_next_element = driver.find_element_by_class_name("calendar-btn-next-mon")
                calender_next_element.click()
            else:
                break
    else:
        # 에러 페이지인 경우 에러 로그 출력
        print("현재 예약 가능한 상품이 없습니다.")


def aruhi_monthly_reservation(people_count):
    # 모든 로직은 월에 표시되는 첫번째 일자부터 시행되어야함. (ex. 2021/4월 달력 -> 3월 28일부터 실행)
    # 하지만 sleep 으로 지연을 주지 않으면 이전 월에서 시행되었던 일자의 로직 이후부터 실행 됨. (ex. 2021/3월 달력에서 4/3까지 로직 실행 후, 4월에는 4/4부터 실행)
    # 이상적인 동작이긴 하지만, 원하던 기대 결과가 아니기 때문에 이를 방지하기 위해 sleep 으로 지연을 줌 (ex. 3월에서 4/3까지 실행 후, 4월에서 3/28일부터 다시 실행)
    time.sleep(1)

    # 유효한 월인지 판단하기 위한 변수. day 가 회색일때 +되며, 달력에 표시된 모든 일자의 수와 값이 동일해질때 해당 월은 유효하지 않다고 판단.
    disabled_day = 0

    day_elements = driver.find_elements_by_class_name("calendar-date")
    # 일자 별 로직 시행
    for day in day_elements:
        day_num_element = day.find_element_by_class_name("num")
        day_num_text = day_num_element.text
        # day 색이 회색 (hex = e4e4e4 / rgba = (228, 228, 228, 1))이 아닐때 로직 시행
        if day_num_element.value_of_css_property('color') != "rgba(228, 228, 228, 1)":
            print(day_num_text, "일 확인 중..")

            # 일자 클릭
            day.click()
            # 일자 클릭 후 time list 를 찾는데 시간이 걸리기 때문에 sleep
            time.sleep(0.5)

            # 시간 list 추출
            is_time_available = False
            time_section_list = driver.find_elements_by_class_name('lst_time')  # 오전 / 오후
            time_element_list = map(lambda time_section: time_section.find_elements_by_xpath(".//li"),
                                    time_section_list)  # [['11:30'], ['1:00']]
            flatten_time_element_list = [y for x in list(time_element_list) for y in x]  # ['11:30', '1:00']

            # 시간별 로직 시행
            for time_element in flatten_time_element_list:
                time_element_color = time_element.find_element_by_tag_name('a').value_of_css_property(
                    'background-color')
                # 시간 색상이 연두색 (rgba = (237, 251, 220, 1))이라면 클릭 후 is_time_available 를 True 로 변경
                if time_element_color == "rgba(237, 251, 220, 1)":
                    time_element.click()
                    is_time_available = True
                    break

            # 가능한 시간이 있을때 로직 시행
            if is_time_available:
                # 초기에 바로 'btn_plus_minus' class 이름으로 elements 를 찾으면 방문 인원 -, + 에 해당하는 element 만 잡히기 때문에 sleep
                # 'btn_plus_minus' class 는 방문인원, 몇인분 등의 -, + 에 모두 적용되는 class.
                time.sleep(0.5)

                # 아루히의 경우 'btn_plus_minus'의 두번째 element 가 인원 + 버튼에 해당 (첫번째는 - )
                person_plus_element = driver.find_elements_by_class_name("btn_plus_minus")[1]  # 인원 + 버튼
                if people_count > 1:
                    # 아루히의 방문 인원 default 값은 1이므로 [0 ~ 인원-1] 만큼 + 버튼 클릭
                    for i in range(0, people_count - 1):
                        person_plus_element.click()

                # 만약 원하는 인원만큼 예약이 가능한지 (인원수만큼 + 클릭했을때 alert 가 뜨지 않는지) 판단하는 변수
                is_desired_people_available = not is_element_exist("_booking_alert_txt")

                # 만약 원하는 인원만큼 예약이 불가능 하다면 alert 창 닫기 후 continue (다음 day 실행)
                # 단, 이곳까지 들어왔다는 것은 1명 이상은 가능하다는 의미이기 때문에 알림 날림
                if not is_desired_people_available:
                    desired_people_failure_message = "{} 일, 해당 인원의 예약은 불가능합니다. 단, 1명은 가능합니다.".format(day_num_text)
                    log_with_voice_alert(desired_people_failure_message)
                    close_element = driver.find_element_by_class_name("btn_cls")
                    close_element.click()
                    continue

                # 아루히의 경우 'btn_plus_minus'의 마지막 element 가 식사 인분 + 버튼에 해당
                meal_plus_element = driver.find_elements_by_class_name("btn_plus_minus")[-1]
                for i in range(0, people_count):
                    # 아루히의 식사 인분 default 값은 0이므로 [0 ~ 인원] 만큼 + 버튼 클릭
                    meal_plus_element.click()

                # 예약 신청 버튼 클릭
                reservation_element = driver.find_element_by_class_name("bottom_btn").find_element_by_tag_name('button')
                reservation_element.click()

                # 예약 성공 전역 변수 (is_reservation_success) 값을 True 로 변경
                global is_reservation_success
                is_reservation_success = True

                # 예약 성공 알림 후 break (day 별 로직 시행 stop)
                print('\007')  # beep sound
                success_message = "{} 일 예약 성공".format(day_num_text)
                log_with_voice_alert(success_message)
                break
        else:
            disabled_day += 1

    # 해당 월이 유효한지 return. (disable_day 가 달력에 표시된 모든 일자의 수와 값이 동일하다면 해당 월은 disable)
    is_month_disable = disabled_day == len(day_elements)
    return is_month_disable


def get_driver(driver_path):
    # localhost:9222 포트로 실행된 크롬 option 설정
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    # 다운로드 받은 chrome driver 경로 설정
    driver = webdriver.Chrome(driver_path, options=chrome_options)
    return driver


def main(schedule_cycle, url, people_count):
    # job 수행 주기 및 수행할 함수 등록
    schedule.every(schedule_cycle).seconds.do(lambda: aruhi_reservation(url, people_count))

    # 예약이 성공할때까지 수행
    while not is_reservation_success:
        # 1초 주기로 등록된 스케쥴 job 의 계획을 확인 및 수행
        schedule.run_pending()
        time.sleep(1)


# 전역변수 설정 - 변경 가능

# 크롬 제어를 위한 웹드라이버 설정 (웹드라이버가 설치된 경로)
driver_path = "/Users/sujikang/Desktop/chromedriver"
driver = get_driver(driver_path)

# job 수행 주기 설정(단위: 초) (ex. 60*5 => 5분)
schedule_cycle = 10

# 예약 하려는 웹 페이지 주소 설정
#   - 아루히 lunch = 'https://booking.naver.com/booking/6/bizes/223362/items/3012318'
#   - 아루히 dinner = 'https://booking.naver.com/booking/6/bizes/223362/items/3020244'
#   - cf. 아루히랑 비슷한 페이지 참고 (워킹 온더 클라우드) url  = 'https://booking.naver.com/booking/6/bizes/83854/items/3237361?area=plt'
url = "https://booking.naver.com/booking/6/bizes/223362/items/3012318"

# 예약 인원 설정
people_count = 2

# 예약 성공 여부 판단 변수
is_reservation_success = False

# 메인 로직 실행
main(schedule_cycle, url, people_count)