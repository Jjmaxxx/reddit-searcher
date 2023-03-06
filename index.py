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
numOfPosts= 0
num=0
search = driver.find_element(By.ID,"header-search-bar")
search.send_keys(playerInput)
WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR,"button[data-testid='search-trigger-item']"))
).click()
# driver.find_element(By.CSS_SELECTOR,"div[data-testid='search-trigger-item']").click()
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
                print("next")
                numOfPosts+=1
                upvotes = WebDriverWait(post, 20).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "_vaFo96phV6L5Hltvwcox"))
                ).text
                #post.find_element(By.CLASS_NAME,"_vaFo96phV6L5Hltvwcox").text
                findK =upvotes.find("k")
                if(findK!= -1):
                    upvotes = int(float(upvotes[0:findK]) * 1000)
                else:
                    upvotes=upvotes[0:upvotes.find(" ")]
                
                postTitle = WebDriverWait(post, 20).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='post-title']"))
                )
                
                # post.find_element(By.CSS_SELECTOR,"div[data-testid='post-title']")
                title = postTitle.find_element(By.TAG_NAME,"h3").text
                words = title.split()
                words.append("posts")
                if post.find_elements(By.CLASS_NAME,"PrfaR-luawcEBK2dhGuDp"):
                    words.append("image")

                #check if paragraph class exists when clicked 
                num+=1
                if(num == 1):
                    WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable(post)
                    ).click()
                # post.click()
                print("post clicked")
                # postContent = WebDriverWait(post,10).until(
                #     EC.presence_of_element_located((By.CSS_SELECTOR,"div[data-testid='post-content']"))
                # )
                insidePost = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.ID,"overlayScrollContainer"))
                )
                # print(insidePost)
                # driver.execute_script("overlayScrollContainer.scrollTo(0, overlayScrollContainer.scrollHeight);")
                paragraphs = WebDriverWait(insidePost,10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME,"p"))
                )
                #paragraphs = insidePost.find_elements(By.TAG_NAME,"p")
                if paragraphs:
                    print("Found")
                    for p in paragraphs:
                        words.append(p.text)
                # postsText = WebDriverWait(post,10).until(
                #     EC.presence_of_all_elements_located((By.TAG_NAME,"p"))
                # )
                # for texts in postsText:
                #     words.append(texts.text)

                # content = postContent.text
                
                close = driver.find_element(By.XPATH,"//button[@title='Close']")
                print(close)
                close.click()
                #WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'subredditvars-r-nfl')))
                
                # driver.find_element(By.XPATH,"//button[@title='Close']").click()
                # print(header)
                # WebDriverWait(header, 20).until(
                #     EC.element_to_be_clickable((By.TAG_NAME,"button"))
                # ).click()                
                # driver.find_element(By.ID,"2x-container").send_keys(Keys.ESCAPE)
                # title = title + " " + content
                
                for word in words:
                    word = word.lower()
                    if any(not char.isalnum() for char in word):
                        continue                    
                    if word in wordsDict:
                        wordsDict[word]+=1
                    else:
                        wordsDict[word]=1
                    print(word+ ": "+str(wordsDict[word]))

                writer.writerow([title,upvotes])
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    with open('wordFrequency.csv','w', encoding="utf-8") as file:
        writer = csv.writer(file)
        
        for word in wordsDict:
            writer.writerow([word,wordsDict[word]])
    print(numOfPosts)
    print("done")
except Exception as e:
    print(e)
    driver.quit()