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


class TelaCoreScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Armazena localmente os "cores" cadastrados
        self.cores_cadastrados = {}

        # ------------------ Fundo da Tela ------------------
        with self.canvas.before:
            Color(0.96, 0.97, 1, 1)  # Tom azul claro
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_background, pos=self.update_background)

        # ------------------ Layout Principal ------------------
        self.main_layout = MDBoxLayout(orientation='vertical', spacing=0, padding=0)
        self.add_widget(self.main_layout)

        # (1) Título
        self.title_label = MDLabel(
            text="Cadastro de Core",
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

        self.core_serie = MDTextField(hint_text="Série", size_hint=(0.5, None), height=50)
        linha1.add_widget(self.core_serie)

        self.core_modelo = MDTextField(hint_text="Modelo", size_hint=(0.5, None), height=50)
        linha1.add_widget(self.core_modelo)

        # Linha 2: Fabricante e Tag
        linha2 = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        self.form_layout.add_widget(linha2)

        self.fabricante_core_input = MDTextField(
            hint_text="Fabricante",
            size_hint=(0.5, None),
            height=50
        )
        linha2.add_widget(self.fabricante_core_input)

        self.core_tag = MDTextField(hint_text="Tag", size_hint=(0.5, None), height=50)
        linha2.add_widget(self.core_tag)

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
            "core_foto_1": "images.jpg",
            "core_foto_2": "images.jpg"
        }

        fotos_label = MDLabel(
            text="Fotos do Core",
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

        self.core_foto_1 = ClickableImage(
            source=self.fotos["core_foto_1"], size_hint=(None, None), size=(170, 170)
        )
        self.core_foto_1.bind(on_release=lambda x: self.abrir_camera("core_foto_1"))
        fotos_layout.add_widget(self.core_foto_1)

        self.core_foto_2 = ClickableImage(
            source=self.fotos["core_foto_2"], size_hint=(None, None), size=(170, 170)
        )
        self.core_foto_2.bind(on_release=lambda x: self.abrir_camera("core_foto_2"))
        fotos_layout.add_widget(self.core_foto_2)

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
        self.btn_cadastrar.bind(on_press=self.cadastrar_core)
        linha_botoes.add_widget(self.btn_cadastrar)

        # Botão para visualizar a lista
        self.visualizar_button = MDRaisedButton(
            text="Visualizar Cores",
            size_hint=(1, None),
            height=50,
            md_bg_color=(0.0, 0.6, 1, 1),
            opacity=0  # só fica visível após primeiro cadastro
        )
        self.form_layout.add_widget(self.visualizar_button)
        self.visualizar_button.bind(on_press=self.ir_para_tela_core_cadastrados)

    # ======================== MÉTODOS ========================
    def update_background(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    # -------------- Abertura de Câmera --------------
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

        if tipo == "core_foto_1":
            self.core_foto_1.source = filename
        elif tipo == "core_foto_2":
            self.core_foto_2.source = filename

    # -------------- Cadastro e Visualização --------------
    def cadastrar_core(self, instance):
        """
        Salva localmente os dados em self.cores_cadastrados.
        Em produção, você pode enviar para um banco de dados/API.
        """
        serie = self.core_serie.text.strip()
        modelo = self.core_modelo.text.strip()
        fabricante = self.fabricante_core_input.text.strip()
        tag = self.core_tag.text.strip()

        pintar = "Sim" if self.checkbox_pintura.active else "Não"

        # Validação simples
        if not serie:
            MDDialog(title="Erro", text="Informe a Série.", size_hint=(0.8, 0.3)).open()
            return

        # Cria dicionário do item
        dados = {
            "serie": serie,
            "modelo": modelo,
            "fabricante": fabricante,
            "tag": tag,
            "sugerir_pintura": pintar,
            "fotos": self.fotos.copy()
        }

        # Salva em self.cores_cadastrados usando a série como chave
        self.cores_cadastrados[serie] = dados

        # Mostra o botão de visualizar
        self.visualizar_button.opacity = 1

        MDDialog(title="Cadastro", text="Core cadastrado com sucesso!", size_hint=(0.8, 0.3)).open()

        # Limpa os campos
        self.core_serie.text = ""
        self.core_modelo.text = ""
        self.fabricante_core_input.text = ""
        self.core_tag.text = ""
        self.checkbox_pintura.active = False

        # Restaura fotos padrão
        self.fotos = {
            "core_foto_1": "images.jpg",
            "core_foto_2": "images.jpg"
        }
        self.core_foto_1.source = self.fotos["core_foto_1"]
        self.core_foto_2.source = self.fotos["core_foto_2"]

    def ir_para_tela_core_cadastrados(self, instance):
        """
        Passa todos os itens para a TelaCoreCadastrados e muda de tela.
        """
        tela_cadastrados = self.manager.get_screen("TelaCoreCadastrados")
        # Limpa a tela anterior e carrega os dados
        tela_cadastrados.cores.clear()

        for key, item_dict in self.cores_cadastrados.items():
            tela_cadastrados.adicionar_core(item_dict)

        self.manager.current = "TelaCoreCadastrados"

    def carregar_informacoes(self, item):
        """
        Recebe um dicionário 'item' com as chaves
        'serie', 'modelo', 'fabricante', 'tag', 'sugerir_pintura', 'fotos' etc.
        e preenche a tela para edição.
        """
        self.core_serie.text = item.get("serie", "")
        self.core_modelo.text = item.get("modelo", "")
        self.fabricante_core_input.text = item.get("fabricante", "")
        self.core_tag.text = item.get("tag", "")

        if item.get("sugerir_pintura", "Não") == "Sim":
            self.checkbox_pintura.active = True
        else:
            self.checkbox_pintura.active = False

        # Fotos
        self.fotos = item.get("fotos", {})
        if not self.fotos:
            self.fotos = {
                "core_foto_1": "images.jpg",
                "core_foto_2": "images.jpg"
            }

        self.core_foto_1.source = self.fotos.get("core_foto_1", "images.jpg")
        self.core_foto_2.source = self.fotos.get("core_foto_2", "images.jpg")

    def voltar(self, instance):
        """Voltar para a tela 'CadastroEquipamentos'"""
        self.manager.current = "CadastroEquipamentos"
