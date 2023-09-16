import tkinter as tk
from tkinter import colorchooser
import analiz

color = ""  # Переменная для сохранения выбранного цвета

def show_color_picker():
    global color
    color = colorchooser.askcolor(title="Выберите цвет")
    if color[1]:
        print("Выбранный цвет:", color[1])

def run():
    analiz.TextAnalyser(file_name='text.txt', pos_list=['VERB', 'NOUN'], chislo=int(entry_amount.get()), background=color[1])

window = tk.Tk()
label = tk.Label(window, text="Анализатор текста", font=("Impact", 19))
button = tk.Button(window, font=("Impact", 17), background="#DAA520", text="сделать вордклауд", command=run)
button2 = tk.Button(window, font=("Impact", 17), background="#DAA520", text="выбрать цвет", command=show_color_picker)
entry_amount = tk.Entry(window, font=("Impact", 18))
label.pack(anchor="nw", padx=6, pady=6)
entry_amount.pack(anchor="nw", padx=6, pady=6)
button.pack(anchor="nw", padx=6, pady=6)
button2.pack(anchor="nw", padx=6, pady=6)

window.mainloop()
