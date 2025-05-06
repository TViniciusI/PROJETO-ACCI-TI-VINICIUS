from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.network.urlrequest import UrlRequest
import json

class CadastroClienteScreen(MDScreen):
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

        # Linha superior: CNPJ e OS
        cnpj_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint=(0.9, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.88}
        )

        self.cnpj_input = MDTextField(
            hint_text='CNPJ',
            size_hint=(0.35, None),
            height=50
        )
        # Antes era MDFilledButton, agora MDRaisedButton:
        cnpj_button = MDRaisedButton(
            text='Pesquisar',
            size_hint_x=0.15,
            height=40,
            md_bg_color=(0.2, 0.6, 0.8, 1)
        )
        cnpj_button.bind(on_press=self.buscar_cnpj)

        self.os_input = MDTextField(
            hint_text='Ordem de Serviço',
            size_hint=(0.35, None),
            height=40
        )
        os_button = MDRaisedButton(
            text='Pesquisar',
            size_hint_x=0.15,
            height=40,
            md_bg_color=(0.2, 0.6, 0.8, 1)
        )
        os_button.bind(on_press=self.buscar_os)

        cnpj_layout.add_widget(self.cnpj_input)
        cnpj_layout.add_widget(cnpj_button)
        cnpj_layout.add_widget(self.os_input)
        cnpj_layout.add_widget(os_button)
        self.layout.add_widget(cnpj_layout)

        # Mensagem de resultado
        self.result_label = MDLabel(
            text='',
            halign='center',
            theme_text_color='Hint',
            size_hint=(0.85, None),
            height=30,
            pos_hint={'center_x': 0.5, 'top': 0.78}
        )
        self.layout.add_widget(self.result_label)

        # Layout centralizado para campos adicionais
        central_layout = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            size_hint=(0.85, None),
            height=250,
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )

        self.nota_fiscal_input = MDTextField(
            hint_text='Nota Fiscal',
            size_hint_y=None,
            height=40
        )
        self.embalagem_input = MDTextField(
            hint_text='Descrição da Embalagem',
            size_hint_y=None,
            height=60
        )
        self.acessorios_input = MDTextField(
            hint_text='Acessórios',
            size_hint_y=None,
            height=60
        )
        self.volume_input = MDTextField(
            hint_text='Volume',
            size_hint_y=None,
            height=40
        )

        central_layout.add_widget(self.nota_fiscal_input)
        central_layout.add_widget(self.embalagem_input)
        central_layout.add_widget(self.acessorios_input)
        central_layout.add_widget(self.volume_input)
        self.layout.add_widget(central_layout)

        # Botão "Adicionar Equipamento"
        adicionar_button = MDRaisedButton(
            text='Adicionar Equipamento',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'y': 0.2},
            md_bg_color=(0.2, 0.6, 0.8, 1)
        )
        adicionar_button.bind(on_press=self.confirmar)
        self.layout.add_widget(adicionar_button)

        # Botão "Voltar" no canto inferior esquerdo
        voltar_button = MDRaisedButton(
            text='Voltar',
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'x': 0.02, 'y': 0.05},
            md_bg_color=(0.8, 0.2, 0.2, 1)
        )
        voltar_button.bind(on_press=self.voltar)
        self.layout.add_widget(voltar_button)

    def update_background(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def buscar_cnpj(self, instance):
        cnpj = self.cnpj_input.text.strip()
        if not cnpj:
            self.result_label.text = "Por favor, insira um CNPJ válido."
            return

        headers = {'Content-Type': 'application/json'}
        body = json.dumps({"CNPJ": cnpj})

        UrlRequest(
            'http://10.11.100.133:5000/api/chavedeapi/pesq_cnpj',
            on_success=self.mostrar_resultado_cnpj,
            on_failure=self.tratar_erro,
            on_error=self.tratar_erro,
            req_body=body,
            req_headers=headers
        )

    def buscar_os(self, instance):
        os_value = self.os_input.text.strip()
        if not os_value:
            self.result_label.text = "Por favor, insira um valor para Ordem de Serviço."
            return
        print(f"Pesquisando OS: {os_value}")

    def mostrar_resultado_cnpj(self, request, result):
        try:
            if isinstance(result, bytes):
                result = result.decode('utf-8')
            result_data = json.loads(result)
            nome_empresa = result_data.get('Empresa', 'CNPJ não encontrado')
            self.result_label.text = f"Empresa: {nome_empresa}"
        except Exception as e:
            self.result_label.text = "Erro ao processar o resultado do CNPJ."
            print(f"Erro: {e}")

    def tratar_erro(self, request, error):
        self.result_label.text = f"Erro na busca: {error}"

    def confirmar(self, instance):
        nota_fiscal = self.nota_fiscal_input.text.strip()
        embalagem = self.embalagem_input.text.strip()
        acessorios = self.acessorios_input.text.strip()
        volume = self.volume_input.text.strip()
        os = self.os_input.text.strip()

        print(f"Nota Fiscal: {nota_fiscal}")
        print(f"Descrição da Embalagem: {embalagem}")
        print(f"Acessórios: {acessorios}")
        print(f"Volume: {volume}")
        print(f"OS: {os}")

        self.result_label.text = "Equipamento adicionado com sucesso."
        self.manager.current = 'CadastroEquipamentos'

    def voltar(self, instance):
        self.manager.current = 'processos'
