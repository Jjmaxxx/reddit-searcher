from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time 
import csv
playerInput = input("What phrase would you like to search up\n")
service = Service("C:\Program Files (x86)\chromedriver_win32")
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(service=service,options=options)
driver.get("https://www.reddit.com/")
wordsDict = {}

search = driver.find_element(By.ID,"header-search-bar")
search.send_keys(playerInput)
search.send_keys(Keys.RETURN)

#wait for element to exist before searching if it exists
try:
    with open('redditPosts.csv','w', encoding="utf-8") as file:
        writer = csv.writer(file)
        
        allPosts = []
        for i in range(5):
            posts = WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div[data-testid='post-container']"))
            )
            for post in posts:
                upvotes = post.find_element(By.CLASS_NAME,"_vaFo96phV6L5Hltvwcox").text
                findK =upvotes.find("k")
                if(findK!= -1):
                    upvotes = int(float(upvotes[0:findK]) * 1000)
                else:
                    upvotes=upvotes[0:upvotes.find(" ")]
                postTitle = post.find_element(By.CSS_SELECTOR,"div[data-testid='post-title']")
                title = postTitle.find_element(By.TAG_NAME,"h3").text
                #if _2c1ElNxHftd8W_nZtcG9zf _33Pa96SGhFVpZeI6a7Y_Pl _2r9BZFotuBbLYnijAaskeZ class name exists, then theres a picture/video
                #check if paragraph class exists when clicked 
                # post.click()
                # postContent = WebDriverWait(driver,10).until(
                #     EC.presence_of_element_located((By.CSS_SELECTOR,"div[data-testid='post-content']"))
                # )
                # content = postContent.text
                # driver.find_element(By.TAG_NAME,"body").send_keys(Keys.ESCAPE)
                # title = title + " " + content
                words = title.split()
                for word in words:
                    word = word.lower()
                    if any(not char.isalnum() for char in word):
                        continue                    
                    if word in wordsDict:
                        wordsDict[word]+=1
                    else:
                        wordsDict[word]=1
                    #print(word+ ": "+str(wordsDict[word]))

                writer.writerow([title,upvotes])
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    with open('wordFrequency.csv','w', encoding="utf-8") as file:
        writer = csv.writer(file)
        
        for word in wordsDict:
            writer.writerow([word,wordsDict[word]])
    print("done")
except Exception as e:
    print(e)
    driver.quit()