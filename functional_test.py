from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"

browser = webdriver.Firefox(
    firefox_options=options,
    executable_path=r"C:/Program Files/Mozilla Firefox/geckodriver.exe"
)
browser.get('http://localhost:8000')
assert 'Django' in browser.title
