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
from kivy.uix.spinner import Spinner
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import MDDialog

from kivy.properties import StringProperty, ObjectProperty
from datetime import datetime
from io import BytesIO
import os


class ClickableImage(ButtonBehavior, Image):
    """Imagem clicável que abre a câmera."""
    pass


class TelaCadastroEquipamento1(Screen):
    lista_fabricantes = ["Siemens", "Emerson", "Yokogawa", "ABB", "Schneider"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ------------------ Dados Iniciais ------------------
        # Equipamentos cadastrados localmente (lista de dicionários)
        self.equipamentos_cadastrados = []
        # Fotos padrão
        self.fotos = {
            "sensor_1": "images.jpg",
            "sensor_2": "images.jpg",
            "eletronica_1": "images.jpg",
            "eletronica_2": "images.jpg"
        }

        # ------------------ Fundo da Tela (azul claro) ------------------
        with self.canvas.before:
            Color(0.96, 0.97, 1, 1)  # Tom bem clarinho
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_background, pos=self.update_background)

        # ------------------ Layout Principal (vertical) ------------------
        self.main_layout = MDBoxLayout(orientation='vertical', spacing=0, padding=0)
        self.add_widget(self.main_layout)

        # (1) Título Superior
        self.title_label = MDLabel(
            text="Cadastro de Equipamento",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height=70,
            theme_text_color="Custom",
            text_color=(0, 0.4, 0.8, 1),
        )
        self.main_layout.add_widget(self.title_label)

        # (2) Layout com ScrollView (80% da tela)
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
        # Linha 1: Sensor e Eletrônica
        linha1 = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        self.form_layout.add_widget(linha1)

        self.sensor_numero = MDTextField(
            hint_text="Número do Sensor",
            size_hint=(0.5, None),
            height=50
        )
        linha1.add_widget(self.sensor_numero)

        self.eletronica_numero = MDTextField(
            hint_text="Número da Eletrônica",
            size_hint=(0.5, None),
            height=50
        )
        linha1.add_widget(self.eletronica_numero)

        # Linha 2: Fabricantes
        linha2 = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        self.form_layout.add_widget(linha2)

        self.fabricante_sensor_input = MDTextField(
            hint_text="Fabricante do Sensor",
            size_hint=(0.5, None),
            height=50
        )
        self.fabricante_sensor_input.bind(on_text_validate=self.on_fabricante_sensor_validate)
        linha2.add_widget(self.fabricante_sensor_input)

        self.fabricante_eletronica_input = MDTextField(
            hint_text="Fabricante da Eletrônica",
            size_hint=(0.5, None),
            height=50
        )
        self.fabricante_eletronica_input.bind(on_text_validate=self.on_fabricante_eletronica_validate)
        linha2.add_widget(self.fabricante_eletronica_input)

        # Linha 3: Modelos
        linha3 = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        self.form_layout.add_widget(linha3)

        self.modelo_sensor_input = MDTextField(
            hint_text="Modelo do Sensor",
            size_hint=(0.5, None),
            height=50
        )
        linha3.add_widget(self.modelo_sensor_input)

        self.modelo_eletronica_input = MDTextField(
            hint_text="Modelo da Eletrônica",
            size_hint=(0.5, None),
            height=50
        )
        linha3.add_widget(self.modelo_eletronica_input)

        # Linha 4: Local do Equipamento
        linha_local = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        self.form_layout.add_widget(linha_local)

        self.local_equipamento_input = MDTextField(
            hint_text="Local do Equipamento",
            size_hint=(1, None),
            height=50
        )
        linha_local.add_widget(self.local_equipamento_input)

        # Linha 5: Spinners (Princípio / Diâmetro)
        linha_spinners1 = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        self.form_layout.add_widget(linha_spinners1)

        self.principio_spinner = Spinner(
            text="Selecione o Princípio",
            values=["Óptico", "Ultrassônico", "Indutivo", "Capacitivo", "Outros"],
            size_hint=(0.5, None),
            height=50
        )
        self.principio_spinner.background_normal = ''
        self.principio_spinner.background_color = (0.2, 0.4, 0.8, 1)
        self.principio_spinner.color = (1, 1, 1, 1)
        linha_spinners1.add_widget(self.principio_spinner)

        self.diametro_spinner = Spinner(
            text="Selecione o Diâmetro",
            values=["10mm", "20mm", "30mm", "40mm", "Outro"],
            size_hint=(0.5, None),
            height=50
        )
        self.diametro_spinner.background_normal = ''
        self.diametro_spinner.background_color = (0.2, 0.4, 0.8, 1)
        self.diametro_spinner.color = (1, 1, 1, 1)
        linha_spinners1.add_widget(self.diametro_spinner)

        # Linha 6: Spinners (Conexão / Integrado ou Remoto)
        linha_spinners2 = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        self.form_layout.add_widget(linha_spinners2)

        self.conexao_spinner = Spinner(
            text="Selecione a Conexão",
            values=["Wi-Fi", "Bluetooth", "Ethernet", "Outra"],
            size_hint=(0.5, None),
            height=50
        )
        self.conexao_spinner.background_normal = ''
        self.conexao_spinner.background_color = (0.2, 0.4, 0.8, 1)
        self.conexao_spinner.color = (1, 1, 1, 1)
        linha_spinners2.add_widget(self.conexao_spinner)

        self.integracao_spinner = Spinner(
            text="Integrado ou Remoto?",
            values=["Integrado", "Remoto"],
            size_hint=(0.5, None),
            height=50
        )
        self.integracao_spinner.background_normal = ''
        self.integracao_spinner.background_color = (0.2, 0.4, 0.8, 1)
        self.integracao_spinner.color = (1, 1, 1, 1)
        linha_spinners2.add_widget(self.integracao_spinner)

        # Linha 7: Checkbox (Sugerir Pintura?)
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

        # Linha 8: Fotos
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

        self.sensor_1_image = ClickableImage(
            source=self.fotos["sensor_1"], size_hint=(None, None), size=(170, 170)
        )
        self.sensor_1_image.bind(on_release=lambda x: self.abrir_camera("sensor_1"))
        fotos_layout.add_widget(self.sensor_1_image)

        self.sensor_2_image = ClickableImage(
            source=self.fotos["sensor_2"], size_hint=(None, None), size=(170, 170)
        )
        self.sensor_2_image.bind(on_release=lambda x: self.abrir_camera("sensor_2"))
        fotos_layout.add_widget(self.sensor_2_image)

        self.eletronica_1_image = ClickableImage(
            source=self.fotos["eletronica_1"], size_hint=(None, None), size=(170, 170)
        )
        self.eletronica_1_image.bind(on_release=lambda x: self.abrir_camera("eletronica_1"))
        fotos_layout.add_widget(self.eletronica_1_image)

        self.eletronica_2_image = ClickableImage(
            source=self.fotos["eletronica_2"], size_hint=(None, None), size=(170, 170)
        )
        self.eletronica_2_image.bind(on_release=lambda x: self.abrir_camera("eletronica_2"))
        fotos_layout.add_widget(self.eletronica_2_image)

        # Linha 9: Botões (Cadastrar e Visualizar)
        linha_botoes = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)
        self.form_layout.add_widget(linha_botoes)

        self.cadastrar_button = MDRaisedButton(
            text="Cadastrar Equipamento",
            size_hint=(0.5, None),
            height=50,
            md_bg_color=(0.2, 0.4, 0.8, 1)
        )
        self.cadastrar_button.bind(on_press=self.cadastrar_equipamento)
        linha_botoes.add_widget(self.cadastrar_button)

        self.visualizar_button = MDRaisedButton(
            text="Visualizar Equipamentos",
            size_hint=(0.5, None),
            height=50,
            md_bg_color=(0.0, 0.6, 1, 1),
            opacity=0  # só aparece após o primeiro cadastro
        )
        self.visualizar_button.bind(on_press=self.ir_para_tela_equipamentos)
        linha_botoes.add_widget(self.visualizar_button)

        # (3) Barra Inferior com Botão Voltar (canto esquerdo)
        bottom_layout = MDBoxLayout(
            orientation='horizontal',
            padding=[10, 10],
            size_hint=(1, 0.08)
        )
        self.main_layout.add_widget(bottom_layout)

        self.btn_voltar = MDRaisedButton(
            text="Voltar",
            size_hint=(None, None),
            size=(130, 50),
            md_bg_color=(0.8, 0.2, 0.2, 1)
        )
        self.btn_voltar.bind(on_press=self.voltar)
        bottom_layout.add_widget(self.btn_voltar)

    # ======================== MÉTODOS ========================
    def update_background(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def on_fabricante_sensor_validate(self, instance):
        text = self.fabricante_sensor_input.text.strip()
        if text and text not in self.lista_fabricantes:
            self.lista_fabricantes.append(text)

    def on_fabricante_eletronica_validate(self, instance):
        text = self.fabricante_eletronica_input.text.strip()
        if text and text not in self.lista_fabricantes:
            self.lista_fabricantes.append(text)

    # -------------------- Câmera e Fotos --------------------
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
        """Salva a foto tirada pela Câmera em arquivo e atualiza a imagem."""
        if not self.camera.texture:
            return
        texture = self.camera.texture
        pixels = texture.pixels
        img = CoreImage(BytesIO(pixels), ext='png')
        filename = f"{tipo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        img.save(filename)

        self.fotos[tipo] = filename

        if tipo == "sensor_1":
            self.sensor_1_image.source = filename
        elif tipo == "sensor_2":
            self.sensor_2_image.source = filename
        elif tipo == "eletronica_1":
            self.eletronica_1_image.source = filename
        elif tipo == "eletronica_2":
            self.eletronica_2_image.source = filename

        self.camera_popup.dismiss()

    # -------------------- Cadastro e Visualização --------------------
    def cadastrar_equipamento(self, instance):
        sensor = self.sensor_numero.text.strip()
        eletronica = self.eletronica_numero.text.strip()
        fabricante_sensor = self.fabricante_sensor_input.text.strip()
        fabricante_eletronica = self.fabricante_eletronica_input.text.strip()
        modelo_sensor = self.modelo_sensor_input.text.strip()
        modelo_eletronica = self.modelo_eletronica_input.text.strip()
        local_eq = self.local_equipamento_input.text.strip()

        principio = self.principio_spinner.text
        diametro = self.diametro_spinner.text
        conexao = self.conexao_spinner.text
        tipo_integracao = self.integracao_spinner.text
        sugerir_pintura = "Sim" if self.checkbox_pintura.active else "Não"

        # Verifica se ao menos sensor ou eletronica foi preenchido
        if not sensor and not eletronica:
            dialog = MDDialog(
                title="Aviso",
                text="Por favor, insira o número do sensor ou da eletrônica antes de cadastrar.",
                auto_dismiss=False,
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_press=lambda *args: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
            return

        # Monta o dicionário usando as chaves "sensor" e "eletronica"
        # (compatível com a TelaEquipamentosCadastrados)
        dados = {
            "sensor": sensor,
            "eletronica": eletronica,
            "fabricante_sensor": fabricante_sensor,
            "fabricante_eletronica": fabricante_eletronica,
            "modelo_sensor": modelo_sensor,
            "modelo_eletronica": modelo_eletronica,
            "local_equipamento": local_eq,
            "principio": principio,
            "diametro": diametro,
            "conexao": conexao,
            "tipo_integracao": tipo_integracao,
            "sugerir_pintura": sugerir_pintura,
            "fotos": self.fotos.copy()  # copia para não perder referências
        }
        self.equipamentos_cadastrados.append(dados)

        # Limpa campos
        self.sensor_numero.text = ""
        self.eletronica_numero.text = ""
        self.fabricante_sensor_input.text = ""
        self.fabricante_eletronica_input.text = ""
        self.modelo_sensor_input.text = ""
        self.modelo_eletronica_input.text = ""
        self.local_equipamento_input.text = ""

        self.principio_spinner.text = "Selecione o Princípio"
        self.diametro_spinner.text = "Selecione o Diâmetro"
        self.conexao_spinner.text = "Selecione a Conexão"
        self.integracao_spinner.text = "Integrado ou Remoto?"
        self.checkbox_pintura.active = False

        # Restaura fotos padrão
        self.fotos = {
            "sensor_1": "images.jpg",
            "sensor_2": "images.jpg",
            "eletronica_1": "images.jpg",
            "eletronica_2": "images.jpg"
        }
        self.sensor_1_image.source = self.fotos["sensor_1"]
        self.sensor_2_image.source = self.fotos["sensor_2"]
        self.eletronica_1_image.source = self.fotos["eletronica_1"]
        self.eletronica_2_image.source = self.fotos["eletronica_2"]

        self.visualizar_button.opacity = 1

        MDDialog(
            title="Cadastro",
            text="Equipamento cadastrado com sucesso!",
            auto_dismiss=True
        ).open()

    def ir_para_tela_equipamentos(self, instance):
        """Envia todos os itens para a TelaEquipamentosCadastrados e muda de tela."""
        if not self.equipamentos_cadastrados:
            # Se lista vazia, avisa
            dialog = MDDialog(
                title="Aviso",
                text="Nenhum equipamento cadastrado ainda.",
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_press=lambda btn: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
            return

        tela_equip = self.manager.get_screen("TelaEquipamentosCadastrados")
        # Para cada equipamento salvo localmente, adiciona no TelaEquipamentosCadastrados
        for eq in self.equipamentos_cadastrados:
            sensor = eq.get("sensor", "")
            eletronica = eq.get("eletronica", "")
            sensor_img = eq["fotos"].get("sensor_1", "")

            tela_equip.adicionar_item_lista(sensor, eletronica, sensor_img)

        # Limpamos a lista local, para não duplicar em chamadas futuras
        self.equipamentos_cadastrados.clear()

        self.manager.current = "TelaEquipamentosCadastrados"

    def alguma_funcao_que_cria_dialog(self):
        """Exemplo de criar um MDDialog sem usar parent.parent.dismiss()."""
        dialog = MDDialog(
            title="Aviso",
            text="Nenhum equipamento cadastrado ainda.",
            auto_dismiss=False,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_press=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def voltar(self, instance):
        """Voltar para a tela 'CadastroEquipamentos' (ou outra)"""
        if self.manager:
            self.manager.current = "CadastroEquipamentos"
        else:
            pass

    def carregar_informacoes(self, item):
        """
        Recebe um dicionário 'item' (com chaves 'sensor', 'eletronica', etc.)
        e preenche todos os campos na tela para edição/visualização.
        """
        # Por exemplo:
        # item = {
        #   "sensor": "...",
        #   "eletronica": "...",
        #   "fabricante_sensor": "...",
        #   ...,
        #   "fotos": {...}
        # }
        self.sensor_numero.text = item.get("sensor", "")
        self.eletronica_numero.text = item.get("eletronica", "")

        self.fabricante_sensor_input.text = item.get("fabricante_sensor", "")
        self.fabricante_eletronica_input.text = item.get("fabricante_eletronica", "")
        self.modelo_sensor_input.text = item.get("modelo_sensor", "")
        self.modelo_eletronica_input.text = item.get("modelo_eletronica", "")
        self.local_equipamento_input.text = item.get("local_equipamento", "")

        self.principio_spinner.text = item.get("principio", "Selecione o Princípio")
        self.diametro_spinner.text = item.get("diametro", "Selecione o Diâmetro")
        self.conexao_spinner.text = item.get("conexao", "Selecione a Conexão")
        self.integracao_spinner.text = item.get("tipo_integracao", "Integrado ou Remoto?")

        if item.get("sugerir_pintura", "Não") == "Sim":
            self.checkbox_pintura.active = True
        else:
            self.checkbox_pintura.active = False

        # Carrega fotos salvas
        fotos_dict = item.get("fotos", {})
        self.fotos["sensor_1"] = fotos_dict.get("sensor_1", "images.jpg")
        self.fotos["sensor_2"] = fotos_dict.get("sensor_2", "images.jpg")
        self.fotos["eletronica_1"] = fotos_dict.get("eletronica_1", "images.jpg")
        self.fotos["eletronica_2"] = fotos_dict.get("eletronica_2", "images.jpg")

        self.sensor_1_image.source = self.fotos["sensor_1"]
        self.sensor_2_image.source = self.fotos["sensor_2"]
        self.eletronica_1_image.source = self.fotos["eletronica_1"]
        self.eletronica_2_image.source = self.fotos["eletronica_2"]
