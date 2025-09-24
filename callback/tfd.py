from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

async def eta0_a():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://tfd.nexon.com/ko/library/eta-0")
    try:
        trade_list = [f"- {i.text.split(' X ')[0]} * {i.text.split(' X ')[1]}" for i in driver.find_elements(By.CLASS_NAME, 'name')]
        return trade_list

    except:
        return None

async def eta0_b():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://tfd.nexon.com/ko/library/eta-0")
    driver.find_element(By.CLASS_NAME, 'select_eta-0').click()
    driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/div[1]/div[2]/div/div/ul/li[2]/button')
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "name")))
    
    try:
        trade_list = [f"- {i.text.split(' X ')[0]} * {i.text.split(' X ')[1]}" for i in driver.find_elements(By.CLASS_NAME, 'name')]
        return trade_list

    except:
        return None