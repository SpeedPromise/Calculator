"""
Project:
        tkinter 计算器

Author:
        Hyacinth
"""
import math
from tkinter import *


class Calculator():

    def __init__(self):

        self.root = Tk()
        self.root.resizable(width=False, height=False)
        self.is_calc = False  # 是否按下运算符
        self.is_end = False  # 是否运算结束
        self.memory = 0  # 存储器
        self.MAXLENGTH = 18  # 最多显示字符数
        self.stack = []  # 运算表达式
        self.expression = StringVar()  # 算数表达式
        self.curr = StringVar()  # 当前显示数字
        self.curr.set('0')

    # 按下数字键（0-9）
    def pressNumber(self, number):
        if self.is_calc or self.curr.get() == '0':
            self.curr.set(number)
            self.is_calc = False
        else:
            if len(self.curr.get()) < self.MAXLENGTH:
                self.curr.set(self.curr.get() + number)
        self.is_end = False

    # 按下小数点
    def pressDP(self):
        if '.' not in self.curr.get():
            self.curr.set(self.curr.get() + '.')

    # 答案修正
    def modifyResult(self, result):
        # 只取整数，判断是否超过显示长度
        result = str(result)
        if len(result) > self.MAXLENGTH:
            if len(result.split('.')[0]) > self.MAXLENGTH:
                result = 'Overflow'
            else:
                result = result[:self.MAXLENGTH]
        return result

    @staticmethod
    def str2digit(x):
        return float(x) if '.' in x else int(x)

    # 运算符
    def pressOperator(self, oprator):
        if oprator == 'MC':
            self.memory = 0
        elif oprator == 'MR':
            self.curr.set(str(self.memory))
            self.is_calc = True
        elif oprator == 'MS':
            self.memory = Calculator.str2digit(self.curr.get())
            self.is_calc = True
        elif oprator == 'M+':
            self.memory = eval(str(self.memory) + '+' + self.curr.get())
            self.is_calc = True
        elif oprator == 'M-':
            self.memory = eval(str(self.memory) + '-' + self.curr.get())
            self.is_calc = True
        elif oprator == 'del':
            if not self.is_calc:
                tmp = self.curr.get()
                if tmp != '0' and len(tmp) > 1:
                    self.curr.set(tmp[:-1])
                else:
                    self.curr.set('0')
        elif oprator == 'CE':
            self.curr.set('0')
        elif oprator == 'C':
            self.stack.clear()
            self.expression.set('')
            self.curr.set('0')
            self.is_calc = False
        elif oprator == 'x^2':
            tmp = str(int(math.pow(Calculator.str2digit(self.curr.get()), 2)))
            self.curr.set(tmp)
        elif oprator == 'sqrt':
            tmp = str(math.sqrt(Calculator.str2digit(self.curr.get())))
            self.curr.set(tmp)
        elif oprator in ['+', '-', '*', '/', '%']:
            if self.is_calc:
                self.stack.pop()
                self.stack.append(oprator)
            self.stack.append(self.curr.get())
            self.stack.append(oprator)
            self.is_calc = True
        elif oprator == '=':
            if self.is_end:
                self.expression.set('')
                self.curr.set('0')
                return
            # 如果前一个为运算符（非平方和开方），则默认添加使用内存数据
            self.stack.append(
                str(self.memory) if self.is_calc and not self.is_end else self.curr.get())
            self.expression.set(''.join(self.stack))
            eval_expression = ''.join(self.stack)
            try:
                result = eval(eval_expression)
            except Exception:
                result = 'illegal expression'
            result = self.modifyResult(result)
            self.curr.set(result)
            self.stack.clear()
            self.is_calc = True
            self.is_end = True
            return
        else:
            pass
        self.expression.set(''.join(self.stack))

    def Frame(self):
        self.root.minsize(320, 420)
        self.root.title('Calculator')

        # 显示框
        label = Label(self.root, textvariable=self.expression, bg='black',
                      anchor='e', fg='white', font=('楷体', 16))
        label.place(x=20, y=10, width=280, height=40)
        label = Label(self.root, textvariable=self.curr, bg='black',
                      anchor='e', fg='white', font=('楷体', 20))
        label.place(x=20, y=50, width=280, height=50)

        # 功能区：Memory clear/read/save/+/-
        button1_1 = Button(text='MC', bg='#666', bd=2,
                           command=lambda: self.pressOperator('MC'))
        button1_1.place(x=20, y=110, width=50, height=35)
        button1_2 = Button(text='MR', bg='#666', bd=2,
                           command=lambda: self.pressOperator('MR'))
        button1_2.place(x=77.5, y=110, width=50, height=35)
        button1_3 = Button(text='MS', bg='#666', bd=2,
                           command=lambda: self.pressOperator('MS'))
        button1_3.place(x=135, y=110, width=50, height=35)
        button1_4 = Button(text='M+', bg='#666', bd=2,
                           command=lambda: self.pressOperator('M+'))
        button1_4.place(x=192.5, y=110, width=50, height=35)
        button1_5 = Button(text='M-', bg='#666', bd=2,
                           command=lambda: self.pressOperator('M-'))
        button1_5.place(x=250, y=110, width=50, height=35)

        button2_1 = Button(text='del', bg='#666', bd=2,
                           command=lambda: self.pressOperator('del'))
        button2_1.place(x=20, y=155, width=50, height=35)
        button2_2 = Button(text='CE', bg='#666', bd=2,
                           command=lambda: self.pressOperator('CE'))
        button2_2.place(x=77.5, y=155, width=50, height=35)
        button2_3 = Button(text='C', bg='#666', bd=2,
                           command=lambda: self.pressOperator('C'))
        button2_3.place(x=135, y=155, width=50, height=35)
        button2_4 = Button(text='x^2', bg='#666', bd=2,
                           command=lambda: self.pressOperator('x^2'))
        button2_4.place(x=192.5, y=155, width=50, height=35)
        button2_5 = Button(text='sqrt', bg='#666', bd=2,
                           command=lambda: self.pressOperator('sqrt'))
        button2_5.place(x=250, y=155, width=50, height=35)

        # 数字及运算符
        button3_1 = Button(text='7', bg='#bbb', bd=2,
                           command=lambda: self.pressNumber('7'))
        button3_1.place(x=20, y=200, width=50, height=35)
        button3_2 = Button(text='8', bg='#bbb', bd=2,
                           command=lambda: self.pressNumber('8'))
        button3_2.place(x=77.5, y=200, width=50, height=35)
        button3_3 = Button(text='9', bg='#bbb', bd=2,
                           command=lambda: self.pressNumber('9'))
        button3_3.place(x=135, y=200, width=50, height=35)
        button3_4 = Button(text='/', bg='#708069', bd=2,
                           command=lambda: self.pressOperator('/'))
        button3_4.place(x=192.5, y=200, width=50, height=35)
        button3_5 = Button(text='%', bg='#708069', bd=2,
                           command=lambda: self.pressOperator('%'))
        button3_5.place(x=250, y=200, width=50, height=35)

        button4_1 = Button(text='4', bg='#bbb', bd=2,
                           command=lambda: self.pressNumber('4'))
        button4_1.place(x=20, y=245, width=50, height=35)
        button4_2 = Button(text='5', bg='#bbb', bd=2,
                           command=lambda: self.pressNumber('5'))
        button4_2.place(x=77.5, y=245, width=50, height=35)
        button4_3 = Button(text='6', bg='#bbb', bd=2,
                           command=lambda: self.pressNumber('6'))
        button4_3.place(x=135, y=245, width=50, height=35)
        button4_4 = Button(text='*', bg='#708069', bd=2,
                           command=lambda: self.pressOperator('*'))
        button4_4.place(x=192.5, y=245, width=50, height=35)
        button4_5 = Button(text='1/x', bg='#708069', bd=2,
                           command=lambda: self.pressOperator('1/x'))
        button4_5.place(x=250, y=245, width=50, height=35)

        button5_1 = Button(text='3', bg='#bbb', bd=2,
                           command=lambda: self.pressNumber('3'))
        button5_1.place(x=20, y=290, width=50, height=35)
        button5_2 = Button(text='2', bg='#bbb', bd=2,
                           command=lambda: self.pressNumber('2'))
        button5_2.place(x=77.5, y=290, width=50, height=35)
        button5_3 = Button(text='1', bg='#bbb', bd=2,
                           command=lambda: self.pressNumber('1'))
        button5_3.place(x=135, y=290, width=50, height=35)
        button5_4 = Button(text='-', bg='#708069', bd=2,
                           command=lambda: self.pressOperator('-'))
        button5_4.place(x=192.5, y=290, width=50, height=35)
        button5_5 = Button(text='=', bg='#708069', bd=2,
                           command=lambda: self.pressOperator('='))
        button5_5.place(x=250, y=290, width=50, height=80)

        button6_1 = Button(text='0', bg='#bbb', bd=2,
                           command=lambda: self.pressNumber('0'))
        button6_1.place(x=20, y=335, width=107.5, height=35)
        button6_2 = Button(text='.', bg='#bbb', bd=2,
                           command=lambda: self.pressDP())
        button6_2.place(x=135, y=335, width=50, height=35)
        button6_3 = Button(text='+', bg='#708069', bd=2,
                           command=lambda: self.pressOperator('+'))
        button6_3.place(x=192.5, y=335, width=50, height=35)

        self.root.mainloop()

    def run(self):
        self.Frame()


if __name__ == '__main__':
    calculator = Calculator()
    calculator.run()
