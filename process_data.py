import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

# Загрузка файла
def load_file(file_path):
    return pd.read_csv(file_path)  # Или pd.read_excel для Excel

# Выполнение расчетов
def calculate_statistics(df):
    return {
        "mean": df["Value"].mean(),
        "max": df["Value"].max(),
        "min": df["Value"].min()
    }

# Отправка в Telegram
def send_to_telegram(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=params)
    return response.status_code == 200

# Отправка на почту
def send_email(subject, body, to_email, smtp_user, smtp_password):
    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(smtp_user, to_email, msg.as_string())
    server.quit()

# Основная функция
def main():
    # Загрузка файла
    file_path = "data.csv"  # Путь к файлу
    df = load_file(file_path)

    # Расчеты
    stats = calculate_statistics(df)
    report = f"Отчет:\nСреднее: {stats['mean']}\nМаксимум: {stats['max']}\nМинимум: {stats['min']}"

    # Сохранение отчета
    with open("report.txt", "w") as f:
        f.write(report)

    # Отправка в Telegram
    bot_token = "ВАШ_ТОКЕН"
    chat_id = "ВАШ_CHAT_ID"
    send_to_telegram(report, bot_token, chat_id)

    # Отправка на почту
    smtp_user = "ВАШ_EMAIL"
    smtp_password = "ВАШ_ПАРОЛЬ"
    to_email = "ПОЛУЧАТЕЛЬ@example.com"
    send_email("Ежедневный отчет", report, to_email, smtp_user, smtp_password)

if __name__ == "__main__":
    main()