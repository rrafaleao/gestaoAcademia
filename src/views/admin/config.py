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
        
        # Sidebar
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
        self.criar_botao_menu("Membros", 1, ativo=True)
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
        
        # Conteúdo principal
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
        
        resultados = self.db.executar_consulta(
            "SELECT nome, telefone, data_nascimento, endereco, email, data_inicio, plano FROM clientes"
        )
        self.db.desconectar()
        
        if resultados:
            for row in resultados:
                data_nasc = row[2].strftime("%d/%m/%Y") if row[2] else ""
                data_inicio = row[5].strftime("%d/%m/%Y") if row[5] else ""
                
                self.tree.insert(
                    "", "end", 
                    values=(row[0], row[1], data_nasc, row[3], row[4], data_inicio, row[6], "Editar / Excluir")
                )

class TelaConfiguracao(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F0F0F0", corner_radius=0)
        self.controller = controller
        self.db = GerenciadorBancoDados()
        self.db.conectar()
        
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
        
        self.grid_columnconfigure(0, minsize=250)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
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
        self.criar_botao_menu("Membros", 1)
        self.criar_botao_menu("Agenda", 2)
        self.criar_botao_menu("Configurações", 4, ativo=True)
        
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
        
        # Conteúdo principal
        self.main_content = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=15
        )
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        
        title_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(title_frame, text="Configurações do Sistema", font=self.title_font, text_color="#333333").pack(side="left")
        
        self.config_frame = ctk.CTkFrame(self.main_content, fg_color="#F8F9FA", corner_radius=10)
        self.config_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        self.criar_secao_config("Configurações Gerais")
        self.nome_academia_entry = self.criar_campo_config("Nome da Academia:")
        self.telefone_entry = self.criar_campo_config("Telefone:")
        self.endereco_entry = self.criar_campo_config("Endereço:")
        self.email_entry = self.criar_campo_config("Email:")

        
        self.criar_secao_config("Configurações de Sistema", pady_top=20)
        
        
        self.backup_frame = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        self.backup_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(
    self.backup_frame, 
    text="Backup automático:", 
    anchor="w", 
    width=150,
    text_color="#333333",  # Texto preto
    font=self.small_font
).pack(side="left")
        
        self.backup_switch = ctk.CTkSwitch(self.backup_frame, text="", onvalue=True, offvalue=False)
        self.backup_switch.pack(side="left")
        
        buttons_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, padx=20, pady=20, sticky="e")
        
        ctk.CTkButton(buttons_frame, text="Cancelar", fg_color="#6c757d", width=100).pack(side="left", padx=(0, 10))
        ctk.CTkButton(buttons_frame, text="Salvar", fg_color="#5A189A", width=100, 
                      command=self.salvar_configuracoes).pack(side="left")
        
        self.carregar_configuracoes()
    
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
    
    def criar_secao_config(self, titulo, pady_top=0):
        section_frame = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        section_frame.pack(fill="x", pady=(pady_top, 5))
        ctk.CTkLabel(section_frame, text=titulo, font=("Barlow", 16, "bold"), text_color="#333333").pack(padx=20, anchor="w")
    
    def criar_campo_config(self, label_text):
        campo_frame = ctk.CTkFrame(self.config_frame, fg_color="transparent")
        campo_frame.pack(fill="x", padx=20, pady=5)
        
        # Label com texto preto
        ctk.CTkLabel(
            campo_frame, 
            text=label_text, 
            anchor="w", 
            width=150,
            text_color="#333333",  # Cor preta ajustada
            font=self.small_font  # Mantendo a fonte consistente
        ).pack(side="left")
        
        # Entry com fundo branco
        entry = ctk.CTkEntry(
            campo_frame, 
            width=300,
            fg_color="white",  # Fundo branco
            border_color="#CCCCCC",  # Borda cinza claro
            text_color="#000000",  # Texto preto
            font=self.small_font
        )
        entry.pack(side="left", padx=(0, 10))
        return entry

    def carregar_configuracoes(self):
        """Carrega configurações existentes do banco de dados"""
        try:
            config = self.db.executar_consulta(
                "SELECT nome_academia, telefone, endereco, email FROM configuracoes LIMIT 1"
            )
            if config:
                self.nome_academia_entry.insert(0, config[0][0])
                self.telefone_entry.insert(0, config[0][1])
                self.endereco_entry.insert(0, config[0][2])
                self.email_entry.insert(0, config[0][3])
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")

    def salvar_configuracoes(self):
        """Salva ou atualiza as configurações no banco de dados"""
        try:
            # Verifica se já existe uma configuração
            existe = self.db.executar_consulta("SELECT id FROM configuracoes LIMIT 1")
            
            if existe:
                # Atualiza registro existente
                self.db.executar_comando(
                    """UPDATE configuracoes 
                    SET nome_academia = %s,
                        telefone = %s,
                        endereco = %s,
                        email = %s""",
                    (
                        self.nome_academia_entry.get(),
                        self.telefone_entry.get(),
                        self.endereco_entry.get(),
                        self.email_entry.get()
                    )
                )
            else:
                # Cria novo registro se não existir
                self.db.executar_comando(
                    """INSERT INTO configuracoes 
                    (nome_academia, telefone, endereco, email)
                    VALUES (%s, %s, %s, %s)""",
                    (
                        self.nome_academia_entry.get(),
                        self.telefone_entry.get(),
                        self.endereco_entry.get(),
                        self.email_entry.get()
                    )
                )
            print("Configurações salvas com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
    
    def navegacao_menu(self, texto):
        if texto == "Dashboard":
            self.controller.mostrar_frame("dashboard")
        elif texto == "Membros":
            self.controller.mostrar_frame("members")
        elif texto == "Agenda":
            self.controller.mostrar_frame("agendar")
        elif texto == "Configurações":
            self.controller.mostrar_frame("config")