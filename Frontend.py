from tkinter import *
from PIL import ImageTk, Image
import json
import math 
import tkinter.messagebox as mb






choosen_car = None
choosen_weather = None
choosen_color = "White"
choosen_ground = None
choosen_height = None
car_text = None

def height_choice(choice_height):
    global choosen_height
    choosen_height = choice_height
    print(choosen_height)
    add_height = Label(window, text=str(choosen_height)+" м", font = "Impact 14", width = 10, height=4, background="white", relief=FLAT, justify=CENTER)
    add_height.place(x = 1400, y = 430)
    

def ground_choice(ground):
    global choosen_ground
    choosen_ground = ground
    add_ground = Label(window, bd=0, relief=FLAT)
    add_ground.configure(image = grounds[ground+"_pic"])
    add_ground.place(x = 1400, y = 305)

def color_choice(color):
    global choosen_color, additions
    choosen_color = color
    various = dictionary[color]
    for i in range(len(various)):
        pics[i] = ImageTk.PhotoImage(Image.open(various[i]))
        cars[i].configure(image=pics[i])
    add_color = Label(window, background="white", fg="black", width=10, height=4, relief=FLAT, text=color.upper(), font = "Impact 14", justify=CENTER)
    add_color.place(x = 1400, y = 520)


def car_choice(car):
    global choosen_car, car_text, additions
    choosen_car = car
    for i in cars:
        if i is not car:
            i.configure(borderwidth=0)
        else:
            i.configure(borderwidth=4)
    if car is suv: car_text = "AUDI Q8"
    elif car is hatch: car_text = "Lexus UX"
    elif car is cross: car_text = "Toyota Rav-4"
    elif car is sport: car_text = "KIA Stinger"
    elif car is rio: car_text = "KIA Rio"
    elif car is granta: car_text = "Lada Granta"
    add_car = Label(window, width=10, height=4, background="white", foreground="black", text=car_text, font = "Impact 14", relief=FLAT, wraplength=60, justify=CENTER)
    add_car.place(x = 1400, y = 600)


def weather_choice(weather): 
    #port suv hatch cross rio granta
    global choosen_weather, additions
    choosen_weather = weather
    add_weather = Label(window, bd=0, relief=FLAT)
    add_weather.configure(image=weathers[weather+"_pic"])
    add_weather.place(x = 1400, y = 180)


def calculation(tm, gr, wt, car_width, car_height, car_long, cl):
    Eo = float(tm * cl)
    print("Eo: ", Eo)
    Ef =  float(tm * gr)
    print("Ef: ", Ef)
    focus =  float(50)
    print("Focus: ", focus)
    vv =  float(1/2.8)
    print("vv: ", vv)
    Eo =  float(wt * Eo * vv*vv/4)
    print("Eo: ", Eo)
    Ef =  float(wt * Ef * vv*vv/4)
    print("Ef: ", Ef)
    Nu =  float( float(choosen_height)/(2*focus* float(0.001)*math.sqrt(car_width*0.001*car_long*0.001)))
    print("Nu: ", Nu)
    x =  float(5*0.0001*Nu*(380+780)*pow(10, -9)/vv)
    print("x: ", x)
    Tv =  float(2/3.14*(math.acos(x)-x*math.sqrt(1-x*x)))
    print("Tv: ", Tv)
    Qe =  float(abs(Eo-Ef)*Tv*0.33/0.4)
    print("Qe: ", Qe)
    d =  float(4.53*pow(10, -6))
    print("d: ", d)
    sig =  float(d* float(choosen_height)/(focus*pow(10, -3)))
    print("sig: ", sig)
    Ne =  float(car_long/sig/1000)
    print("Ne: ", Ne)
    Qv =  float(Qe*Ne/math.sqrt(1+(Qe*Qe/(16*Ne*Ne))))
    print("Qv: ", Qv)
    pov = -0.623*math.pow(Qv-3.2, 2)
    print(pov)
    if Qv >= 3.2:
        res =  float(0.5*(1+math.sqrt(1-pow(2.73, pov))))
    else:
        res =  float(0.5*(1-math.sqrt(1-pow(2.73, pov))))
    print("res: ", res)
    
    return(res)

    


