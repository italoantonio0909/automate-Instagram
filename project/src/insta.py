from selenium import webdriver
from urllib.parse import urlparse
from decouple import config
import requests
import time
import os
import pprint
import sys


def login(*, browser):

    #Credentials
    USERNAME_INSTA = config('INSTA_USERNAME',default='username')
    PASSWORD_INSTA= config('INSTA_PASSWORD',default='12345')

    time.sleep(3)
    username_field = browser.find_elements_by_xpath("//input[@name='username']")
    password_field = browser.find_elements_by_xpath("//input[@name='password']")
    button_submit=browser.find_element_by_xpath("//button[@type='submit']")

    username_field[0].send_keys(USERNAME_INSTA)
    password_field[0].send_keys(PASSWORD_INSTA)

    time.sleep(2)
    button_submit.click()
    


def automate_follow(*, browser):
    time.sleep(5)
    my_follow_btn_xpath = "//button[contains(text(), 'Seguir')][not(contains(text(), 'Siguiendo'))]"
    follow_btns=browser.find_elements_by_xpath(my_follow_btn_xpath)
    for follow in follow_btns:
        time.sleep(2)
        try:
            follow.click()
        except:
            pass



def automate_posts(*, data, username_instagram: str):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DOWNLOAD_DIR = os.path.join(BASE_DIR, 'posts')
    DOWNLOAD_DIR_USERNAME = os.path.join(DOWNLOAD_DIR, username_instagram)
    
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    os.makedirs(DOWNLOAD_DIR_USERNAME,exist_ok=True)

    for iterator in data:
        url = iterator.get_attribute('src')
        base_url = urlparse(url).path
        base_name = os.path.basename(base_url)
        filename = os.path.join(DOWNLOAD_DIR_USERNAME, base_name)

        with requests.get(url, stream=True) as request:
            try:
                request.raise_for_status()
            except:
                continue
            with open(filename, 'wb') as file:
                for chunck in request.iter_content(chunk_size=1024):
                    if chunck:
                        file.write(chunck)



def automate_comment(*, browser, username: str):
    
    comment = f"@{username} Hey men, I'm an automation software, I'm using your profile for my neural learning"
    
    posts_elements_xpath    = "//a[contains(@href, '/p/')]"
    textarea_comment_xpath = "//textarea[contains(@placeholder, 'Añade un comentario...')]"
    button_comment_xpath = "button[type='submit']"

    post_element = browser.find_elements_by_xpath(posts_elements_xpath)

    if len(post_element) > 0:
        time.sleep(2)
        url_post=post_element[0].get_attribute('href')
        browser.get(url_post)

        time.sleep(1)
        textarea_comment = browser.find_element_by_xpath(textarea_comment_xpath)
        button_submit = browser.find_element_by_css_selector(button_comment_xpath)
        textarea_comment.send_keys(comment)
        time.sleep(2)
        button_submit.click()



def automate_likes(*, browser):
    posts_elements_xpath    = "//a[contains(@href, '/p/')]"
    likes_xpath = "//*[contains(@aria-label ,'Me gusta')]"
    max_heart_height=-1
        
    time.sleep(2)
    post_elements = browser.find_elements_by_xpath(posts_elements_xpath)
    url_post=post_elements[0].get_attribute('href')
    browser.get(url_post)

    time.sleep(2)

    #Calculate max heart height 
    likes=browser.find_elements_by_xpath(likes_xpath)
    for like in likes:
        height = like.get_attribute('height')
        current_height = int(height)

        if current_height > max_heart_height:
            max_heart_height = current_height
    
    for like in likes:
        height_str = like.get_attribute('height')
        height = int(height_str)

        if height == max_heart_height:
            parent_button = like.find_element_by_xpath('..')
            time.sleep(2)
            try:
                parent_button.click()
                print('Like')
            except:
                pass







if __name__ == '__main__':
    try:
        username_instagram = str(sys.argv[1])
    except:
        raise ValueError('Username required')

    instagram_url = 'https://www.instagram.com/'
    browser = webdriver.Chrome()
    browser.get(instagram_url)

    # Login account instagram
    login(browser=browser)
    time.sleep(3)

    # Profile
    browser.get(f'{instagram_url}{username_instagram}/')
    
    time.sleep(3)
    automate_comment(browser=browser,username=username_instagram)
    
    # Images or videos
    #time.sleep(3)
    #automate_likes(browser=browser)    
    #data=browser.find_elements_by_xpath('//img')
    #automate_posts(data=data,username_instagram=username_instagram)
