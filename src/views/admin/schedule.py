import customtkinter as ctk
from datetime import datetime
from tkinter import ttk
from database.db_connection import GerenciadorBancoDados

class TelaAgendamentoAulas(ctk.CTkFrame):
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

        # Sidebar idêntica à da tela de alunos
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
        self.criar_botao_menu("Agenda", 2, True)
        self.criar_botao_menu("Configurações", 3)

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
            text="Agendamento de Aulas",
            font=self.title_font,
            text_color="#333333"
        )
        title_label.grid(row=0, column=0, sticky="w")

        # Formulário de agendamento - DESIGN ATUALIZADO
        self.form_frame = ctk.CTkFrame(
            self.main_content,
            fg_color="#F8F9FA",
            corner_radius=10
        )
        self.form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Configurar o grid para o formulário
        self.form_frame.grid_columnconfigure(0, weight=0)  # Coluna para labels
        self.form_frame.grid_columnconfigure(1, weight=1)  # Coluna para inputs
        
        # Professor
        professor_label = ctk.CTkLabel(
            self.form_frame,
            text="Professor:",
            font=self.small_font,
            text_color="#333333",
            anchor="e"
        )
        professor_label.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="e")
        
        self.professor_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=["João silva", "Pedro Gabriel", "Enzo Rafael"],
            width=300,
            fg_color="white",
            border_color="#CCCCCC"
        )
        self.professor_combobox.grid(row=0, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Tipo de Aula
        tipo_aula_label = ctk.CTkLabel(
            self.form_frame,
            text="Tipo de Aula:",
            font=self.small_font,
            text_color="#333333"
        )
        tipo_aula_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="e")
        
        self.tipo_aula_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=["Ginastica", "Yoga", "Jump", "Musculação"],
            width=300,
            fg_color="white",
            border_color="#CCCCCC"
        )
        self.tipo_aula_combobox.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Horário
        horario_label = ctk.CTkLabel(
            self.form_frame,
            text="Horário:",
            font=self.small_font,
            text_color="#333333"
        )
        horario_label.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="e")
        
        self.horario_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=['08:00', '09:00', "10:00", '11:00', '12:00', "13:00", '14:00', '15:00', "16:00", '17:00', '18:00', "19:00"],
            width=300,
            fg_color="white",
            border_color="#CCCCCC"
        )
        self.horario_combobox.grid(row=2, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Data
        data_label = ctk.CTkLabel(
            self.form_frame,
            text="Data:",
            font=self.small_font,
            text_color="#333333"
        )
        data_label.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="e")
        
        self.data_entry = ctk.CTkEntry(
            self.form_frame,
            width=300,
            placeholder_text="dd/mm/yyyy",
            fg_color="white",
            border_color="#CCCCCC"
        )
        self.data_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.data_entry.grid(row=3, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Aluno
        aluno_label = ctk.CTkLabel(
            self.form_frame,
            text="Aluno:",
            font=self.small_font,
            text_color="#333333"
        )
        aluno_label.grid(row=4, column=0, padx=(20, 10), pady=10, sticky="e")
        
        self.aluno_combobox = ctk.CTkComboBox(
            self.form_frame,
            values=["Rafael", "Mariani"],
            width=300,
            fg_color="white",
            border_color="#CCCCCC"
        )
        self.aluno_combobox.grid(row=4, column=1, padx=(0, 20), pady=10, sticky="w")
        
        # Botão de Agendar
        self.agendar_button = ctk.CTkButton(
            self.form_frame,
            text="Agendar",
            fg_color="#5A189A",
            hover_color="#7B2CBF",
            corner_radius=8,
            command=self.agendar_aula,
            width=150
        )
        self.agendar_button.grid(row=5, column=0, columnspan=2, pady=20)

        # Tabela de agendamentos
        self.tree = ttk.Treeview(
            self.main_content,
            columns=("Data", "Horário", "Professor", "Aula", "Aluno"),
            show="headings",
            height=10
        )
        self.tree.heading("Data", text="Data")
        self.tree.heading("Horário", text="Horário")
        self.tree.heading("Professor", text="Professor")
        self.tree.heading("Aula", text="Aula")
        self.tree.heading("Aluno", text="Aluno")
        
        self.tree.column("Data", width=100)
        self.tree.column("Horário", width=80)
        self.tree.column("Professor", width=120)
        self.tree.column("Aula", width=120)
        self.tree.column("Aluno", width=150)
        
        scrollbar = ttk.Scrollbar(self.main_content, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")

        self.atualizar_tabela()

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

    def navegacao_menu(self, texto):
        if texto == "Membros" and self.controller:
            self.controller.mostrar_frame("members")
        elif texto == "Dashboard" and self.controller:
            self.controller.mostrar_frame("dashboard")
        elif texto == "Agenda" and self.controller:
            self.controller.mostrar_frame("agendar")
        elif texto == "Configurações" and self.controller:
            self.controller.mostrar_frame("config")

    def atualizar_tabela(self):
        """Atualiza a tabela com dados do banco"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        resultados = self.db.executar_consulta(
            "SELECT data, horario, professor, tipo_aula, aluno FROM aulas"
        )
        self.db.desconectar()
        
        if resultados:
            for row in resultados:
                data_formatada = row[0].strftime("%d/%m/%Y") if row[0] else ""
                self.tree.insert(
                    "", "end", 
                    values=(data_formatada, row[1], row[2], row[3], row[4])
                )

    def agendar_aula(self):
        """Registra novo agendamento no banco de dados"""
        try:
            data = datetime.strptime(self.data_entry.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            self.db.executar_comando(
                "INSERT INTO aulas (professor, tipo_aula, data, horario, aluno) VALUES (%s, %s, %s, %s, %s)",
                (self.professor_combobox.get(), 
                 self.tipo_aula_combobox.get(), 
                 data,
                 self.horario_combobox.get(), 
                 self.aluno_combobox.get())
            )
            self.atualizar_tabela()
        except Exception as e:
            print(f"Erro ao agendar aula: {e}")