import logging

import selenium.webdriver as webdriver


URL = 'https://drw.com/work-at-drw/listings?filterType=category&value=Technology'

def get_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    logging.info(f"Fetching html content for dynamic website {url}")
    driver.get(url)
    driver.implicitly_wait(1)
    content = driver.page_source
    driver.quit()
    return content

# print(get_html(URL))