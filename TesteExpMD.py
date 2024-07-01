from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.core.window import Window

class TelaCadastroEquipamento1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal
        layout_principal = GridLayout(cols=2, spacing=20, padding=50)
        layout_principal.bind(size=self._atualizar_imagem_fundo, pos=self._atualizar_imagem_fundo)

        # Adicionando imagem de fundo
        with layout_principal.canvas.before:
            self.rect = Rectangle(source='vetor.jpg', pos=layout_principal.pos, size=layout_principal.size)

        # Título Sensor
        titulo_sensor = Label(text='[color=000000]Sensor[/color]', markup=True, font_size=24, size_hint_y=None, height=50)
        layout_principal.add_widget(titulo_sensor)
        layout_principal.add_widget(Label(size_hint_y=None, height=50))  # Espaçamento

        # Container para dados do Sensor
        self.sensor_serie = TextInput(hint_text='Série do Sensor', size_hint=(None, None), size=(200, 30), background_color=(1, 1, 1, 0.5))
        self.sensor_fabricante = Spinner(text='Fabricante', values=('Fabricante A', 'Fabricante B', 'Fabricante C'), size_hint=(None, None), size=(200, 30), background_color=(0.7, 0.8, 1, 1))
        self.sensor_modelo = TextInput(hint_text='Modelo', size_hint=(None, None), size=(200, 30), background_color=(1, 1, 1, 0.5))
        self.sensor_tag = TextInput(hint_text='Tag', size_hint=(None, None), size=(200, 30), background_color=(1, 1, 1, 0.5))
        self.sensor_principio = TextInput(hint_text='Princípio', size_hint=(None, None), size=(200, 30), background_color=(1, 1, 1, 0.5))
        self.sensor_conexao = Spinner(text='Conexão', values=('Conexão A', 'Conexão B', 'Conexão C'), size_hint=(None, None), size=(200, 30), background_color=(0.7, 0.8, 1, 1))
        self.sensor_diametro = Spinner(text='Diâmetro', values=('Diâmetro A', 'Diâmetro B', 'Diâmetro C'), size_hint=(None, None), size=(200, 30), background_color=(0.7, 0.8, 1, 1))
        self.sensor_integrado = Spinner(text='...', values=('Integrado', 'Remoto'), size_hint=(None, None), size=(200, 30), background_color=(0.7, 0.8, 1, 1))

        container_sensor = GridLayout(cols=2, spacing=10, size_hint_y=None, height=300)
        container_sensor.add_widget(self.sensor_serie)
        container_sensor.add_widget(self.sensor_fabricante)
        container_sensor.add_widget(self.sensor_modelo)
        container_sensor.add_widget(self.sensor_tag)
        container_sensor.add_widget(self.sensor_principio)
        container_sensor.add_widget(self.sensor_conexao)
        container_sensor.add_widget(self.sensor_diametro)
        container_sensor.add_widget(self.sensor_integrado)
        layout_principal.add_widget(container_sensor)

        # Adicionar quadrados para imagens abaixo do Sensor
        container_imagens_sensor = GridLayout(cols=2, spacing=10, size_hint_y=None, height=200)
        for i in range(4):
            image_placeholder = Image(source='placeholder.png', size_hint=(None, None), size=(100, 100))
            container_imagens_sensor.add_widget(image_placeholder)

        layout_principal.add_widget(container_imagens_sensor)

        # Título Eletrônica
        titulo_eletronica = Label(text='[color=000000]Eletrônica[/color]', markup=True, font_size=24, size_hint_y=None, height=50)
        layout_principal.add_widget(titulo_eletronica)
        layout_principal.add_widget(Label(size_hint_y=None, height=50))  # Espaçamento

        # Container para dados da Eletrônica
        self.eletronica_serie = TextInput(hint_text='Série da Eletrônica', size_hint=(None, None), size=(200, 30), background_color=(1, 1, 1, 0.5))
        self.eletronica_fabricante = Spinner(text='Fabricante', values=('Fabricante X', 'Fabricante Y', 'Fabricante Z'), size_hint=(None, None), size=(200, 30), background_color=(0.7, 0.8, 1, 1))
        self.eletronica_modelo = TextInput(hint_text='Modelo', size_hint=(None, None), size=(200, 30), background_color=(1, 1, 1, 0.5))
        self.eletronica_tag = TextInput(hint_text='Tag', size_hint=(None, None), size=(200, 30), background_color=(1, 1, 1, 0.5))
        self.sugerir_pintura_spinner = Spinner(text='Sugerir pintura', values=('Sim', 'Não'), size_hint=(None, None), size=(200, 30), background_color=(0.7, 0.8, 1, 1))

        container_eletronica = GridLayout(cols=2, spacing=10, size_hint_y=None, height=300)
        container_eletronica.add_widget(self.eletronica_serie)
        container_eletronica.add_widget(self.eletronica_fabricante)
        container_eletronica.add_widget(self.eletronica_modelo)
        container_eletronica.add_widget(self.eletronica_tag)

        layout_principal.add_widget(container_eletronica)

        # Adicionar quadrados para imagens abaixo da Eletrônica
        container_imagens_eletronica = GridLayout(cols=2, spacing=10, size_hint_y=None, height=200)
        for i in range(4):
            image_placeholder = Image(source='placeholder.png', size_hint=(None, None), size=(100, 100))
            container_imagens_eletronica.add_widget(image_placeholder)

        layout_principal.add_widget(container_imagens_eletronica)

        # Caixa de texto para "Local" (sem título)
        self.local_input = TextInput(hint_text='Local', size_hint=(None, None), size=(200, 30), background_color=(1, 1, 1, 0.5))
        layout_principal.add_widget(self.local_input)

        # Adicionar espaço entre a caixa de texto e os botões
        layout_principal.add_widget(Label(size_hint_y=None, height=50))  # Espaçamento

