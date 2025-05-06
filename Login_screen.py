from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle

class LoginScreen(MDScreen):
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

        # Logo
        self.logo_image = AsyncImage(
            source='logo.png',
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={'center_x': 0.5, 'top': 0.92}
        )
        self.layout.add_widget(self.logo_image)

        # Campo de usuário
        self.username_input = MDTextField(
            hint_text='Usuário',
            size_hint=(0.85, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.7}
        )
        self.layout.add_widget(self.username_input)

        # Campo de senha
        self.password_input = MDTextField(
            hint_text='Senha',
            password=True,
            size_hint=(0.85, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.58}
        )
        self.layout.add_widget(self.password_input)

        # Botão de login (revertido para MDRaisedButton)
        self.login_button = MDRaisedButton(
            text='Login',
            size_hint=(0.85, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.46},
            md_bg_color=(0.2, 0.6, 0.8, 1)
        )
        self.login_button.bind(on_press=self.realizar_login)
        self.layout.add_widget(self.login_button)
        
        # Mensagem de erro ou sucesso
        self.message_label = MDLabel(
            text='',
            halign='center',
            color=(0, 0, 0, 1),
            size_hint=(0.85, None),
            height=30,
            font_size=16,
            pos_hint={'center_x': 0.5, 'top': 0.38}
        )
        self.layout.add_widget(self.message_label)

        # Rodapé
        self.developed_by_label = MDLabel(
            text='Desenvolvido por: Vinícius Magalhães',
            halign='center',
            theme_text_color='Hint',
            font_size=16,
            size_hint=(None, None),
            height=30,
            width=300,
            pos_hint={'center_x': 0.5, 'y': 0.01}
        )
        self.layout.add_widget(self.developed_by_label)

    def update_background(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def realizar_login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if username and password:
            self.manager.user_name = username  # Armazena o nome do usuário
            self.message_label.text = "Login bem-sucedido!"
            self.manager.current = 'processos'  # Exemplo para navegar para a tela de processos

            processos_screen = self.manager.get_screen('processos')
            processos_screen.update_user_info(username, "12345")
        else:
            self.message_label.text = "Por favor, insira usuário e senha."
