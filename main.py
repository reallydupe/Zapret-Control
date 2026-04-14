import Modules.CheckServiceRunning as CSR
import customtkinter as ctk
import subprocess
import sys
import os
import Modules.workingPyWinStyle as pywinstyles   # единственный модуль от которого у меня нету резервной копии, она оч важна так как там моджно применять стили не только к root
from Modules.runAsAdmin import * 

#---------------------------------Че делает код--------------------------
# 1: Интерфейс.
# 2: Интерфейс.
# 3: Интерфейс.
# 4: Тоже интерф-
# Короче надеюсь понятно

noAdmin = True # При тесте лучше включать а то вывода в консоль в том же самом VS Code не будет
if not is_admin() and noAdmin == False:
    if run_as_admin():
        sys.exit()
    else:
        sys.exit(1)

def update_status():
    _, stat = CSR.Check_stat(2)
    StatChange(stat)
    root.after(500, update_status)

x = "250"

geom = f"{x}x{int(x) + 100}"
root = ctk.CTk()
statTitle = "Инициализация"  # Тупо, но работает
root.title(f"Zapret Control ({statTitle})")
root.geometry(geom)

fileDir = os.path.dirname(__file__)
binDir = os.path.join(fileDir, "Resources")
root.iconbitmap(f"{binDir}\\zapret.ico")
fileDir = os.path.dirname(__file__)
binDir = os.path.join(fileDir, "Bin")

_, b = CSR.Check_stat(2)

if b == True:
    subprocess.run("taskkill /f /im winws.exe", shell=True) # чтобы не ломалось

def on_closing():
    if ToState == False:
        subprocess.run("taskkill /f /im winws.exe", shell=True)
    #root.quit()
    sys.exit(0)

def StatChange(stat):
    global statTitle
    global ToState
    if stat == True:
        statusLbl.configure(text="Включен", text_color="green")
        statTitle = "Включен"
        btn.configure(text="Выключить", border_color="red", hover_color="red")
        ToState = False
    else:
        statusLbl.configure(text="Выключен", text_color="red")
        statTitle = "Выключен"
        btn.configure(text="Включить", border_color="green", hover_color="green")
        ToState = True
    
    root.title(f"Zapret Control ({statTitle})")

ToState = True
def ZapretControl():
    if ToState == True:
        subprocess.run("Server.bat", shell=True, cwd=binDir)
    else:
        subprocess.run("taskkill /f /im winws.exe", shell=True)


statusLbl = ctk.CTkLabel(root, text="Выключен", text_color="red")
statusLbl.pack()
statusLbl.place(x=90, y=120)

btn = ctk.CTkButton(root, text="Включить", command=ZapretControl, fg_color="transparent", border_width=0.6, border_color="green", hover_color="green")
btn.pack()
btn.place(x=50, y=165)
root.after(1000, update_status)


def apply_style():
    pywinstyles.apply_style(root, style="aero")
    pywinstyles.apply_style(btn, style="aero")

root.after(0, apply_style)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.resizable(False, False)
root.mainloop()