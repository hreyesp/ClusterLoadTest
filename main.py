import subprocess
import pandas as pd
import numpy as np
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk
from cluster import *
from regresion import *

## Tipo de peticiones y clusters
values = ["Secuenciales", "Concurrentes"]
values2 = ["2", "3"]

## Proceso botón "Iniciar"
def Main():
    txt.delete("1.0", tk.END)
    txtpor.delete("1.0", tk.END)
    if (str(url.get()) == "" or str(pet.get()) == ""):
        print(messagebox.showinfo(message="Complete todos los campos", title="Alerta"))
    else:
        try:
            peti = int(pet.get())
            if (combo.get() == values[0]):

                ## Configurar barra de progreso
                Progressbar = ttk.Progressbar(tab1, mode="indeterminate")
                Progressbar.place(x=275, y=490, width=200)
                msj = tk.Label(tab1, text="Cargando Resultados...")
                msj.place(x=295, y=455)

                ##Procesamiento de datos y Control de excepciones
                try:
                    p = subprocess.Popen("ab -n " + pet.get() + " -e datos.csv " + url.get(), shell=True,
                                         stdout=subprocess.PIPE, universal_newlines=True)
                    Progressbar.start(18)
                    while p.poll() is None:
                        tab1.update()
                    Progressbar.stop()
                    Progressbar.destroy()
                    msj.destroy()
                    res = p.communicate()[0]
                    if (res == ""):
                        print(messagebox.showinfo(message="La URL ingresada es incorrecta!", title="Alerta"))
                    else:
                        txt.delete("1.0", tk.END)
                        txt.insert(tk.END, res)
                        txtpor.delete("1.0", tk.END)
                        datos = pd.read_csv("datos.csv", names=["porc", "tiempo"], delimiter=",", header=0)
                        datos = datos.drop([95, 96, 97, 98, 99])
                        pd.set_option('display.max_rows', datos.shape[0] + 1)
                        txtpor.insert(tk.END, datos)
                        clustering(datos, str(combo2.get()), tabControl2, clus1)
                        tabControl.tab(1, state='normal')
                except Exception as e:
                    print(messagebox.showinfo(message="Error al procesar la URL ingresada!", title="Alerta"))
            else:

                ## Configurar barra de progreso
                Progressbar = ttk.Progressbar(tab1, mode="indeterminate")
                Progressbar.place(x=275, y=490, width=200)
                msj = tk.Label(tab1, text="Cargando Resultados...")
                msj.place(x=295, y=455)

                ##Procesamiento de datos y Control de excepciones
                try:
                    p = subprocess.Popen("ab -n " + pet.get() + " -c " + pet.get() + " -e datos.csv " + url.get(),
                                         shell=True, stdout=subprocess.PIPE, universal_newlines=True)
                    Progressbar.start(15)
                    while p.poll() is None:
                        tab1.update()
                    Progressbar.stop()
                    Progressbar.destroy()
                    msj.destroy()
                    res = p.communicate()[0]
                    print(res)

                    if (res == ""):
                        print(messagebox.showinfo(message="La URL ingresada es incorrecta!", title="Alerta"))
                    else:
                        txt.delete("1.0", tk.END)
                        txt.insert(tk.END, res)
                        txtpor.delete("1.0", tk.END)
                        datos = pd.read_csv("datos.csv", names=["porc", "tiempo"], delimiter=",", header=0)
                        datos = datos.drop([95, 96, 97, 98, 99])
                        pd.set_option('display.max_rows', datos.shape[0] + 1)
                        txtpor.insert(tk.END, datos)
                        regresion(datos, regr, tabControl2)
                        tabControl.tab(1, state='normal')

                except subprocess.CalledProcessError as e:
                    print(messagebox.showinfo(message="Error al momento de procesar URL!!", title="Alerta"))
        except ValueError:
            print(messagebox.showinfo(message="Error en número de peticiones!", title="Alerta"))


def centroides():
    centr = clustering.centroides
    cade = ""
    for i,val in enumerate(centr):
        cade += "Centroide " + str(i+1) + " " + str(np.round(val, 2)) + "\n"
    messagebox.showinfo(message=cade, title="Mostrar Centroides")

## Habilitar elección clústeres (solo al escoger peticiones secuenciales)
def eventCombo():
    if (combo.get() == values[0]):
        combo2.configure(None, state="readonly")
    else:
        combo2.configure(None, state="disabled")


root = tk.Tk()
root.title("Pruebas de Carga - Regresión y Clustering")
root.eval('tk::PlaceWindow . center')
root.geometry("800x550")

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

#Control de Pestañas
tabControl.add(tab1, text='Menú Principal')
tabControl.add(tab2, text='Gráficos Regresión y Clústeres')
tabControl.pack(expand=1, fill="both")

#Subpestañas de la sección de gráficos
tabControl2 = ttk.Notebook(tab2)
regr = ttk.Frame(tabControl2)
clus1 = ttk.Frame(tabControl2)
tabControl2.add(regr, text='Regresión')
tabControl2.add(clus1, text='Clústeres')
tabControl2.pack(expand=1, fill="both")

tk.Label(tab1, text="Página Web (Agregar '/' al final)").place(x=50, y=35)
url = tk.Entry(tab1, width=33, text="")
url.place(x=50, y=60)
url.insert(tk.END, "")

## Seleccion del tipo de peticiones
tk.Label(tab1, text="Tipo de Peticiones").place(x=50, y=90)
combo = ttk.Combobox(tab1, state="readonly", width=14, values=values)
combo.bind("<<ComboboxSelected>>", lambda _: eventCombo())
combo.grid(column=1, row=1)
combo.place(x=180, y=90)
combo.current(0)

##Selección de Clústeres
tk.Label(tab1, text="# Clústeres").place(x=410, y=90)
combo2 = ttk.Combobox(tab1, state="readonly", width=8, values=values2)
combo2.grid(column=1, row=1)
combo2.place(x=510, y=90)
combo2.current(0)

##Campo para digitar número de peticiones
tk.Label(tab1, text="# Peticiones").place(x=410, y=60)
pet = tk.Entry(tab1, width=8, text="")
pet.place(x=520, y=60)
pet.insert(tk.END, "")

#Botón iniciar
btn = tk.Button(tab1, command=Main, text="Iniciar")
btn.place(x=640, y=65)

#Botón para mostrar centroides
btn = tk.Button(clus1, command=centroides, text="Mostrar centroides")
btn.place(x=340, y=5)


## Obtención de resultados de Apache Benchmark
tk.Label(tab1, text="Resultados ApacheBenchmark").place(x=110, y=145)
txt = scrolledtext.ScrolledText(tab1, width=40, height=16)
txt.place(x=50, y=175)

tk.Label(tab1, text="Tiempos y porcentajes de carga").place(x=440, y=145)
txtpor = scrolledtext.ScrolledText(tab1, width=25, height=16)
txtpor.place(x=440, y=175)

tabControl.tab(1, state='disabled')
tk.mainloop()