def result():
    print(additions)
    if any(additions) == None:
        mb.showinfo(message="Не все параметры выбраны!", title="Ошибка!")
        return()
    if (choosen_weather == "snow" or choosen_ground == "snowgr"):
        tm =  float(15)
    else:
        tm =  float(7)
    wt =  float(params[choosen_weather])
    gr =  float(params[choosen_ground])
    cl =  float(params[choosen_color])
    car_width =  float(dimensions[car_text]["width"])
    car_height =  float(dimensions[car_text]["height"])
    car_long =  float(dimensions[car_text]["long"])
    text = f"Длина авто: {round(car_long/1000, 2)}\nШирина авто: {round(car_width/1000, 2)}\nВысота авто:{round(car_height/1000, 2)}\n"
    text+=f"Вероятность обнаружения объекта составляет приблизительно {round(calculation(tm, gr, wt, car_width, car_height, car_long, cl)*100, 2)}%"
    mb.showinfo(title="Результат", message=text)
        


        


if __name__ == "__main__":


    with open ("pathes.json", "r") as file:
        dictionary = json.load(file)

    with open ("params.json", "r") as p:
        params = json.load(p)

    with open ("CarParams.json", "r") as c:
        dimensions = json.load(c)



    window = Tk()
    width= window.winfo_screenwidth()
    height= window.winfo_screenheight()
    window.geometry("%dx%d" % (width, height))
    window.configure(background="white")  
    
    weathers = {"snow_pic" : ImageTk.PhotoImage(Image.open("Pictures/Snow.png")), "sun_pic"  : ImageTk.PhotoImage(Image.open(dictionary["sun"])), "rain_pic" : ImageTk.PhotoImage(Image.open(dictionary["rain"])), "smoke_pic" : ImageTk.PhotoImage(Image.open(dictionary["smoke"]))}
    grounds = {"dirt_pic" : ImageTk.PhotoImage(Image.open(dictionary["dirt"])), "snowgr_pic" : ImageTk.PhotoImage(Image.open(dictionary["snowgr"])), "asphalt_pic" : ImageTk.PhotoImage(Image.open(dictionary["asphalt"])), "grass_pic" : ImageTk.PhotoImage(Image.open(dictionary["grass"]))}
    additions = []


    #PART 1----------------------------------------------------------------------------------------------------------------------------

    title1 = Label(window, text = "Выберите параметры", width=84, height=2, font="Impact 18", bg="white", fg="black", )
    title1.place(x=0, y=0)

    title2 = Label(window, text = "Итог:", width=12, height=6, font="Impact 18", bg="white", fg="black", wraplength=75, justify=LEFT)
    title2.place(x=1380, y = 0)
    
    sport_pic = ImageTk.PhotoImage(Image.open("Pictures\WhiteStinger.png"))
    sport = Button(window, image=sport_pic, width=498, height=218, relief=FLAT, bd=0)
    sport.configure(command=lambda: car_choice(sport))
    sport.place(x=2, y=90)

    suv_pic = ImageTk.PhotoImage(Image.open("Pictures\WhiteSUV.png"))
    suv = Button(window, image=suv_pic, width=498, height=218, relief=FLAT, bd=0)
    suv.configure(command = lambda: car_choice(suv))
    suv.place(x=2, y=315)

    rio_pic = ImageTk.PhotoImage(Image.open("Pictures\WhiteSedan.png"))
    rio = Button(window, image=rio_pic, width=498, height=218, relief=FLAT, bd=0)
    rio.configure(command=lambda: car_choice(rio))
    rio.place(x=2, y=541)

    granta_pic = ImageTk.PhotoImage(Image.open("Pictures\WhiteGranta.png"))
    granta = Button(window, image=granta_pic, width=498, height=218, relief=FLAT, bd=0)
    granta.configure(command = lambda: car_choice(granta))
    granta.place(x=506, y=90)

    cross_pic = ImageTk.PhotoImage(Image.open("Pictures\WhiteCross.png"))
    cross = Button(window, image=cross_pic, width=498, height=218, relief=FLAT, bd=0)
    cross.configure(command = lambda: car_choice(cross))
    cross.place(x=506, y=315)

    hatch_pic = ImageTk.PhotoImage(Image.open("Pictures\WhiteHatch.png"))
    hatch = Button(window, image=hatch_pic, width=498, height=218, relief=FLAT, bd=0)
    hatch.configure(command = lambda: car_choice(hatch))
    hatch.place(x=506, y=541)

    pics = [sport_pic, suv_pic, hatch_pic, cross_pic, rio_pic, granta_pic]
    cars = [sport, suv, hatch, cross, rio, granta]

