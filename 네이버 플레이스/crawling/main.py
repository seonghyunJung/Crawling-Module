import config
import web
import logger

# Globals
logger = logger.instance


def main():
    logger.info('Script started.')
    config.init_web()

    web.start()
    driver = web.driver
    driver.get('https://www.google.com')


if __name__ == '__main__':
    main()
