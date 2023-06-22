import tweetnlp, time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

model = tweetnlp.Sentiment()


keyword = 'liverpool'

driver = webdriver.Chrome()
driver.get("https://twitter.com/login")

wait = WebDriverWait(driver, 10)
email_field = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'input')))
email_field.send_keys(os.environ.get('TWITTER_EMAIL'))
email_field.send_keys(Keys.RETURN)

phone_verify = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="ocfEnterTextTextInput"]')))

if phone_verify:
    phone_verify.send_keys(os.environ.get('TWITTER_PHONE'))
    phone_verify.send_keys(Keys.RETURN)

password_field = wait.until(EC.element_to_be_clickable((By.NAME, 'password')))
password_field.send_keys(os.environ.get('TWITTER_PASSWORD'))
password_field.send_keys(Keys.RETURN)

time.sleep(5)
driver.get(f"https://twitter.com/search?q={keyword}&src=typed_query&f=live")

tweets = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="tweetText"]')))

for tweet in tweets:
    print(tweet.text)
    probability = model.sentiment(tweet.text, return_probability=True)['probability']
    print(probability)
    print()


driver.quit()