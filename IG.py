from Scrapper import instagram
import requests
import json
from bs4 import BeautifulSoup
import re
import pandas as pd 
from colorthief import ColorThief
import colorsys


ig = instagram("kirilmn13@gmail.com", "dobleduelo7")     #Se define la sesión con contraseña y cuenta
ig.login()                                               #Nos logueamos
ig.goloc("224043086")                                    #Ir a geolocalización con código
enlaces = ig.gethref(2)                                 #extraer enlaces con nscrool=10
print(len(enlaces))                                      #numero de posts extraidos
ig.control("img")                                        #Crear carpeta o comprobar si existe
df = pd.DataFrame(columns=('imgurl','usuario','nombre','tiempo','likes','seguidores','texto','hashtags','color1','color2'))  #Creamos DataFrame

 
for enlace in enlaces:
    data = ig.extract_json(enlace)                           #Extraemos JSON del enlace
    info = ig.parse_json(data)                               #Extraemos información de JSON    
    x=ig.saveimage("img",info[0])                            #Guardamos imagen en carpeta

    #################################################################################################################################################################################################
    colort = ColorThief(x)                                   #Asociamos imagen con path como return de la función saveimage
    palette = colort.get_palette(color_count=2,quality=1)    #Obtenemos la paleta de colores con colorthief
    rgb1 = palette[0]
    rgb2 = palette[1]
    newrgb1 = list(map(lambda x: x/255, rgb1))
    newrgb2 = list(map(lambda x: x/255, rgb2))
    print(newrgb1)                                                                             #OBTENCIÓN Y TRANSFORMACIÓN DE COLOR
    print(newrgb2)
    c1 = colorsys.rgb_to_hls((newrgb1[0]),(newrgb1[1]),(newrgb1[2]))
    c2 = colorsys.rgb_to_hls((newrgb2[0]),(newrgb2[1]),(newrgb2[2]))        
    color1 = [c1[0]*360,c1[1]*100,c1[2]*100]       
    color2 = [c2[0]*360,c2[1]*100,c2[2]*100]  
    print(color1)
    print(color2)
    #################################################################################################################################################################################################
    info.append(color1)
    info.append(color2)
    a_series = pd.Series(info, index = df.columns)           #COnvertimos a objeto "Serie" de Pandas
    df = df.append(a_series, ignore_index=True)              #Escribimos en Dataframe


print(df)
df.to_csv('C:/Users/Kiril/Desktop/Práctica 1 Tipológia/igdataframe.csv', index = False)







#Guardar Json de cada post por si hiciera Falta
#with open(r"C:\Users\Kiril\Desktop\Práctica 1 Tipológia\data.json", 'w', encoding='utf-8') as outfile:
    #json.dump(data, outfile, ensure_ascii=False, indent=4)






