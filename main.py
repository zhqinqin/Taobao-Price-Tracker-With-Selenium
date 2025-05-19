import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import smtplib
from email.mime.text import MIMEText

# 读取配置
with open('config.json') as f:
    config = json.load(f)

def send_email(subject):
    """发送邮件通知"""
    msg = MIMEText(f"您监控的商品已降价！立即查看：{config['product_url']}")
    msg['Subject'] = subject
    msg['From'] = config['email_sender']
    msg['To'] = config['email_receiver']
    
    with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
        server.login(config['email_sender'], config['email_password'])
        server.send_message(msg)

def check_price():
    """检查商品价格"""
    driver = webdriver.Chrome()
    driver.get(config['product_url'])
    
    # 关闭登录弹窗（如有）
    try:
        driver.find_element(By.CLASS_NAME, 'icon-close').click()
        time.sleep(1)
    except:
        pass
    
    # 获取价格
    price_text = driver.find_element(By.XPATH, '//*[@class="price"]').text
    price = float(price_text.replace('¥', '').strip())
    
    if price < config['target_price']:
        send_email(f"【降价提醒】当前价：¥{price}")

    driver.quit()

if __name__ == '__main__':
    check_price()
