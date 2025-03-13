import customtkinter as ctk
from datetime import datetime, timedelta
import calendar
from tkcalendar import Calendar
import pandas as pd

class TelaAgendamentoAulas(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F5F5F5")
        self.controller = controller
        
        # Fontes
        self.title_font = ctk.CTkFont(family="Helvetica", size=20, weight="bold")
        self.subtitle_font = ctk.CTkFont(family="Helvetica", size=16, weight="bold")
        self.normal_font = ctk.CTkFont(family="Helvetica", size=14)
        self.small_font = ctk.CTkFont(family="Helvetica", size=12)
        
        # Configuração de layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Inicialização dos componentes
        self.setup_sidebar()
        self.setup_main_content()
        
        # Dados de exemplo
        self.professores = ["João Silva", "Maria Oliveira", "Carlos Pereira", "Ana Santos", "Pedro Almeida"]
        self.tipos_aula = ["Musculação", "Yoga", "Pilates", "CrossFit", "Funcional", "Spinning", "Dança", "Natação"]
        
        # Preencher campos com dados
        self.preencher_combobox_professores()
        self.preencher_combobox_tipos_aula()
        self.atualizar_horarios_disponiveis()
        
    def setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(
            self,
            fg_color="#5A189A",
            corner_radius=0,
            width=250
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)
        
        # Logo ou nome do sistema
        logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="GymSystem",
            font=self.title_font,
            text_color="white"
        )
        logo_label.pack(pady=(30, 40))
        
        # Itens do menu
        self.criar_botao_menu("Dashboard", 0)
        self.criar_botao_menu("Membros", 1)
        self.criar_botao_menu("Agenda", 2, True)
        self.criar_botao_menu("Funcionários", 3)
        self.criar_botao_menu("Configurações", 4)
        
        # Informações do usuário no rodapé da sidebar
        user_frame = ctk.CTkFrame(
            self.sidebar_frame,
            fg_color="transparent"
        )
        user_frame.pack(side="bottom", pady=20, fill="x")
        
        # Foto de perfil (simulada como um círculo)
        profile_frame = ctk.CTkFrame(
            user_frame,
            fg_color="transparent"
        )
        profile_frame.pack(pady=5)
        
        # Círculo para foto de perfil
        profile_size = 70
        profile_photo = ctk.CTkFrame(
            profile_frame,
            width=profile_size,
            height=profile_size,
            corner_radius=profile_size//2,
            fg_color="#E0E0E0"
        )
        profile_photo.pack(pady=5)
        
        # Iniciais do usuário dentro da foto de perfil
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
            command=lambda: self.aftercontroller.mostrar_frame("login") if hasattr(self.controller, "mostrar_frame") else None
        )
        logout_button.pack(pady=5)
    
    def criar_botao_menu(self, texto, indice, ativo=False):
        btn = ctk.CTkButton(
            self.sidebar_frame,
            text=texto,
            font=self.normal_font,
            fg_color="#9D4EDD" if ativo else "transparent",
            text_color="white",
            hover_color="#7B2CBF",
            anchor="w",
            height=40,
            width=200,
            corner_radius=8
        )
        btn.pack(pady=5, padx=20)
        return btn
        
    def setup_main_content(self):
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=15
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Título da página
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        page_title = ctk.CTkLabel(
            title_frame,
            text="Agendamento de Aulas",
            font=self.title_font,
            text_color="#5A189A"
        )
        page_title.pack(side="left")
        
        # Conteúdo principal dividido em duas colunas
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Coluna esquerda - Formulário de agendamento
        left_frame = ctk.CTkFrame(content_frame, fg_color="#F8F9FA", corner_radius=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=0)
        
        form_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título do formulário
        form_title = ctk.CTkLabel(
            form_frame,
            text="Dados da Aula",
            font=self.subtitle_font,
            text_color="#5A189A"
        )
        form_title.pack(anchor="w", pady=(0, 20))
        
        # Campos do formulário
        # 1. Seleção de professor
        prof_label = ctk.CTkLabel(form_frame, text="Professor:", font=self.normal_font)
        prof_label.pack(anchor="w", pady=(0, 5))
        
        self.professor_combobox = ctk.CTkComboBox(
            form_frame,
            width=300,
            font=self.normal_font,
            dropdown_font=self.normal_font,
            button_color="#9D4EDD",
            border_color="#9D4EDD",
            button_hover_color="#7B2CBF",
            dropdown_hover_color="#7B2CBF"
        )
        self.professor_combobox.pack(anchor="w", pady=(0, 15))
        self.professor_combobox.configure(command=self.atualizar_horarios_disponiveis)
        
        # 2. Tipo de aula
        tipo_label = ctk.CTkLabel(form_frame, text="Tipo de Aula:", font=self.normal_font)
        tipo_label.pack(anchor="w", pady=(0, 5))
        
        self.tipo_aula_combobox = ctk.CTkComboBox(
            form_frame,
            width=300,
            font=self.normal_font,
            dropdown_font=self.normal_font,
            button_color="#9D4EDD",
            border_color="#9D4EDD",
            button_hover_color="#7B2CBF",
            dropdown_hover_color="#7B2CBF"
        )
        self.tipo_aula_combobox.pack(anchor="w", pady=(0, 15))
        
        # 3. Data
        data_label = ctk.CTkLabel(form_frame, text="Data:", font=self.normal_font)
        data_label.pack(anchor="w", pady=(0, 5))
        
        data_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        data_frame.pack(anchor="w", fill="x", pady=(0, 15))
        
        now = datetime.now()
        self.cal = Calendar(
            data_frame, 
            selectmode='day',
            year=now.year,
            month=now.month,
            day=now.day,
            background="#9D4EDD",
            foreground="white",
            selectbackground="#5A189A",
            normalbackground="white",
            weekendbackground="#F0F0F0"
        )
        self.cal.pack(pady=5)
        self.cal.bind("<<CalendarSelected>>", lambda e: self.atualizar_horarios_disponiveis())
        
        # 4. Horário
        horario_label = ctk.CTkLabel(form_frame, text="Horário Disponível:", font=self.normal_font)
        horario_label.pack(anchor="w", pady=(0, 5))
        
        self.horario_combobox = ctk.CTkComboBox(
            form_frame,
            width=300,
            font=self.normal_font,
            dropdown_font=self.normal_font,
            button_color="#9D4EDD",
            border_color="#9D4EDD",
            button_hover_color="#7B2CBF",
            dropdown_hover_color="#7B2CBF"
        )
        self.horario_combobox.pack(anchor="w", pady=(0, 15))
        
        # 5. Aluno
        aluno_label = ctk.CTkLabel(form_frame, text="Aluno:", font=self.normal_font)
        aluno_label.pack(anchor="w", pady=(0, 5))
        
        self.aluno_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            font=self.normal_font,
            border_color="#9D4EDD",
            fg_color="white"
        )
        self.aluno_entry.pack(anchor="w", pady=(0, 15))
        
        # 6. Observações
        obs_label = ctk.CTkLabel(form_frame, text="Observações:", font=self.normal_font)
        obs_label.pack(anchor="w", pady=(0, 5))
        
        self.obs_textbox = ctk.CTkTextbox(
            form_frame,
            width=300,
            height=100,
            font=self.normal_font,
            border_color="#9D4EDD",
            fg_color="white",
            scrollbar_button_color="#9D4EDD"
        )
        self.obs_textbox.pack(anchor="w", pady=(0, 20))
        
        # Botões
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        self.cancelar_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            font=self.normal_font,
            fg_color="#E0E0E0",
            text_color="black",
            hover_color="#CCCCCC",
            width=140,
            height=40,
            corner_radius=8
        )
        self.cancelar_btn.pack(side="left", padx=(0, 10))
        
        self.agendar_btn = ctk.CTkButton(
            buttons_frame,
            text="Agendar Aula",
            font=self.normal_font,
            fg_color="#9D4EDD",
            hover_color="#7B2CBF",
            width=140,
            height=40,
            corner_radius=8,
            command=self.agendar_aula
        )
        self.agendar_btn.pack(side="left")
        
        # Coluna direita - Agenda do professor
        right_frame = ctk.CTkFrame(content_frame, fg_color="#F8F9FA", corner_radius=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=0)
        
        agenda_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        agenda_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título da agenda
        agenda_title = ctk.CTkLabel(
            agenda_frame,
            text="Agenda do Professor",
            font=self.subtitle_font,
            text_color="#5A189A"
        )
        agenda_title.pack(anchor="w", pady=(0, 20))
        
        # Tabela de agendamentos
        self.tree_frame = ctk.CTkFrame(agenda_frame, fg_color="transparent")
        self.tree_frame.pack(fill="both", expand=True)
        
        # Como o Treeview do tkinter não é suportado diretamente pelo customtkinter,
        # vamos simular uma tabela com labels
        
        # Cabeçalho da tabela
        header_frame = ctk.CTkFrame(self.tree_frame, fg_color="#9D4EDD", corner_radius=0)
        header_frame.pack(fill="x", pady=(0, 1))
        
        headers = ["Data", "Horário", "Tipo de Aula", "Aluno"]
        widths = [0.25, 0.15, 0.3, 0.3]
        
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=self.normal_font,
                text_color="white"
            )
            header_label.pack(side="left", expand=True, fill="both", padx=5, pady=8)
        
        # Conteúdo da tabela (exemplo)
        self.table_content_frame = ctk.CTkScrollableFrame(
            self.tree_frame,
            fg_color="transparent",
            scrollbar_button_color="#9D4EDD"
        )
        self.table_content_frame.pack(fill="both", expand=True)
        
        # Preencher com dados de exemplo
        self.atualizar_tabela_agendamentos()
    
    def preencher_combobox_professores(self):
        self.professor_combobox.configure(values=self.professores)
        self.professor_combobox.set(self.professores[0])
    
    def preencher_combobox_tipos_aula(self):
        self.tipo_aula_combobox.configure(values=self.tipos_aula)
        self.tipo_aula_combobox.set(self.tipos_aula[0])
    
    def atualizar_horarios_disponiveis(self, *args):
        # Horários disponíveis (simulação)
        base_horarios = ["07:00", "08:00", "09:00", "10:00", "11:00", 
                         "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"]
        
        professor = self.professor_combobox.get()
        data_sel = self.cal.get_date()
        
        # Simula indisponibilidades aleatórias para o professor
        import random
        random.seed(hash(professor + data_sel))
        horarios_disponiveis = [h for h in base_horarios if random.random() > 0.3]
        
        if not horarios_disponiveis:
            horarios_disponiveis = ["Sem horários disponíveis"]
        
        self.horario_combobox.configure(values=horarios_disponiveis)
        self.horario_combobox.set(horarios_disponiveis[0])
    
    def agendar_aula(self):
        professor = self.professor_combobox.get()
        tipo_aula = self.tipo_aula_combobox.get()
        data = self.cal.get_date()
        horario = self.horario_combobox.get()
        aluno = self.aluno_entry.get()
        observacoes = self.obs_textbox.get("1.0", "end-1c")
        
        if horario == "Sem horários disponíveis":
            return
        
        if not aluno:
            # Mostrar erro (simplificado)
            error_window = ctk.CTkToplevel(self)
            error_window.title("Erro")
            error_window.geometry("300x150")
            error_window.attributes("-topmost", True)
            
            error_label = ctk.CTkLabel(
                error_window,
                text="Por favor, preencha o nome do aluno.",
                font=self.normal_font
            )
            error_label.pack(pady=20)
            
            ok_button = ctk.CTkButton(
                error_window,
                text="OK",
                command=error_window.destroy,
                fg_color="#9D4EDD",
                hover_color="#7B2CBF"
            )
            ok_button.pack(pady=10)
            return
        
        # Simular o agendamento
        # Em um sistema real, salvaria no banco de dados
        
        # Mostrar confirmação
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Sucesso")
        confirm_window.geometry("300x150")
        confirm_window.attributes("-topmost", True)
        
        confirm_label = ctk.CTkLabel(
            confirm_window,
            text="Aula agendada com sucesso!",
            font=self.normal_font
        )
        confirm_label.pack(pady=20)
        
        ok_button = ctk.CTkButton(
            confirm_window,
            text="OK",
            command=confirm_window.destroy,
            fg_color="#9D4EDD",
            hover_color="#7B2CBF"
        )
        ok_button.pack(pady=10)
        
        # Limpar campos
        self.aluno_entry.delete(0, "end")
        self.obs_textbox.delete("1.0", "end")
        
        # Atualizar a tabela
        self.atualizar_tabela_agendamentos(novo_agendamento={
            "data": data,
            "horario": horario,
            "tipo_aula": tipo_aula,
            "aluno": aluno
        })
    
    def atualizar_tabela_agendamentos(self, novo_agendamento=None):
        # Limpar tabela atual
        for widget in self.table_content_frame.winfo_children():
            widget.destroy()
        
        # Dados de exemplo (simulação)
        dados = [
            {"data": "13/03/2025", "horario": "08:00", "tipo_aula": "Musculação", "aluno": "Carlos Mendes"},
            {"data": "13/03/2025", "horario": "10:00", "tipo_aula": "Pilates", "aluno": "Ana Pereira"},
            {"data": "14/03/2025", "horario": "15:00", "tipo_aula": "Yoga", "aluno": "Luiza Silva"},
            {"data": "14/03/2025", "horario": "17:00", "tipo_aula": "Funcional", "aluno": "Marcelo Costa"},
            {"data": "15/03/2025", "horario": "09:00", "tipo_aula": "CrossFit", "aluno": "Juliana Santos"}
        ]
        
        # Adicionar novo agendamento, se houver
        if novo_agendamento:
            dados.append(novo_agendamento)
        
        # Mostrar os dados na tabela
        for i, dado in enumerate(dados):
            row_color = "#F5F5F5" if i % 2 == 0 else "white"
            row_frame = ctk.CTkFrame(self.table_content_frame, fg_color=row_color, corner_radius=0)
            row_frame.pack(fill="x", pady=(0, 1))
            
            data_label = ctk.CTkLabel(
                row_frame,
                text=dado["data"],
                font=self.small_font
            )
            data_label.pack(side="left", expand=True, fill="both", padx=5, pady=8)
            
            horario_label = ctk.CTkLabel(
                row_frame,
                text=dado["horario"],
                font=self.small_font
            )
            horario_label.pack(side="left", expand=True, fill="both", padx=5, pady=8)
            
            tipo_label = ctk.CTkLabel(
                row_frame,
                text=dado["tipo_aula"],
                font=self.small_font
            )
            tipo_label.pack(side="left", expand=True, fill="both", padx=5, pady=8)
            
            aluno_label = ctk.CTkLabel(
                row_frame,
                text=dado["aluno"],
                font=self.small_font
            )
            aluno_label.pack(side="left", expand=True, fill="both", padx=5, pady=8)