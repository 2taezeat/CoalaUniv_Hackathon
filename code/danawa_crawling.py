from selenium import webdriver
# 브라우저 조종 도구

import time
import openpyxl

wb = openpyxl.Workbook()

sheet = wb.active


driver = webdriver.Chrome('./chromedriver')
# 실제 브라우저, 브라우저 조종 권한 생김.

driver.get('http://prod.danawa.com/list/?cate=112758&15main_11_02')
# request 처럼 get 씀.

# 검색창 누르고, 치킨 치고, 엔터.
# searchbar = driver.find_element_by_css_selector('input#search-input') # html.select_one 과 같은 기능

# searchbar.send_keys('치킨') #자판에 있는 치킨을 눌러주세요.
# button = driver.find_element_by_css_selector('button.spm')
# button.click()

time.sleep(2)

# 큰 컨테이너 div.prod_main_info
# 작은 컨테이너 div.prod_main_info div.prod_info (이름과 스펙만)
# 이름 div.prod_main_info div.prod_info p.prod_name a
# 가격 div.prod_main_info div.prod_pricelist p.price_sect strong
# 가격 조건 div.prod_main_info div.prod_pricelist p.memory_sect (있는 것이 있고 없는 것이 있음)
# 애드포인트(광고) 5개 스펙 div.prod_info ul.spec_list a
# 나머지 스펙 div.prod_info dd div.spec_list a
# 다른 가격 더 보여 주기 div.prod_main_info div.prod_pricelist a.open
# 페이지 넘기기 div.number_wrap a 숫자페이지
# 페이지 넘기기 div.num_nav_wrap a

# plusbuttons = driver.find_elements_by_css_selector('div.prod_main_info div.prod_pricelist a.open')
# for plusbutton in plusbuttons:
#     plusbutton.click()

# time.sleep(2)

# stores = driver.find_elements_by_css_selector('div.prod_main_info')

# print(len(stores))
# html.select 와 동일한 기능.
# 선택자는 표준이기 때문에 바뀌는 게 없다.

# txt = stores.find_element_by_css_selector('div#txtTarget').text
# print(txt)

for page in range(1, 50):
    plusbuttons = driver.find_elements_by_css_selector('div.prod_main_info div.prod_pricelist a.open')
    for plusbutton in plusbuttons:
        plusbutton.click()

    time.sleep(1)

    stores = driver.find_elements_by_css_selector('div.prod_main_info')

    for store in stores:
        data = []
        try:
            name = store.find_element_by_css_selector('div.prod_info p.prod_name a').text
        except:
            name = '오류'

        price_list = []
        try:
            prices = store.find_elements_by_css_selector('div.prod_pricelist p.price_sect strong')
            for price in prices:
                price_list.append(price.text)
        except:
            price_list.append('오류')

        pricetag_list = []
        try:
            pricetags = store.find_elements_by_css_selector('div.prod_pricelist p.memory_sect')
            for pricetag in pricetags:
                pricetag_list.append(pricetag.text)
            if len(pricetag_list) == 0:
                pricetag_list.append(0)
        except:
            pricetag_list.append('없음')

        spec_list = []
        spec_list2 = []

        try:
            specs = store.find_elements_by_css_selector('div.prod_info dd div.spec_list')
            for spec in specs:
                spec_list.append(spec.text)
        except:
            spec_list.append('없음')
        try:
            specs2 = store.find_elements_by_css_selector('div.prod_info ul.spec_list a')
            for spec in specs2:
                spec_list2.append(spec.text)
        except:
            spec_list2.append('없음')

        print(name)
        print('옵션 조건 :', pricetag_list, '가격 :', price_list)
        spec_list_split = []
        data.append(name)

        if len(spec_list) == 0:
            print(spec_list2)
            data += spec_list2
        else:
            print(spec_list)
            spec_list_split = spec_list[0].split(' / ')
            print(spec_list_split)
            data += spec_list_split

        if len(pricetag_list) > 1:
            for n in range(len(pricetag_list)):
                print(data[:1] + [pricetag_list[n] , price_list[n]] + data[1:])
                if pricetag_list[n] != 0:
                    sheet.append(data[:1] + [pricetag_list[n] , price_list[n]] + data[1:])
        else:
            data = data[:1] + pricetag_list + price_list + data[1:]
            if pricetag_list[0] != 0:
                sheet.append(data)

        print(data)
        print()

    try:
        pagebar = driver.find_elements_by_css_selector("div.num_nav_wrap a") # 모든 태그 다 선택.
        if page % 10 != 0:
            pagebar[page % 10 +1].click()
        else:
            pagebar[10].click()
    except:
        break   # for에서 하던 도중에 많이 남았어도 끝내고 나와라.

    # pagebar[n + 1].click()    # 3번째 잇는 것이 2번째 페이지니까 list[2]
    print(page)
    print(page % 10)
    time.sleep(2)



wb.save('test3.xlsx')


# time.sleep(2)
# # 2초만 쉬어라.
#
# driver.get('http://daum.net/')

# driver.close()


