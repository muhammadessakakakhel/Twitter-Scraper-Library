from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import pandas as pd

from io import BytesIO
from PIL import Image

import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

# driver = webdriver.Chrome()
# opens a userprofile and gets the first 'n' tweets

def get_n_tweets_from_current_page(n):
    user_tags = []
    time_stamps = []
    tweets = []
    no_replies_list = []
    no_re_tweet_list = []
    no_like_list = []

    last_height = 10
    # print(len(tweet_container))
    while True:
        tweet_container = driver.find_elements(by="xpath",
                                               value="//article[@data-testid='tweet']")  # getting tweet container
        try:
            for tweet in tweet_container:
                user_tag = driver.find_element(by="xpath",
                                               value="//div[@data-testid='User-Name']//*//*//*//*//*//*//span")
                time_stamp = driver.find_element(by="xpath", value="//time")  # getting time stamp
                tweet = driver.find_element(by="xpath", value="//div[@data-testid='tweetText']//span")  # getting tweet
                no_replies = driver.find_element(by="xpath",
                                                 value="//div[@data-testid='reply']//div[position()=2]//span//span//span")  # getting reply
                no_re_tweet = driver.find_element(by="xpath",
                                                  value="//div[@data-testid='retweet']//div[position()=2]//span//span//span")  # getting re-tweet
                no_like = driver.find_element(by="xpath",
                                              value="//div[@data-testid='like']//div[position()=2]//span//span//span")  # getting like

                if len(tweet.text) > 1 and tweet.text not in tweets:
                    user_tags.append(user_tag.text)
                    time_stamps.append(time_stamp.get_attribute("datetime"))
                    tweets.append(tweet.text)
                    no_replies_list.append(no_replies.text)
                    no_re_tweet_list.append(no_re_tweet.text)
                    no_like_list.append(no_like.text)
        except:
            print("error")
        # driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        driver.execute_script(f"window.scrollTo(0, {last_height});")
        time.sleep(0.1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height <= last_height:
            break
        Tweets2 = list(set(tweets))
        last_height += 300
        if len(Tweets2) > 3:
            break

    user_tags = list(dict.fromkeys(user_tags))
    time_stamps = list(dict.fromkeys(time_stamps))
    tweets = list(dict.fromkeys(tweets))
    no_replies_list = list(dict.fromkeys(no_replies_list))
    no_re_tweet_list = list(dict.fromkeys(no_re_tweet_list))
    no_like_list = list(dict.fromkeys(no_like_list))

    df = pd.DataFrame(zip(user_tags, time_stamps, tweets, no_replies_list, no_re_tweet_list, no_like_list),
                      columns=["User Tags", "Time Stamps", "Tweets", "No. Replies", "No. Retweets", "No. likes"])
    return df

def login(username="MuneebWale80142", password="muneebwalee"):
    driver.get("https://twitter.com/login")
    time.sleep(30)  # wait for 4 seconds

    driver.find_element(by="xpath", value="//input[@type='text']").send_keys(username)  # entering username

    driver.find_element(by="xpath", value="//span[contains(text(), 'Next')]").click()  # clicking next button

    time.sleep(4)  # wait for 4 seconds

    driver.find_element(by="xpath", value="//input[@name='password']").send_keys(password)  # entering password

    driver.find_element(by="xpath", value="//span[contains(text(), 'Log in')]").click()  # clicking login button

    time.sleep(4)  # wait for 4 seconds


def get_n_tweets(n, username):
    f = open(f"{username}.txt", "w")
    driver.get(f'https://twitter.com/{username}')

    wait = WebDriverWait(driver, 10)

    time.sleep(30)

    last_height = 10
    tweets = []
    while len(tweets) < n:
        print("Tweets:", len(tweets))
        driver.execute_script(f"window.scrollTo(0, {last_height});")
        time.sleep(0.1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height <= last_height:
            break
        tweetDiv = driver.find_elements(By.XPATH, "//div[@dir='auto' and @lang='en']")[:n]
        for i, tweet in enumerate(tweetDiv):
            try:
                if len(tweet.text) >1 and tweet.text not in tweets:
                    tweets.append(tweet.text)
                    f.write(f"Tweet:{len(tweets)}->{tweets[-1]}\n")
            except:
                print("error")
        last_height += 300
    print(tweets)
    print(len(tweets))
    f.close()
    input("Enter")

# opens explore page of twitter and gets the first 'n' tweets
def get_explore_tweets(n):
    # driver = webdriver.Chrome()
    driver.get(f'https://twitter.com/explore')

    time.sleep(20)

    last_height = 10
    tweets = []
    while len(tweets) < n:
        driver.execute_script(f"window.scrollTo(0, {last_height + 2});")
        time.sleep(0.1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        tweetDiv = driver.find_elements(By.XPATH, "//div[@dir='auto' and @lang='en']")[:n]
        for i, tweet in enumerate(tweetDiv):
            if len(tweet.text) > 1 and tweet.text not in tweets:
                tweets.append(tweet.text)
        last_height += 200
    print(tweets)
    print(len(tweets))
    input("Enter")

# given URL of a tweet, it will return the text in that tweet.
def get_tweet_from_URL(url):
    # driver = webdriver.Chrome()
    driver.get(url)
    print("Sleeping")
    time.sleep(20)

    td = driver.find_element(By.XPATH, "//div[@data-testid='cellInnerDiv']")
    tweetDiv = td.find_elements(By.XPATH, "//div[@dir='auto' and @lang='en']")
    # tweetDiv = driver.find_elements(By.XPATH, "//div[@dir='auto' and @lang='en']")
    if (len(tweetDiv)>=1):
        tweet = tweetDiv[0].text
        print("Tweet:", tweet)
    input("Enter")



# function to get the top trends on Twitter and save them in a CSV file
def get_top_trends():
    # chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    # options = webdriver.ChromeOptions()
    # options.binary_location = chrome_path
    # driver = webdriver.Chrome(executable_path='chromedriver', options=options)
    # driver = webdriver.Chrome()
    driver.get("https://twitter.com/explore")

    wait = WebDriverWait(driver, 10)

    # wait until the trends section is loaded
    trend_section = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='trend']")))

    # get the list of trends
    trend_list = trend_section.find_elements(By.XPATH, "//span[@dir='auto']")

    # create a CSV file to store the trends
    with open('twitter_trends.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Trend', 'URL'])

        # iterate through the trends and save them in the CSV file
        for trend in trend_list:
            trend_name = trend.text
            trend_url = trend.find_element(By.XPATH, "./..").get_attribute('href')
            writer.writerow([trend_name, trend_url])

    driver.quit()


def getHashtagTweets(hashtag="elonmusk"):
    driver.get(f"https://twitter.com/hashtag/{hashtag}")

    time.sleep(10)  # wait for 4 seconds

    user_tags = []
    time_stamps = []
    tweets = []
    no_replies_list = []
    no_re_tweet_list = []
    no_like_list = []

    last_height = 10
    # print(len(tweet_container))
    while True:
        tweet_container = driver.find_elements(by="xpath",
                                               value="//article[@data-testid='tweet']")  # getting tweet container
        try:
            for tweet in tweet_container:
                user_tag = driver.find_element(by="xpath", value="//div[@data-testid='User-Name']//*//*//*//*//*//*//span")
                time_stamp = driver.find_element(by="xpath", value="//time")  # getting time stamp
                t = driver.find_element(by="xpath", value="//div[@data-testid='tweetText']")  # getting tweet
                no_replies = driver.find_element(by="xpath",
                                                 value="//div[@data-testid='reply']//div[position()=2]//span//span//span")  # getting reply
                no_re_tweet = driver.find_element(by="xpath",
                                                  value="//div[@data-testid='retweet']//div[position()=2]//span//span//span")  # getting re-tweet
                no_like = driver.find_element(by="xpath",
                                              value="//div[@data-testid='like']//div[position()=2]//span//span//span")  # getting like
                print("tweet:", t.text)
                if len(tweet.text) > 1 and t.text not in tweets:
                    user_tags.append(user_tag.text)
                    time_stamps.append(time_stamp.get_attribute("datetime"))
                    tweets.append(t.text)
                    no_replies_list.append(no_replies.text)
                    no_re_tweet_list.append(no_re_tweet.text)
                    no_like_list.append(no_like.text)
        except:
            print("error")
        # driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        driver.execute_script(f"window.scrollTo(0, {last_height});")
        time.sleep(0.1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height <= last_height:
            break
        Tweets2 = list(set(tweets))
        last_height += 300
        if len(Tweets2) > 3:
            break

    user_tags = list(dict.fromkeys(user_tags))
    time_stamps = list(dict.fromkeys(time_stamps))
    tweets = list(dict.fromkeys(tweets))
    no_replies_list = list(dict.fromkeys(no_replies_list))
    no_re_tweet_list = list(dict.fromkeys(no_re_tweet_list))
    no_like_list = list(dict.fromkeys(no_like_list))


    df = pd.DataFrame(zip(user_tags, time_stamps, tweets, no_replies_list, no_re_tweet_list, no_like_list),
                      columns=["User Tags", "Time Stamps", "Tweets", "No. Replies", "No. Retweets", "No. likes"])

    print(df.head())

    # df.t(f"hashtag:{hashtag}.xlsx", index=False)
    df.to_csv(f"hashtag:{hashtag}.xlsx", index=False, sep=',')

def displayImageFromURL(imageURL):
    response = requests.get(imageURL)
    img = Image.open(BytesIO(response.content))

    # Display the image
    img.show()

def imageTweet(url="https://twitter.com/US_Stormwatch/status/1666238597031395328"):
    driver.get(url)
    td = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='cellInnerDiv']")))
    # td = driver.find_element(By.XPATH, "//div[@data-testid='cellInnerDiv']")
    tweetTextDiv = td.find_elements(By.XPATH, "//div[@dir='auto' and @lang='en']")
    # tweetDiv = driver.find_elements(By.XPATH, "//div[@dir='auto' and @lang='en']")
    if (len(tweetTextDiv) >= 1):
        tweet = tweetTextDiv[0].text
        print("Tweet:", tweet)
    imageURL = None
    try:
        imageURL = td.find_elements(By.XPATH, ".//img[@alt='Image']")[0].get_attribute('src')

    except:
        print("no image")
    if imageURL: displayImageFromURL(imageURL)

    input("enter")

# login()
# getHashtagTweets()
# get_top_trends()
# get_n_tweets(100, 'elonmusk')
# get_explore_tweets(10)
# get_tweet_from_URL("https://twitter.com/Exulansista/status/1654540589730521088")
imageTweet()

