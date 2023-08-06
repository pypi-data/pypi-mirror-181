def get_browser(browser_type=None):
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("ignore-certificate-errors")
    if browser_type not in webdriver.__all__ or "Chrome" == browser_type:
        browser = webdriver.Chrome(options=options)
    else:
        browser = getattr(webdriver, browser_type)()
    return browser
