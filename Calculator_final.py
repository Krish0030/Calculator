from tkinter import *
import re
root = Tk()
root.title("Calculator!")

label = Label(root, text="CALCULATOR!", font=("Arial", 24), fg='purple')
label.pack(side="top")

frame = Frame(root, highlightbackground='darkred', highlightthickness=8, bd=0)
frame1 = Frame(root, highlightbackground='darkred', highlightthickness=8, bd=0)
frame.pack(padx=5,pady=5)
frame1.pack(padx=5,pady=5)

e = Entry(frame, width=30, font=("Arial", 16), borderwidth=10, justify='right', state='readonly')
e.pack()
#used for restricting manual input into entry box
def _set_entry(text):
    e.config(state='normal')
    e.delete(0, END)
    e.insert(0, text)
    e.config(state='readonly')

def _append_entry(text):
    e.config(state='normal')
    e.insert(END, text)
    e.config(state='readonly')

def inp(val):
    _append_entry(val)
def delete_num():
    s = e.get()
    if not s:
        return
    _set_entry(s[:-1])
def clear_all():
    _set_entry("")
def insert_power():
    _append_entry('^')
def safe_eval(entry:str):
    #to allow only numbers and operatin signs in entry, and give error on diff input
    if not re.fullmatch(r'[\d\.\+\-\*/\(\)\s\^]+', entry or ''):
        raise ValueError("Invalid characters")
    entry=entry.replace('^','**')
    #used to evaluate in restricted environment, so no dangerous code can be injected
    try:
        result = eval(entry, {"__builtins__": None}, {})
    except ZeroDivisionError:
        raise
    except Exception:
        raise ValueError("Malformed expression")
    return result
def calculate():
    entry = e.get()
    if not entry.strip():
        return
    try:
        result = safe_eval(entry)
        _set_entry(str(result))
    except ZeroDivisionError:
        _set_entry("Error: Not divisible by zero")
    except Exception:
        _set_entry("Error")

buttons = [('0', 3, 1), ('1', 2, 0), ('2', 2, 1), 
('3', 2, 2),('4', 1, 0), ('5', 1, 1), 
('6', 1, 2),('7', 0, 0), ('8', 0, 1), 
('9', 0, 2)]
buttons_operation=[('+',0,3), ('-',1,3), ('*',2,3), 
('/',3,3),('.', 3, 0)]
for val,row,col in buttons_operation:
    plusbtn=Button(frame1, text=val, font=("Arial", 16, "bold"), width=4, height=2, fg='black',bg='lightgrey',command=lambda v=val: inp(v))
    plusbtn.grid(row=row,column=col)
for val, row, col in buttons:
    button=Button(frame1, text=val,font=("Arial", 16),width=4,height=2,fg='purple',command=lambda v=val: inp(v))
    button.grid(row=row, column=col)
clear_btn = Button(frame1, text='C', font=("Arial", 16, "bold"),width=4, height=2, fg='black', bg='lightgrey',command=clear_all)
clear_btn.grid(row=0, column=4,rowspan=2,sticky="nsew")
pow_btn = Button(frame1, text='^', font=("Arial", 16, "bold"),width=4, height=2, fg='black', bg='lightgrey',command=insert_power)
pow_btn.grid(row=3,column=2)
delete_btn=Button(frame1,text='del',font=("Arial", 16,"bold"),width=4,height=2,fg='black',bg='lightgrey',command=delete_num)
delete_btn.grid(row=2,column=4,rowspan=2,sticky="nsew")
equal_btn=Button(frame1,text="=", font=("Arial", 16, "bold"), width=4, height=2, fg='black',bg='lightgrey',command=calculate)
equal_btn.grid(row=4, column=0, columnspan=5, sticky="nsew")
for ch in '0123456789':
    root.bind(ch, lambda e, c=ch: inp(c))
for ch in '+-*/.':
    root.bind(ch, lambda e, c=ch: inp(c))
for ch in '()':
    root.bind(ch, lambda e, c=ch: inp(c))
root.bind('^',lambda e: inp('^'))
root.bind('<Return>', lambda e:calculate())
root.bind('<BackSpace>', lambda e:delete_num())
root.bind('<Escape>', lambda e:clear_all())
#for binding buttons to numpad of keyboard
root.bind('<KP_Add>',      lambda e: inp('+'))
root.bind('<KP_Subtract>', lambda e: inp('-'))
root.bind('<KP_Multiply>', lambda e: inp('*'))
root.bind('<KP_Divide>',   lambda e: inp('/'))
#for x in ['Add','Subtract,'Multiply','Divide']: root.bind('<KP_{x}>, lambda e: imp('y'))
root.bind('<KP_Enter>',    lambda e: calculate())
for ch in '0123456789':
    root.bind(f'<KP_{ch}>', lambda e, c=ch: inp(c))
e.focus_set()


root.mainloop()
