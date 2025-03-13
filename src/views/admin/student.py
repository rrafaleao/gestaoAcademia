import customtkinter as ctk
from tkinter import ttk, StringVar
import datetime
from tkcalendar import DateEntry
from database.db_connection import GerenciadorBancoDados

class AlunosFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F0F0F0", corner_radius=0)
        
        self.controller = controller
        self.db = GerenciadorBancoDados()
        
        try:
            self.barlow_font = ctk.CTkFont(family="Barlow", size=16, weight="bold")
            self.title_font = ctk.CTkFont(family="Barlow", size=24, weight="bold")
            self.subtitle_font = ctk.CTkFont(family="Barlow", size=20, weight="bold")
            self.small_font = ctk.CTkFont(family="Barlow", size=14)
            self.large_value_font = ctk.CTkFont(family="Barlow", size=48, weight="bold")
            self.metric_label_font = ctk.CTkFont(family="Barlow", size=18)
        except Exception as e:
            self.barlow_font = ("Arial", 16)
            self.title_font = ("Arial", 24, "bold")
            self.subtitle_font = ("Arial", 20, "bold")
            self.small_font = ("Arial", 14)
            self.large_value_font = ("Arial", 48, "bold")
            self.metric_label_font = ("Arial", 18)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.sidebar_frame = ctk.CTkFrame(
            self,
            fg_color="#5A189A",
            corner_radius=0,
            width=250
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)
        
        logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="GymSystem",
            font=self.title_font,
            text_color="white"
        )
        logo_label.pack(pady=(30, 40))
        
        self.criar_botao_menu("Dashboard", 0)
        self.criar_botao_menu("Membros", 1, True)
        self.criar_botao_menu("Agenda", 2)
        self.criar_botao_menu("Funcionários", 3)
        self.criar_botao_menu("Configurações", 4)
        
        user_frame = ctk.CTkFrame(
            self.sidebar_frame,
            fg_color="transparent"
        )
        user_frame.pack(side="bottom", pady=20, fill="x")
        
        profile_frame = ctk.CTkFrame(
            user_frame,
            fg_color="transparent"
        )
        profile_frame.pack(pady=5)
        
        profile_size = 70
        profile_photo = ctk.CTkFrame(
            profile_frame,
            width=profile_size,
            height=profile_size,
            corner_radius=profile_size//2,
            fg_color="#E0E0E0"
        )
        profile_photo.pack(pady=5)
        
        initials_label = ctk.CTkLabel(
            profile_photo,
            text="AD",
            font=self.title_font,
            text_color="#5A189A"
        )
        initials_label.place(relx=0.5, rely=0.5, anchor="center")
        
        user_name = ctk.CTkLabel(
            user_frame,
            text="Admin",
            font=self.small_font,
            text_color="white"
        )
        user_name.pack(pady=2)
        
        logout_button = ctk.CTkButton(
            user_frame,
            text="Sair",
            fg_color="#9D4EDD",
            hover_color="#7B2CBF",
            height=30,
            width=100,
            corner_radius=8,
            command=lambda: controller.mostrar_frame("login") if hasattr(controller, "mostrar_frame") else None
        )
        logout_button.pack(pady=5)
        
        self.main_content = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=15
        )
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(2, weight=1)
        
        title_frame = ctk.CTkFrame(
            self.main_content,
            fg_color="transparent"
        )
        title_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="Gerenciamento de Alunos",
            font=self.title_font,
            text_color="#333333"
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        button_frame = ctk.CTkFrame(
            title_frame,
            fg_color="transparent"
        )
        button_frame.grid(row=0, column=1, sticky="e")
        
        add_button = ctk.CTkButton(
            button_frame,
            text="+ Novo Aluno",
            fg_color="#5A189A",
            hover_color="#7B2CBF",
            height=35,
            width=130,
            corner_radius=8,
            command=lambda: controller.mostrar_frame("novo_aluno") if hasattr(controller, "mostrar_frame") else None
        )
        add_button.pack(side="left", padx=5)
        
        table_frame = ctk.CTkFrame(
            self.main_content,
            fg_color="transparent"
        )
        table_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        style = ttk.Style()
        style.configure("Treeview", font=self.small_font, rowheight=40)
        style.configure("Treeview.Heading", font=self.barlow_font, background="#E6E6E6")
        style.map("Treeview", background=[("selected", "#9D4EDD")])
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=("nome", "telefone", "data_nascimento", "endereco", "email", "data_inicio", "plano", "acoes"),
            show="headings",
            height=10
        )
        
        self.tree.heading("nome", text="Nome")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("data_nascimento", text="Data Nasc.")
        self.tree.heading("endereco", text="Endereço")
        self.tree.heading("email", text="Email")
        self.tree.heading("data_inicio", text="Data Início")
        self.tree.heading("plano", text="Plano")
        self.tree.heading("acoes", text="Ações")
        
        self.tree.column("nome", width=180)
        self.tree.column("telefone", width=120)
        self.tree.column("data_nascimento", width=100)
        self.tree.column("endereco", width=200)
        self.tree.column("email", width=180)
        self.tree.column("data_inicio", width=100)
        self.tree.column("plano", width=120)
        self.tree.column("acoes", width=120)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.carregar_dados_exemplo()
    
    def navegacao_menu(self, texto):
        if texto == "Membros" and self.controller:
            self.controller.mostrar_frame("members")
        elif texto == "Dashboard" and self.controller:
            self.controller.mostrar_frame("dashboard")
        elif texto == "Agenda" and self.controller:
            self.controller.mostrar_frame("agendar")
        elif texto == "Configurações" and self.controller:
            self.controller.mostrar_frame("settings")
    
    def criar_botao_menu(self, texto, indice, ativo=False):
        bg_color = "#9D4EDD" if ativo else "transparent"
        fg_color = "white" if ativo else "#E0E0E0"
        
        btn = ctk.CTkButton(
            self.sidebar_frame,
            text=texto,
            fg_color=bg_color,
            text_color=fg_color,
            hover_color="#7B2CBF",
            anchor="w",
            height=40,
            width=220,
            corner_radius=8,
            font=self.barlow_font,
            command=lambda t=texto: self.navegacao_menu(t)
        )
        btn.pack(pady=5, padx=15)
        return btn
    
    def carregar_dados_exemplo(self):
        """Carrega dados reais do banco de dados"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Busca todos os clientes no banco
        resultados = self.db.executar_consulta(
            "SELECT nome, telefone, data_nascimento, endereco, email, data_inicio, plano FROM clientes"
        )
        self.db.desconectar()
        
        if resultados:
            for row in resultados:
                # Formata datas para dd/mm/yyyy
                data_nasc = row[2].strftime("%d/%m/%Y") if row[2] else ""
                data_inicio = row[5].strftime("%d/%m/%Y") if row[5] else ""
                
                self.tree.insert(
                    "", "end", 
                    values=(row[0], row[1], data_nasc, row[3], row[4], data_inicio, row[6], "Editar / Excluir")
                )
    
    def filtrar_alunos(self, *args):
        """Filtra alunos com base na busca"""
        texto_busca = self.search_var.get().lower()
        
        if not texto_busca:
            self.carregar_dados_exemplo()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Busca filtrada no banco
        search_term = f"%{texto_busca}%"
        query = """
            SELECT nome, telefone, data_nascimento, endereco, email, data_inicio, plano 
            FROM clientes 
            WHERE LOWER(nome) LIKE %s 
            OR LOWER(email) LIKE %s 
            OR telefone LIKE %s
        """
        params = (search_term, search_term, search_term)
        
        resultados = self.db.executar_consulta(query, params)
        self.db.desconectar()
        
        if resultados:
            for row in resultados:
                data_nasc = row[2].strftime("%d/%m/%Y") if row[2] else ""
                data_inicio = row[5].strftime("%d/%m/%Y") if row[5] else ""
                
                self.tree.insert(
                    "", "end", 
                    values=(row[0], row[1], data_nasc, row[3], row[4], data_inicio, row[6], "Editar / Excluir")
                )