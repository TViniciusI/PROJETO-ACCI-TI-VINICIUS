from kivy.core.window import Window
Window.size = (900, 1200)  # Ajuste se desejar outro tamanho

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.camera import Camera
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.core.image import Image as CoreImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.clock import Clock

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import MDDialog

from kivy.properties import StringProperty, ObjectProperty
from datetime import datetime
from io import BytesIO
import os

class ClickableImage(ButtonBehavior, Image):
    """Imagem clicável que abre a câmera."""
    pass

class TelaOutrosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Dicionário local que armazena todos os itens "Outros" cadastrados
        # Exemplo de estrutura: {"Série1": {dados_do_outros}, "Série2": {dados_do_outros}, ...}
        self.outros_cadastrados = {}

        # ------------------ Fundo da Tela (Azul Claro) ------------------
        with self.canvas.before:
            Color(0.96, 0.97, 1, 1)  # Cor azul claro
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_background, pos=self.update_background)

        # ------------------ Layout Principal ------------------
        self.main_layout = MDBoxLayout(orientation='vertical', spacing=0, padding=0)
        self.add_widget(self.main_layout)

        # (1) Título
        self.title_label = MDLabel(
            text="Cadastro de Outros",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height=70,
            theme_text_color="Custom",
            text_color=(0, 0.4, 0.8, 1),
        )
        self.main_layout.add_widget(self.title_label)

        # (2) Layout com ScrollView
        self.scroll_container = MDBoxLayout(orientation='vertical', size_hint=(1, 0.82))
        self.main_layout.add_widget(self.scroll_container)

        self.scroll_view = MDScrollView()
        self.scroll_container.add_widget(self.scroll_view)

        self.form_layout = MDBoxLayout(
            orientation='vertical',
            padding=[20, 20],
            spacing=15,
            size_hint_y=None
        )
        self.form_layout.bind(minimum_height=self.form_layout.setter('height'))
        self.scroll_view.add_widget(self.form_layout)

        # ---------- CAMPOS DO FORMULÁRIO ----------
        linha1 = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        self.form_layout.add_widget(linha1)

        self.outros_serie = MDTextField(hint_text="Série", size_hint=(0.5, None), height=50)
        linha1.add_widget(self.outros_serie)

        self.outros_modelo = MDTextField(hint_text="Modelo", size_hint=(0.5, None), height=50)
        linha1.add_widget(self.outros_modelo)

        # Linha 2: Fabricante e Tag
        linha2 = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        self.form_layout.add_widget(linha2)

        self.outros_fabricante = MDTextField(
            hint_text="Fabricante",
            size_hint=(0.5, None),
            height=50
        )
        linha2.add_widget(self.outros_fabricante)

        self.outros_tag = MDTextField(hint_text="Tag", size_hint=(0.5, None), height=50)
        linha2.add_widget(self.outros_tag)

        # Linha 3: Sugerir Pintura?
        linha_checkbox = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        self.form_layout.add_widget(linha_checkbox)

        self.checkbox_pintura = MDCheckbox(size_hint=(None, None), size=(50, 50))
        self.pintura_label = MDLabel(
            text="Sugerir Pintura?",
            size_hint=(1, None),
            height=50,
            valign="center"
        )
        linha_checkbox.add_widget(self.checkbox_pintura)
        linha_checkbox.add_widget(self.pintura_label)

        # Linha 4: Fotos
        self.fotos = {
            "outros_foto_1": "images.jpg",
            "outros_foto_2": "images.jpg"
        }

        fotos_label = MDLabel(
            text="Fotos do Equipamento",
            font_style="Subtitle1",
            halign="left",
            size_hint_y=None,
            height=30,
            theme_text_color="Custom",
            text_color=(0, 0.4, 0.8, 1)
        )
        self.form_layout.add_widget(fotos_label)

        fotos_layout = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=180)
        self.form_layout.add_widget(fotos_layout)

        self.outros_foto_1 = ClickableImage(
            source=self.fotos["outros_foto_1"], size_hint=(None, None), size=(170, 170)
        )
        self.outros_foto_1.bind(on_release=lambda x: self.abrir_camera("outros_foto_1"))
        fotos_layout.add_widget(self.outros_foto_1)

        self.outros_foto_2 = ClickableImage(
            source=self.fotos["outros_foto_2"], size_hint=(None, None), size=(170, 170)
        )
        self.outros_foto_2.bind(on_release=lambda x: self.abrir_camera("outros_foto_2"))
        fotos_layout.add_widget(self.outros_foto_2)

        # Linha 5: Botões
        linha_botoes = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        self.form_layout.add_widget(linha_botoes)

        self.btn_voltar = MDRaisedButton(
            text="Voltar",
            size_hint=(0.5, None),
            height=50,
            md_bg_color=(0.8, 0.2, 0.2, 1)
        )
        self.btn_voltar.bind(on_press=self.voltar)
        linha_botoes.add_widget(self.btn_voltar)

        self.btn_cadastrar = MDRaisedButton(
            text="Cadastrar",
            size_hint=(0.5, None),
            height=50,
            md_bg_color=(0.2, 0.4, 0.8, 1)
        )
        self.btn_cadastrar.bind(on_press=self.cadastrar_outros)
        linha_botoes.add_widget(self.btn_cadastrar)

        # Botão para visualizar a lista
        self.visualizar_button = MDRaisedButton(
            text="Visualizar Outros",
            size_hint=(1, None),
            height=50,
            md_bg_color=(0.0, 0.6, 1, 1),
            opacity=0  # só fica visível após primeiro cadastro
        )
        self.form_layout.add_widget(self.visualizar_button)
        self.visualizar_button.bind(on_press=self.ir_para_tela_outros_cadastrados)

    # ======================== MÉTODOS ========================
    def update_background(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def abrir_camera(self, tipo):
        """Abre um Popup com a Câmera para tirar foto."""
        self.camera_popup = Popup(
            title="Tire a foto",
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
            pos_hint={"center_x": 0.5}
        )
        btn_capturar.bind(on_press=lambda x: self.capturar_foto(tipo))
        content.add_widget(btn_capturar)

        self.camera_popup.content = content
        self.camera_popup.open()

    def capturar_foto(self, tipo):
        """Captura a imagem da câmera e salva localmente."""
        if not self.camera.texture:
            return
        self.camera_popup.dismiss()

        texture = self.camera.texture
        pixels = texture.pixels

        # Salva em arquivo
        img = CoreImage(BytesIO(pixels), ext='png')
        filename = f"{tipo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        img.save(filename)

        self.fotos[tipo] = filename

        if tipo == "outros_foto_1":
            self.outros_foto_1.source = filename
        elif tipo == "outros_foto_2":
            self.outros_foto_2.source = filename

    def cadastrar_outros(self, instance):
        """
        Lê os campos e salva localmente em self.outros_cadastrados.
        """
        serie = self.outros_serie.text.strip()
        modelo = self.outros_modelo.text.strip()
        fabricante = self.outros_fabricante.text.strip()
        tag = self.outros_tag.text.strip()
        sugerir = "Sim" if self.checkbox_pintura.active else "Não"

        if not serie:
            MDDialog(title="Erro", text="Informe a Série.", size_hint=(0.8, 0.3)).open()
            return

        # Monta dicionário do item
        dados_outros = {
            "serie": serie,
            "modelo": modelo,
            "fabricante": fabricante,
            "tag": tag,
            "sugerir_pintura": sugerir,
            "fotos": self.fotos.copy()
        }

        # Salva num dicionário local usando a Série como chave
        self.outros_cadastrados[serie] = dados_outros

        # Ativa o botão de visualizar
        self.visualizar_button.opacity = 1

        MDDialog(title="Cadastro", text="Equipamento (Outros) cadastrado com sucesso!", size_hint=(0.8, 0.3)).open()

        # Limpa campos
        self.outros_serie.text = ""
        self.outros_modelo.text = ""
        self.outros_fabricante.text = ""
        self.outros_tag.text = ""
        self.checkbox_pintura.active = False

        # Restaura fotos padrão
        self.fotos = {
            "outros_foto_1": "images.jpg",
            "outros_foto_2": "images.jpg"
        }
        self.outros_foto_1.source = self.fotos["outros_foto_1"]
        self.outros_foto_2.source = self.fotos["outros_foto_2"]

    def ir_para_tela_outros_cadastrados(self, instance):
        """Passa os itens para a TelaOutrosCadastrados e muda de tela."""
        tela_cadastrados = self.manager.get_screen("TelaOutrosCadastrados")
        # Limpa a lista anterior e carrega as novas
        tela_cadastrados.outros.clear()

        for _, item_dict in self.outros_cadastrados.items():
            tela_cadastrados.adicionar_outros(item_dict)

        self.manager.current = "TelaOutrosCadastrados"

    def carregar_informacoes(self, item):
        """
        Recebe um dicionário com as chaves:
        {"serie", "modelo", "fabricante", "tag", "sugerir_pintura", "fotos": {...}}
        e preenche a tela para edição.
        """
        self.outros_serie.text = item.get("serie", "")
        self.outros_modelo.text = item.get("modelo", "")
        self.outros_fabricante.text = item.get("fabricante", "")
        self.outros_tag.text = item.get("tag", "")

        if item.get("sugerir_pintura") == "Sim":
            self.checkbox_pintura.active = True
        else:
            self.checkbox_pintura.active = False

        # Fotos
        self.fotos = item.get("fotos", {})
        if not self.fotos:
            self.fotos = {
                "outros_foto_1": "images.jpg",
                "outros_foto_2": "images.jpg"
            }

        self.outros_foto_1.source = self.fotos.get("outros_foto_1", "images.jpg")
        self.outros_foto_2.source = self.fotos.get("outros_foto_2", "images.jpg")

    def voltar(self, instance):
        """Voltar para a tela 'CadastroEquipamentos' ou outra tela que quiser."""
        self.manager.current = "CadastroEquipamentos"
