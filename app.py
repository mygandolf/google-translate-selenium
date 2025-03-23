from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import os

app = Flask(__name__)

# مسیر درایور کروم در داکر (لینوکس)

CHROMEDRIVER_PATH = "/app/chromedriver"

# تنظیمات Selenium

def translate_text(text, timeout=10):    

    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # بدون رابط کاربری
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")        # ایجاد درایور با استفاده از فایل درایور محلی
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://translate.google.com/?sl=en&tl=fa")
        time.sleep(2)  # زمان برای لود اولیه
    except:
        driver.quit()
        print("Cant Open Chrome Driver")
        return 0
    try:
        input_selector = "textarea.er8xn"
        result_selector = "div.KkbLmb"
        input_element = driver.find_element(By.CSS_SELECTOR, input_selector)
    except:
        driver.quit()
        return 0
    try:
        input_element.clear()
        input_element.send_keys(text)
    except:
        driver.quit()
        print("Cant Enter Inputs")
        return 0
    try:
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                result_element = driver.find_element(By.CSS_SELECTOR, result_selector)
                translated_text = result_element.text
                if translated_text:
                    driver.quit()
                    return translated_text
            except:
                pass
            time.sleep(0.5)

        driver.quit()
        print("Cant Receive Result")
        return 0  # اگر بعد از timeout نتیجه نیامد
    
    except:
        driver.quit()
        print("Cant read results")
        return 0


@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    if "text" not in data:
        return jsonify({"error": "Missing 'text' in request"}), 400
    translated_text = translate_text(data["text"])
    if translated_text != 0 or translated_text != None:
        return jsonify({"translated_text": translated_text})
    else:
        return jsonify({"error": "Translation timeout, try again"}), 202  # درخواست پذیرفته شد ولی هنوز آماده نیست

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
