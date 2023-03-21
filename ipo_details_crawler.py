import selenium
from selenium import webdriver
import pandas as pd


chromedriver_path = r'C:\Users\benjamin.luk\.spyder-py3\IPO_analysis\chromedriver'


def crawl_one(ds, code):
    company_info_link = 'http://www.aastocks.com/tc/stocks/market/ipo/upcomingipo/company-info?symbol=' + code.strip(".HK") + '&s=3&o=1#info'
    ipo_info_link = 'http://www.aastocks.com/tc/stocks/market/ipo/upcomingipo/ipo-info?symbol=' + code.strip(".HK") + "&s=3&o=1#info"
    ds.get(company_info_link)
    company_info = []
    for i in [2, 3, 4, 5]:
        company_info.append(ds.find_element("xpath", f'''//*[@id="UCCompanyInfo"]/div[1]/table/tbody/tr[{i}]/td[2]''').text)
    print(company_info)
    ds.get(ipo_info_link)
    ipo_info = []
    for j in [6, 7, 9, 10]:
        ipo_info.append(ds.find_element("xpath", f'''//*[@id="UCIPOInfo"]/div[1]/table/tbody/tr[{j}]/td[2]''').text)
    print(ipo_info)

    return company_info + ipo_info


def crawl_all(ds, codes):
    for code in codes:
        print( 'Crawling ' + str(code))
        fail_count = 0
        while fail_count <= 5:
            try:
                output = crawl_one(ds, code)
                print(output)
                return
            except Exception as e:
                print( e)
                print( 'Try ' + str(fail_count+1) + ' Time')
                continue
    


if __name__ == '__main__':
    codes = pd.read_csv('data/ipo_list.csv')['code']
    ds = webdriver.Chrome(executable_path=chromedriver_path)
    ds.implicitly_wait(10)
    ds.set_page_load_timeout(10)
    crawl_all(ds, codes)
        
