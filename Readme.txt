Overview:

This scraping is done through fuctions/modules each having specific purpose. The flow of scraping is as follows:
----------------------------------------------------------------------------------------------------------------------
					
							Source webpage
								↓
					→→→		List of individual webpages
					↑			↓
					↑		List of products
					↑			↓
					←←← 		Product details page
					
----------------------------------------------------------------------------------------------------------------------
1) From the webiste extract ---> no.of pages and links for individual pages.
2) Next, from each page extract --> all links of products in that single page.
3) From each product link, extract below details---> Product Name,Price,Ratings per 5★,No.of ratings,Resolution,Sound Output,Refresh Rate,Model Name,Launch year,Wall Mount Included,View Angle,Supported Apps,Operating System,Ram Capacity,Storage Memory
4) Write these details into a spreadesheet format(Excel sheet)
5) Frame and extract insights from cleansed data
6) Produce appropriate visuals in Python and Power BI
