import xlsxwriter
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
def main():
    parent_link='https://www.flipkart.com/search?q=tv&p%5B%5D=facets.smart_tv%255B%255D%3DYes&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock'
    start=time.time()
    Pages=get_page_links(parent_link)
    products_detailed_links=[]
    print('Getting products from all pages😕.....')
    for i in range(len(Pages)):
        products_detailed_links.append(get_products_links(Pages[i]))
        #print('Products in',Pages[i],'are:',len(products_detailed_links[i]))
    #print(products_detailed_links)
    TVs=[]
    for page in products_detailed_links:
        for product in page:
            TVs.append(product)
    print('Yup😃 no.of TVs gathered:-',len(TVs))
    #print(TVs)
    final_result = []
    TV_details=dict()
    c=1
    print('Getting TV details!!!😤🤯')
    for i in TVs:
        TV_details=get_product_details(i)
        #print(c,TV_details)
        final_result.append(TV_details)
        # if c==2:
        #   break
        c+=1
    print('Completed😌!!!Details ready😎')
    end=time.time()
    #Calculating time taken
    print('Scraped in:',round(end-start,2),'sec')
    #print(final_result)
    #Writing to excel file
    pd_writer=pd.DataFrame(final_result)
    pd_writer.to_excel('FK_TV_scraping_output.xlsx',sheet_name='Flipkart_scrape_results',index=False)
def get_page_links(parent_link)->list:
    print('Generating pages🤔...')
    soup = BeautifulSoup(requests.get(parent_link).content, 'html.parser')
    page_links=[]
    no_of_pages=int(soup.find('div',class_='_2MImiq').find('span').text.split()[-1].strip())
    pages=soup.find('a',class_='_1LKTO3').get('href')[:-1]
    for i in range(1,no_of_pages+1):
        page_links.append(parent_link+pages+str(i))
    print('Collected all pages😀',len(page_links))
    return page_links
def get_products_links(page_link)->list:
    product_soup=BeautifulSoup(requests.get(page_link).content,'html.parser')
    product_links=[]
    for i in range(len(product_soup.find_all('a',class_='_1fQZEK'))):
        product_links.append('https://www.flipkart.com'+product_soup.find_all('a',class_='_1fQZEK')[i].get('href'))
    return product_links
def get_product_details(proucts_detailed_link)->dict:
    TV=dict()
    try:
        soup = BeautifulSoup(requests.get(proucts_detailed_link).content, 'html.parser')
    except requests.exceptions.ConnectionError as e:
        time.sleep(5)
    if(soup.find('span',class_='B_NuCI') is None):
        TV['Product Name'] = 'N/A'
    else:
        TV['Product Name']=soup.find('span',class_='B_NuCI').text
    if(soup.find('div',class_='_30jeq3 _16Jk6d') is None):
        TV['Price'] = 'N/A'
    else:
        TV['Price']=soup.find('div',class_='_30jeq3 _16Jk6d').text
    if(soup.find('div',class_='_3LWZlK') is None):
        TV['Ratings per 5★'] = 'N/A'
    else:
        TV['Ratings per 5★'] = soup.find('div',class_='_3LWZlK').text
    if(soup.find('span',class_='_2_R_DZ') is None):
        TV['No.of ratings'] = 'N/A'
    else:
        TV['No.of ratings'] =soup.find('span',class_='_2_R_DZ').text.split('&')[0].strip().split(' ')[0].strip()
    for i in (soup.find_all('li',class_='_21Ahn-')):
        try:
            TV[i.text.split(':')[0]]=i.text.split(':')[1].strip(' ')
        except:
            pass
    specification=soup.find_all('tr',class_='_1s_Smc row')
    for i in range(1,len(specification)):
        criteria=specification[i].find('td',class_="_1hKmbr col col-3-12")
        if criteria is not None:
            if(criteria.text.strip()=='Launch Year'):
                TV['Launch year'] = specification[i].find('td',class_="URwL2w col col-9-12").text.strip()
            elif(criteria.text.strip()=='Wall Mount Included'):
                TV['Wall Mount Included'] = specification[i].find('td',class_="URwL2w col col-9-12").text.strip()
            elif(criteria.text.strip()=='Model Name'):
                TV['Model Name'] = specification[i].find('td',class_="URwL2w col col-9-12").text.strip()
            elif(criteria.text.strip()=='Ram Capacity'):
                TV['Ram Capacity']=specification[i].find('td',class_="URwL2w col col-9-12").text.strip()
            elif(criteria.text.strip()=='View Angle'):
                TV['View Angle']=specification[i].find('td',class_="URwL2w col col-9-12").text.strip()
            elif(criteria.text.strip()=='Storage Memory'):
                TV['Storage Memory']=specification[i].find('td',class_="URwL2w col col-9-12").text.strip()
            else:
                pass
        else:
            pass
        #print(criteria)
    return TV

if __name__=='__main__':
    main()