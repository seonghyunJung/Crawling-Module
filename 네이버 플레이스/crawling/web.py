from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import config
import logger


# Globals
driver = None
logger = logger.instance


def init(p_logger):
    global logger
    logger = p_logger


def start(headless=True):
    global driver

    if not headless:
        chrome_options = Options()
        chrome_options.add_argument('--blink-settings=imagesEnabled=false') #브라우저에서 이미지 로딩을 하지 않습니다.
        driver = webdriver.Chrome(options=chrome_options)
    elif config.headless:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = config.chrome_bin
        driver = webdriver.Chrome(
            executable_path=config.chrome_driver_bin,
            chrome_options=chrome_options
        )
    else:
        chrome_options = Options()
        chrome_options.add_argument('--blink-settings=imagesEnabled=false') #브라우저에서 이미지 로딩을 하지 않습니다.
        driver = webdriver.Chrome(options=chrome_options)

    driver.implicitly_wait(10)
    logger.info('Selenium started')
