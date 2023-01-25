Overview:

This scraping is done through fuctions/modules each having specific purpose. The flow of scraping is as follows:
----------------------------------------------------------------------------------------------------------------------
					
					Source webpage
								↓
					→→→ List of individual webpages
					↑			↓
					↑	List of products
					↑			↓
					←←← Product page
					
----------------------------------------------------------------------------------------------------------------------
1) From the webiste extract ---> no.of pages of products and links for individual pages.
2) Next, from each page extract --> all links of products in that single page.
3) From each product link, extract below details---> Product Name
													 Price
													 Ratings per 5★
													 No.of ratings
													 Resolution
													 Sound Output
													 Refresh Rate
													 Model Name	
													 Launch year
													 Wall Mount Included
													 View Angle
													 Supported Apps
													 Operating System
													 Ram Capacity
													 Storage Memory

4) Write these details into a spreadesheet format(Excel sheet)

Questions to be analysed:

1) How many different brands, different types of OS, different sizes are available?
2) What is the average _______ of ______ TVs?
	---> Price, Company
	---> Price, Display sizes
	---> Price, Ratings
	---> Ratings, OS
	---> Ratings, Company
3) Company wise average ratings for all of their TVs
4) For flipkart dataset, list the compoanies based on their customer_score, where customer_score=Ratings per 5★ x No.of ratings
5) For reliance-digital dataset, list the companies along with the average number of OTTs supported and commonly supported OTTs of among their products
6) For an input money and display size, return the list of TVs with:
	(a) max number of OTTs(for reliance-digital dataset) &
	(b) most customer_score