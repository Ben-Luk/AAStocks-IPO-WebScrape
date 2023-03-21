#!/user/bin/env python
# coding:utf-8
import pandas as pd
import selenium
from selenium import webdriver

start_link = 'http://www.aastocks.com/tc/stocks/market/ipo/listedipo.aspx'
chromedriver_path = r'C:\Users\benjamin.luk\.spyder-py3\IPO_analysis\chromedriver'
output_path = r"C:\Users\benjamin.luk\.spyder-py3\IPO_analysis\data\ipo_list.csv"


def get_ipo_info(ds):
    cols = 9
    stocks = ds.find_elements('xpath', '//a[@class="cls"]')
    infos = ds.find_elements('xpath', '//td[@class="txt_r cls"]')
    long_line = [element.text for element in infos]
    sep_list = [[stock_num.text] + long_line[i:i+cols] for stock_num, i in zip(stocks ,range(0, len(long_line), cols))]   
    page_df = pd.DataFrame(sep_list, columns = ['code', 'listing_date', 'lot_size', 'mktcap', 'offer_price', 'listing_price', 'oversub_rate', 'app_lots_for_one_lot', 'one_lot_success_rate', 'last'])
    print(page_df)
    return page_df

def crawl_hk_ipo():
    dataframe = pd.DataFrame()
    ds = webdriver.Chrome(executable_path=chromedriver_path)
    ds.implicitly_wait(10)
    ds.set_page_load_timeout(10)
    crawl_finish = 0
    ds.get(start_link)
    
    while crawl_finish == 0:
        cur_page_num = str(ds.find_element('xpath', '//span[@class="current"]').text)
        cur_page_num = int(cur_page_num)
        print('Crawling page ' + str(cur_page_num))
        dataframe = pd.concat([dataframe, get_ipo_info(ds)], axis = 0)
       
        try:
            cur_page_num += 1
            next_page_button = ds.find_element('xpath', '//div[@class="p_last"]')
            next_page_button.click()
        except Exception as e:
            #print str(e)
            print('Crawling Finished!')
            crawl_finish = 1
    
    return  dataframe

if __name__ == '__main__':
    df = crawl_hk_ipo()
    df.to_csv(output_path)
