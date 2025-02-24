# views/main/main_screen.py
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from tkinter import messagebox

class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F0F0F0", corner_radius=0)
        
        self.controller = controller
        self.current_frame = None
        
        # Configuração de fontes
        try:
            self.title_font = ctk.CTkFont(family="Barlow", size=24, weight="bold")
            self.sidebar_font = ctk.CTkFont(family="Barlow", size=16, weight="bold")
            self.content_font = ctk.CTkFont(family="Barlow", size=14)
        except Exception as e:
            print(f"Erro ao carregar a fonte 'Barlow': {e}")
            self.title_font = ("Arial", 24, "bold")
            self.sidebar_font = ("Arial", 16, "bold")
            self.content_font = ("Arial", 14)
        
        # Criação da estrutura principal
        self.create_layout()
        
        # Por padrão, exibe o dashboard
        self.mostrar_conteudo("dashboard")
    
    def create_layout(self):
        # Layout principal com sidebar e área de conteúdo
        self.sidebar = self.create_sidebar()
        self.sidebar.pack(side="left", fill="y")
        
        self.content_area = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.content_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    def create_sidebar(self):
        # Frame da sidebar
        sidebar = ctk.CTkFrame(self, fg_color="#5A189A", width=250, corner_radius=0)
        
        # Logo da academia no topo
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(pady=20)
        
        # Aqui seria carregado o logo da academia
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="FITPRO",
            font=ctk.CTkFont(family="Barlow", size=28, weight="bold"),
            text_color="white"
        )
        logo_label.pack()
        
        slogan_label = ctk.CTkLabel(
            logo_frame,
            text="Sistema de Gestão",
            font=ctk.CTkFont(family="Barlow", size=12),
            text_color="white"
        )
        slogan_label.pack()
        
        # Separador
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#9D4EDD")
        separator.pack(fill="x", padx=20, pady=10)
        
        # Itens do menu
        menu_items = [
            {"id": "dashboard", "text": "Dashboard", "icon": "dashboard.png"},
            {"id": "alunos", "text": "Alunos", "icon": "users.png"},
            {"id": "planos", "text": "Planos", "icon": "planos.png"},
            {"id": "aulas", "text": "Aulas", "icon": "aulas.png"},
            {"id": "financeiro", "text": "Financeiro", "icon": "financeiro.png"},
            {"id": "relatorios", "text": "Relatórios", "icon": "report.png"},
            {"id": "configuracoes", "text": "Configurações", "icon": "settings.png"}
        ]
        
        for item in menu_items:
            self.create_menu_item(sidebar, item)
        
        # Separador
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#9D4EDD")
        separator.pack(fill="x", padx=20, pady=10)
        
        # Informações do usuário logado
        user_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        user_frame.pack(pady=10, padx=20, fill="x")
        
        user_label = ctk.CTkLabel(
            user_frame,
            text="Bem-vindo,",
            font=self.content_font,
            text_color="white"
        )
        user_label.pack(anchor="w")
        
        user_name = ctk.CTkLabel(
            user_frame,
            text="Nome do Usuário",
            font=self.sidebar_font,
            text_color="white"
        )
        user_name.pack(anchor="w")
        
        # Botão de logout
        logout_btn = ctk.CTkButton(
            sidebar,
            text="Sair",
            fg_color="#9D4EDD",
            hover_color="#7B2CBF",
            font=self.sidebar_font,
            width=200,
            height=40,
            corner_radius=10,
            command=self.logout
        )
        logout_btn.pack(pady=20, padx=20)
        
        return sidebar
    
    def create_menu_item(self, sidebar, item):
        item_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        item_frame.pack(pady=5, padx=20, fill="x")
        
        # Aqui você carregaria o ícone com PIL
        # Para exemplo, estamos criando apenas o botão sem o ícone
        item_btn = ctk.CTkButton(
            item_frame,
            text=item["text"],
            fg_color="transparent",
            hover_color="#9D4EDD",
            text_color="white",
            anchor="w",
            font=self.sidebar_font,
            width=200,
            height=40,
            corner_radius=10,
            command=lambda i=item["id"]: self.mostrar_conteudo(i)
        )
        item_btn.pack(fill="x")
    
    def mostrar_conteudo(self, content_id):
        # Limpa o conteúdo atual
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Título do conteúdo
        content_title_map = {
            "dashboard": "Dashboard",
            "alunos": "Gestão de Alunos",
            "planos": "Planos e Mensalidades",
            "aulas": "Aulas e Atividades",
            "financeiro": "Controle Financeiro",
            "relatorios": "Relatórios",
            "configuracoes": "Configurações"
        }
        
        # Título da seção
        title_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        title_frame.pack(fill="x", pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=content_title_map.get(content_id, "Conteúdo"),
            font=self.title_font,
            text_color="black"
        )
        title_label.pack(anchor="w")
        
        # Linha separadora
        separator = ctk.CTkFrame(self.content_area, height=2, fg_color="#5A189A")
        separator.pack(fill="x", pady=10)
        
        # Conteúdo específico para cada seção
        if content_id == "dashboard":
            self.criar_dashboard()
        elif content_id == "alunos":
            self.criar_secao_alunos()
        # Implemente outras seções conforme necessário
    
    def criar_dashboard(self):
        # Grid para os cards de resumo
        grid_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, pady=20)
        
        # Configurar o grid com 2 colunas
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)
        
        # Cards de resumo
        cards_info = [
            {"title": "Total de Alunos", "value": "152", "color": "#9D4EDD"},
            {"title": "Mensalidades Pendentes", "value": "28", "color": "#E63946"},
            {"title": "Aulas Hoje", "value": "12", "color": "#457B9D"},
            {"title": "Novos Cadastros", "value": "7", "color": "#2A9D8F"}
        ]
        
        # Criar os cards em grid
        for i, card in enumerate(cards_info):
            row, col = divmod(i, 2)
            self.criar_card_resumo(grid_frame, card, row, col)
        
        # Seção de atividades recentes
        recent_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        recent_frame.pack(fill="both", expand=True, pady=20)
        
        recent_label = ctk.CTkLabel(
            recent_frame,
            text="Atividades Recentes",
            font=self.sidebar_font,
            text_color="black"
        )
        recent_label.pack(anchor="w", pady=10)
        
        # Lista de atividades recentes
        activities = [
            "João Silva fez check-in às 08:30",
            "Maria Oliveira pagou mensalidade de Fevereiro",
            "Nova aula de Spinning adicionada para Quarta-feira",
            "Carlos Santos cancelou agendamento de personal trainer",
            "Atualização no plano Trimestral"
        ]
        
        for activity in activities:
            activity_frame = ctk.CTkFrame(recent_frame, fg_color="#F8F9FA", corner_radius=5)
            activity_frame.pack(fill="x", pady=5)
            
            activity_label = ctk.CTkLabel(
                activity_frame,
                text=activity,
                font=self.content_font,
                text_color="black"
            )
            activity_label.pack(anchor="w", padx=10, pady=10)
    
    def criar_card_resumo(self, parent, card_info, row, col):
        card = ctk.CTkFrame(parent, fg_color=card_info["color"], corner_radius=10)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        value_label = ctk.CTkLabel(
            card,
            text=card_info["value"],
            font=ctk.CTkFont(family="Barlow", size=36, weight="bold"),
            text_color="white"
        )
        value_label.pack(pady=(20, 5))
        
        title_label = ctk.CTkLabel(
            card,
            text=card_info["title"],
            font=self.sidebar_font,
            text_color="white"
        )
        title_label.pack(pady=(5, 20))
    
    def criar_secao_alunos(self):
        # Exemplo de implementação para a seção de alunos
        actions_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        actions_frame.pack(fill="x", pady=10)
        
        search_entry = ctk.CTkEntry(
            actions_frame,
            placeholder_text="Buscar aluno...",
            width=300,
            height=40,
            fg_color="white",
            text_color="black",
            corner_radius=10,
            border_color="#5A189A",
            border_width=2
        )
        search_entry.pack(side="left", padx=5)
        
        search_btn = ctk.CTkButton(
            actions_frame,
            text="Buscar",
            fg_color="#5A189A",
            hover_color="#3C096C",
            width=100,
            height=40,
            font=self.content_font,
            corner_radius=10
        )
        search_btn.pack(side="left", padx=5)
        
        add_btn = ctk.CTkButton(
            actions_frame,
            text="Novo Aluno",
            fg_color="#2A9D8F",
            hover_color="#1F7A6F",
            width=150,
            height=40,
            font=self.content_font,
            corner_radius=10
        )
        add_btn.pack(side="right", padx=5)
        
        # Tabela de alunos (simulação)
        table_frame = ctk.CTkFrame(self.content_area, fg_color="white", corner_radius=10, border_width=1, border_color="#E0E0E0")
        table_frame.pack(fill="both", expand=True, pady=20)
        
        # Cabeçalho da tabela
        header_frame = ctk.CTkFrame(table_frame, fg_color="#F0F0F0", corner_radius=0)
        header_frame.pack(fill="x")
        
        headers = ["ID", "Nome", "Plano", "Vencimento", "Status", "Ações"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=self.sidebar_font,
                text_color="black",
                width=100
            )
            header_label.grid(row=0, column=i, padx=10, pady=10, sticky="w")
        
        # Dados da tabela (exemplo)
        alunos_exemplo = [
            {"id": "001", "nome": "João Silva", "plano": "Mensal", "vencimento": "15/03/2025", "status": "Ativo"},
            {"id": "002", "nome": "Maria Oliveira", "plano": "Trimestral", "vencimento": "22/04/2025", "status": "Ativo"},
            {"id": "003", "nome": "Carlos Santos", "plano": "Anual", "vencimento": "05/01/2026", "status": "Inativo"},
            {"id": "004", "nome": "Ana Pereira", "plano": "Mensal", "vencimento": "10/03/2025", "status": "Pendente"},
            {"id": "005", "nome": "Lucas Mendes", "plano": "Semestral", "vencimento": "30/07/2025", "status": "Ativo"}
        ]
        
        for row_idx, aluno in enumerate(alunos_exemplo, start=1):
            row_bg = "#FFFFFF" if row_idx % 2 == 0 else "#F8F9FA"
            row_frame = ctk.CTkFrame(table_frame, fg_color=row_bg, corner_radius=0, height=40)
            row_frame.pack(fill="x")
            
            # Status color
            status_color = {
                "Ativo": "#4CAF50",
                "Inativo": "#F44336",
                "Pendente": "#FFC107"
            }.get(aluno["status"], "#757575")
            
            # Dados da linha
            ctk.CTkLabel(row_frame, text=aluno["id"], text_color="black", width=100).grid(row=0, column=0, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(row_frame, text=aluno["nome"], text_color="black", width=100).grid(row=0, column=1, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(row_frame, text=aluno["plano"], text_color="black", width=100).grid(row=0, column=2, padx=10, pady=10, sticky="w")
            ctk.CTkLabel(row_frame, text=aluno["vencimento"], text_color="black", width=100).grid(row=0, column=3, padx=10, pady=10, sticky="w")
            
            status_frame = ctk.CTkFrame(row_frame, fg_color=status_color, corner_radius=5, width=80, height=25)
            status_frame.grid(row=0, column=4, padx=10, pady=10)
            ctk.CTkLabel(status_frame, text=aluno["status"], text_color="white", font=("Arial", 12)).pack(pady=2)
            
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            actions_frame.grid(row=0, column=5, padx=10, pady=5)
            
            edit_btn = ctk.CTkButton(
                actions_frame,
                text="Editar",
                fg_color="#5A189A",
                hover_color="#3C096C",
                width=70,
                height=30,
                font=("Arial", 12),
                corner_radius=5
            )
            edit_btn.pack(side="left", padx=2)
            
            del_btn = ctk.CTkButton(
                actions_frame,
                text="Excluir",
                fg_color="#E63946",
                hover_color="#C1121F",
                width=70,
                height=30,
                font=("Arial", 12),
                corner_radius=5
            )
            del_btn.pack(side="left", padx=2)
    
    def logout(self):
        """Realiza o logout do usuário"""
        if messagebox.askyesno("Logout", "Deseja realmente sair?"):
            self.controller.mostrar_frame("login")