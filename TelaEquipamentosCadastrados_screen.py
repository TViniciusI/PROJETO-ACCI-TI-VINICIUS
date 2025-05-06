from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.dialog import MDDialog


class ClickableCard(MDCard, ButtonBehavior):
    """
    MDCard que é clicável, chamando voltar_para_cadastro_com_dados(item)
    ao ser clicado.
    """
    def __init__(self, item_dados, parent_screen, **kwargs):
        super().__init__(**kwargs)
        self.item_dados = item_dados
        self.parent_screen = parent_screen
        self.bind(on_release=self.on_card_click)

    def on_card_click(self, *args):
        """
        Ao clicar no card, chamamos a tela de equipamentos para
        voltar para a tela de cadastro com os dados do item.
        """
        self.parent_screen.voltar_para_cadastro_com_dados(self.item_dados)


class TelaEquipamentosCadastrados(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Lista local de equipamentos.
        # Cada item -> {"sensor": "...", "eletronica": "...", "foto": "..." }
        self.equipamentos = []

        # ------------- Layout principal (vertical) -------------
        self.main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        # Título
        self.title_label = MDLabel(
            text="Lista de Equipamentos Cadastrados",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=50,
            theme_text_color="Custom",
            text_color=(0, 0.4, 0.8, 1)
        )
        self.main_layout.add_widget(self.title_label)

        # ScrollView + container de cards
        self.scroll_view = MDScrollView()
        self.card_container = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None
        )
        self.card_container.bind(
            minimum_height=self.card_container.setter("height")
        )
        self.scroll_view.add_widget(self.card_container)
        self.main_layout.add_widget(self.scroll_view)

        # Barra inferior (Voltar, Salvar)
        self.bottom_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=70,
            padding=[10, 10]
        )

        # Botão Voltar (canto esquerdo)
        self.voltar_button = MDRaisedButton(
            text="Voltar",
            size_hint=(None, None),
            size=(150, 60),
            md_bg_color=(0.8, 0.2, 0.2, 1)
        )
        self.voltar_button.bind(on_press=self.voltar_para_cadastro)

        # Layout para manter o botão "Voltar" à esquerda
        left_layout = MDBoxLayout(orientation='horizontal', size_hint=(None, 1))
        left_layout.add_widget(self.voltar_button)
        self.bottom_layout.add_widget(left_layout)

        # Layout central para o botão "Salvar"
        center_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 1))

        self.salvar_button = MDRaisedButton(
            text="Salvar Informações",
            size_hint=(None, None),
            size=(200, 60),
            md_bg_color=(0.2, 0.6, 0.8, 1)
        )
        self.salvar_button.bind(on_press=self.salvar_informacoes)
        center_layout.add_widget(self.salvar_button)

        # Adiciona o layout centralizado para "Salvar"
        self.bottom_layout.add_widget(center_layout)

        self.main_layout.add_widget(self.bottom_layout)
        self.add_widget(self.main_layout)

    # =====================================================
    #   RE-CONSTRUIR TODOS OS CARDS
    # =====================================================
    def rebuild_cards(self):
        """
        Limpa o container e recria todos os cards
        de acordo com self.equipamentos, enumerando as linhas.
        """
        self.card_container.clear_widgets()
        linha_counter = 1

        for item in self.equipamentos:
            sensor = item.get("sensor", "")
            eletronica = item.get("eletronica", "")
            foto = item.get("foto", None)

            # Se tiver eletronica => 2 linhas, senão => 1
            if eletronica:
                lines_used = 2
            else:
                lines_used = 1

            linha_sensor = linha_counter
            linha_eletronica = linha_counter + 1 if lines_used == 2 else None
            linha_counter += lines_used

            # Criamos um ClickableCard
            card = ClickableCard(
                item_dados=item,
                parent_screen=self,
                size_hint=(None, None),
                size=(600, 220),
                elevation=12,
                padding=15,
                radius=[20],
                pos_hint={'center_x': 0.5},
                md_bg_color=(0.96, 0.98, 1, 1),
                line_color=(0.2, 0.4, 0.8, 1)
            )

            # Layout interno
            card_layout = MDBoxLayout(
                orientation='horizontal',
                spacing=15
            )

            # Informações do item
            info_layout = MDBoxLayout(orientation='vertical', spacing=6)
            if sensor:
                info_layout.add_widget(MDLabel(
                    text=f"Sensor: {sensor}",
                    theme_text_color="Primary",
                    font_style="H6"
                ))
            if eletronica:
                info_layout.add_widget(MDLabel(
                    text=f"Eletrônica: {eletronica}",
                    theme_text_color="Primary",
                    font_style="H6"
                ))

            # Linha X ou Linhas X e Y
            if linha_eletronica:
                line_text = f"Linhas {linha_sensor} e {linha_eletronica}"
            else:
                line_text = f"Linha {linha_sensor}"

            info_layout.add_widget(MDLabel(
                text=line_text,
                theme_text_color="Hint"
            ))

            # Foto
            indicador_layout = MDBoxLayout(
                orientation='vertical',
                spacing=5,
                size_hint=(None, None),
                size=(50, 50)
            )
            if foto:
                indicador_layout.add_widget(Image(
                    source=foto,
                    size_hint=(None, None),
                    size=(50, 50)
                ))
            else:
                indicador_layout.add_widget(MDLabel(
                    text="N/A",
                    theme_text_color="Hint",
                    font_style="Caption"
                ))

            # Botão Remover
            remover_button = MDRaisedButton(
                text="Remover",
                size_hint=(None, None),
                size=(100, 50),
                md_bg_color=(0.9, 0.3, 0.3, 1)
            )
            remover_button.bind(
                on_press=lambda btn, s=sensor, e=eletronica: self.remover_item(s, e)
            )

            card_layout.add_widget(info_layout)
            card_layout.add_widget(indicador_layout)
            card_layout.add_widget(remover_button)

            card.add_widget(card_layout)
            self.card_container.add_widget(card)

    # =====================================================
    #   ADICIONAR ITEM E RECONSTRUIR
    # =====================================================
    def adicionar_item_lista(self, sensor, eletronica="", foto=None):
        """
        Acrescenta um item no formato {"sensor": ..., "eletronica":..., "foto": ...}
        e atualiza a tela.
        """
        item = {
            "sensor": sensor,
            "eletronica": eletronica,
            "foto": foto
        }
        self.equipamentos.append(item)
        self.rebuild_cards()

    # =====================================================
    #   REMOVER ITEM
    # =====================================================
    def remover_item(self, sensor, eletronica):
        """
        Remove o dicionário que tiver esses valores de sensor/eletronica
        e refaz a tela.
        """
        for i, eq in enumerate(self.equipamentos):
            if eq.get("sensor", "") == sensor and eq.get("eletronica", "") == eletronica:
                self.equipamentos.pop(i)
                break
        self.rebuild_cards()

    # =====================================================
    #   SALVAR
    # =====================================================
    def salvar_informacoes(self, instance):
        """Exemplo de salvamento (apenas imprime no console)."""
        print("Equipamentos cadastrados:", self.equipamentos)

    # =====================================================
    #   VOLTAR PARA TELA DE CADASTRO SEM DADOS
    # =====================================================
    def voltar_para_cadastro(self, instance):
        """Apenas troca para a tela 'TelaCadastroEquipamento1'."""
        if self.manager:
            self.manager.current = "TelaCadastroEquipamento1"

    # =====================================================
    #   VOLTAR PARA TELA DE CADASTRO COM DADOS
    # =====================================================
    def voltar_para_cadastro_com_dados(self, item):
        """
        Chama 'carregar_informacoes(item)' na tela de cadastro 
        e troca para 'TelaCadastroEquipamento1'.
        """
        tela_cadastro = self.manager.get_screen("TelaCadastroEquipamento1")
        tela_cadastro.carregar_informacoes(item)
        self.manager.current = "TelaCadastroEquipamento1"
