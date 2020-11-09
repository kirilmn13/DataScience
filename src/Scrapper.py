from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from random import choice
import json
from bs4 import BeautifulSoup
import requests
import urllib.request
from datetime import datetime
import os, sys
from os import path
from colorthief import ColorThief

class instagram:

    def __init__(self, usuario, contrasena):
        self.usuario = usuario
        self.contrasena = contrasena
        self.driver = webdriver.Chrome()

    def close(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        espaciousuario = driver.find_element_by_xpath("//input[@name='username']")
        espaciousuario.clear()
        espaciousuario.send_keys(self.usuario)
        espaciocontrasena = driver.find_element_by_xpath("//input[@name='password']")
        espaciocontrasena.clear()
        espaciocontrasena.send_keys(self.contrasena)
        espaciocontrasena.send_keys(Keys.RETURN)
        time.sleep(3)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Ahora no')]") \
            .click()
        time.sleep(5)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Ahora no')]") \
            .click()
    def goloc(self, locationid):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/locations/" + locationid + "/")
        time.sleep(2)

    def gethref(self, nscroll): 
        driver = self.driver

        pic_hrefs = []
        for i in range(1, nscroll):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]

            except Exception:
                continue
        return pic_hrefs
            

    def extract_json(self, href):
        r = requests.get(href)
        soup = BeautifulSoup(r.content,'html.parser')
        body = soup.find('body')
        script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
        script=str(script)
        page_json = script.split(' = ', 1)
        page_json1 = page_json[1]
        page_json1 = str(page_json1)[:-10]
        data = json.loads(page_json1)
        return (data)


    def parse_json(self, data):
        tiempo = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["taken_at_timestamp"]
        tiempo = datetime.utcfromtimestamp(tiempo).strftime('%Y-%m-%d %H:%M:%S')

        try:
            texto = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
        except IndexError:
            texto = 'null'
        
        hashtags = list(set(part[1:] for part in texto.split() if part.startswith('#')))
        usuario = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["owner"]["username"]
        nombre = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["owner"]["full_name"]
        likes = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_media_preview_like"]["count"]
        imgurl = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["display_url"]
        tamano = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["dimensions"]
        localizacion = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["location"]
        seguidores = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["owner"]["edge_followed_by"]["count"]
        return [imgurl,usuario,nombre,tiempo,likes,seguidores,texto,hashtags]

    def control(self, folder):
        """
        Nueva carpeta
        """
        folder_path = 'C:/Users/Kiril/Desktop/Práctica 1 Tipológia/'+folder+'/'
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        else:
            print (folder, "ya existe")
    
    def saveimage(self,folder,href):
        folder_path ='C:/Users/Kiril/Desktop/Práctica 1 Tipológia/'+folder+'/'
        r = requests.get(href)
        split1= str(href.split("nc",1)[1])

        PATH = folder_path+split1+".jpg"
        if os.path.isfile(PATH):
            print("La imagen ya existe")
        else:
            with open(folder_path+split1+".jpg", 'wb') as f:
                    f.write(r.content)
        return str(folder_path+split1+".jpg")
if __name__ == "__main__":
    ig = instagram("kirilmn13@gmail.com", "dobleduelo7")
    ig.login()
    
