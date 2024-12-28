import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

def get_usd_rate():
    url = 'https://mybuh.kz/nbrk/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find('table', {'class': 'table table-bordered'})
    rows = table.find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1 and 'USD' in cols[0].text:  # Ищем строку с USD
            usd_rate = cols[1].text.strip().replace(',', '.')
            return float(usd_rate)
    return None

class CurrencyConverter:
    def __init__(self, rate):
        self.rate = rate  # Курс доллара

    def convert_to_usd(self, amount):
        return amount / self.rate
      
class CurrencyConverterApp:
    def __init__(self, root, converter):
        self.root = root
        self.converter = converter
        self.root.title("Конвертер валют")
        
        self.amount_label = tk.Label(root, text="Введите сумму в вашей валюте:")
        self.amount_label.pack(padx=10, pady=10)
        
        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack(padx=10, pady=10)
        
        self.convert_button = tk.Button(root, text="Конвертировать", command=self.convert)
        self.convert_button.pack(padx=10, pady=10)

    def convert(self):
        try:
            amount = float(self.amount_entry.get())
            usd_amount = self.converter.convert_to_usd(amount)
            result_message = f"Ваша сумма в долларах США: {usd_amount:.2f} USD"
            messagebox.showinfo("Результат", result_message)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите правильное число")

usd_rate = get_usd_rate()

if usd_rate:
    root = tk.Tk()
    converter = CurrencyConverter(usd_rate)
    app = CurrencyConverterApp(root, converter)
    root.mainloop()
else:
    print("Не удалось получить курс доллара.")
