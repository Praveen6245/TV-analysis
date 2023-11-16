import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

def main():
    parent_link = 'https://www.flipkart.com/thomson-alpha-80-cm-32-inch-hd-ready-led-smart-linux-tv-30-w-sound-output-bezel-less-design/product-reviews/itm0e90bcdadb9c9?pid=TVSGEMQV7R4CMTGA&lid=LSTTVSGEMQV7R4CMTGAODWDFI&marketplace=FLIPKART'
    start = time.time()
    pages = get_page_links(parent_link)

    # Create lists to store data for each attribute using list comprehension
    attributes = ['Reviewer', 'Rating from reviewer (out of 5)', 'Review_summary', 'Review', 'Review_timeline', 'Likes', 'Dislikes']
    data = {attr: [] for attr in attributes}

    # Page counter
    # c = 0
    for page in pages:
        print('Gathering review details from Page', page)
        page_data = get_review_details(page)

        # Append data to respective lists
        for attr in attributes:
            data[attr].extend(page_data[attr])

        # c += 1
        # if c == 10:
        #     break

        time.sleep(5)

    # Create DataFrame from dictionary
    df = pd.DataFrame(data)

    # Write DataFrame to CSV
    write_to_csv(df, 'Customer_reviews_scraping_output.csv')

    end = time.time()
    print('Review data scraped in:', round(end - start, 2), 'sec')

def get_page_links(parent_link):
    print('Generating pages...')
    soup = BeautifulSoup(requests.get(parent_link).content, 'lxml')
    no_of_pages = int(soup.find('div', class_='_2MImiq _1Qnn1K').find('span').get_text().split()[-1])
    page_links = [parent_link + '&page=' + str(i) for i in range(1, no_of_pages + 1)]
    print('Collected all pages', len(page_links))
    return page_links

def get_review_details(page_link):
    data = {
        'Reviewer': [],
        'Rating from reviewer (out of 5)': [],
        'Review_summary': [],
        'Review': [],
        'Review_timeline': [],
        'Likes': [],
        'Dislikes': []
    }

    try:
        review_soup = BeautifulSoup(requests.get(page_link).content, 'lxml')
        review_block = review_soup.findAll('div', class_='_27M-vq')
    except requests.exceptions.ConnectionError as e:
        time.sleep(5)

    for review_item in review_block:
        try:
            reviewer = review_item.find('div', class_='col _2wzgFH K0kLPL').find('p', class_='_2sc7ZR _2V5EHH').get_text()
        except AttributeError:
            reviewer = 'N/A'
        
        if(review_item.find('div', class_='_3LWZlK _1BLPMq') is not None):
            ratings_in_review=int(review_item.find('div', class_='_3LWZlK _1BLPMq').get_text())
        elif(review_item.find('div', class_='_3LWZlK _1rdVr6 _1BLPMq') is not None):
            ratings_in_review=review_item.find('div', class_='_3LWZlK _1rdVr6 _1BLPMq').get_text()
        else:
            ratings_in_review='N/A'
    
        try:
            review_summary = review_item.find('div', class_='col _2wzgFH K0kLPL').find('p', class_='_2-N8zT').get_text()
        except AttributeError:
            review_summary = 'N/A'
        
        try:
            review = review_item.find('div', class_='col _2wzgFH K0kLPL').find('div', class_='t-ZTKy').find('div').find('div', class_='').get_text()
        except AttributeError:
            review = 'N/A'
        
        try:
            review_timeline = review_item.find('div', class_='row _3n8db9').findAll('p', class_='_2sc7ZR')[-1].get_text()
        except AttributeError:
            review_timeline = 'N/A'
        
        try:
            likes = int(review_item.find('div', class_='col _2wzgFH K0kLPL').find('div', class_='_1LmwT9').find('span', class_='_3c3Px5').get_text())
        except AttributeError:
            likes = 'N/A'
        
        try:
            dislikes = int(review_item.find('div', class_='col _2wzgFH K0kLPL').find('div', class_='_1LmwT9 pkR4jH').find('span', class_='_3c3Px5').get_text())
        except AttributeError:
            dislikes = 'N/A'
        
        data['Reviewer'].append(reviewer)
        data['Rating from reviewer (out of 5)'].append(ratings_in_review)
        data['Review_summary'].append(review_summary)
        data['Review'].append(review)
        data['Review_timeline'].append(review_timeline)
        data['Likes'].append(likes)
        data['Dislikes'].append(dislikes)

    return data

def write_to_csv(dataframe, file_name):
    dataframe.to_csv(file_name, index=False)
    print(f'Data written to {file_name}')

if __name__ == '__main__':
    main()