#PART 2 ----------------------------------------------------------------------------------------------------------------------------


    sun_pic = ImageTk.PhotoImage(Image.open("Pictures\Sun.png"))
    sun = Button(window, image=sun_pic, width=98, height=98, relief=RAISED, bd=1)
    sun.configure(command=lambda: weather_choice("sun"))
    sun.place(x=1020, y=90)

    rain_pic = ImageTk.PhotoImage(Image.open("Pictures\Rain.png"))
    rain = Button(window, image=rain_pic, width=98, height=98, relief=RAISED, bd=1)
    rain.configure(command=lambda: weather_choice("rain"))
    rain.place(x=1160, y=90)

    snow_pic = ImageTk.PhotoImage(Image.open("Pictures\Snow.png"))
    snow = Button(window, image=snow_pic, width=98, height=98, relief=RAISED, bd=1)
    snow.configure(command=lambda: weather_choice("snow"))
    snow.place(x=1020, y=205)

    smoke_pic = ImageTk.PhotoImage(Image.open("Pictures\Smoke.png"))
    smoke = Button(window, image=smoke_pic, width=98, height=98, relief=RAISED, bd=1)
    smoke.configure(command=lambda: weather_choice("smoke"))
    smoke.place(x=1160, y=205)


#PART 3 -----------------------------------------------------------------------------------------------------------------------------

    helper_red = Label(window, background="#DCDCDC", width=14, height=6, relief=FLAT)
    helper_red.place(x=1020, y=318)
    red = Button(window, background="red", width=12, height=5, relief=RAISED, bd=4)
    red.configure(command=lambda: color_choice("red"))
    red.place(x=1023, y=321)


    helper_black = Label(window, background="#DCDCDC", width=14, height=6, relief=FLAT)
    helper_black.place(x=1160, y=318)
    black = Button(window, background="black", width=12, height=5, relief=RAISED, bd=4)
    black.configure(command=lambda: color_choice("black"))
    black.place(x=1163, y=321)

    helper = Label(window, background="#DCDCDC", width=14, height=6, relief=FLAT)
    helper.place(x=1020, y=433)
    white = Button(window, background="white", width=12, height=5, relief=RAISED, bd=4)
    white.configure(command=lambda: color_choice("white"))
    white.place(x=1023, y=436)

    helper_grey = Label(window, background="#DCDCDC", width=14, height=6, relief=FLAT)
    helper_grey.place(x=1160, y=433)
    grey = Button(window, background="grey", width=12, height=5, relief=RAISED, bd=4)
    grey.configure(command=lambda: color_choice("gray"))
    grey.place(x=1163, y=436)

#PART 4 -------------------------------------------------------------------------------------------------------------------------------

    asphalt_pic = ImageTk.PhotoImage(Image.open("Pictures\Asphalt.png"))
    asphalt = Button(window, image=asphalt_pic, width=98, height=98, relief=RAISED, bd=1)
    asphalt.configure(command=lambda: ground_choice("asphalt"))
    asphalt.place(x=1020, y=543)

    snowgr_pic = ImageTk.PhotoImage(Image.open("Pictures\SnowGR.png"))
    snowgr = Button(window, image=snowgr_pic, width=98, height=98, relief=RAISED, bd=1)
    snowgr.configure(command=lambda: ground_choice("snowgr"))
    snowgr.place(x=1160, y=543)

    grass_pic = ImageTk.PhotoImage(Image.open("Pictures\Grass.png"))
    grass = Button(window, image=grass_pic, width=98, height=98, relief=RAISED, bd=1)
    grass.configure(command=lambda: ground_choice("grass"))
    grass.place(x=1020, y=661)

    dirt_pic = ImageTk.PhotoImage(Image.open("Pictures\Dirt.png"))
    dirt = Button(window, image=dirt_pic, width=98, height=98, relief=RAISED, bd=1)
    dirt.configure(command=lambda: ground_choice("dirt"))
    dirt.place(x=1160, y=661)

#PART 5-----------------------------------------------------------------------------------------------------------------

    h = Scale(window, from_ = 1000, to = 50, length=400, width=30, relief=FLAT, bd=0)
    h.configure(orient=VERTICAL, resolution=50, activebackground="white", bg = "white", bd = 0, relief=FLAT, sliderlength=20)
    h.configure(font = "TimesNewRoman 12", fg = "black", highlightbackground="white", highlightcolor="gray", troughcolor="light gray")
    h.place(x = 1285, y = 90)

    height = Button(window, command=lambda: height_choice(h.get()), text="Выбрать Высоту", width=8, height=3, bg="white", bd = 1, relief=RAISED, font="TimesNewRoman 10", wraplength=75)
    height.place(x = 1305, y = 510)

#PART 6-------------------------------------------------------------------------------------------------------------------

    Result_pic = ImageTk.PhotoImage(Image.open("Pictures\play.png"))
    Result = Button(window, image=Result_pic, font="Impact 18", bg="white", fg="black", relief=FLAT, bd = 0, command=result)
    Result.place(x=1290, y = 630)



    window.mainloop()

