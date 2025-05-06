from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
import cv2
from pyzbar.pyzbar import decode
from kivy.network.urlrequest import UrlRequest
import json


class CadastroEquipamentosScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Adiciona o background cinza claro
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_background, pos=self.update_background)

        # Layout principal
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Layout horizontal para caixas de texto e botão "Buscar"
        self.top_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={'center_x': 0.5, 'top': 0.95}
        )
        self.layout.add_widget(self.top_layout)

        self.pesquisar_os_input = MDTextField(
            hint_text='Certificado',
            size_hint=(0.4, None),
            height=50
        )
        self.top_layout.add_widget(self.pesquisar_os_input)

        self.pesquisar_tag_input = MDTextField(
            hint_text='Tag',
            size_hint=(0.4, None),
            height=50
        )
        self.top_layout.add_widget(self.pesquisar_tag_input)

        # TROCA: MDFilledButton -> MDRaisedButton
        buscar_button = MDRaisedButton(
            text='Buscar',
            size_hint=(None, None),
            size=(100, 50),
            md_bg_color=(0.2, 0.6, 0.8, 1)
        )
        buscar_button.bind(on_press=self.buscar_equipamento)
        self.top_layout.add_widget(buscar_button)

        self.menu_items = [
            {'text': 'Serial do Sensor', 'viewclass': 'OneLineListItem', 'on_release': lambda x='Serial do Sensor': self.menu_callback(x)},
            {'text': 'Serial da Eletrônica', 'viewclass': 'OneLineListItem', 'on_release': lambda x='Serial da Eletrônica': self.menu_callback(x)},
            {'text': 'Core', 'viewclass': 'OneLineListItem', 'on_release': lambda x='Core': self.menu_callback(x)},
            {'text': 'Outros', 'viewclass': 'OneLineListItem', 'on_release': lambda x='Outros': self.menu_callback(x)},
            {'text': 'QR Code', 'viewclass': 'OneLineListItem', 'on_release': lambda x='QR Code': self.menu_callback(x)}
        ]

        # TROCA: MDFilledButton -> MDRaisedButton
        self.menu_button = MDRaisedButton(
            text='',
            size_hint=(None, None),
            size=(0, 50),
            pos_hint={'center_x': 0.5, 'top': 0.85},
            md_bg_color=(0.3, 0.4, 0.5, 1)
        )
        self.layout.add_widget(self.menu_button)

        self.menu = MDDropdownMenu(
            caller=self.menu_button,
            items=self.menu_items,
            width_mult=4
        )

        # TROCA: MDFilledButton -> MDRaisedButton
        self.menu_button = MDRaisedButton(
            text='Selecionar Tipo de Pesquisa',
            size_hint=(None, None),
            size=(250, 50),
            pos_hint={'center_x': 0.5, 'top': 0.85},
            md_bg_color=(0.3, 0.4, 0.5, 1)
        )
        self.menu_button.bind(on_release=lambda x: self.menu.open())
        self.layout.add_widget(self.menu_button)

        # Campo de entrada de dados
        self.text_input = MDTextField(
            hint_text='Digite aqui',
            size_hint=(0.8, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.75}
        )
        self.layout.add_widget(self.text_input)
        self.text_input.opacity = 0  # Inicia invisível

        # QR Code inicialmente invisível
        self.qr_image = Image(
            source='qrcode.png',
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={'center_x': 0.5, 'top': 0.65},
            opacity=0
        )
        self.qr_image.bind(on_touch_down=self.abrir_camera)
        self.layout.add_widget(self.qr_image)

        # TROCA: MDFilledButton -> MDRaisedButton
        cadastrar_button = MDRaisedButton(
            text='Adicionar Equipamento',
            size_hint=(None, None),
            size=(250, 70),
            pos_hint={'center_x': 0.5, 'top': 0.5},
            md_bg_color=(0.2, 0.6, 0.8, 1)
        )
        cadastrar_button.bind(on_press=self.cadastrar_equipamento)
        self.layout.add_widget(cadastrar_button)

        # TROCA: MDFilledButton -> MDRaisedButton
        voltar_button = MDRaisedButton(
            text='Voltar',
            size_hint=(None, None),
            size=(200, 70),
            pos_hint={'x': 0.02, 'y': 0.05},
            md_bg_color=(0.8, 0.2, 0.2, 1)
        )
        voltar_button.bind(on_press=self.voltar_inserir_nota_fiscal)
        self.layout.add_widget(voltar_button)

    def update_background(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def abrir_camera(self, instance, touch):
        """Abre a câmera para escanear um QR Code."""
        if self.qr_image.collide_point(*touch.pos):
            self.dialog = MDDialog(
                title="Escanear QR Code",
                text="Aguarde... Abrindo a câmera.",
                buttons=[
                    MDFlatButton(
                        text="Cancelar",
                        theme_text_color="Custom",
                        text_color=(1, 0, 0, 1),
                        on_release=lambda x: self.fechar_camera()
                    )
                ],
                radius=[20, 20, 20, 20]
            )
            self.dialog.open()
            Clock.schedule_once(self.iniciar_captura, 1)

    def iniciar_captura(self, dt):
        """Inicia a captura da câmera para leitura do QR Code."""
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            self.dialog.dismiss()
            self.dialog = MDDialog(
                title="Erro na Câmera",
                text="Não foi possível abrir a câmera. Verifique as permissões.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=(1, 0, 0, 1),
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ],
                radius=[20, 20, 20, 20]
            )
            self.dialog.open()
            return

        Clock.schedule_interval(self.processar_frame, 1.0 / 30.0)  # 30 FPS

    def processar_frame(self, dt):
        """Processa os frames da câmera e detecta QR Codes."""
        ret, frame = self.capture.read()
        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        qr_codes = decode(gray)

        for qr_code in qr_codes:
            texto = qr_code.data.decode('utf-8')
            self.capture.release()
            Clock.unschedule(self.processar_frame)

            self.dialog.dismiss()
            self.dialog = MDDialog(
                title="QR Code Detectado",
                text=f"Conteúdo: {texto}",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=(0, 0.5, 1, 1),
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ],
                radius=[20, 20, 20, 20]
            )
            self.dialog.open()
            break

    def fechar_camera(self):
        """Fecha o popup e encerra a captura da câmera."""
        self.dialog.dismiss()
        if hasattr(self, "capture") and self.capture.isOpened():
            self.capture.release()

    def menu_callback(self, text_item):
        """Atualiza o campo de entrada e exibe a opção correta ao usuário."""
        self.menu_button.text = text_item
        self.menu.dismiss()

        is_qr_code = text_item == 'QR Code'
        self.qr_image.opacity = 1 if is_qr_code else 0
        self.text_input.opacity = 0 if is_qr_code else 1

        hint_texts = {
            "Serial do Sensor": "Digite o Serial do Sensor",
            "Serial da Eletrônica": "Digite o Serial da Eletrônica",
            "Core": "Digite o Core",
            "Outros": "Digite a Informação"
        }
        self.text_input.hint_text = hint_texts.get(text_item, "")

    def buscar_equipamento(self, instance):
        """Exibe um popup informando que a busca está em andamento."""
        self.dialog = MDDialog(
            title="Buscando Equipamento",
            text="Aguarde... Estamos verificando os dados.",
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=(0, 0.5, 1, 1),
                    on_release=lambda x: self.dialog.dismiss()
                )
            ],
            radius=[20, 20, 20, 20]
        )
        self.dialog.open()

    def cadastrar_equipamento(self, instance):
        equipamento_numero = self.text_input.text.strip()
        tipo_pesquisa = self.menu_button.text

        if not equipamento_numero:
            self.mostrar_popup("Erro", "Por favor, insira um número de serial válido.", (1, 0, 0, 1))
            return

        # Redirecionando para a tela de cadastro 1
        if tipo_pesquisa in ["Serial do Sensor", "Serial da Eletrônica"]:
            self.manager.current = 'TelaCadastroEquipamento1'
        elif tipo_pesquisa == "Core":
            self.manager.current = 'TelaCore'
        elif tipo_pesquisa == "Outros":
            self.manager.current = 'TelaOutros'
        else:
            popup = Popup(title='Erro',
                          content=MDLabel(text='Selecione um tipo válido antes de continuar.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        # Enviando requisição à API
        url = "http://10.11.100.133:5000/api/chavedeapi/pesq_cnpj"
        headers = {'Content-Type': 'application/json'}
        body = json.dumps({"numero": equipamento_numero, "tipo": tipo_pesquisa})

        UrlRequest(
            url,
            on_success=self.processar_resposta_api,
            on_failure=self.tratar_erro_api,
            on_error=self.tratar_erro_api,
            req_body=body,
            req_headers=headers
        )

    def mostrar_popup(self, titulo, mensagem, cor_texto=(0, 0.5, 1, 1)):
        """Cria um popup padronizado usando MDDialog."""
        if hasattr(self, "dialog") and self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title=titulo,
            text=mensagem,
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=cor_texto,
                    on_release=lambda x: self.dialog.dismiss()
                )
            ],
            radius=[20, 20, 20, 20]
        )
        self.dialog.open()

    def voltar_inserir_nota_fiscal(self, instance):
        self.manager.current = 'CadastroCliente'

    def processar_resposta_api(self, request, result):
        try:
            if isinstance(result, bytes):
                result = result.decode('utf-8')
            result_data = json.loads(result)

            if result_data.get("status") == "encontrado":
                self.result_label.text = "Equipamento encontrado, redirecionando..."
                tela_cadastro = self.manager.get_screen('TelaCadastroEquipamento1')
                tela_cadastro.carregar_dados(result_data)
                self.manager.current = 'TelaCadastroEquipamento1'
            else:
                self.result_label.text = "Equipamento não encontrado, iniciando um novo cadastro."
                tela_cadastro = self.manager.get_screen('TelaCadastroEquipamento1')
                tela_cadastro.carregar_dados({"numero": self.text_input.text, "tipo": self.menu_button.text})
                self.manager.current = 'TelaCadastroEquipamento1'
        except Exception as e:
            self.result_label.text = "Erro ao processar resposta da API."
            print(f"Erro: {e}")

    def tratar_erro_api(self, request, error):
        """Mostra um popup de erro mais bonito ao falhar na conexão com a API."""
        close_button = MDFlatButton(
            text="OK",
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1)
        )

        self.dialog = MDDialog(
            title="Equipamento não Encontrado",
            text="Iniciando um novo Cadastro",
            buttons=[close_button],
            radius=[20, 20, 20, 20]
        )
        close_button.bind(on_release=lambda x: self.dialog.dismiss())
        self.dialog.open()
