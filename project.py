import ctypes
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sympy as sp


def dark_title_bar(window):
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ctypes.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ctypes.c_int(value)
    set_window_attribute(hwnd , rendering_policy , ctypes.byref(value) , ctypes.sizeof(value))
    window.update()


root = tk.Tk()
dark_title_bar(root)
root.tk.call("source" , "azure.tcl")
root.tk.call("set_theme" , "dark")

image_path = 'calculator.png'
original_image = Image.open(image_path)
tk_image = ImageTk.PhotoImage(original_image)

root.iconphoto(False, tk_image)

button_colors = {
    'AC': 'Accent2.TButton',
    '←': 'Accent2.TButton',
    '%': 'Accent2.TButton',
    '÷': 'Accent2.TButton',
    'X': 'Accent2.TButton',
    '-': 'Accent2.TButton',
    '+': 'Accent2.TButton',
    'sin': 'Accent2.TButton',
    'cos': 'Accent2.TButton',
    'sqrt': 'Accent2.TButton',
    '^': 'Accent2.TButton',
    'log': 'Accent2.TButton',
    'exp': 'Accent2.TButton',
    '(': 'Accent2.TButton',
    '0': '',
    ')': 'Accent2.TButton',
    '1': '',
    '2':'',
    '3':'',
    '4': '',
    '5': '',
    '6':'',
    '7':'',
    '8':'',
    '9':'',
    '00':'',
    '.':'',
    '=': 'Accent.TButton'
}

def on_enter(e):
    if  e.widget['style']== 'Accent2.TButton':
        e.widget['style'] = ''
    elif  e.widget['style']== '':
        e.widget['style'] = 'Accent2.TButton'


def on_leave(e):
    e.widget['style'] = button_colors[e.widget['text']]


def remove_trailing_zeros(num):
    str_num = f"{num:f}"
    before = len(str_num)
    print(before)
    str_num = str_num.rstrip('0').rstrip('.')
    if '.' not in str_num:
        return int(str_num) , 0
    else:
        if (len(str_num) == before):
            return float(str_num) , 1
        return float(str_num) , 0


result_var = tk.StringVar(value = '0')
result_history_var = tk.StringVar(value = '')

display_frame = tk.Frame(root , height = 30 , bg = '#202021')
display_frame.pack(side = tk.TOP , fill = tk.BOTH , expand = True)

label_result2 = tk.Label(display_frame , textvariable = result_var , anchor = 'se' , bg = "#202021" , fg = "white" ,
                         font = ("Arial" , 32 , "bold"))
label_result1 = tk.Label(display_frame , textvariable = result_history_var , anchor = 'se' , bg = "#202021" ,
                         fg = "#3d3d3d" , font = ("Arial" , 13))
label_result1.pack(side = tk.TOP , fill = tk.BOTH , expand = True)
label_result2.pack(side = tk.TOP , fill = tk.BOTH , expand = True)

buttons = [
    ('AC' , '←' , '%' , '÷') ,
    ('sqrt' , '^' , 'log' , 'exp') ,
    ('sin' , 'cos' , '(' , ')') ,
    ('7' , '8' , '9' , 'X') ,
    ('4' , '5' , '6' , '-') ,
    ('1' , '2' , '3' , '+') ,
    ('00' , '0' , '.' , '=') ,
]

button_frame = ttk.Frame(root)
button_frame.pack(side = tk.TOP , fill = tk.BOTH , expand = True , padx = 4 , pady = 4)


def add(content):
    if ((result_var.get() == '0' and not content in '.X/+-') or result_var.get() == "error"):
        result_var.set('')
    result_var.set(result_var.get() + content)


def cal(content):
    new_content = content.replace('X' , '*')
    new_content = new_content.replace('÷' , '/')
    result = sp.sympify(new_content)
    result = result.evalf()
    result , flag = remove_trailing_zeros(float(result))
    if flag:
        return f"{result:.4f}"
    else:
        return f"{result}"


def press_button(content):
    if content in '+-X÷.':
        add(content)
    elif content in '0123456789':
        add(content)
    elif content in ('sin' , 'cos' , '(' , ')'):
        add(content)
    elif content in ('sqrt' , '^' , 'log' , 'exp' , '%'):
        add(content)
    elif content == '00':
        add(content)
    elif content == '←':
        result_var.set(result_var.get()[:-1])
        if result_var.get() == '':
            result_var.set('0')
    elif content == 'AC':
        result_var.set('0')
        result_history_var.set('')
    elif content == '=':
        try:
            cal(result_var.get())
        except Exception as e:
            print(e)
            result_var.set("error")
            result_history_var.set("")
        else:
            result_history_var.set(result_var.get() + '=' + cal(result_var.get()))
            result_var.set(cal(result_var.get()))


for row_index , row_values in enumerate(buttons):
    button_frame.grid_rowconfigure(row_index , weight = 1)
    for col_index , col_value in enumerate(row_values):
        button_frame.grid_columnconfigure(col_index , weight = 1 , uniform = "group1")  # 确保每一列的宽度相同
        button = ttk.Button(
            button_frame ,
            text = col_value ,  # 设置按钮文本
            style = button_colors.get(col_value,'Accent2.TButton'),
            command = lambda value = col_value:press_button(value)
        )
        button.grid(row = row_index , column = col_index , sticky = "nesw" , padx = 1 ,
                    pady = 1)  # 将按钮放置在网格布局中的适当位置，按钮扩展填充整个单元格，设置按钮之间的水平和垂直间距
        button.bind('<Enter>' , on_enter)
        button.bind('<Leave>' , on_leave)

root.title('计算器')
root.geometry("500x800+1000+300")
root.mainloop()
