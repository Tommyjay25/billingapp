# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 13:59:46 2021

@author: tomas.guzman
"""
from datetime import datetime
from kivymd.app import MDApp
from kivymd.uix.list import MDList
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem,TwoLineListItem,ThreeLineListItem
from kivy.lang import Builder
import random as rnd
from kivy.uix.button import Button
import pandas as pd
import sqlite3 as sql
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class InventarioApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "App Inventario"
        super().__init__(**kwargs)
        self.kv = Builder.load_file('Robertapp.kv')

        Meses=("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto",
               "Septiembre","Octubre","Noviembre","Diciembre")
        menu_meses = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.menu_callback(x),
            } for i in Meses
        ]
        self.menumes = MDDropdownMenu(
            caller=self.kv.ids.mes,
            items=menu_meses,
            width_mult=4,
        )
        """menu_meses2 = [
            {
                "text": f"{j}",
                "viewclass": "OneLineListItem",
                "on_release": lambda y=f"{j}": self.menu_callback2(y),
            } for j in Meses
        ]
        self.menumes2 = MDDropdownMenu(
            caller=self.kv.ids.mes2,
            items=menu_meses2,
            width_mult=4,
        )
        
    """
    """Este metodo sirve para llamar los meses que se encuentran en la pagina 
    de reportes"""
    def menu_callback2(self,y):
        self.root.ids.mes2.text=y
        self.menumes2.dismiss()

    def menu_callback(self, x):
        self.root.ids.mes.text = x
        self.menumes.dismiss()
    """Este metodo sera utilizado para entrar a la pagina principal y destruir scrollview existente"""
    def pagprincipal(self):
        self.root.current="Pantalla principal"
    """En este metodo se abre la hoja del inventario junto con el reporte en un scrollview"""
    def abririnv(self):
        self.root.current="Hoja de inventario"
        self.inventario=MDList()
        conn=sql.connect("Reportes.db")
        cur=conn.cursor()
        cur.execute("SELECT * FROM inventario")
        self.articulos=cur.fetchall()
        for self.articulo in self.articulos:
            self.inventario.add_widget(ThreeLineListItem(text=f"{self.articulo[0]}",
                                                         secondary_text=f"precio {self.articulo[2]}, cantidad en inventario {self.articulo[1]}",
                                                         tertiary_text=f"Tipo de mercancia {self.articulo[7]}",on_release=self.cantidadasacar))
        self.root.ids.listinventario.add_widget(self.inventario)
        
        conn.commit()
        conn.close()
    """Este metodo se utilizara para actualizar la pagina cada vez que se salga de la pagina de inventario"""
    def destroyinv(self):
        self.root.ids.listinventario.remove_widget(self.inventario)
        self.pagprincipal()
    """En este metodo se actualiza la hoja de agregar al inventario"""    
    def pagagregar(self):
        self.root.ids.listinventario.remove_widget(self.inventario)
        self.root.current = "Articulos inventario"
    """Este metodo funciona para abrir un popup cuando se le da a un articulo en inventario"""
    def cantidadasacar(self,instance):
        conn=sql.connect("Reportes.db")
        cur=conn.cursor()
        self.content=BoxLayout(size_hint=(0.8,0.8))
        self.labelcantidad=Label(size_hint=(0.1,0.05),text=instance.text,color=(0,0,0,1))
        """Aqui habria que agregarle mas informacion sobre el producto"""
        self.cantidadentrada=TextInput(size_hint=(0.07,0.11))
        self.content.add_widget(self.cantidadentrada)
        self.content.add_widget(self.labelcantidad)
        self.botonaceptar=MDFlatButton(text="Aceptar", 
                                       text_color=self.theme_cls.primary_color,
                                       on_release=self.aceptarcantidad)
        
        self.botoncancel=MDFlatButton(text="Cancelar", 
                                      text_color=self.theme_cls.primary_color,
                                       on_release=self.cancelcantidad)
        self.popupcant=MDDialog(title="Introduzca la cantidad",
                                buttons=[self.botonaceptar,self.botoncancel],
                                size_hint=(0.7,0.7), pos_hint={"x":0.15,"y":0.15},
                                )
        
        self.popupcant.add_widget(self.content)
        self.root.ids.inventario.add_widget(self.popupcant)
    def cancelcantidad(self,intance):
        self.root.ids.inventario.remove_widget(self.popupcant)
    """Este metodo sera para aceptar la cantidad y la informacion seleccionada en el inventario"""    
    def aceptarcantidad(self,instance):
        
        self.cantidadentrada.text
        self.labelcantidad.text
        self.root.ids.inventario.remove_widget(self.popupcant)
        """Al codigo hay que agregarle una forma de guardar 
        la informacion que aparece en el popupdialog"""
        conn=sql.connect("Reportes.db")
        cur=conn.cursor()
        cur.execute(f"""SELECT cantidad FROM inventario WHERE articulo="{self.labelcantidad.text}";""")  
        c=cur.fetchall()
        for cs in c:
            self.antiguacantidad=cs[0]
        cur.execute(f"""SELECT cantidad,precio FROM inventario WHERE articulo="{self.labelcantidad.text}";""")
        j=cur.fetchall()
        for i in j:
            a=int(int(self.cantidadentrada.text)*i[1])
            print(a)
        hoy=hoy=datetime.today()
        mes={1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",7:"Julio",8:"Agosto"
                ,9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"}
        cur.execute("""INSERT INTO entradas(entradas,dia,mes,
                                    año,Concepto_de_entradas) VALUES (?,?,?,?,?)""",
                        (int(a),hoy.strftime("%d"),mes.get(int(hoy.strftime("%m"))),hoy.strftime("%y"),
                         self.labelcantidad.text,
                         ))
        self.nuevacantidad=self.antiguacantidad-(int(self.cantidadentrada.text))
        if self.nuevacantidad>=0:
            cur.execute(f"""UPDATE inventario set cantidad="{self.nuevacantidad}" 
                        WHERE articulo="{self.labelcantidad.text}";""")
            self.destroyinv()          
        else:
            self.botonaceptarno=MDFlatButton(text="Aceptar", 
                                       text_color=self.theme_cls.primary_color,
                                       on_release=self.aceptarcantidadno)
            self.popupno=MDDialog(title="Inventario por debajo de cero",
                                buttons=[self.botonaceptarno],
                                size_hint=(0.7,0.7), pos_hint={"x":0.15,"y":0.15},
                                )
            self.root.ids.inventario.add_widget(self.popupno)          
        """Aqui abajo se pondra una restriccion para los valores menores a 0"""
        conn.commit()
        conn.close()
    """Este metodo se utiliza para darle a aceptar cuando se pase de la cantidad total"""
    def aceptarcantidadno(self,instance):
        self.root.ids.inventario.remove_widget(self.popupno)
    
    """Metodo para guardar en la base de datos las entradas hechas"""
    def savedbent(self):
        if self.root.ids.Entrada.text != "" or self.root.ids.conceptentrada.text != "":
            conn = sql.connect("Reportes.db")
            cur = conn.cursor()
            cur.execute("""INSERT INTO entradas(entradas,dia,mes,
                                    año,Concepto_de_entradas) VALUES (?,?,?,?,?)""",
                        (self.root.ids.Entrada.text, self.root.ids.dia.text,
                         self.root.ids.mes.text,
                         self.root.ids.año.text, self.root.ids.conceptentrada.text,
                         ))
            conn.commit()
            conn.close()
            self.root.ids.año.text = ""
            self.root.ids.dia.text = ""
            self.root.ids.Entrada.text = ""
            self.root.ids.conceptentrada.text = ""
    """Metodo que guarda la informacion de los gastos realizados"""        
    def savedbsalida(self):
        if self.root.ids.gastos.text != "" or self.root.ids.concetpgastos.text != "":
            conn = sql.connect("Reportes.db")
            cur = conn.cursor()
            cur.execute("""INSERT INTO gastos(gastos,dia,mes,
                                            año,Concepto_de_gastos) VALUES (?,?,?,?,?)""",
                        (self.root.ids.gastos.text, self.root.ids.dia.text,
                         self.root.ids.mes.text,
                         self.root.ids.año.text, self.root.ids.concetpgastos.text,
                         ))
            conn.commit()
            conn.close()
            self.root.ids.año.text = ""
            self.root.ids.dia.text = ""
            self.root.ids.gastos.text = ""
            self.root.ids.concetpgastos.text = ""
    """Estos son los productos que se tendran en inventario"""
    def insertinventario(self):
        if self.root.ids.Nombrearticulo.text and self.root.ids.Precio.text !="":
            hoy=datetime.today()
            mes={1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",7:"Julio",8:"Agosto"
                ,9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"}
            conn=sql.connect("Reportes.db")
            cur=conn.cursor()
            cur.execute("""INSERT INTO inventario(Articulo,Cantidad,Precio,Costo,dia,mes,año,Tipo_de_mercancia)VALUES (?,?,?,?,?,?,?,?)
            """,(self.root.ids.Nombrearticulo.text,self.root.ids.Cantidad.text,self.root.ids.Precio.text,self.root.ids.Costo.text,hoy.strftime("%d"),mes.get(int(hoy.strftime("%m"))),hoy.strftime("%y"),self.root.ids.Mercancia.text))
            self.root.ids.Nombrearticulo.text=""
            self.root.ids.Precio.text=""
            self.root.ids.Costo.text=""
            self.root.ids.Cantidad.text=""
            self.root.ids.Mercancia.text=""
            conn.commit()
            conn.close()
    """Este metodo te permite buscar la informacion dentro de la base de datos a partir
    de la informacion suministrada"""
    def busqueda(self):
        conn=sql.connect("Reportes.db")
        cur=conn.cursor()
        self.buscador=MDList()
        cur.execute(f"""SELECT * FROM inventario WHERE articulo LIKE 
                    "{self.root.ids.Nombrearticulo.text}%";
                    """)
        c=cur.fetchall()            
        for i in c:
            if i[0]!="":
                self.buscador.add_widget(ThreeLineListItem(text=f"{i[0]}",
                                                             secondary_text=f"precio {i[2]}, cantidad en inventario {i[1]}",
                                                             tertiary_text=f"Tipo de mercancia {i[7]}",on_release=self.Colocarinfo))
        try:
            if i[0]:
                self.root.ids.BuscadorArticulo.add_widget(self.buscador)
                self.actualizarinfob=Button(text="Actualizar informacion",
                                           pos_hint={"x":0.15,"y":0.85},size_hint=(0.25,0.05),
                                           on_press=self.actualizarinfo)
                self.borrarinfob=Button(text="Borrar info",
                                           pos_hint={"x":0.15,"y":0.80},size_hint=(0.25,0.05),
                                           on_press=self.borrarinfo)
                self.root.ids.Agregarinv.add_widget(self.actualizarinfob)
                self.root.ids.Agregarinv.add_widget(self.borrarinfob)
        except:
            pass
        conn.commit()
        conn.close()            
    """Este metodo funciona para colocar la informacion relacionada con lo que se quiere actualizar"""
    def Colocarinfo(self,instance):
        conn=sql.connect("Reportes.db")
        cur=conn.cursor()
        self.root.ids.Nombrearticulo.text=instance.text
        cur.execute(f"""SELECT * FROM inventario WHERE articulo="{self.root.ids.Nombrearticulo.text}";""")  
        c=cur.fetchall()
        for i in c:
            self.root.ids.Cantidad.text=str(int(i[1]))
            self.root.ids.Precio.text=str(int(i[2]))
            self.root.ids.Costo.text=str(int(i[3]))
            self.root.ids.Mercancia.text=str(i[7]) 
        conn.commit()
        conn.close()    
    """Este metodo generara un pop up que saldra cuando se presione el inventario""" 
    def actualizarinfo(self,instance):
        conn=sql.connect("Reportes.db")
        cur=conn.cursor()
        cur.execute(f"""UPDATE inventario SET cantidad="{self.root.ids.Cantidad.text}",precio="{self.root.ids.Precio.text}",
                    costo="{self.root.ids.Costo.text}",tipo_de_mercancia="{self.root.ids.Mercancia.text}" WHERE articulo="{self.root.ids.Nombrearticulo.text}";""")
        self.root.ids.Nombrearticulo.text=""
        self.root.ids.Cantidad.text=""
        self.root.ids.Precio.text=""
        self.root.ids.Costo.text=""
        self.root.ids.Mercancia.text=""
        try:
            self.root.ids.BuscadorArticulo.remove_widget(self.buscador)
        except:
            pass
        self.pagprincipal()         
        conn.commit()
        conn.close()
    """Este metodo se ejecutara cuando se quiera borrar 
    informacion de la base de datos del inventario"""
    def borrarinfo(self,instance):
        conn=sql.connect("Reportes.db")
        cur=conn.cursor()
        cur.execute(f"""DELETE FROM inventario WHERE articulo="{self.root.ids.Nombrearticulo.text}";""")
        self.root.ids.Nombrearticulo.text=""
        self.root.ids.Cantidad.text=""
        self.root.ids.Precio.text=""
        self.root.ids.Costo.text=""
        self.root.ids.Mercancia.text=""
        self.root.ids.BuscadorArticulo.remove_widget(self.buscador)
        self.pagprincipal()
        conn.commit()
        conn.close()
    def getsalidas(self):
        self.Listaprueba2 = MDList()
        self.conn = sql.connect("Reportes.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""select sum(gastos) from gastos""")
        self.gastos=self.cur.fetchone()[0]
        self.root.ids.Salidas.text = f"Gastos totales: RD$ {self.gastos}"
        self.cur.execute("SELECT * FROM gastos")
        self.rows = self.cur.fetchall()
        for self.row in self.rows:
            """Cuando se habla de listprueba es una lista MDmenu"""
            self.Listaprueba2.add_widget(ThreeLineListItem(text=f"Gasto de {self.row[0]} RD$",
                                                          secondary_text=f"El {self.row[1]}/{self.row[2]}/{self.row[3]}",
                                                          tertiary_text=f"Por concepto de {self.row[4]}"))
        self.root.ids.ReportesGastos.add_widget(self.Listaprueba2)
        self.conn.commit()
        self.conn.close()
    """Metodo de creacion del listado de la informacion"""
    def getentradas(self):
        self.Listaprueba = MDList()
        self.root.current = "Pantalla Reportes"
        self.conn = sql.connect("Reportes.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""select sum(entradas) from entradas""")
        self.ingresos=self.cur.fetchone()[0]
        self.root.ids.Ingresos.text = f"Ingresos totales: RD$ {self.ingresos}"
        self.cur.execute("SELECT * FROM entradas")
        self.rows = self.cur.fetchall()
        for self.row in self.rows:
            self.Listaprueba.add_widget(ThreeLineListItem(text=f"Entrada {self.row[0]} RD$",
                                                    secondary_text=f"El {self.row[1]}/{self.row[2]}/{self.row[3]}",
                                                     tertiary_text=f"Por concepto de {self.row[4]}"))
        self.root.ids.ReportesEntradas.add_widget(self.Listaprueba)
        self.conn.commit()
        self.conn.close()
        self.kv.ids.Total.text = f"Dinero total {self.ingresos - self.gastos}"
    """Esto sirve para borrar los errores cometidos en entradas"""  
    """def borrarentrada(self,instance):
        conn=sql.connect("reportes.db")
        cur=conn.cursor()
        print(self.row[4])
        
        conn.commit()
        conn.close()
        self.root.ids.ReportesGastos.remove_widget(self.Listaprueba2)
        self.root.ids.ReportesEntradas.remove_widget(self.Listaprueba)
        self.pagprincipal()"""
    def borardatos(self):
        conn=sql.connect("reportes.db")
        cur=conn.cursor()
        cur.execute("DELETE FROM inventario")
        conn.commit()
        conn.close()
        
    def volver(self):
        self.root.current="Pantalla principal"
        self.root.ids.ReportesEntradas.remove_widget(self.Listaprueba)
        self.root.ids.ReportesGastos.remove_widget(self.Listaprueba2)
    """Estos serian los metodos que llamarian la base de datos este metodo solo se utilizara para
    mejorar la base de datos"""
    def createtable(self):
        conn=sql.connect("Reportes.db")
        cur=conn.cursor()
        cur.execute("""CREATE TABLE inventario(
            Articulo text,
            Cantidad integer,
            Precio integer,
            Costo integer,
            dia integer,
            mes text,
            año integer,
            Tipo_de_mercancia text)
        """)
        conn.commit()
        conn.close()
    """Metodo constructor"""    
    def build(self):
       return self.kv     

if __name__ == "__main__":
    InventarioApp().run()        