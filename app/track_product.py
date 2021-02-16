import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from core.models import Product

import requests
from bs4 import BeautifulSoup
import html5lib
import environ
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

root = environ.Path(__file__) - 3  # get root of the project
env = environ.Env()
environ.Env.read_env()

products = Product.objects.all().filter(is_active=True)

def product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Accept-Language": "en",

    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html5lib")
    price = soup.select_one(selector="#priceblock_ourprice").getText() if soup.select_one(selector="#priceblock_ourprice") is not None else soup.select_one(selector="#priceblock_dealprice").getText()

    title = soup.select_one(selector="#productTitle").getText().strip()
    return float(re.sub('[^0123456789.]', '', price)), title

def send_email(emails, title, price, current_price, url):
    smtp = smtplib.SMTP(host='smtp.gmail.com', port=587)
    smtp.starttls()
    smtp.login(env.str('SMTP_EMAIL'), env.str('SMTP_PASSWORD'))

    message = f"<p>Hi,<br><br>Your product have discount of <b>{price-current_price}</b> <a href='{url}' target='_blank'>click here</a> to buy your product <b>@{current_price}<b>.</p><br><br>Regards,<br>UpTechnoTricks"
    msg = MIMEMultipart('alternative')
    msg['From']='noreply@pricetracker.com <uptechnotricks@gmail.com>'
    msg['To']=','.join(emails)
    msg['Subject']=title
    msg.attach(MIMEText(message, 'html'))

    smtp.send_message(msg)
    
    del msg

for product in products:
    url = product.url
    price = product.price
    name = product.name
    current_price, title = product_details(url)
    if(current_price <= price):
        Product.objects.filter(pk=product.id).update(is_active=False)
        emails = result = [x.strip() for x in product.email.split(',')]
        send_email(emails, title, price, current_price, url)    
