from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from Login_screen import LoginScreen
from processos_screen import ProcessosScreen
from CadastroCliente_screen import CadastroClienteScreen
from CadastroEquipamentos_screen import CadastroEquipamentosScreen
from TelaCadastroEquipamento1_screen import TelaCadastroEquipamento1
from TelaEquipamentosCadastrados_screen import TelaEquipamentosCadastrados
from TelaCore_screen import TelaCoreScreen
from TelaOutros_screen import TelaOutrosScreen
from TelaOutrosCadastrados import TelaOutrosCadastrados
from TelaCoreCadastrados import TelaCoreCadastrados
from Conferencia_screen import ConferenciaScreen 
from Coleta_screen import TelaColeta  # Confirme que o nome do arquivo está correto

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Adiciona a imagem da SplashScreen
        self.logo = Image(
            source="logo.png",
            size_hint=(None, None),
            size=(200, 200),  # Ajuste conforme necessário
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            opacity=0  # Começa invisível
        )
        self.add_widget(self.logo)

        # Inicia a animação quando a tela carrega
        Clock.schedule_once(self.start_animation, 0.5)

    def start_animation(self, dt):
        fade_in = Animation(opacity=1, duration=1.5)
        stay_visible = Animation(duration=1)
        fade_out = Animation(opacity=0, duration=1)
        fade_out.bind(on_complete=self.switch_to_login)
        fade_in += stay_visible + fade_out
        fade_in.start(self.logo)

    def switch_to_login(self, animation, widget):
        self.manager.current = "login"

class ExpApp(MDApp):
    def build(self):
        print("🚀 Iniciando o aplicativo...")

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        sm = ScreenManager()
        sm.add_widget(SplashScreen(name="splash"))  
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(ProcessosScreen(name="processos"))
        sm.add_widget(CadastroClienteScreen(name="CadastroCliente"))
        sm.add_widget(CadastroEquipamentosScreen(name="CadastroEquipamentos"))
        sm.add_widget(TelaCadastroEquipamento1(name="TelaCadastroEquipamento1"))
        sm.add_widget(TelaEquipamentosCadastrados(name="TelaEquipamentosCadastrados"))
        sm.add_widget(TelaCoreScreen(name="TelaCore"))
        sm.add_widget(TelaOutrosScreen(name="TelaOutros"))
        sm.add_widget(TelaCoreCadastrados(name="TelaCoreCadastrados"))
        sm.add_widget(TelaOutrosCadastrados(name="TelaOutrosCadastrados"))
        sm.add_widget(ConferenciaScreen(name="conferencia"))
        sm.add_widget(TelaColeta(name="coleta"))  # Correção aqui

        # Exibir as telas registradas no console para depuração
        print("📋 Telas registradas no ScreenManager:", sm.screen_names)

        return sm

    def on_start(self):
        print("✅ App iniciado com sucesso!")
        self.root.current = "splash"

    
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA, 
                Permission.WRITE_EXTERNAL_STORAGE, 
                Permission.READ_EXTERNAL_STORAGE, 
                Permission.INTERNET
            ])
        except ImportError:
            print("Rodando no PC, ignorando permissões Android.")


if __name__ == "__main__":
    ExpApp().run()
