#importations
from zhdate import ZhDate as lunar_date
import turtle
from datetime import *
import os
from random import randint
#intializations
houclock=0
minclock=0
ifclock=0
#HELPfunctions
def skip(step):
    turtle.penup()
    turtle.forward(step)
    turtle.pendown()


def mkHand(name, length, size):
    turtle.reset()
    skip(-length * 0.1)
    turtle.begin_poly()
    turtle.pensize(size)
    turtle.forward(length * 1.1)
    turtle.end_poly()
    handForm = turtle.get_poly()
    turtle.register_shape(name, handForm)

#BELLfunction
def button(x, y):
    global houclock, minclock, ifclock
    if x < 20 and x > -20 and y < 350 and y > 250:
        if ifclock==1:
            ifdelete = turtle.textinput("闹钟","你已经有一个%d:%d的闹钟了哦~\n想删除闹钟输入1,否则不输入" % (houclock,minclock))
            if ifdelete == "1":
                houclock=0
                minclock=0
                ifclock=0
                turtle.textinput("闹钟","已删除闹钟！")
        else:
            houclock = int(turtle.textinput("闹钟", "几时："))
            minclock = turtle.textinput("闹钟", "几分：")
            if minclock=='00':
                minclock=0
            else:
                minclock=int(minclock)
            turtle.textinput("闹钟", "设定成功！")
            ifclock=1
    

#INITfuntion
def init():
    global secHand, minHand, houHand, printer, buttoner
    turtle.mode("logo")
    turtle.title("时钟")
    mkHand("secHand", 135, 10)
    mkHand("minHand", 125, 20)
    mkHand("houHand", 90, 30)
    buttoner = turtle.Turtle()
    buttoner.penup()
    buttoner.goto(0, 300)
    buttoner.write("闹钟", align="center", font=("Courier", 25, "bold"))
    buttoner.hideturtle()
    turtle.onscreenclick(button, 1, add=False)
    turtle.listen()
    secHand = turtle.Turtle()
    secHand.shape("secHand")
    minHand = turtle.Turtle()
    minHand.shape("minHand")
    houHand = turtle.Turtle()
    houHand.shape("houHand")
    for hand in secHand, minHand, houHand:
        hand.shapesize(1, 1, 3)
        hand.speed(0)
    printer = turtle.Turtle()
    printer.hideturtle()
    printer.penup()

#CLOCKfunction
def setupClock(radius):
    turtle.reset()
    turtle.hideturtle()
    turtle.pensize(7)
    for i in range(60):
        skip(radius)
        if i % 5 == 0:
            turtle.forward(20)
            skip(-radius - 20)
            skip(radius + 20)
            if i == 0:
                turtle.write(int(12), align="center",
                             font=("Courier", 14, "bold"))
            elif i == 30:
                skip(25)
                turtle.write(int(i/5), align="center",
                             font=("Courier", 14, "bold"))
                skip(-25)
            elif (i == 25 or i == 35):
                skip(20)
                turtle.write(int(i/5), align="center",
                             font=("Courier", 14, "bold"))
                skip(-20)
            else:
                turtle.write(int(i/5), align="center",
                             font=("Courier", 14, "bold"))
            skip(-radius - 20)
        else:
            turtle.dot(5)
            skip(-radius)
        turtle.right(6)

#TIMEfunctions
def week(t):
    week = ["星期一\nMonday", "星期二\nTuesday", "星期三\nWednesday",
            "星期四\nThursday", "星期五\nFriday", "星期六\nSaturday", "星期日\nSunday"]
    return week[t.weekday()]


def date(t):
    y = t.year
    m = t.month
    d = t.day
    return "%s/%d/%d" % (y, m, d)


def ndate(t):
    y = t.year
    m = t.month
    d = t.day
    return lunar_date.from_datetime(datetime(y, m, d))

#TICKfunction
def tick():
    global houclock,minclock,ifclock
    t = datetime.today()
    second = t.second + t.microsecond * 0.000001
    minute = t.minute + second / 60.0
    hour = t.hour + minute / 60.0
    secHand.pensize(10)
    secHand.setheading(6 * second)
    minHand.pensize(20)
    minHand.setheading(6 * minute)
    houHand.pensize(30)
    houHand.setheading(30 * hour)
    turtle.tracer(False)
    printer.forward(65)
    printer.write(week(t), align="center",
                  font=("Courier", 14, "bold"))
    printer.back(130)
    printer.write(date(t), align="center",
                  font=("Courier", 14, "bold"))
    printer.back(20)
    printer.write(ndate(t), align="center",
                  font=("Courier", 14, "bold"))
    printer.home()
    if houclock == datetime.today().hour and minclock == datetime.today().minute and ifclock == 1:
        os.system("start "+os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\src\%d.mp3" % randint(1,3))
        turtle.textinput("闹钟", "时间到啦！")
        ifclock = 0
    turtle.tracer(True)
    turtle.ontimer(tick, 100)

#theMAINfunction
def main():
    turtle.tracer(False)
    init()
    setupClock(160)
    turtle.tracer(True)
    tick()
    print("Clock is Spawned")
    turtle.mainloop()

