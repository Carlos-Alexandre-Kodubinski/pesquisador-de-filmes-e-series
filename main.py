import requests, random
from kivy.core import text
from requestIMDB import IMDB
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty
from kivy.lang import Builder, builder

Builder.load_file('popup.kv')

movie = BooleanProperty()
resultadosDaPesquisa = None
categories = 'Categories'
resultadoFinal = []

class MyButton(Button):
    def send_button(self, title):
        global resultadosDaPesquisa, movie
        try:
            resultadosDaPesquisa.clear()
        except:
            pass
        if not movie:
            titles = IMDB().search_series(title)
        else:
            titles = IMDB().search_movies(title)
            
        resultadosDaPesquisa = titles


class ResultsSelectPage(Screen):
    def multiple_widgets(self):
        global resultadosDaPesquisa, categories
        _ = [self.ids.idBox,
             self.ids.titleBox,
             self.ids.posterBox,
             self.ids.selectBox,]
        
        for i in _:
            i.clear_widgets()
        for i in resultadosDaPesquisa:
            #if categories in IMDB().get_genres_title(i['id']):
            self.ids.idBox.add_widget(
                Label(text=f'{i["id"]}', size_hint=(1, .2)))
            self.ids.titleBox.add_widget(
                Label(text=f'{i["title"]}', size_hint=(1, .2)))
            self.ids.posterBox.add_widget(
                Button(text=f'poster', size_hint=(1, .2), on_press=self.popup_poster,
                background_color=(150/255, 20/255, 82/255, 1)))
            self.ids.selectBox.add_widget(
                Button(text=f'See', size_hint=(1, .2), 
                on_press=self.next_screen, background_color=(150/255, 20/255, 82/255, 1)))
        
            
        for i in _:
            i.add_widget(Label())
       
    
    def next_screen(self, *args):
        indexBotton = self.get_index_children(args[0], 
                      self.ids.selectBox.children)
        resultadoFinal.append(IMDB().search_title(
            self.ids.idBox.children[indexBotton].text, allResult=False))
        self.manager.current = 'FinalResultPage'

    def popup_poster(self, btn):
        #posterIndex = -self.get_index_children(btn, self.ids.posterBox.children)
        #print(posterIndex)
        #bl = BoxLayout(orientation='vertical')
        #bl.add_widget(AsyncImage(source=resultadosDaPesquisa[posterIndex]['image']))
        #btn = Button(text='Close', size_hint=(.3, .3), background_color=(150/255, 20/255, 82/255, 1))
        #al = AnchorLayout(size_hint=(1,.1), anchor_x='center', anchor_y='bottom')
        #al.add_widget(btn)
        #bl.add_widget(al)
        #pp = Popup(title='Poster', content=bl, auto_dismiss=False)
        #btn.bind(on_press=pp.dismiss)
        #return pp.open()
        pass
       

    def get_index_children(self, childre, listChildren):
        index = listChildren.index(childre)
        return index


class FinalResultPage(Screen):
    pass


class FilterCheckBox(CheckBox):
    pass


class SearchTextInput(TextInput):
    foreground_color = (160/255, 140/255, 140/255, 1)
    def on_focus(self, instance, value=True):
        if not value and self.text == '':
            self.padding = [(self.width/2-len(self.hint_text*3)), 
            self.height/4,0,0]
        else:
            self.padding = [5,self.height/4,0,0]

    textinput = TextInput()
    textinput.bind(focus=on_focus)


class ImdbWidonw(Screen):
    boxLayoutWidth = BoxLayout.width
    def set_movie(self):
        global movie
        movie = True

    def set_series(self):
        global movie
        movie = False

    def get_categorie(self, categorie):
        global categories
        categories = categorie

class MainApp(App):
    def build(self):
        self.title = 'Search imDb-API app'
        tela = ImdbWidonw()
        return tela


MainApp().run()