# Botão para voltar
        botao_voltar = Button(text='Voltar', size_hint=(None, None), size=(100, 30),
                      pos=(50, 0),  # Definir posição x e y
                      background_normal='', background_color=(0.2, 0.6, 0.9, 1), color=(1, 1, 1, 1))
        layout_principal.add_widget(botao_voltar)

# Botão para salvar
        botao_salvar = Button(text='Salvar', size_hint=(None, None), size=(100, 30),
                      pos=(750, 0),  # Definir posição x e y
                      background_normal='', background_color=(0.2, 0.6, 0.9, 1), color=(1, 1, 1, 1))
        botao_salvar.bind(on_press=self.salvar)
        layout_principal.add_widget(botao_salvar)

        self.add_widget(layout_principal)

    def _atualizar_imagem_fundo(self, instance, size):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def salvar(self, instance):
        dados_sensor = {
            'Série do Sensor': self.sensor_serie.text,
            'TAG': self.sensor_tag.text,
            'Fabricante': self.sensor_fabricante.text,
            'Princípio': self.sensor_principio.text,
            'Modelo': self.sensor_modelo.text,
            'Conexão': self.sensor_conexao.text,
            'Diâmetro': self.sensor_diametro.text,
            '': self.sensor_integrado.text
        }

        dados_eletronica = {
            'Série da Eletrônica': self.eletronica_serie.text,
            'TAG': self.eletronica_tag.text,
            'Fabricante': self.eletronica_fabricante.text,
            'Sugerir pintura': self.sugerir_pintura_spinner.text,
            'Modelo': self.eletronica_modelo.text
        }

        local = self.local_input.text

        print(f'Dados Sensor: {dados_sensor}')
        print(f'Dados Eletrônica: {dados_eletronica}')
        print(f'Local: {local}')

class AppCadastroEquipamento(App):
    def build(self):
        Window.size = (1000, 800)  # Definir tamanho da janela
        return TelaCadastroEquipamento1()

if __name__ == '__main__':
    AppCadastroEquipamento().run()

