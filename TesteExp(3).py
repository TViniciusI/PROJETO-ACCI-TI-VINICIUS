from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
import datetime
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.core.window import Window
from datetime import date

Window.size = (600, 800)  # Definindo tamanho da janela


Config.set('graphics', 'font_name', 'Arial Black') #Definindo a Fonte 


class CustomScreen(Screen): #Gerenciar o Screen manager
    def __init__(self, **kwargs): #__init__ Feito para criar instância da classe
        super().__init__(**kwargs) # Super() Uma função usada para dar acesso a métodos da classe base
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10) # É um layout do Kivy que organiza widgets em uma única linha ou coluna, configuram o layout para ter uma orientação vertical, um padding de 10 pixels ao redor dos widgets, e um espaçamento de 10 pixels entre os widgets.
        self.add_widget(self.layout) # É adicionado como um widget filho da instância de CustomScreen. O método add_widget é usado para adicionar widgets ao layout ou à tela.

        with self.canvas.before: #Este bloco de código indica que qualquer comando gráfico inserido dentro dele será executado antes de qualquer outra coisa desenhada no canvas.
            self.background = Rectangle(source='vetor.jpg', pos=self.pos, size=self.size) #Um Rectangle é criado e atribuído à variável self.background. Este retângulo usa a imagem vetor.jpg como textura (especificada pelo parâmetro source), e sua posição (pos) e tamanho (size) são definidos para coincidir com a posição e o tamanho do widget (self.pos e self.size).
            self.bind(pos=self.update_background, size=self.update_background) # Aqui, ela vincula as propriedades pos (posição) e size (tamanho) do widget ao método self.update_background. Isso significa que toda vez que a posição ou o tamanho do widget mudar, o método update_background será chamado.

    def update_background(self, instance, value): #Define um método chamado update_background que é chamado quando a posição (pos) ou o tamanho (size) do widget muda.
        self.background.pos = instance.pos #Atualiza a posição do retângulo de fundo (self.background) para coincidir com a nova posição do widget (instance.pos).
        self.background.size = instance.size #Atualiza o tamanho do retângulo de fundo para coincidir com o novo tamanho do widget (instance.size).

class LoginScreen(CustomScreen):
    def __init__(self, **kwargs): #__init__ Feito para criar instância da classe
        super().__init__(**kwargs) # Super() Uma função usada para dar acesso a métodos da classe base
        self.logo_image = AsyncImage(source='logo.png', size_hint=(None, None), size=(200, 150), #AsyncImage: Um widget usado para carregar e exibir imagens de forma assíncrona.
                                     pos_hint={'center_x': 0.5}) #source='logo.png': Especifica o caminho da imagem a ser carregada.
        self.username_input = TextInput(hint_text='Usuário', size_hint=(None, None), size=(300, 30), #size_hint=(None, None): Define que o tamanho do widget será explicitamente especificado (200x150 pixels).
                                        pos_hint={'center_x': 0.5}) #pos_hint={'center_x': 0.5}: Centraliza horizontalmente a imagem no layout.
        self.password_input = TextInput(hint_text='Senha', password=True, size_hint=(None, None), size=(300, 30), #hint_text='Usuário': Texto de dica que aparece no campo de entrada.
                                        pos_hint={'center_x': 0.5})
        login_button = Button(text='Login', size_hint=(None, None), size=(100, 30), #Button: Cria um botão de login.
                              background_color=(0.2, 0.6, 0.8, 0.5), pos_hint={'center_x': 0.5})  
        login_button.bind(on_press=self.realizar_login)
        self.message_label = Label(color=(0, 0, 0, 1), pos_hint={'center_x': 0.5})  
        developed_by_label = Label(
            text='Desenvolvido por: Vinícius Magalhães', color=(0.5, 0.5, 0.5, 1), font_size=10,
            pos_hint={'center_x': 0.5, 'y': 0.1})  
        self.layout.add_widget(self.logo_image)
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(login_button)
        self.layout.add_widget(self.message_label)
        self.layout.add_widget(developed_by_label)

    def realizar_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if username == '' and password == '':
            self.manager.current = 'processos'
        else:
            self.message_label.text = 'Nome de usuário ou senha incorretos!'

