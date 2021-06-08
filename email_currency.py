import requests 
from bs4 import BeautifulSoup 
import time 
import schedule
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Ссылка на нужную страницу
DOLLAR_RUB = 'https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei=N9l0XtDXHs716QTcuaXoAg&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4'
EURO_RUB = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B5%D0%B2%D1%80%D0%BE&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B5%D0%B2%D1%80%D0%BE&aqs=chrome..69i57j0i433l4j0i457j0i402j0j0i433j0.9339j1j7&sourceid=chrome&ie=UTF-8'

def get_currency(url):
   
    # Заголовки для передачи вместе с URL
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

    full_page = requests.get(url, headers = headers )

    # Парсер html страницы
    soup = BeautifulSoup(full_page.content, 'html.parser')
 
    # Парсинг определенных тегов HTML
    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    return convert[0].text
  

msg_from = input('Введите логин :')# Логин от аккаунта , с которого будет происходить рассылка почты 
password = input('Введите пароль :')# Пароль от аккаунта , с которого будет происходить рассылка почты 
msg_to = input('Кому отправить : ')# Почта получателя

# Функция отправки сообщения
def send_mail():

    msg = MIMEMultipart()
    message = (f'Добрый день, курс валют на сегодня : \n\nКурс доллара ($)  - ' + get_currency(DOLLAR_RUB) + ' руб' + '\nКурс евро (€) - '+ get_currency(EURO_RUB) + ' руб')
    
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com: 587')# 587 для gmail , для mail.ru 25 ,для yandex 465
    server.starttls() 
    # Авторизация отправителя
    server.login(msg_from, password)
    # Отправка сообщения на сервер
    server.sendmail(msg_from, msg_to, msg.as_string())
    print("successfully sent email to :" + str(msg_to))
send_mail()

# Расписание выполнения работ
def job():
   send_mail()

schedule.every().day.at("14:30").do(job)#

while True:
    schedule.run_pending()
    time.sleep(1)

server.quit()

# если запуск из cmd  win , раскоменнтируй строку  :
# input()
