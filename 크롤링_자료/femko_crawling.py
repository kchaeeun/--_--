import dload
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

# 웹드라이버 실행
driver = webdriver.Chrome()  # Chrome 드라이버 경로 설정 필요
base_url = "https://www.fmkorea.com/index.php?mid=lol&sort_index=pop&order_type=desc&listStyle=webzine&page={}"
time.sleep(5)  # 페이지 로딩을 위해 충분한 시간 기다리기

titles_list = []

for page in range(1,501):
    url = base_url.format(page)
    driver.get(url)
    time.sleep(5)  
    
    # 현재 페이지의 HTML 가져오기
    page_source = driver.page_source

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(page_source, 'html.parser')

    # 'a.hotdeal_var8' 클래스를 가진 <a> 태그를 선택
    td_tags = soup.find_all('a', class_='hotdeal_var8')

    # # 각 <a> 태그에서 텍스트 부분만 추출
    for tag in td_tags:
        text = ''.join(tag.find_all(string=True, recursive=False)).strip()  # 모든 자식 텍스트를 가져옴
        titles_list.append(text)
        print(text)

# 웹드라이버 종료
driver.quit()

df = pd.DataFrame(titles_list, columns=['Titles'])

# 엑셀 파일로 저장
excel_file = 'titles_list_500_page.xlsx'
df.to_excel(excel_file, index=False)

print(f"제목들이 {excel_file} 파일에 저장되었습니다.")
