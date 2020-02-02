import Face_Rec
import cv2
from tkinter import *
from PIL import Image, ImageTk
import fnmatch
import os

# Обновляем ImageLabel каждые 34мс/30fps
def callback():
    # Получаем кортеж возвращаемых значений
    frame, name= Face_Rec.video()
    # Декодируем изображение и обновляем ImageLabel родителя
    img2 = ImageTk.PhotoImage(image=Image.fromarray(frame))
    Output_Frame.configure(image=img2)
    Output_Frame.image = img2
    # Запускаем функцию каждые 34мс
    Main.after(34, callback)

# Сохраняем лицо
def Save_Snap(frame, Name):
    # Получаем длинну всех .jpg файлов в дериктории
    fName = len(fnmatch.filter(os.listdir("/Users/safindaniil/PycharmProjects/Visible/Face/"), '*.jpg'))+1
    # Сохраняем фото лица в формате "Номер_Имя.jpg"
    cv2.imwrite(str(fName)+'_'+str(Name.get())+".jpg",cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

# Создаем новое окно для предпросмотра и заполнения данных
def FaceSnap():
    # Инициализируем новое окно и присваиваем имя заголовка
    SF = Toplevel()
    SF.title("Preview save snap")
    # Делаем "снимок" с WebCam
    Cheezz = cv2.VideoCapture(0)
    ret, frame = Cheezz.read()
    # Закрываем поток
    Cheezz.release()
    # Декодируем изображения
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    previmg = ImageTk.PhotoImage(Image.fromarray(frame))
    # Создаем ImageLabel для вывода декодированного изображения
    Preview = Label(SF, image=previmg)
    Preview.pack()
    # Создает "textbox" для ввода информации о новой персоне
    Name_Entry = Entry(SF)
    Name_Entry.pack(side="bottom")
    # Просто TextLabel
    Name_label = Label(SF, text="Enter your Name")
    Name_label.pack(side="bottom")
    # Кнопка для подтвержения и сохранения получившегося результата
    Add_Person = Button(SF, text="Confirm snap!", width=25,command=lambda: Save_Snap(frame, Name_Entry))
    Add_Person.pack(side="bottom")
    # Запуск нового окна
    SF.mainloop()

# Добавляем в список каждого распознанного человека
def listbox_update():
    # Получаем кортеж возвращаемых значений
    frame, name= Face_Rec.video()
    l=listbox.size()
    str="Unknown"
    print (l)
    for i in range(1,l):
        print(listbox.get(i))
        str+=listbox.get(i)
    str.lower()
    for i in range (0,len(name)):
        if(str.find(name[i])<0):
            listbox.insert(END,name[i])
    Main.after(1500,listbox_update)

# "Родитель" формы
Main = Tk()
Main.title("Face Recognition")
Main.geometry('800x360')
# Получаем кортеж возвращаемых значений
frame,name=Face_Rec.video()
# Декодируем изображения
im = Image.fromarray(frame)
img = ImageTk.PhotoImage(image=im)
# Создаем ImageLabel для вывода декодированного изображения
Output_Frame = Label(Main, image=img, width=640, height=360)
Output_Frame.pack(side="left", fill="both", expand="yes")
# Создаем кнопку для добавления "обьекта" распознованя
Preview = Button(Main, text="Add new person", width=25, command=FaceSnap)
Preview.pack(side="bottom")
# Создаем список для записи всех идентифицированных "обьектов"
listbox=Listbox(Main)
listbox.pack(side="right", ipady=80)
listbox.insert(END,"Tut?")
# Запуск "Родителя"
Main.after_idle(callback)
Main.after_idle(listbox_update)
Main.mainloop()