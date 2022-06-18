# Standart modules
import os
import json
import time

# Selenium modules
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Other modules
from bs4 import BeautifulSoup as BS

# Paths
BASE_DIR = os.getcwd()
WEBDRIVER_PATH = os.path.join(BASE_DIR, 'chromedriver')
RESULT_JSON_PATH = os.path.join(BASE_DIR, 'result.json')

# Parameters
URL = 'https://www.avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie/videokarty-ASgBAgICAkTGB~pm7gmmZw?cd=1&p='
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
PAGE_LIMIT = 5

# Main program function
def main() -> None:
    """ Runs the program """

    try:
        content = get_content()
        items = parse_content(content)
        write_to_json(items)

    except Exception as _ex:
        print(f'Exception: {_ex}')


# Functinos
def get_content() -> list[dict]:
    """ Gets content from pages """

    try:
        browser = init_webdriver()
        page_count = get_page_count(browser)

        return get_page_sources(browser, page_count)

    except Exception as _ex:
        print(f'Execption: {_ex}')

    finally:
        browser.close()
        browser.quit


def init_webdriver() -> WebDriver:
    """ Inits webdriver with bot-detection bypass """

    try:
        service = Service(WEBDRIVER_PATH)
        options = Options()

        options.add_argument(f'user-agent={USER_AGENT}')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        return WebDriver(service=service, options=options)

    except Exception as _ex:
        print(f'Exception: {_ex}')


def get_page_sources(browser: WebDriver, page_count: int) -> list[WebDriver.page_source]:
    """ Gets page_sources from a site """

    try:
        page_sources = []

        for page in range(page_count):
            browser.get(f'{URL}&p={page}')
            page_sources.append(browser.page_source)

        return page_sources

    except Exception as _ex:
        print(f'Exception: {_ex}')


def parse_content(page_sources: list[WebDriver.page_source]) -> list[dict]:
    """ Parses content from a page """
    try:
        if len(page_sources) > 5:
            page_sources = page_sources[:5]

        items = []
        
        for page_source in page_sources:
            content = BS(page_source, 'html.parser')
            items_container = content.find('div', class_='items-items-kAJAg')
            not_parsed_items = items_container.find_all('div', class_='iva-item-content-rejJg')

            for item in not_parsed_items:
                item_info = {
                    'Name': item.find('h3', class_='title-root-zZCwT').text.replace('\xa0', ' '),
                    'Price': item.find('span', class_='price-text-_YGDY').text.replace('\xa0', ' ')
                }

                items.append(item_info)

        return items
            
    except Exception as _ex:
        print(f'Exception: {_ex}')


def get_page_count(browser: WebDriver) -> int:
    """ Gets page count"""

    try:
        browser.get(URL)
        pagination_container = browser.find_element(By.CLASS_NAME, 'pagination-root-Ntd_O')
        pagination_container_elements = pagination_container.find_elements(By.CLASS_NAME, 'pagination-item-JJq_j')
        last_page_num = int(pagination_container_elements[-2].text)

        if last_page_num > PAGE_LIMIT & PAGE_LIMIT != 0:
            return PAGE_LIMIT

        return last_page_num

    except Exception as _ex:
        print(f'Exception: {_ex}')


def write_to_json(items: list[dict]) -> None:
    """ Writes results to json """

    try: 
        with open(RESULT_JSON_PATH, 'w+', encoding='utf-8') as file:
            for item in items:
                json.dump(item, file, ensure_ascii=False, indent=4)

    except Exception as _ex:
        print(f'Exception: {_ex}')

# Program enter point
if __name__ == '__main__':
    main()
