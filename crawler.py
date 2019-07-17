# coding: utf-8

import urllib
from bs4 import BeautifulSoup
from csv import writer
import numpy as np

def colist(url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', write = False):
    request = urllib.request.Request(url)
    request.get_method = lambda: 'GET'
    response_body = urllib.request.urlopen(request).read().decode('euc-kr')
    soup=BeautifulSoup(response_body,"html")
    temp = soup.find_all('tr')
    colist = {}
    for i in range(1,len(temp)):
        coname = temp[i].find_all('td')[0].get_text()
        code = temp[i].find_all('td')[1].get_text()
        colist[coname] = code
        
    if write == True:
        w = writer(open("colist.csv","w"))
        for key, val in colist.items():
            w.writerow([key,val])
    return colist



# X변수
def Xcrawler(co_list,co_name='삼성전기', pages = 5):
    """
    Xcrawler is crawling price data from naver finance page
    colist : dict of stock
    co_name : compnay you want
    """
    code = co_list[co_name]
    date = []
    endp = []
    maxp = []
    minp = []
    mass = []
    page = 1
    while page <= pages:
        print((page-1)/pages*100)
        url=f'https://finance.naver.com/item/sise_day.nhn?code={code}&page={page}'
        request = urllib.request.Request(url)
        response_body = urllib.request.urlopen(request).read().decode('euc-kr')
        soup=BeautifulSoup(response_body,"html")
        temp = soup.find_all('span', attrs={'class': 'tah p11'})
        date_temp = soup.find_all('span', attrs={'class': 'tah p10 gray03'})
        i = 0 
        for i in range(1,len(date_temp)):
            date.append(date_temp[i].get_text())
            endp.append(temp[5*i+2].get_text())
            maxp.append(temp[5*i+3].get_text())
            mass.append(temp[5*i+4].get_text())
        page +=1
    print(100.0)
    return date, endp, maxp, mass
