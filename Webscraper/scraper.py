from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import io
from PIL import Image
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    image_urls = set()
    skips = 0
    while len(image_urls) < max_images:
        scroll_down(wd)

        # Wait for the images to load after scrolling
        time.sleep(delay)

        thumbnails = wd.find_elements(By.CLASS_NAME, 'Q4LuWd')

        for img in thumbnails:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            # Find the full-sized image
            images = wd.find_elements(By.CLASS_NAME, 'n3VNCb')
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")

    return image_urls



def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print('FAILED -', e)

url = 'https://www.google.com/search?q=artificial+intelligence&tbm=isch&ved=2ahUKEwjzsLz7q6-EAxX7vWMGHTP1AuUQ2-cCegQIABAA&oq=ARtific&gs_lp=EgNpbWciB0FSdGlmaWMqAggAMg0QABiABBiKBRhDGLEDMg0QABiABBiKBRhDGLEDMgoQABiABBiKBRhDMhAQABiABBiKBRhDGLEDGIMBMg0QABiABBiKBRhDGLEDMggQABiABBixAzIFEAAYgAQyCBAAGIAEGLEDMgoQABiABBiKBRhDMggQABiABBixA0i8KFC0BFiEHHABeACQAQCYAdYBoAGYCKoBBTAuNy4xuAEByAEA-AEBigILZ3dzLXdpei1pbWeoAgrCAgQQIxgnwgIEEAAYA8ICBxAAGIAEGBjCAgcQIxjqAhgnwgILEAAYgAQYsQMYgwGIBgE&sclient=img&ei=kw_PZbObKfv7juMPs-qLqA4&authuser=0&bih=911&biw=1920&hl=en'
driver.get(url)


urls = get_images_from_google(driver, 1, 6)
for i, url in enumerate(urls):
    download_image("imgs/", url, str(i) + ".jpg")
