# استفاده از تصویر رسمی پایتون
FROM docker.arvancloud.ir/python:3.9

# نصب وابستگی‌ها
RUN pip install flask selenium

# نصب Google Chrome و ChromeDriver
RUN apt-get update && apt-get install -y wget unzip \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install \
    && rm google-chrome-stable_current_amd64.deb

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی کردن کروم‌درایور لینوکسی
COPY chromedriver /app/chromedriver
RUN chmod +x /app/chromedriver  # اعطای مجوز اجرا

# باز کردن پورت 5000
EXPOSE 5000

# اجرای برنامه
CMD ["python", "app.py"]
