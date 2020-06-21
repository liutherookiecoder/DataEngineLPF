"""
    Action1：汽车投诉信息采集：
    数据源：http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-1.shtml
    投诉编号，投诉品牌，投诉车系，投诉车型，问题简述，典型问题，投诉时间，投诉状态
    可以采用Python爬虫，或者第三方可视化工具
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
# 请求URL
def get_url(page_number):
    url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-'+ str(page_number+1)+ '.shtml'
    # 得到页面的内容
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(url,headers=headers,timeout=10)
    content = html.text
    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup
"""
#输出第一个 title 标签
print(soup.title)
#输出第一个 title 标签的标签名称
print(soup.title.name)
#输出第一个 title 标签的包含内容
print(soup.title.string)
"""

#投诉信息分析获取函数
def Analysis(soup):
# 找到完整的投诉信息框
    temp = soup.find('div',class_="tslb_b")
    # 创建DataFrame
    df = pd.DataFrame(columns = ['id', 'brand', 'car_model', 'car_type', 'desc', 'problem', 
    'datetime', 'status'])
    tr_list = temp.find_all('tr')
    #print(tr_list)
    for tr in tr_list:
        #提取投诉信息
        temp1 = {}
        td_list = tr.find_all('td')
        #print(td_list)
        if len(td_list)>0:
            complain_id, brand, car_model, car_type, desc, problem, datetime, status = td_list[0].text, td_list[1].text, td_list[2].text, td_list[3].text, td_list[4].text, td_list[5].text, td_list[6].text, td_list[7].text
            temp1['id'], temp1['brand'], temp1['car_model'], temp1['car_type'], temp1['desc'], temp1['problem'], temp1['datetime'], temp1['status'] = complain_id, brand, car_model, car_type, desc, problem, datetime, status
            #添加入表格中储存
            df = df.append(temp1,ignore_index = True)
    return df

#主函数：获取前total_page_number页的投诉信息并生成csv
def main(total_page_number):
    result = pd.DataFrame(columns = ['id', 'brand', 'car_model', 'car_type', 'desc', 'problem', 
    'datetime', 'status'])
    for i in range(total_page_number):
        soup = get_url(i)
        df1 = Analysis(soup)
        result = result.append(df1,sort= False)
    result.to_csv('result.csv',index = False,encoding='utf-8-sig')
    return print(result)
    
#运行主函数并获取前两页信息及生成CSV
main(2)

    
    
    