class ProcessosScreen(CustomScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = FloatLayout()

        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None), size=(600, 50))
        button_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        recebimento_button = Button(text="Recebimento", size_hint=(None, None), size=(200, 50),
                                    background_color=(0.2, 0.6, 0.8, 0.5))
        recebimento_button.bind(on_press=self.processo_recebimento)
        button_layout.add_widget(recebimento_button)

        conferencia_button = Button(text="Conferência", size_hint=(None, None), size=(200, 50),
                                    background_color=(0.2, 0.6, 0.8, 0.5))
        conferencia_button.bind(on_press=self.processo_conferencia)
        button_layout.add_widget(conferencia_button)

        coleta_button = Button(text="Coleta", size_hint=(None, None), size=(200, 50),
                               background_color=(0.2, 0.6, 0.8, 0.5))
        coleta_button.bind(on_press=self.processo_coleta)
        button_layout.add_widget(coleta_button)

        main_layout.add_widget(button_layout)

        voltar_button = Button(text="Voltar", size_hint=(None, None), size=(100, 30),
                               pos_hint={'x': 0.05, 'y': 0.05}, background_color=(0.8, 0.2, 0.2, 0.5))
        voltar_button.bind(on_press=self.voltar_para_login)
        main_layout.add_widget(voltar_button)

        self.add_widget(main_layout)

    def processo_recebimento(self, instance):
        self.manager.current = 'cnpj_input'

    def processo_conferencia(self, instance):
        self.manager.current = 'conferencia'

    def processo_coleta(self, instance):
        self.manager.current = 'coleta'

    def voltar_para_login(self, instance):
        self.manager.current = 'login'

class ConferenciaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = GridLayout(cols=1, spacing=10, padding=100)
        main_layout.bind(size=self._update_rect, pos=self._update_rect)

        with main_layout.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos, source='vetor.jpg')

        label_data = Label(text=self.get_data_atual(), color=(0, 0, 0, 1), size_hint_y=None, height=30)
        main_layout.add_widget(label_data)

        label_os = Label(text="OS:", color=(0, 0, 0, 1), size_hint_y=None, height=30)
        main_layout.add_widget(label_os)

        self.volumes_input = TextInput(hint_text='Volumes', size_hint=(None, None), height=30, width=200, pos_hint={'center_x': 0.5})
        main_layout.add_widget(self.volumes_input)

        self.dimensoes_input = TextInput(hint_text='Dimensões', size_hint=(None, None), height=30, width=200, pos_hint={'center_x': 0.5})
        main_layout.add_widget(self.dimensoes_input)

        self.peso_input = TextInput(hint_text='Peso (kg)', size_hint=(None, None), height=30, width=200, pos_hint={'center_x': 0.5})
        main_layout.add_widget(self.peso_input)

        self.tipo_spinner = Spinner(text='Tipo', values=('CAIXA', 'MALETA', 'PALETE', 'SOLTO', 'OUTROS'),
                               size_hint=(None, None), height=25, width=200, pos_hint={'center_x': 0.5})
        main_layout.add_widget(self.tipo_spinner) 

        self.responsavel_spinner = Spinner(text='Responsável', values=('VINÍCIUS', 'NICOLAS', 'ANDRÉ', 'MATEUS', 'GUILHERME'),
                                     size_hint=(None, None), height=25, width=200, pos_hint={'center_x': 0.5})
        main_layout.add_widget(self.responsavel_spinner)

        button_layout = GridLayout(cols=1, spacing=10, size_hint=(None, None), height=60, width=200, pos_hint={'center_x': 0.5})

        salvar_button = Button(text='Salvar', size_hint=(None, None), size=(100, 30), background_color=(0.2, 0.6, 0.8, 0.5))
        salvar_button.bind(on_press=self.salvar)
        button_layout.add_widget(salvar_button)

        main_layout.add_widget(button_layout)

        scroll_view = ScrollView()
        scroll_view.add_widget(main_layout)

        self.add_widget(scroll_view)

        self._update_rect(self, self.size)

        # Adicionar o botão "Voltar"
        voltar_button = Button(text='Voltar', size_hint=(None, None), size=(100, 30),
                               pos_hint={'x': 0.05, 'y': 0.05}, background_color=(0.8, 0.2, 0.2, 0.5))
        voltar_button.bind(on_press=self.voltar_para_processos)
        self.add_widget(voltar_button)

    def _update_rect(self, instance, size):
        self.rect.size = size
        self.rect.pos = instance.pos

    def get_data_atual(self):
        data_atual = date.today()
        data_formatada = data_atual.strftime("%d/%m/%Y")
        return f'Data de hoje: {data_formatada}'

    def salvar(self, instance):
        volumes = self.volumes_input.text
        dimensoes = self.dimensoes_input.text
        peso = self.peso_input.text
        tipo = self.tipo_spinner.text
        responsavel = self.responsavel_spinner.text
        print(f'Dados: Volumes={volumes}, Dimensões={dimensoes}, Peso={peso}, Tipo={tipo}, Responsável={responsavel}')

    def voltar_para_processos(self, instance):
        self.manager.current = 'processos'

