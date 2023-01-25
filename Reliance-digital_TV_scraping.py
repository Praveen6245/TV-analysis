import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import xlsxwriter

def main():
    parent_link='https://www.reliancedigital.in/televisions/c/S101812?searchQuery=:relevance:availability:Exclude%20out%20of%20Stock'
    start=time.time()
    Pages=generate_pages(parent_link)
    products_detailed_links=[]
    print('Getting products from all pages😕.....')
    for i in range(len(Pages)):
        products_detailed_links.append(get_products_links(Pages[i]))
        print('TVs available in page',i+1,'are:',len(products_detailed_links[i]))
    TVs=[]
    for page in products_detailed_links:
        for product in page:
            TVs.append(product)
    print('Yup😃 no.of TVs gathered:-',len(TVs))
    final_result = []
    TV_details=dict()
    c=1
    print('Getting TV details!!!😤🤯')
    for i in TVs:
        TV_details=get_product_details(i)
        #print(c,TV_details)
        final_result.append(TV_details)
        # if c==5:
        #   break
        # c+=1
    print('Details ready😎')
    end=time.time()
    #Calculating time taken
    print('Scraped in:',round(end-start,2),'sec')
    #print(final_result)
    #Writing to excel file
    pd_writer=pd.DataFrame(final_result)
    #writer=pd.ExcelWriter('TV_scraping_output.xlsx',engine='xlsxwriter')
    pd_writer.to_excel('RD_TV_scraping_output.xlsx',sheet_name='Reliance-digital_scrape_results',index=False)
def generate_pages(parent_link)->list:
    print('Generating pages🤔...')
    page_links=[]
    soup = BeautifulSoup(requests.get(parent_link).content, 'lxml')
    total_no_of_products=int(soup.find('div',class_='pl__headline').find('p').text.split()[-2])
    products_per_page=len(soup.find_all('div',class_='sp grid'))
    for i in range(int(total_no_of_products/products_per_page)+1):
        page_links.append(parent_link+'&page='+str(i))
    print('No.of pages available :-',len(page_links))
    return page_links
def get_products_links(page_link)->list:
    child_soup=BeautifulSoup(requests.get(page_link).content,'lxml')
    products_links=[]
    page_soup=child_soup.find_all('div',class_='sp grid')
    for i in range(len(page_soup)):
        products_links.append('https://www.reliancedigital.in'+page_soup[i].find('a',{'attr-tag':'anchor'}).get('href'))
    return products_links
def get_product_details(proucts_detailed_link)->dict:
    TV=dict()
    try:
        soup = BeautifulSoup(requests.get(proucts_detailed_link).content, 'lxml')
    except requests.exceptions.ConnectionError as e:
        time.sleep(5)
    specification=soup.find_all('div',class_='pdp__specification-row')
    if soup.find('h1',class_='pdp__title') is not None:
        TV['Product Name']=soup.find('h1',class_='pdp__title').text
    else:
        pass
    if soup.find('span',class_='pdp__offerPrice') is not None:
        TV['Price']=soup.find('span',class_='pdp__offerPrice').text
    else:
        pass
    if soup.find('span',class_='TextWeb__Text-sc-1cyx778-0 jSjoSJ Block-sc-u1lygz-0 feHVTb') is not None:
        TV['Ratings per 5★']=soup.find('span',class_='TextWeb__Text-sc-1cyx778-0 jSjoSJ Block-sc-u1lygz-0 feHVTb').text.split('/')[0]
    else:
        pass
    for i in range(1,len(specification)):
        criteria=specification[i].find('div',class_="pdp__tab-info__list__name blk__sm__6 blk__xs__6")
        if criteria is not None:
            if(criteria.text.strip()=='Screen Resolution'):
                TV['Resolution'] = specification[i].find('div',class_="pdp__tab-info__list__value blk__sm__6 blk__xs__6").text.strip()
            elif(criteria.text.strip()=='Rated Speaker Output Power (RMS)'):
                TV['Sound Output'] = specification[i].find('div',class_="pdp__tab-info__list__value blk__sm__6 blk__xs__6").text.strip()
            elif(criteria.text.strip()=='Refresh Rate'):
                TV['Refresh Rate'] = specification[i].find('div',class_="pdp__tab-info__list__value blk__sm__6 blk__xs__6").text.strip()
            elif(criteria.text.strip()=='Brand'):
                TV['Company']=specification[i].find('div',class_="pdp__tab-info__list__value blk__sm__6 blk__xs__6").text.strip()
            elif(criteria.text.strip()=='TV Operating System'):
                TV['OS']=specification[i].find('div',class_="pdp__tab-info__list__value blk__sm__6 blk__xs__6").text.strip()
            elif(criteria.text.strip()=='Preloaded Apps'):
                TV['Supported OTT']=specification[i].find('div',class_="pdp__tab-info__list__value blk__sm__6 blk__xs__6").text.strip()
            else:
                pass
        else:
            pass
    return TV

if __name__=='__main__':
    main()