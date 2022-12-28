
import pandas as pd
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))




driver.get('https://www.naukri.com/')
driver.maximize_window()

myElem0 = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "login_Layer")))
myElem0.click()


username= WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.form-row:nth-child(2) > input')))
username.click()
username.send_keys('mathisit052@gmail.com')


password=WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.form-row:nth-child(3) > input')))
password.click()
password.send_keys('bemech99921')

login=WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.loginButton')))
login.click()

placeholder=WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.nI-gNb-sb__placeholder')))
placeholder.click()

key=WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.active .suggestor-input')))
key.click()
key.send_keys("python developer")


experience=WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID,'experienceDD')))
experience.click()


a=2

experience1=WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH,f"//li[{a}]/div/span")))
experience1.click()

time.sleep(10)

location=WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH,".//input[@value='']")))
location.click()
location.send_keys("Bangalore/Bengaluru")

search=WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR,".nI-gNb-sb__icon-wrapper > span:nth-child(2)")))
search.click()


list1=[]
list2=[]
list3=[]
list4=[]
list5=[]
list6=[]
list7=[]

webdriver = driver.current_url

time.sleep(2)
for i in range(30):
    page=WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, f".pages > a:nth-child({i+1})")))
    page.click()

    time.sleep(1)

    page = driver.execute_script('return document.body.innerHTML')
    page_soup = BeautifulSoup(''.join(page), 'html.parser')

    divTag = page_soup.find_all("div", {"class": "content"})




    for i in divTag:
        # tdTags = i.find_all("section", {"class": "listContainer fleft"})
        # for j in tdTags:
        #     k=j.find_all("div",{"class": "list"})
            for l in i:
                m=l.find_all("article", {"class": "jobTuple bgWhite br4 mb-8"})
                for p in m:
                    # o=n.find_all("div", {"class": "jobTupleHeader"})


                    p1=p.find_all("a", {"class":"title fw500 ellipsis"})
                    n1=p.find_all("a", {"class":"subTitle ellipsis fleft"})
                    disclosed = p.find_all("span", {"class": "ellipsis fleft fs12 lh16"})
                    loc = p.find_all("span", {"class": "ellipsis fleft fs12 lh16 locWdth"})
                    ex = p.find_all("span", {"class": "ellipsis fleft fs12 lh16 expwdth"})



                    for p2,n2,disclosed1,loc1,ex1 in zip(p1,n1,disclosed,loc,ex):
                        #d=[p2.get('href'),p2.get('title'),n2.get('href'),n2.get('title'),disclosed1.text,loc1.text,ex1.text]
                        list1.append(p2.get('href'))
                        list2.append(p2.get('title'))
                        list3.append(n2.get('href'))
                        list4.append(n2.get('title'))
                        list5.append(disclosed1.text)
                        list6.append(loc1.text)
                        list7.append(ex1.text)



df_data = pd.DataFrame(list(zip(list1, list2,list3,list4,list5,list6,list7)), columns =['apply link', 'job_role','comapanyjob', 'company_name','status','location','experiment'])

df_data.to_csv('data.csv')




df = pd.read_csv("data.csv")
url = df['apply link'].tolist()
company_name = df['company_name'].tolist()

APPLY_ON_COMPANY_SITE = pd.DataFrame(columns=['apply link', 'company_name', 'status'])

APPLY_ON_COMPANY_SITE.to_csv("APPLY_ON_COMPANY_SITE.csv", index=False)

com_url = []

index = 0
excount = 0
for i, j in zip(url[:400], company_name):

    driver.get(i)
    time.sleep(1)

    try:

        try:
            c = driver.find_element(By.CSS_SELECTOR, '.apply-button-container > .waves-ripple').text
        except:
            c = driver.find_element(By.CSS_SELECTOR, '.already-applied:nth-child(1)').text

        if c == 'APPLY ON COMPANY SITE':

            print("APPLY ON COMPANY SITE'")

            ds = pd.DataFrame(list(zip([i], [j], ["APPLY ON COMPANY SITE"])),
                              columns=['apply link', 'company_name', 'status'])
            ds.to_csv("APPLY_ON_COMPANY_SITE.csv", mode='a', index=False, header=False)

        elif c == "APPLY":

            print("APPLY")
            time.sleep(10)

            apply = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".apply-button-container > .waves-ripple")))
            apply.click()

            time.sleep(10)

            ds = pd.DataFrame(list(zip([i], [j], ["APPLIED"])), columns=['apply link', 'company_name', 'status'])
            ds.to_csv("APPLY_ON_COMPANY_SITE.csv", mode='a', index=False, header=False)


        else:
            print("Already Applied")

            ds = pd.DataFrame(list(zip([i], [j], ["Already Aplied"])), columns=['apply link', 'company_name', 'status'])
            ds.to_csv("APPLY_ON_COMPANY_SITE.csv", mode='a', index=False, header=False)


    except:
        print("Your'e reached maximum limit")
        driver.close()

                    # print(p1)
                    #
                    # for q in p:
                    #     r=q.find_all("div", {"class": "mt-7 companyInfo subheading lh16"})
                    #
                    #     for s in r:
                    #         r1=s.find_all("a")
                    #
                    #         print(r1)
                    #
                    #
                    #
                    #
                    #
                    #
                    #




#         print(k)
#
#
#
#
# print(divTag)

#
# for i in divTag:
#         i.find_all('article'):
#     for j in i.find_all('div', {"class": "jobTupleHeader"}):
#         for k in j.find_all('div', {"class": "info fleft"}):
#             for l in k:
#                 print(l.find('a'))










#
# time.sleep(10)
#
# a = driver.current_url
# print(a)
#
# urls=[]
# page = driver.execute_script('return document.body.innerHTML')
# page_soup = BeautifulSoup(''.join(page), 'html.parser')
#
#
# divTag = page_soup.find_all("div", {"class": "pagination lastCompMark"})
#
# for tag in divTag:
#     tdTags = tag.find_all("div", {"class": "fleft pages"})
#     for tag in tdTags:
#         j=tag.find_all('a')
#         for k in j:
#             d=k.get('href')
#             d1=str(d)+"?k"
#             urls.append(d1)
# b=a.replace("https://www.naukri.com/","")
# c=b.split("=")[0]
#
# final_url=[]
#
# print(urls)
# print(c)
# for i in urls:
#     url = a.replace(c, i,1)
#     final_url.append(url)
#
# print(final_url)
#
