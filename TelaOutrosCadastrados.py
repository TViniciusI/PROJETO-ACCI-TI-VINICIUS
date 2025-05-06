from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivy.uix.behaviors import ButtonBehavior


class ClickableCard(MDCard, ButtonBehavior):
    """
    Card clicável que, ao ser clicado, chama
    voltar_para_outros_com_dados(item) na tela de listagem.
    """
    def __init__(self, item_outros, parent_screen, **kwargs):
        super().__init__(**kwargs)
        self.item_outros = item_outros
        self.parent_screen = parent_screen
        self.bind(on_release=self.on_card_click)

    def on_card_click(self, *args):
        self.parent_screen.voltar_para_outros_com_dados(self.item_outros)


class TelaOutrosCadastrados(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Lista local de “Outros”
        # Cada item: {"serie": ..., "modelo": ..., "fabricante": ..., "tag": ..., "sugerir_pintura": ..., "fotos": {...}}
        self.outros = []

        # Layout principal
        self.main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        # Título
        self.title_label = MDLabel(
            text="Lista de Outros Cadastrados",
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
        self.card_container.bind(minimum_height=self.card_container.setter("height"))
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

        # Botão Voltar
        self.voltar_button = MDRaisedButton(
            text="Voltar",
            size_hint=(None, None),
            size=(150, 60),
            md_bg_color=(0.8, 0.2, 0.2, 1)
        )
        self.voltar_button.bind(on_press=self.voltar_para_outros)

        # Layout para manter "Voltar" à esquerda
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

        # Adiciona layout centralizado
        self.bottom_layout.add_widget(center_layout)

        self.main_layout.add_widget(self.bottom_layout)
        self.add_widget(self.main_layout)

    # ========================= RECONSTRUIR CARDS =========================
    def rebuild_cards(self):
        self.card_container.clear_widgets()

        for item in self.outros:
            # item = { "serie": ..., "modelo": ..., "fabricante": ..., "tag": ..., "sugerir_pintura": ..., "fotos": {...} }

            card = ClickableCard(
                item_outros=item,
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

            card_layout = MDBoxLayout(orientation='horizontal', spacing=15)

            # Campos
            info_layout = MDBoxLayout(orientation='vertical', spacing=6)
            serie = item.get("serie", "")
            modelo = item.get("modelo", "")
            fabricante = item.get("fabricante", "")
            tag = item.get("tag", "")
            pintar = item.get("sugerir_pintura", "")

            if serie:
                info_layout.add_widget(MDLabel(text=f"Série: {serie}", font_style="H6"))
            if modelo:
                info_layout.add_widget(MDLabel(text=f"Modelo: {modelo}", font_style="H6"))
            if fabricante:
                info_layout.add_widget(MDLabel(text=f"Fabricante: {fabricante}", font_style="H6"))
            if tag:
                info_layout.add_widget(MDLabel(text=f"Tag: {tag}", font_style="H6"))
            if pintar == "Sim":
                info_layout.add_widget(MDLabel(text="Pintura: Sim", font_style="H6"))

            # Foto principal
            fotos = item.get("fotos", {})
            foto1 = fotos.get("outros_foto_1", "images.jpg")

            foto_layout = MDBoxLayout(orientation='vertical', spacing=5, size_hint=(None, None), size=(50, 50))
            foto_layout.add_widget(Image(source=foto1, size_hint=(None, None), size=(50, 50)))

            # Botão Remover
            remover_button = MDRaisedButton(
                text="Remover",
                size_hint=(None, None),
                size=(100, 50),
                md_bg_color=(0.9, 0.3, 0.3, 1)
            )
            remover_button.bind(on_press=lambda btn, s=serie: self.remover_outros(s))

            card_layout.add_widget(info_layout)
            card_layout.add_widget(foto_layout)
            card_layout.add_widget(remover_button)

            card.add_widget(card_layout)
            self.card_container.add_widget(card)

    # ========================= ADICIONAR =========================
    def adicionar_outros(self, item_outros):
        """Recebe um dict e adiciona na lista local, depois atualiza os cards."""
        self.outros.append(item_outros)
        self.rebuild_cards()

    # ========================= REMOVER =========================
    def remover_outros(self, serie):
        """Remove da lista local o item que tiver a série informada."""
        for i, item in enumerate(self.outros):
            if item.get("serie") == serie:
                self.outros.pop(i)
                break
        self.rebuild_cards()

    # ========================= SALVAR =========================
    def salvar_informacoes(self, instance):
        """Exemplo de salvamento (apenas imprime no console)."""
        print("Outros cadastrados:", self.outros)

    # ========================= VOLTAR =========================
    def voltar_para_outros(self, instance):
        """Volta para TelaOutrosScreen sem dados."""
        self.manager.current = "TelaOutros"

    def voltar_para_outros_com_dados(self, item):
        """
        Carrega as infos na TelaOutrosScreen
        e troca de tela para 'TelaOutros'.
        """
        tela_outros = self.manager.get_screen("TelaOutros")
        tela_outros.carregar_informacoes(item)
        self.manager.current = "TelaOutros"