class CNPJInputScreen(CustomScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(text='Pesquisar CNPJ:', font_size=15, color=(0, 0, 0, 1))  
        self.cnpj_input = TextInput(hint_text='CNPJ', size_hint=(None, None), size=(100, 30), pos_hint={'center_x': 0.5})
        confirm_button = Button(text='Confirmar', size_hint=(None, None), size=(100, 30), background_color=(0.2, 0.6, 0.8, 0.5), pos_hint={'center_x': 0.5})  
        confirm_button.bind(on_press=self.validar_cnpj)
        self.message_label = Label(color=(0, 0, 0, 1), pos_hint={'center_x': 0.5})  
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.cnpj_input)
        self.layout.add_widget(confirm_button)
        self.layout.add_widget(self.message_label)

    
        voltar_button = Button(text='Voltar', size_hint=(None, None), size=(100, 30), background_color=(0.8, 0.2, 0.2, 0.5), pos_hint={'x': 0, 'y': 0})  
        voltar_button.bind(on_press=self.voltar_processos)
        self.layout.add_widget(voltar_button)

    def voltar_processos(self, instance):
        self.manager.current = 'processos'


    def validar_cnpj(self, instance):
        cnpj = self.cnpj_input.text.strip()
        if cnpj == '':
            self.manager.current = 'inserir_nota_fiscal'
        else:
            self.message_label.text = 'CNPJ inválido. Por favor, insira um CNPJ válido!'

class InserirNotaFiscalScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout principal da tela
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Imagem de fundo
        with self.canvas.before:
            self.background = Rectangle(source='vetor.jpg', pos=self.pos, size=self.size)
            self.bind(pos=self.update_background, size=self.update_background)
        
        # Widgets da tela
        self.label_ordem_servico = Label(text='ORDEM DE SERVIÇO (OS)', font_size=24, halign='center', size_hint_y=None, height=50, color=(0, 0, 0, 1))
        self.label_nota_fiscal = Label(text='Número da Nota Fiscal:', font_size=18, color=(0, 0, 0, 1))
        self.nota_fiscal_input = TextInput(hint_text='Número da Nota Fiscal', size_hint=(None, None), size=(150, 30), pos_hint={'center_x': 0.5})
        self.label_embalagem = Label(text='Descrição da Embalagem:', font_size=18, color=(0, 0, 0, 1))
        self.embalagem_input = TextInput(hint_text='Descrição da Embalagem', size_hint=(None, None), size=(400, 80), pos_hint={'center_x': 0.5})
        self.label_acessorios = Label(text='Acessórios:', font_size=18, color=(0, 0, 0, 1))
        self.acessorios_input = TextInput(hint_text='Acessórios', size_hint=(None, None), size=(400, 80), pos_hint={'center_x': 0.5})
        
        confirmar_button = Button(text='Adicionar Equipamento', size_hint=(None, None), size=(200, 30), background_color=(0.2, 0.6, 0.8, 0.5), pos_hint={'center_x': 0.5})
        confirmar_button.bind(on_press=self.confirmar)
        
        voltar_button = Button(text='Voltar', size_hint=(None, None), size=(100, 30), pos_hint={'x': 0.05, 'y': 0.05}, background_color=(0.8, 0.2, 0.2, 0.5))
        voltar_button.bind(on_press=self.voltar)
        
        self.message_label = Label(color=(0, 0, 0, 1), pos_hint={'center_x': 0.5})
        
        # Adicionando widgets ao layout
        self.layout.add_widget(self.label_ordem_servico)
        self.layout.add_widget(self.label_nota_fiscal)
        self.layout.add_widget(self.nota_fiscal_input)
        self.layout.add_widget(self.label_embalagem)
        self.layout.add_widget(self.embalagem_input)
        self.layout.add_widget(self.label_acessorios)
        self.layout.add_widget(self.acessorios_input)
        self.layout.add_widget(confirmar_button)
        self.layout.add_widget(self.message_label)
        self.add_widget(self.layout)
        self.add_widget(voltar_button)  # Adicionando o botão de voltar à tela
    
    def update_background(self, instance, value):
        self.background.pos = self.pos
        self.background.size = self.size
    
    def confirmar(self, instance):
        # Lógica para adicionar equipamento
        numero_nota_fiscal = self.nota_fiscal_input.text.strip()
        descricao_embalagem = self.embalagem_input.text.strip()
        acessorios = self.acessorios_input.text.strip()
        
        # Navega para outra tela (simulado)
        self.manager.current = 'cadastro'  # Substituir pelo nome da tela desejada
    
    def voltar(self, instance):
        # Navega para a tela anterior
        self.manager.current = 'cnpj_input'  # Substituir pelo nome da tela anterior

