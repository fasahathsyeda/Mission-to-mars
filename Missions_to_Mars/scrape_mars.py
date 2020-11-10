# Dependencies
import time
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import re




def scrape_all_content():
    browser = Browser("chrome",executable_path="chromedriver.exe", headless=False)

    news_title, news_para, news_date=mars_news(browser)
    featured_image_url=featured_image(browser)
    mars_table=mars_fact()
    mars_hemis=mars_hemisphere(browser)


    # Create a dictionary for all of the scraped data
    mars_data = {
        "news_title":news_title,
        "news_paragraph":news_para,
        "news_date":news_date,
        "featured_image_url":featured_image_url,
        "mars_table":mars_table,
        "mars_hemis":mars_hemis
    }

    browser.quit()

    return mars_data

def mars_news(browser):

    nasa_news_url='https://mars.nasa.gov/news/'
    browser.visit(nasa_news_url)
    # Scrape page using Beautifulsoup
    html = browser.html
    nasa_soup = BeautifulSoup(html,'html.parser')
    try:

        # save the most recent article, title and date
        article = nasa_soup.find("div", class_="list_text")
        news_title = article.find("div", class_="content_title").text
        news_para = article.find("div", class_="article_teaser_body").text
        news_date = article.find("div", class_="list_date").text
        

    except AttributeError:
        return None,None,None

    return news_title,news_para,news_date

def featured_image(browser):
    jpl_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    html = browser.html

    jpl_soup = BeautifulSoup(html,'html.parser')
    try:
        images=jpl_soup.find('article',attrs={'class':'carousel_item'})
        images.attrs
        featured_img_style=images['style']
        featured_img_src=re.findall(r"'(.*?)'",featured_img_style)
        featured_img_url='https://www.jpl.nasa.gov'+featured_img_src[0]
    except AttributeError:
        return None
    
    return featured_img_url

def mars_fact():
    mars_facts_url='https://space-facts.com/mars/'
    try:
        facts_df = pd.read_html(mars_facts_url)[0]
        facts_df.columns=['Description','Mars']
        facts_df.set_index('Description',inplace=True)
        mars_table=facts_df.to_html("table.html")
        mars_table=facts_df.to_html(classes = "table table-hover table-dark table-box")
    except AttributeError:
        return None

    return mars_table

def mars_hemisphere(browser):
    hmsphr_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hmsphr_url)
    hmsphr_html = browser.html
    hmsphr_soup = BeautifulSoup(hmsphr_html,'html.parser')
    try:
        mars_hemis=[]
        # loop through the four tags and load the data to the dictionary

        for i in range (4):
            time.sleep(5)
            images = browser.find_by_tag('h3')
            print(images)
            images[i].click()
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            partial_url = soup.find("img", class_="wide-image")["src"]
            img_title = soup.find("h2",class_="title").text
            img_url = 'https://astrogeology.usgs.gov'+ partial_url
            dictionary={"title":img_title,"img_url":img_url}
            mars_hemis.append(dictionary)
            browser.back()
    except AttributeError:
        return None

    return mars_hemis
    

    




if __name__=='__name__':

    print(scrape_all_content())
