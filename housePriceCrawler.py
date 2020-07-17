import time
import random
import csv

import requests #網頁資源(URL)擷取套件
from bs4 import BeautifulSoup #HTML剖析套件


def countItem(pages, url):
    # 直接抓第一頁的搜尋結果
    itemURL = url + "1" +".html"
    result = requests.get(itemURL)
    soup = BeautifulSoup(result.text,'html.parser')
    itemText = soup.find('div', attrs={'class':'communityTabSmall'}).text
    countStr = ""
    # 前面是"共有"
    for c in itemText[2:]:
        if c.isdigit():
            countStr += c
        else:
            break
    # print(int(countStr))
    return int(countStr)

    # 藉由爬每一頁計算有多少個結果
    # count = 0
    # itemURL = ""
    # for i in range(1, pages+1):
    #     itemURL = url + str(i) +".html" #https://www.sinyi.com.tw/communitylist/Taipei-city/uniprice-desc/
    #     result = requests.get(itemURL)
    #     soup = BeautifulSoup(result.text,'html.parser')
    #     count += len(soup.find_all('div', attrs={'class':'LongInfoCardBody row'}))
    # return count

def houseSize(sizeList):
    """
    處理屋況的函數，主要將字串排除，並將有缺漏的資料填入None
    包含四個欄位：坪數、主＋陽(主建物)、屋齡、樓層
    坪數可能為建坪或建物面積
    此爬蟲未抓取主建物坪數與建案名稱
    """
    returnList = []
    if len(sizeList) > 4:
        sizeList = sizeList[:4]
    if '主建物' in sizeList[1]:
        del sizeList[1]
    if '建坪' in sizeList[0]:
        returnList.append(float(sizeList[0].replace('建坪', '')))
    elif '建物面積(坪)' in sizeList[0]:
        returnList.append(float(sizeList[0].replace('建物面積(坪)', '')))
    
    index = 1
    while index < len(sizeList):
        if '主+陽' in sizeList[index] and len(returnList)==1:
            returnList.append(float(sizeList[index].replace('主+陽', '')))
            index += 1
        elif len(returnList)==1:
            returnList.append(None)
        if '年' in sizeList[index] and len(returnList)==2:
            returnList.append(float(sizeList[index].replace('年', '')))
            index += 1
        elif len(returnList)==2:
            returnList.append(None)
        if '樓' in sizeList[index] and len(returnList)==3:
            returnList.append(sizeList[index].replace('樓', ''))
            index += 1
        elif len(returnList)==3:
            returnList.append(None)
    return returnList


def housePattern(patternList):
    """
    處理房屋格局的函數，主要將字串排除，並合計有加蓋之格局數量
    包含五個欄位：房、廳、衛、室、是否為加蓋
    第五個欄位為布林值
    """
    resultList = []
    resultList.append(int(patternList[0].replace('房', '')))
    resultList.append(int(patternList[1].replace('廳', '')))
    resultList.append(float(patternList[2].replace('衛', '')))
    resultList.append(int(patternList[3].replace('室', '')))
    resultList.append(0)
    
    if len(patternList) > 4:
        resultList[0] += int(patternList[5].replace('房', ''))
        resultList[1] += int(patternList[6].replace('廳', ''))
        resultList[2] += float(patternList[7].replace('衛', ''))
        resultList[3] += int(patternList[8].replace('室', ''))
        resultList[4] = 1 
        
    return resultList

def houseType(typeStr):
    """
    處理屋型的函數，主要將字串以“、”切割開來
    並將屋型以布林值存放，若為該屋型，布林值為1
    此網頁將屋型分為12大類
    """
    houseTypes ={
        '電梯多樓層': 0, 
        '多樓層': 0, 
        '透天厝': 0, 
        '新成屋': 0, 
        '電梯大樓': 0, 
        '電梯其他': 0, 
        '預售': 0, 
        '公寓': 0, 
        '其他': 0, 
        '成屋': 0, 
        '電梯透天厝': 0, 
        '電梯華廈': 0
    }
    
    types = typeStr.split('、')
    for item in types:
        if item in houseTypes:
            houseTypes[item] = 1
    typeList = []
    for t in houseTypes:
        typeList.append(houseTypes[t])
    return typeList


def houseFunction(functionList):
    """
    處理機能的函數，主要將字串對應至布林值中
    若為該房屋有機能，布林值為1
    但網頁中可能為空值，故需另外處理
    """
    houseFunctions = {
        # '社區':""
        '近捷運':0, 
        '新上架':0, 
        '店長推薦':0, 
        '低總價':0, 
        '近學校':0, 
        '近市場':0, 
        '近公園':0, 
        '租賃中':0
    }
    resultList = []
    if len(functionList) == 0:
        for f in houseFunctions:
            resultList.append(houseFunctions[f])
        return resultList
    else:
        for item in functionList:
            if item in houseFunctions:
                houseFunctions[item] = 1
        for f in houseFunctions:
            resultList.append(houseFunctions[f])
    return resultList

