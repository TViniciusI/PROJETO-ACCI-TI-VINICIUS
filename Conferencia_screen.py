from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, RoundedRectangle
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from datetime import date


class ClickableImage(ButtonBehavior, Image):
    """Imagem clicável que abre a câmera."""
    pass


class ConferenciaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fundo da Tela
        with self.canvas.before:
            Color(0.96, 0.97, 1, 1)  # Azul Claro
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_background, pos=self.update_background)

        # Layout Principal
        self.main_layout = MDBoxLayout(orientation='vertical', spacing=0, padding=0)
        self.add_widget(self.main_layout)

        # Título
        self.title_label = MDLabel(
            text="Conferência de Envio",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height=70,
            theme_text_color="Custom",
            text_color=(0, 0.4, 0.8, 1),
        )
        self.main_layout.add_widget(self.title_label)

        # Layout com ScrollView
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

        # Data Atual
        self.data_label = MDLabel(
            text=f"Data: {date.today().strftime('%d/%m/%Y')}",
            font_style="Subtitle1",
            halign="center",
            size_hint_y=None,
            height=40,
            theme_text_color="Custom",
            text_color=(0.2, 0.4, 0.8, 1)
        )
        self.form_layout.add_widget(self.data_label)

        # Campos de Entrada
        self.os_input = MDTextField(hint_text="OS", size_hint=(1, None), height=50)
        self.volumes_input = MDTextField(hint_text="Volumes", size_hint=(1, None), height=50)
        self.dimensoes_input = MDTextField(hint_text="Dimensões", size_hint=(1, None), height=50)
        self.peso_input = MDTextField(hint_text="Peso (kg)", size_hint=(1, None), height=50)
        
        self.form_layout.add_widget(self.os_input)
        self.form_layout.add_widget(self.volumes_input)
        self.form_layout.add_widget(self.dimensoes_input)
        self.form_layout.add_widget(self.peso_input)

        # Seleção Tipo
        self.tipo_dropdown = MDDropdownMenu()
        self.tipo_selecionado = MDTextField(hint_text="Selecione o Tipo", size_hint=(1, None), height=50)
        self.tipo_selecionado.bind(on_focus=self.open_tipo_dropdown)
        self.form_layout.add_widget(self.tipo_selecionado)

        self.tipo_menu = MDDropdownMenu(
            caller=self.tipo_selecionado,
            items=[{"viewclass": "MDMenuItem", "text": tipo, "on_release": lambda x=tipo: self.set_tipo(x)}
                   for tipo in ["CAIXA", "MALETA", "PALETE", "SOLTO", "OUTROS"]],
            width_mult=4
        )

        # Seleção Responsável
        self.responsavel_selecionado = MDTextField(hint_text=" Responsável", size_hint=(1, None), height=50)
        self.responsavel_selecionado.bind(on_focus=self.open_responsavel_dropdown)
        self.form_layout.add_widget(self.responsavel_selecionado)

        self.responsavel_menu = MDDropdownMenu(
            caller=self.responsavel_selecionado,
            items=[{"viewclass": "MDMenuItem", "text": nome, "on_release": lambda x=nome: self.set_responsavel(x)}
                   for nome in ["VINÍCIUS", "NICOLAS", "ANDRÉ", "MATEUS", "GUILHERME"]],
            width_mult=4
        )

        # Seção de Fotos
        self.fotos_label = MDLabel(
            text="Fotos do Envio",
            font_style="Subtitle1",
            halign="left",
            size_hint_y=None,
            height=30,
            theme_text_color="Custom",
            text_color=(0, 0.4, 0.8, 1)
        )
        self.form_layout.add_widget(self.fotos_label)

        fotos_layout = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=180)
        self.form_layout.add_widget(fotos_layout)

        self.foto_1 = ClickableImage(source="images.jpg", size_hint=(None, None), size=(170, 170))
        self.foto_2 = ClickableImage(source="images.jpg", size_hint=(None, None), size=(170, 170))
        self.foto_3 = ClickableImage(source="images.jpg", size_hint=(None, None), size=(170, 170))
        self.foto_4 = ClickableImage(source="images.jpg", size_hint=(None, None), size=(170, 170))
        
        fotos_layout.add_widget(self.foto_1)
        fotos_layout.add_widget(self.foto_2)
        fotos_layout.add_widget(self.foto_3)
        fotos_layout.add_widget(self.foto_4)

        # Botões
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

        self.conferido_button = MDRaisedButton(
            text="Conferido",
            size_hint=(0.5, None),
            height=50,
            md_bg_color=(0.2, 0.4, 0.8, 1)
        )
        self.conferido_button.bind(on_press=self.salvar)
        linha_botoes.add_widget(self.conferido_button)

    def update_background(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def open_tipo_dropdown(self, instance, value):
        """Abre o menu dropdown do tipo."""
        if value:
            self.tipo_menu.open()

    def set_tipo(self, tipo):
        """Define o tipo selecionado."""
        self.tipo_selecionado.text = tipo
        self.tipo_menu.dismiss()

    def open_responsavel_dropdown(self, instance, value):
        """Abre o menu dropdown do responsável."""
        if value:
            self.responsavel_menu.open()

    def set_responsavel(self, nome):
        """Define o responsável selecionado."""
        self.responsavel_selecionado.text = nome
        self.responsavel_menu.dismiss()

    def salvar(self, instance):
        print("✅ Conferência Salva")

    def voltar(self, instance):
        self.manager.current = "processos"
