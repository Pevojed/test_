from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

web = "https://www.kwserbia.com/agents"
path = "C:/Users/38163/PycharmProjects/ChDriver/chromedriver.exe"

service_path = Service(path)
driver = webdriver.Chrome(service = service_path)


driver.get(web)
driver.maximize_window()
time.sleep(5)

# Pagination 1
pagination = driver.find_element(By.XPATH,'//ul[@class = "pagination"]')  # locating pagination bar
pages = pagination.find_elements(By.TAG_NAME,'li')  # locating each page displayed in the pagination bar
last_page = int(pages[-2].text)  # getting the last page with negative indexing (starts from where the array ends)

agent_link = []


# Pagination 2
current_page = 1   # this is the page the bot starts scraping

# The while loop below will work until the the bot reaches the last page of the website, then it will break
while current_page <= last_page:
    # let the page render correctly
    container = driver.find_element(By.XPATH,'//div[@id="list-container"]')
    time.sleep(2)
    agents = container.find_elements(By.XPATH,'.//div[contains(@class,"officeagent-item")]')
    time.sleep(2)
    print(len(agents))
    # products = container.find_elements_by_xpath('./li')

    for agent in agents:
        elem = agent.find_element(By.TAG_NAME,'a')
        link = elem.get_attribute('href')
        agent_link.append(link)
        #elem.click()
        print(link)
        #driver.back()
        #print(agent_name)
    #     agent_author.append(product.find_element_by_xpath('.//li[contains(@class, "authorLabel")]').text)
    #     agent_length.append(product.find_element_by_xpath('.//li[contains(@class, "runtimeLabel")]').text)

    current_page = current_page + 1  # increment the current_page by 1 after the data is extracted
    # Locating the next_page button and clicking on it. If the element isn't on the website, pass to the next iteration
    try:
        next_page = driver.find_element(By.XPATH, './/a[text()=">"]')
        time.sleep(2)
        next_page.click()
    except:
        print('nije nasao')
        pass

agent_name = []
agent_link1 = []
agent_photo = []
agent_direct_tel = []
#agent_tel = []
agent_mobile = []
agent_email = []
agent_site = []
agent_facebook = []
agent_linkedin = []
agent_instagram = []
agent_youtube = []
agent_twitter = []
agent_languages = []
for item_link in agent_link:

    driver.get(item_link)
    time.sleep(3)
    name = driver.find_element(By.XPATH, '//div[@class="agent-name"]/h2[@class="ng-binding"]').text
    # elem1 = driver.find_element(By.XPATH, '//a[@class="icon-btn-phone"]')
    # try:
    #     tel = elem1.get_attribute('href')
    # except:
    #     tel = 'tel'

    try:
        elem2 = driver.find_element(By.XPATH, '//div[@ng-if="chat.enabled"]/a[@class="icon-btn-whatsapp"]')
        mobile = elem2.get_attribute('href')
        pos = mobile.index('?')
        mobile = mobile[pos+1:]
        mobile.replace('phone=','mobile:+' )
    except:
        mobile = 'mobile'

    try:
        elem3 = driver.find_element(By.XPATH, '//div[@ng-if="vm.agent.personalWebsite"]/span/a')
        site = elem3.get_attribute('href')

    except:
        site = 'site'

    elem5s = driver.find_elements(By.XPATH,'//div[@class= "prof-language ng-binding"]' )
    time.sleep(1)
    language_list=[]
    for elem5 in elem5s:
        language_list.append(elem5.text)
    languages = " ".join(language_list)



    try:
        elem5 = driver.find_element(By.XPATH, '//a[contains(@class,"show-more-link")]')
        elem5.click()
        direct_tel =driver.find_element(By.XPATH, '//a[@ng-if="vm.showFullAgentDirectLine"]').text
        time.sleep(2)
    except:
        direct_tel = "tel:"

    try:
        elem6 = driver.find_element(By.XPATH, '//a[@class="facebook"]')
        facebook = elem6.get_attribute('href')

    except:
        facebook = 'facebook'

    try:
        elem7 = driver.find_element(By.XPATH, '//a[@class="linkedin"]')
        linkedin = elem7.get_attribute('href')

    except:
        linkedin = 'linkedin'

    try:
        elem8 = driver.find_element(By.XPATH, '//a[@class="instagram"]')
        instagram = elem8.get_attribute('href')

    except:
        instagram = 'instagram'

    try:
        elem9 = driver.find_element(By.XPATH, '//a[@class="youtube"]')
        youtube = elem9.get_attribute('href')

    except:
        youtube = 'youtube'
    try:
        elem10 = driver.find_element(By.XPATH, '//a[@class="twitter"]')
        twitter = elem10.get_attribute('href')

    except:
        twitter = 'twitter'
    try:
        elem11 = driver.find_element(By.XPATH, '//div[@class="agent-photo-div"]/img')
        photo = elem11.get_attribute('src')

    except:
        photo = 'photo'

    agent_name.append(name)
    agent_link1.append(item_link)
    agent_photo.append(photo)
    agent_direct_tel.append(direct_tel)
    agent_mobile.append(mobile)
    agent_site.append(site)
    agent_facebook.append(facebook)
    agent_linkedin.append(linkedin)
    agent_instagram.append(instagram)
    agent_youtube.append(youtube)
    agent_twitter.append(twitter)
    agent_languages.append(languages)






#driver.quit()

#df_books = pd.DataFrame({'name': agent_name, 'telephone': agent_tel, 'E-mail': agent_email})
df_books = pd.DataFrame({'name': agent_name,'link': agent_link1, 'photo': agent_photo, 'tel': agent_direct_tel, 'mobile': agent_mobile,
                         'site': agent_site, 'facebook': agent_facebook, 'linkedin': agent_linkedin,
                         'instagram': agent_instagram, 'youtube': agent_youtube, 'twitter': agent_twitter,
                         'languages': agent_languages})

df_books.to_csv('agents_srb.csv', index=False)
