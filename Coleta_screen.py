from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivy.uix.camera import Camera
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.clock import Clock
from datetime import datetime
from kivy.metrics import dp


class TelaColeta(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.data_atual = datetime.now().strftime('%d/%m/%Y')

        self.main_layout = MDBoxLayout(orientation='vertical', padding=[20, 10], spacing=15)
        self.add_widget(self.main_layout)

        # Título
        self.title_label = MDLabel(
            text="Coleta",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height=dp(70),
            theme_text_color="Custom",
            text_color=(0, 0.4, 0.8, 1),
        )
        self.main_layout.add_widget(self.title_label)

        # Data
        self.date_label = MDLabel(
            text=f"Data de hoje: {self.data_atual}",
            size_hint_y=None,
            height=dp(40),
            theme_text_color="Secondary"
        )
        self.main_layout.add_widget(self.date_label)

        # Scroll View
        self.scroll_view = MDScrollView()
        self.main_layout.add_widget(self.scroll_view)

        self.form_layout = MDBoxLayout(orientation='vertical', padding=[10, 10], spacing=15, size_hint_y=None)
        self.form_layout.bind(minimum_height=self.form_layout.setter('height'))
        self.scroll_view.add_widget(self.form_layout)

        # Campo de Responsável (Dropdown)
        self.responsavel_label = MDLabel(text="Responsável", size_hint_y=None, height=dp(30))
        self.form_layout.add_widget(self.responsavel_label)

        self.responsavel_input = MDRaisedButton(
            text="Selecionar Responsável",
            size_hint=(1, None),
            height=dp(50),
            on_release=self.abrir_menu_responsavel
        )
        self.form_layout.add_widget(self.responsavel_input)

        self.menu_items = [
            {"text": nome, "on_release": lambda x=nome: self.selecionar_responsavel(x)}
            for nome in ["VINÍCIUS", "NICOLAS", "ANDRÉ", "MATEUS", "GUILHERME"]
        ]

        self.menu_responsavel = MDDropdownMenu(
            caller=self.responsavel_input,
            items=self.menu_items,
            width_mult=3
        )

        # Campos de entrada
        self.motorista_input = MDTextField(hint_text='Motorista', size_hint_y=None, height=dp(50))
        self.form_layout.add_widget(self.motorista_input)

        self.transportadora_input = MDTextField(hint_text='Transportadora', size_hint_y=None, height=dp(50))
        self.form_layout.add_widget(self.transportadora_input)

        self.rg_input = MDTextField(hint_text='RG', size_hint_y=None, height=dp(50))
        self.form_layout.add_widget(self.rg_input)

        self.placa_input = MDTextField(hint_text='Placa', size_hint_y=None, height=dp(50))
        self.form_layout.add_widget(self.placa_input)

        # Botão de câmera
        self.camera_button = MDRaisedButton(
            text="Abrir Câmera",
            size_hint=(1, None),
            height=dp(50),
            md_bg_color=(0.2, 0.6, 0.8, 1),
            on_press=self.abrir_camera
        )
        self.form_layout.add_widget(self.camera_button)

        # Botões de ação
        self.button_layout = MDBoxLayout(orientation='horizontal', spacing=15, size_hint_y=None, height=dp(60))
        self.form_layout.add_widget(self.button_layout)

        self.voltar_button = MDRaisedButton(
            text='Voltar',
            size_hint=(0.5, None),
            height=dp(50),
            md_bg_color=(0.8, 0.2, 0.2, 1),
            on_press=self.voltar_para_processos
        )
        self.button_layout.add_widget(self.voltar_button)

        self.gravar_button = MDRaisedButton(
            text='Gravar',
            size_hint=(0.5, None),
            height=dp(50),
            md_bg_color=(0.2, 0.6, 0.8, 1),
            on_press=self.gravar_coleta
        )
        self.button_layout.add_widget(self.gravar_button)

    def abrir_menu_responsavel(self, instance):
        self.menu_responsavel.open()

    def selecionar_responsavel(self, nome):
        self.responsavel_input.text = nome
        self.menu_responsavel.dismiss()

    def abrir_camera(self, instance):
        self.camera_popup = Popup(
            title="Captura de Imagem",
            size_hint=(0.8, 0.8)
        )
        content = MDBoxLayout(orientation='vertical', spacing=10)
        self.camera = Camera(play=True)
        content.add_widget(self.camera)

        btn_capturar = MDRaisedButton(
            text="Capturar",
            size_hint=(None, None),
            size=(150, 50),
            md_bg_color=(0.2, 0.7, 0.3, 1),
            pos_hint={"center_x": 0.5},
            on_press=self.capturar_foto
        )
        content.add_widget(btn_capturar)

        self.camera_popup.content = content
        self.camera_popup.open()

    def capturar_foto(self, instance):
        if not self.camera.texture:
            return
        self.camera_popup.dismiss()
        MDDialog(title="Foto Capturada", text="Imagem salva com sucesso!", size_hint=(0.8, 0.3)).open()

    def gravar_coleta(self, instance):
        responsavel = self.responsavel_input.text
        motorista = self.motorista_input.text.strip()
        transportadora = self.transportadora_input.text.strip()
        rg = self.rg_input.text.strip()
        placa = self.placa_input.text.strip()

        if responsavel == "Selecionar Responsável" or not motorista or not transportadora or not rg or not placa:
            MDDialog(title="Erro", text="Preencha todos os campos!", size_hint=(0.8, 0.3)).open()
            return

        MDDialog(title="Sucesso", text="Coleta registrada com sucesso!", size_hint=(0.8, 0.3)).open()
        self.limpar_campos()

    def limpar_campos(self):
        self.responsavel_input.text = 'Selecionar Responsável'
        self.motorista_input.text = ''
        self.transportadora_input.text = ''
        self.rg_input.text = ''
        self.placa_input.text = ''

    def voltar_para_processos(self, instance):
        if self.manager:
            self.manager.current = 'processos'
        else:
            MDDialog(title="Erro", text="Gerenciador de telas não encontrado!", size_hint=(0.8, 0.3)).open()
