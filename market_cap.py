import os # 파일 조작
import pandas as pd # 데이터 조작
from selenium import webdriver # 웹 자동화
from selenium.webdriver.common.by import By

browser = webdriver.Chrome() # Chrome 웹 드라이버를 초기화
browser.maximize_window() # 창 최대화

# 1. 페이지 이동
url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

# 2. 조회 항목 초기화(체크 되어 있는 항목 체크 해제)
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected(): # 체크된 상태라면?
        checkbox.click() # 클릭 (체크 해제)
        
# 3. 조회 항목 설정 (원하는 항목)
# items_to_select = ['영업이익', '자산총계', '매출액']
items_to_select = ['시가', '고가', '저가']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..') # 부모 element를 찾음
    label = parent.find_element(By.TAG_NAME, 'label') # 부모 요소 안에서 '<label>' 요소를 찾음.
    # print(label.text) # 이름 확인
    
    # 위에서 찾은 라벨의 텍스트가 'item_to_select' 리스트 안에 있는지 확인.
    if label.text in items_to_select: # 현재 체크박스의 라벨이 선택하려는 항목 중 하나인지를 검사
        checkbox.click() # 체크
        
# 4. 적용하기 클릭
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()

for idx in range(1,45): # 1 이상 45 미만 페이지 반복
    
    # 사전 작업: 페이지 이동
    browser.get(url + str(idx)) # https://naver.com....&page=2
    
    # 5. 데이터 추출
    df = pd.read_html(browser.page_source)[1] # 웹페이지에서 두 번째 테이블에 해당하는 데이터프레임을 담음
    df.dropna(axis='index', how='all', inplace=True) # 행 방향으로 누락된 값을 삭제, 제거(해당 행이 모든 요소가 누락된 경우에만)
    df.dropna(axis='columns', how='all', inplace=True) # 열 방향으로 누락된 값을 삭제, 제거(해당 열이 모든 요소가 누락된 경우에만)
    if len(df) == 0: # 더 이상 가져올 데이터가 없으면?
        break

    # 6. 파일 저장
    f_name = 'sise.csv'
    if os.path.exists(f_name): # 파일이 있다면? 헤더 제외
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else: # 파일이 없다면? 헤더 포함
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f'{idx} 페이지 완료')
    
browser.quit() # 브라우저 종료
