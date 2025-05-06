from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
# TROCAR:
# from kivymd.uix.button import MDFilledButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle

class ProcessosScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Adiciona um background sutil atrás do layout principal
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Cinza claro
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.bind(size=self.update_background, pos=self.update_background)

        # Layout principal
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Mensagem de boas-vindas no topo
        self.user_info_label = MDLabel(
            text='Bem-vindo, Vinicius',
            halign='center',
            font_style='H5',
            pos_hint={'center_x': 0.5, 'top': 1.3}
        )
        self.layout.add_widget(self.user_info_label)

        # Layout para os botões principais centralizados em linha horizontal
        button_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=40,
            size_hint=(None, None),
            width=900,
            height=250,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Botões principais (agora MDRaisedButton)
        recebimento_button = MDRaisedButton(
            text='Recebimento',
            size_hint=(None, None),
            size=(200, 100),
            md_bg_color=(0.2, 0.6, 0.8, 1),
        )
        recebimento_button.bind(on_press=self.processo_recebimento)

        conferencia_button = MDRaisedButton(
            text='Conferência',
            size_hint=(None, None),
            size=(200, 100),
            md_bg_color=(0.2, 0.6, 0.8, 1),
        )
        conferencia_button.bind(on_press=self.processo_conferencia)

        coleta_button = MDRaisedButton(
            text='Coleta',
            size_hint=(None, None),
            size=(200, 100),
            md_bg_color=(0.2, 0.6, 0.8, 1),
        )
        coleta_button.bind(on_press=self.processo_coleta)

        button_layout.add_widget(recebimento_button)
        button_layout.add_widget(conferencia_button)
        button_layout.add_widget(coleta_button)

        self.layout.add_widget(button_layout)

        # Botão de voltar
        voltar_button = MDRaisedButton(
            text='Voltar',
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'center_x': 0.5, 'y': 0.05},
            md_bg_color=(0.8, 0.2, 0.2, 1),
        )
        voltar_button.bind(on_press=self.voltar_para_login)
        self.layout.add_widget(voltar_button)

    def update_background(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def update_user_info(self, nome, user_id):
        self.user_info_label.text = f'Bem-vindo, {nome}'

    def processo_recebimento(self, instance):
        self.manager.current = 'CadastroCliente'

    def processo_conferencia(self, instance):
        self.manager.current = 'conferencia'

    def processo_coleta(self, instance):
        self.manager.current = 'coleta'

    def voltar_para_login(self, instance):
        self.manager.current = 'login'