class CustomSpinner(Spinner):
    background_color = ListProperty([1, 1, 1, 1]) 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_background, size=self.update_background)

    def update_background(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.background_color)
            Rectangle(pos=self.pos, size=self.size)

class CadastroEquipamentosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Imagem como fundo
        self.background = Image(source='vetor.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        # Label para exibir a data atual
        self.label_data = Label(text=self.get_data_atual(), size_hint=(1, None), height=50, color=(1, 1, 1, 1))  # Branco
        self.layout.add_widget(self.label_data)

        # Espaço em branco para centralizar elementos
        self.layout.add_widget(Label())  # Espaço em branco

        # Spinner para seleção do tipo de pesquisa
        self.spinner_tipo_pesquisa = Spinner(text='Tipo de Pesquisa', values=('Certificado', 'Serial do Sensor', 'Serial da Eletrônica'),
                                            size_hint=(None, None), size=(300, 30), pos_hint={'center_x': 0.5})  # Use o CustomSpinner aqui
        self.layout.add_widget(self.spinner_tipo_pesquisa)

        # TextInput para entrada de dados
        self.text_input = TextInput(hint_text='', multiline=False, size_hint=(None, None), size=(300, 30), pos_hint={'center_x': 0.5})  # Ajuste conforme necessário
        self.layout.add_widget(self.text_input)

        # Botão 'Salvar OS' centralizado
        salvar_button = Button(text='Salvar OS', size_hint=(None, None), size=(150, 30), background_color=(0.2, 0.6, 0.8, 0.5), pos_hint={'center_x': 0.5})  # Azul claro transparente
        salvar_button.bind(on_press=self.salvar_os)
        self.layout.add_widget(salvar_button)

        # Espaço em branco para centralizar elementos
        self.layout.add_widget(Label())  # Espaço em branco

        # Botão 'Voltar' no canto inferior esquerdo
        voltar_button = Button(text='Voltar', size_hint=(None, None), size=(100, 30), pos_hint={'x': 0.05, 'y': 0.05}, background_color=(0.8, 0.2, 0.2, 0.5))  # Cor padrão (branco)
        voltar_button.bind(on_press=self.voltar_inserir_nota_fiscal)
        self.layout.add_widget(voltar_button)

        self.add_widget(self.layout)

    def voltar_inserir_nota_fiscal(self, instance):
        self.manager.current = 'inserir_nota_fiscal'

    def salvar_os(self, instance):
        # Adicione aqui a lógica para salvar a OS
        pass

    def get_data_atual(self):
        data_atual = datetime.date.today()
        data_formatada = data_atual.strftime("%d/%m/%Y")
        return f'Data de hoje: {data_formatada}'

class GerenciadorTelas(ScreenManager):
    pass

class ColetaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=(10, 50))
        main_layout.bind(minimum_height=main_layout.setter('height'))

        with self.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.vetor_image = Image(source='vetor.jpg', allow_stretch=True, keep_ratio=False)
            self.bind(size=self._update_rect, pos=self._update_rect)

        label_titulo = Label(text='Despacho', size_hint=(1, None), height=30, color=(0, 0, 0, 1)) 
        main_layout.add_widget(label_titulo)

        label_data = Label(text=self.get_data_atual(), size_hint=(1, None), height=30, color=(0, 0, 0, 1))
        main_layout.add_widget(label_data)

        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        self.responsavel_spinner = Spinner(text='Responsável', values=('VINÍCIUS', 'NICOLAS', 'ANDRÉ', 'MATEUS', 'GUILHERME'),
                                           size_hint_y=None, height=30)
        form_layout.add_widget(self.responsavel_spinner)

        self.motorista_input = TextInput(hint_text='Motorista', size_hint_y=None, height=30)
        form_layout.add_widget(self.motorista_input)

        self.transportadora_input = TextInput(hint_text='Transportadora', size_hint_y=None, height=30)
        form_layout.add_widget(self.transportadora_input)

        self.rg_input = TextInput(hint_text='RG', size_hint_y=None, height=30)
        form_layout.add_widget(self.rg_input)

        self.placa_input = TextInput(hint_text='Placa', size_hint_y=None, height=30)
        form_layout.add_widget(self.placa_input)

        main_layout.add_widget(form_layout)

        button_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=60)
        
        voltar_button = Button(text='Voltar', size_hint=(None, None), size=(100, 30), background_color=(0.8, 0.2, 0.2, 0.5))
        voltar_button.bind(on_press=self.voltar_para_processos)
        button_layout.add_widget(voltar_button)

        gravar_button = Button(text='Gravar', size_hint=(None, None), size=(100, 30), background_color=(0.2, 0.6, 0.8, 0.5))
        gravar_button.bind(on_press=self.gravar_coleta)  # Ação de gravar
        button_layout.add_widget(gravar_button)

        main_layout.add_widget(button_layout)

        scroll_view = ScrollView(size_hint=(None, None), size=(Window.width, Window.height))
        scroll_view.add_widget(main_layout)
        scroll_view.center = Window.center  # Centraliza o ScrollView na janela

        self.add_widget(scroll_view)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
        self.vetor_image.size = instance.size

    def get_data_atual(self):
        data_atual = date.today()
        data_formatada = data_atual.strftime("%d/%m/%Y")
        return f'Data de hoje: {data_formatada}'

    def voltar_para_processos(self, instance):
        self.manager.current = 'processos'

    def gravar_coleta(self, instance):
        numero_os = self.os_input.text.strip()
        responsavel = self.responsavel_spinner.text
        motorista = self.motorista_input.text.strip()
        transportadora = self.transportadora_input.text.strip()
        rg = self.rg_input.text.strip()
        placa = self.placa_input.text.strip()

        # Lógica para gravar os dados no banco de dados
        # Aqui você implementaria a lógica para conectar ao banco de dados e gravar os dados coletados
        print(f'Dados de coleta gravados: OS={numero_os}, Responsável={responsavel}, Motorista={motorista}, Transportadora={transportadora}, RG={rg}, Placa={placa}')
        # Após gravar os dados, você pode limpar os campos se desejar
        self.os_input.text = ''
        self.responsavel_spinner.text = 'Responsável'
        self.motorista_input.text = ''
        self.transportadora_input.text = ''
        self.rg_input.text = ''
        self.placa_input.text = ''

class GerenciadorTelas(ScreenManager):
    pass

class ACCIApp(App):

    def build(self):
        gerenciador = GerenciadorTelas()
        gerenciador.add_widget(LoginScreen(name='login'))
        gerenciador.add_widget(ProcessosScreen(name='processos'))
        gerenciador.add_widget(ConferenciaScreen(name='conferencia'))
        gerenciador.add_widget(CNPJInputScreen(name='cnpj_input'))
        gerenciador.add_widget(InserirNotaFiscalScreen(name='inserir_nota_fiscal'))
        gerenciador.add_widget(CadastroEquipamentosScreen(name='cadastro'))
        gerenciador.add_widget(ColetaScreen(name='coleta'))
        return gerenciador

if __name__ == '__main__':
    ACCIApp().run()
