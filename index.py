from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time 
playerInput = input("What phrase would you like to search up\n")
service = Service("C:\Program Files (x86)\chromedriver_win32")
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(service=service,options=options)
driver.get("https://www.reddit.com/")

search = driver.find_element(By.ID,"header-search-bar")
search.send_keys(playerInput)
search.send_keys(Keys.RETURN)

class Post:
    def __init__(this,title,upvotes):
        this.title = title
        this.upvotes = upvotes
#wait for element to exist before searching if it exists
try:
    # main = WebDriverWait(driver,10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR,"div[data-testid='posts-list']"))
    # )
    # print(main)
    # posts = WebDriverWait(driver,10).until(
    #     EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div[data-testid='post-title']"))
    # )
    allPosts = []
    for i in range(5):
        posts = WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div[data-testid='post-container']"))
        )
        for post in posts:
            postTitle = post.find_element(By.CSS_SELECTOR,"div[data-testid='post-title']")
            title = postTitle.find_element(By.TAG_NAME,"h3")
            upvotes = post.find_element(By.CLASS_NAME,"_vaFo96phV6L5Hltvwcox")
            
            newPost = Post(title.text,upvotes.text)
            allPosts.append(newPost)
            print(title.text)
            print(upvotes.text)
        # print(postTitles)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    for post in allPosts:
        print("Post Title: " + post.title)
        print("Upvotes: " + post.upvotes)
        time.sleep(0.2)
except:
    print("couldnt find!")
    driver.quit()
# main = driver.find_element(By.ID,"posts-list")


while(True):
    pass