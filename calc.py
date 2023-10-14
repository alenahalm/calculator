from tkinter import *
from tkinter import ttk
from functools import partial

calcs = []

ops = ['+', '-', '*', '/']

def get_memory():
    newWindow = Toplevel(root)
    newWindow.title("Memory")
    newWindow.geometry("400x600")
    
    calculations = Text(master=newWindow, font="Segoe 20", height=80)
    calculations.pack()
    copy = calcs.copy()
    copy.reverse()
    for each in copy:
        for i in range(len(each)-1):
            calculations.insert(END, each[i])
        calculations.insert(END, '=')
        calculations.insert(END, each[-1])
        calculations.insert(END, '\n')
    calculations.config(state=DISABLED)


def key_press(event):
    key = event.char
    code = event.keycode
    if code == 13:
        click_button('=')
    elif code == 8:
        click_button('<-')
    else:
        click_button(key)

def click_button(btn_id: str):

    if len(calcs) == 0:
        if btn_id.isdigit() or btn_id == '.':
            output(btn_id)
            calcs.append([btn_id])
        
    elif btn_id.isdigit() or btn_id == '.':
        out = True
        match len(calcs[-1]):
            case 1 | 3:
                if calcs[-1][-1] == '0' and btn_id == '0' or '.' in calcs[-1][-1] and btn_id == '.':
                    out = False
                elif calcs[-1][-1] == '0' and btn_id != '0':
                    out = True
                    clear()
                    calcs[-1][-1] = btn_id
                elif calcs[-1][-1][-1] == '.' and btn_id != '.':
                    out = True
                    calcs[-1][-1] += btn_id
                else:
                    calcs[-1][-1] += btn_id
            case 2:
                calcs[-1].append(btn_id)
            case 4:
                calcs.append([btn_id])
                clear(True)
        if out:
            output(btn_id)

    elif btn_id in ops:
        match len(calcs[-1]):
            case 1:
                calcs[-1].append(btn_id)
            case 2:
                clear()
                calcs[-1][-1] = btn_id
            case 3:
                clear(True)
                calcs[-1].append(operand_calc())
                calcs.append([calcs[-1][-1], btn_id])
            case 4:
                calcs.append([calcs[-1][-1], btn_id])
                clear(True)
                output(calcs[-1][-2])
        output(btn_id)

    elif btn_id == '=':
        match len(calcs[-1]):
            case 1:
                output("="+calcs[-1][0])
                fill('=')
                calcs[-1].append(calcs[-1][0])
            case 2:
                output(calcs[-1][0])
                calcs[-1].append(calcs[-1][0])
                click_button('=')
            case 3:
                output("=")
                calcs[-1].append(operand_calc())
            case 4:
                if calcs[-1][1] != calcs[-1][2]:
                    clear(True)
                    calcs.append([calcs[-1][-1], calcs[-1][1], calcs[-1][2]])
                    output(calcs[-1][0] + calcs[-1][1] + calcs[-1][2])
                    click_button('=')

    elif btn_id == 'C':
        if len(calcs) > 0:
            del calcs[-1]
        clear(True)
    
    elif btn_id == '<-':
        match len(calcs[-1]):
            case 1 | 3:
                if len(calcs[-1][-1]) == 1:
                    del calcs[-1][-1]
                else:
                    calcs[-1][-1] = calcs[-1][-1][:-1]
                clear()
            case 4:
                clear(True)

    elif btn_id == "sqrt":
        match len(calcs[-1]):
            case 1:
                clear(True)
                output("sqrt(" + calcs[-1][0] + ")")
                fill('sqrt')
                calcs[-1].append(sqrt(calcs[-1][0]))
                output("=" + calcs[-1][-1])
            case 2:
                output("sqrt(" + calcs[-1][0] + ")=")
                calcs[-1].append(sqrt(calcs[-1][0]))
                num = operand_calc()
                calcs[-1].append(num)
            case 3:
                clear(True)
                output(calcs[-1][0] + calcs[-1][1])
                calcs[-1][-1] = sqrt(calcs[-1][-1])
                output(calcs[-1][-1])
                # click_button("sqrt")
            case 4:
                clear(True)
                output(calcs[-1][-1])
                calcs.append([calcs[-1][-1]])
                click_button("sqrt")

    elif btn_id == "%":
        match len(calcs[-1]):
            case 1:
                clear(True)
                output('0')
            case 2:
                calcs[-1].append(percent(calcs[-1][0], calcs[-1][0]))
                output(calcs[-1][-1])
                click_button("=")
            case 3:
                length = len(calcs[-1][-1])
                num = calcs[-1][-1]
                for _ in range(length):
                    clear()
                del calcs[-1][-1]
                calcs[-1].append(percent(num, calcs[-1][0]))
                output(calcs[-1][-1])
                click_button("=")
            case 4:
                clear(True)
                resp = percent(calcs[-1][-1], calcs[-1][-1])
                output(resp)
                calcs.append([calcs[-1][-1], "%", "%", resp])

def fill(character):
    calcs[-1].append(character)
    calcs[-1].append(character)

def sqrt(character):
    result = str(float(character)**0.5)
    if result[-2:] == '.0':
        result = result[:-2]
    return result

def percent(num, percent):
    return str(float(num) / 100 * float(percent))

def operand_calc():
    n1, op, n2 = calcs[-1]
    n1 = float(n1)
    n2 = float(n2)
    result = ''
    match op:
        case '+':
            result = n1 + n2
        case '-':
            result = n1 - n2
        case '*':
            result = n1 * n2
        case '/':
            result = n1 / n2
    result = str(result)
    if result[-2:] == '.0':
        result = result[:-2]
    output(result)
    return result

def clear(all=False):
    txt.config(state=NORMAL)
    if all:
        txt.delete('1.0', END)
    else:
        txt.delete("end-2c")
    txt.config(state=DISABLED)

def output(character):
    txt.config(state=NORMAL)
    txt.insert(END, character)
    txt.config(state=DISABLED)

root = Tk()
root.title("Calculator")
root.geometry("400x600")

txt = Text(font="Segoe 25", height=6, state=DISABLED)
txt.grid(row=0, column=0, padx=0, pady=20, columnspan=4)

buttons = [
    ['C', '%', 'sqrt', '<-'],
    ['7', '8', '9', '*'],
    ['4','5','6','-'],
    ['1','2','3','+'],
    ['0','.','/','=']
]

mmr_btn = Button(text='journal', command=get_memory)
mmr_btn.place(x=0, y=0)

for r in range(len(buttons) + 1):
    root.columnconfigure(index=r, weight=1)
    root.rowconfigure(index=r, weight=1)

for r in range(len(buttons)):
    for c in range(len(buttons[r])):
        name = buttons[r][c]
        btn = ttk.Button(text=name, command=partial(click_button, name))
        btn.grid(row=r+1, column=c, ipadx=8, ipady=8, padx=2, pady=2, sticky=NSEW)

def close(_):
    root.destroy()

root.bind('<BackSpace>', key_press)
root.bind('<KeyPress>', key_press)
root.bind('<Escape>', close)


root.mainloop()