def findAllPageNumber(cityName):
    #最後一頁
    
    url = "https://www.sinyi.com.tw/communitylist/"
    city = cityName
    condition = "/uniprice-desc/"
    itemURL = url + city + condition + "1" +".html"
    result = requests.get(itemURL)
    soup = BeautifulSoup(result.text,'html.parser')
    lastPage = soup.find_all("li", {"class": "pageClassName"})[-1].text
    print('The last page is ' + lastPage)
    return int(lastPage)

if __name__ == '__main__':
    
    # print('If you want to crawl all page data, input number -1.')
    # pages = int(input('Input how much pages you want to crawl：'))

    # cityList = ["Taipei-city", "NewTaipei-city", "Hsinchu-city", 
    # "Hsinchu-county", "Taoyuan-city", "Taichung-city", "Changhua-county",
    # "Tainan-city", "Kaohsiung-city"]

    cityList = ["NewTaipei-city", "Hsinchu-city", 
    "Hsinchu-county", "Taoyuan-city", "Taichung-city", "Changhua-county",
    "Tainan-city", "Kaohsiung-city"]

    origTargetURL = "https://www.sinyi.com.tw/communitylist/"
    condition = "/uniprice-desc/"

    for city_name in cityList:

        resultList = []

        targetURL = origTargetURL + city_name + condition

        pages = findAllPageNumber(city_name)
        
        total_items = 0
        
        start = time.time()
        print('Start parsing ' + city_name + " house price")
        
        itemCounter = 0
        total_items = countItem(pages,targetURL)

        print('共%d項房屋資訊' % total_items)
        
        #地址、屋況(houseSize)、格局(housePattern)、屋型(houseType)、機能(houseFunction)、房價(萬)
        for i in range(1, pages+1):
            itemURL = targetURL + str(i) +".html"
            result = requests.get(itemURL)
            soup = BeautifulSoup(result.text,'html.parser')
            
            itemsParent = soup.find('div', attrs={'id':'communitySearchListContent'})
            items = itemsParent.find_all('a')
            for item in items:
                houseInfo = []
                address = item.find('div', attrs={'class', 'LongInfoCard_Type_Address'}).text.strip().replace(',', '//')   #地址
                footageItem = item.select(".LongInfoCard_Type_HouseInfo > span:nth-child(3)")   #坪數
                if len(footageItem) == 0:
                    footage = "None"
                else:
                    footageText = footageItem[0].text
                    if "坪" in footageText:
                        footRange = footageText[:-1].split('~')
                        footMin, footMax = int(float(footRange[0])), int(float(footRange[1]))
                        footage = str(int((footMin + footMax) / 2))
                    else:
                        footage = "None"
                
                priceItem = item.select(".LongInfoCard_Type_Right > div:nth-child(2) > span:nth-child(1)")   #單坪房價
                if len(priceItem) == 0:
                    price = "None"
                else:
                    price = priceItem[0].text

                community = item.find('div', attrs={'class':'LongInfoCard_Type_Name'}).text.strip()   #社區名

                numHouseItem = item.find('div', attrs={'class':'LongInfoCard_Type_HouseInfo'})   #戶數
                numHouse = numHouseItem.findChildren("span", recursive=False)[-1].text[:-1]
                beenYear = numHouseItem.findChildren("span", recursive=False)[0].text[:-1]   #屋齡
                communityHref = "https://www.sinyi.com.tw" + item['href']
                communityResult = requests.get(communityHref)
                communitySoup = BeautifulSoup(communityResult.text,'html.parser')
                try:
                    districtName = communitySoup.select(".trade-obj-card-web > div:nth-child(2)")[0].text[3:6]
                except:
                    districtName = "None"

                houseInfo.append(city_name)
                houseInfo.append(districtName)
                houseInfo.append(address)
                houseInfo.append(community)
                houseInfo.append(beenYear)
                houseInfo.append(numHouse)
                houseInfo.append(price)
                houseInfo.append(footage)

            #     houseInfo += houseSize(item.select('.detail_line2')[0].text.strip().split())                   #屋況
            #     houseInfo += housePattern(item.select('.detail_line2')[1].text.strip().split())                #格局
            #     houseInfo += houseType(item.select('.detail_line1 span:nth-of-type(2)')[0].text.strip())       #屋型
                
        #         if len(item.select('.detail_tagGroup')) > 0:
        #             funConvert = []
        #             for f in range(0,len(item.select('div.detail_tagGroup > div.detail_tag'))):
        #                 funConvert.append(item.select('div.detail_tagGroup > div.detail_tag')[f].text)          #機能                                                      
        #         else:
        #             funConvert = []
        #         houseInfo += houseFunction(funConvert)
                
        #         houseInfo.append(float(item.select('.price_new')[0].text.strip().split()[0].replace(',','')))  #房價(萬)
                resultList.append(houseInfo)
                
                itemCounter += 1
                #print(items)
                if itemCounter % 20 == 0:
                    print('Crawler: {:.2%}'.format(itemCounter / total_items)) 
        
        #with open(fileName, 'wb') as f:
        #    f.write(content.encode('utf8'))
        
        resultFile = "housePrice" + city_name + ".csv"


        with open(resultFile, 'w', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',' ,quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for result in resultList:
                filewriter.writerow(result)
    
    print('花費: %f 秒' % (time.time() - start))
    print('----------END----------')
    
    print()
    print()
    print('前10項房屋資訊：')
    for result in resultList[:10]:
        print(result)