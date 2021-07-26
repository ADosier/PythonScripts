# Knowledgebase Builder
  - This builder is an exercise in harvesting relevant text from articles around the web to use in further natural language processing projects. 
  
  - WebCrawler.py
      - This web crawler scrapes URLs from a starting URL that pertain to some topic. The text from each of the URLs found are scraped and collected into individual files. They are then processed to remove unwanted characters and saved as binary .pickle files. The top most frequent terms are collected as each file is processed and a separate file is made to hold the top 40 most relevant terms.
    
  - KnowledgeBaseBuilder.py
      - After manually selecting the top 10 terms from the top 40 terms collected from the previous script this script creates a knowledge base from the other files in the same directory. The knowledge base is a simple dictionary where the keys are the top 10 terms and the values are sentences from one of the several cleaned text files in the directory. What is left is a dictionary of sentences that contain one of the top 10 terms related to the topic so you end up with data pertaining to your topic. 
      - This does not come without its flaws though. The URLs that are scraped could have a lot of irrelevant data since it is just using the links collected off of one starting spot so the end result isn't ideal. This will work much better if the URLs are manually put into the URL file prior to scraping. Alternatively the web crawling could be optimized to prevent bad links from ending up in the web scraping process. As the saying goes garbage in, garbage out.

# webpTOjpeg
  - This script was just something I made because I found a website that contained a lot of profile pictures that I wanted to use elsewhere. I decided to create my own python script since it looked like a quick and easy way to practice. If you have a lot of .webp images in a directory and run this script directly in the same folder, it will convert all the .webp images into .jpeg
