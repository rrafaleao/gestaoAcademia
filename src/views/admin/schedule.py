import customtkinter as ctk
from datetime import datetime, timedelta
import calendar
from tkcalendar import Calendar
import pandas as pd

class TelaAgendamentoAulas(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F5F5F5")
        self.controller = controller
        
        try:
            self.barlow_font = ctk.CTkFont(family="Barlow", size=16, weight="bold")
            self.title_font = ctk.CTkFont(family="Barlow", size=24, weight="bold")
            self.subtitle_font = ctk.CTkFont(family="Barlow", size=20, weight="bold")
            self.small_font = ctk.CTkFont(family="Barlow", size=14)
            self.large_value_font = ctk.CTkFont(family="Barlow", size=48, weight="bold")
            self.metric_label_font = ctk.CTkFont(family="Barlow", size=18)
        except Exception as e:
            print(f"Erro ao carregar a fonte 'Barlow': {e}")
            self.barlow_font = ("Arial", 16)
            self.title_font = ("Arial", 24, "bold")
            self.subtitle_font = ("Arial", 20, "bold")
            self.small_font = ("Arial", 14)
            self.large_value_font = ("Arial", 48, "bold")
            self.metric_label_font = ("Arial", 18)
        
        # Configuração de layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Mantendo a sidebar como solicitado
        self.sidebar_frame = ctk.CTkFrame(
            self,
            fg_color="#5A189A",
            corner_radius=0,
            width=250
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)  # Para empurrar os itens para cima
        
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
            command=lambda: controller.mostrar_frame("login") if hasattr(controller, "mostrar_frame") else None
        )
        logout_button.pack(pady=5)

        # Inicialização dos componentes
        self.setup_main_content()
        
        # Dados de exemplo
        self.professores = ["João Silva", "Maria Oliveira", "Carlos Pereira", "Ana Santos", "Pedro Almeida"]
        self.tipos_aula = ["Musculação", "Yoga", "Pilates", "CrossFit", "Funcional", "Spinning", "Dança", "Natação"]
        
        # Preencher campos com dados
        self.preencher_combobox_professores()
        self.preencher_combobox_tipos_aula()
        self.atualizar_horarios_disponiveis()
        
    
    def criar_botao_menu(self, texto, indice, ativo=False):
        btn = ctk.CTkButton(
            self.sidebar_frame,
            text=texto,
            font=self.barlow_font,
            fg_color="#9D4EDD" if ativo else "transparent",
            text_color="white",
            hover_color="#7B2CBF",
            anchor="w",
            height=40,
            width=200,
            command=lambda: self.navegacao_menu(texto),
            corner_radius=8
        )
        btn.pack(pady=5, padx=20)
        return btn
        
    def setup_main_content(self):
        # Melhorado o background do frame principal para um branco mais suave
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_width=1,
            border_color="#E0E0E0"
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Título da página com estilo melhorado
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        page_title = ctk.CTkLabel(
            title_frame,
            text="Agendamento de Aulas",
            font=self.title_font,
            text_color="#5A189A"
        )
        page_title.pack(side="left")
        
        # Adicionado um botão de atualização na barra de título
        refresh_btn = ctk.CTkButton(
            title_frame,
            text="Atualizar",
            font=self.small_font,
            fg_color="#9D4EDD",
            hover_color="#7B2CBF",
            width=100,
            height=35,
            corner_radius=8,
            command=self.atualizar_horarios_disponiveis
        )
        refresh_btn.pack(side="right")
        
        # Conteúdo principal dividido em duas colunas
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Coluna esquerda - Formulário de agendamento com visual melhorado
        left_frame = ctk.CTkFrame(
            content_frame, 
            fg_color="#F8F9FA", 
            corner_radius=10,
            border_width=1,
            border_color="#E0E0E0"
        )
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=0)
        
        form_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título do formulário com ícone visual
        form_title_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_title_frame.pack(fill="x", pady=(0, 20))
        
        form_title = ctk.CTkLabel(
            form_title_frame,
            text="Dados da Aula",
            font=self.subtitle_font,
            text_color="#5A189A"
        )
        form_title.pack(side="left")
        
        # Indicador visual para campos obrigatórios
        required_label = ctk.CTkLabel(
            form_title_frame,
            text="* Campos obrigatórios",
            font=self.small_font,
            text_color="#888888"
        )
        required_label.pack(side="right")
        
        # Campos do formulário com estilo melhorado
        # 1. Seleção de professor
        prof_label = ctk.CTkLabel(form_frame, text="Professor: *", font=self.barlow_font, text_color="#333333")
        prof_label.pack(anchor="w", pady=(0, 5))
        
        self.professor_combobox = ctk.CTkComboBox(
            form_frame,
            width=300,
            font=self.barlow_font,
            dropdown_font=self.barlow_font,
            button_color="#9D4EDD",
            border_color="#9D4EDD",
            button_hover_color="#7B2CBF",
            dropdown_hover_color="#7B2CBF",
            fg_color="white"
        )
        self.professor_combobox.pack(anchor="w", pady=(0, 15))
        self.professor_combobox.configure(command=self.atualizar_horarios_disponiveis)
        
        # 2. Tipo de aula
        tipo_label = ctk.CTkLabel(form_frame, text="Tipo de Aula: *", font=self.barlow_font, text_color="#333333")
        tipo_label.pack(anchor="w", pady=(0, 5))
        
        self.tipo_aula_combobox = ctk.CTkComboBox(
            form_frame,
            width=300,
            font=self.barlow_font,
            dropdown_font=self.barlow_font,
            button_color="#9D4EDD",
            border_color="#9D4EDD",
            button_hover_color="#7B2CBF",
            dropdown_hover_color="#7B2CBF",
            fg_color="white"
        )
        self.tipo_aula_combobox.pack(anchor="w", pady=(0, 15))
        
        # 3. Data com calendário melhorado
        data_label = ctk.CTkLabel(form_frame, text="Data: *", font=self.barlow_font, text_color="#333333")
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
            weekendbackground="#F0F0F0",
            bordercolor="#E0E0E0",
            headersbackground="#9D4EDD",
            headersforeground="white"
        )
        self.cal.pack(pady=5)
        self.cal.bind("<<CalendarSelected>>", lambda e: self.atualizar_horarios_disponiveis())
        
        # 4. Horário com estilo melhorado
        horario_label = ctk.CTkLabel(form_frame, text="Horário Disponível: *", font=self.barlow_font, text_color="#333333")
        horario_label.pack(anchor="w", pady=(0, 5))
        
        self.horario_combobox = ctk.CTkComboBox(
            form_frame,
            width=300,
            font=self.barlow_font,
            dropdown_font=self.barlow_font,
            button_color="#9D4EDD",
            border_color="#9D4EDD",
            button_hover_color="#7B2CBF",
            dropdown_hover_color="#7B2CBF",
            fg_color="white"
        )
        self.horario_combobox.pack(anchor="w", pady=(0, 15))
        
        # 5. Aluno com estilo melhorado
        aluno_label = ctk.CTkLabel(form_frame, text="Aluno: *", font=self.barlow_font, text_color="#333333")
        aluno_label.pack(anchor="w", pady=(0, 5))
        
        self.aluno_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            font=self.barlow_font,
            border_color="#9D4EDD",
            fg_color="white",
            placeholder_text="Nome do aluno"
        )
        self.aluno_entry.pack(anchor="w", pady=(0, 15))
        
        # 6. Observações com estilo melhorado
        obs_label = ctk.CTkLabel(form_frame, text="Observações:", font=self.barlow_font, text_color="#333333")
        obs_label.pack(anchor="w", pady=(0, 5))
        
        self.obs_textbox = ctk.CTkTextbox(
            form_frame,
            width=300,
            height=100,
            font=self.barlow_font,
            border_color="#9D4EDD",
            fg_color="white",
            scrollbar_button_color="#9D4EDD"
        )
        self.obs_textbox.pack(anchor="w", pady=(0, 20))
        
        # Botões com estilo melhorado
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        self.cancelar_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            font=self.barlow_font,
            fg_color="#E0E0E0",
            text_color="#333333",
            hover_color="#CCCCCC",
            width=140,
            height=40,
            corner_radius=8
        )
        self.cancelar_btn.pack(side="left", padx=(0, 10))
        
        self.agendar_btn = ctk.CTkButton(
            buttons_frame,
            text="Agendar Aula",
            font=self.barlow_font,
            fg_color="#9D4EDD",
            hover_color="#7B2CBF",
            width=140,
            height=40,
            corner_radius=8,
            command=self.agendar_aula
        )
        self.agendar_btn.pack(side="left")
        
        # Coluna direita - Agenda do professor com visual melhorado
        right_frame = ctk.CTkFrame(
            content_frame, 
            fg_color="#F8F9FA", 
            corner_radius=10,
            border_width=1,
            border_color="#E0E0E0"
        )
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=0)
        
        agenda_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        agenda_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título da agenda com ícone visual
        agenda_title_frame = ctk.CTkFrame(agenda_frame, fg_color="transparent")
        agenda_title_frame.pack(fill="x", pady=(0, 20))
        
        agenda_title = ctk.CTkLabel(
            agenda_title_frame,
            text="Agenda do Professor",
            font=self.subtitle_font,
            text_color="#5A189A"
        )
        agenda_title.pack(side="left")
        
        # Filtro de professor para a agenda
        self.filtro_professor_label = ctk.CTkLabel(
            agenda_title_frame,
            text="Filtrar por professor:",
            font=self.small_font,
            text_color="#555555"
        )
        self.filtro_professor_label.pack(side="right", padx=(0, 10))
        
        self.filtro_professor_combobox = ctk.CTkComboBox(
            agenda_title_frame,
            width=150,
            font=self.small_font,
            dropdown_font=self.small_font,
            button_color="#9D4EDD",
            border_color="#9D4EDD",
            button_hover_color="#7B2CBF",
            dropdown_hover_color="#7B2CBF",
            fg_color="white",
            command=self.filtrar_agenda_por_professor
        )
        self.filtro_professor_combobox.pack(side="right")
        
        # Tabela de agendamentos com visual melhorado
        self.tree_frame = ctk.CTkFrame(agenda_frame, fg_color="transparent")
        self.tree_frame.pack(fill="both", expand=True)
        
        # Cabeçalho da tabela com estilo melhorado
        header_frame = ctk.CTkFrame(self.tree_frame, fg_color="#9D4EDD", corner_radius=8)
        header_frame.pack(fill="x", pady=(0, 1))
        
        # Adicionar professor à tabela
        headers = ["Data", "Horário", "Professor", "Tipo de Aula", "Aluno"]
        
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=self.barlow_font,
                text_color="white"
            )
            header_label.pack(side="left", expand=True, fill="both", padx=5, pady=8)
        
        # Conteúdo da tabela com estilo melhorado
        self.table_content_frame = ctk.CTkScrollableFrame(
            self.tree_frame,
            fg_color="transparent",
            scrollbar_button_color="#9D4EDD",
            height=300  # Altura fixa para melhor visualização
        )
        self.table_content_frame.pack(fill="both", expand=True)
        
        # Preencher com dados de exemplo
        self.atualizar_tabela_agendamentos()
    
    def preencher_combobox_professores(self):
        self.professor_combobox.configure(values=self.professores)
        self.professor_combobox.set(self.professores[0])
        
        # Também preencher o combobox de filtro
        valores_filtro = ["Todos"] + self.professores
        self.filtro_professor_combobox.configure(values=valores_filtro)
        self.filtro_professor_combobox.set("Todos")
    
    def preencher_combobox_tipos_aula(self):
        self.tipo_aula_combobox.configure(values=self.tipos_aula)
        self.tipo_aula_combobox.set(self.tipos_aula[0])
    
    def navegacao_menu(self, texto):
        if texto == "Membros" and self.controller:
            self.controller.mostrar_frame("members")
        elif texto == "Dashboard" and self.controller:
            self.controller.mostrar_frame("dashboard")
        elif texto == "Agenda" and self.controller:
            self.controller.mostrar_frame("agendar")
        elif texto == "Configurações" and self.controller:
            self.controller.mostrar_frame("settings")
    
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
        
        # Atualizar a tabela também
        self.atualizar_tabela_agendamentos()
    
    def filtrar_agenda_por_professor(self, *args):
        # Atualizar a tabela com o filtro selecionado
        self.atualizar_tabela_agendamentos()
    
    def agendar_aula(self):
        professor = self.professor_combobox.get()
        tipo_aula = self.tipo_aula_combobox.get()
        data = self.cal.get_date()
        horario = self.horario_combobox.get()
        aluno = self.aluno_entry.get()
        observacoes = self.obs_textbox.get("1.0", "end-1c")
        
        if horario == "Sem horários disponíveis":
            self.mostrar_mensagem("Aviso", "Não há horários disponíveis para este professor nesta data.")
            return
        
        if not aluno:
            self.mostrar_mensagem("Erro", "Por favor, preencha o nome do aluno.")
            return
        
        # Simular o agendamento
        # Em um sistema real, salvaria no banco de dados
        
        # Mostrar confirmação com estilo melhorado
        self.mostrar_mensagem("Sucesso", "Aula agendada com sucesso!")
        
        # Limpar campos
        self.aluno_entry.delete(0, "end")
        self.obs_textbox.delete("1.0", "end")
        
        # Atualizar a tabela
        self.atualizar_tabela_agendamentos(novo_agendamento={
            "data": data,
            "horario": horario,
            "professor": professor,
            "tipo_aula": tipo_aula,
            "aluno": aluno
        })
    
    def mostrar_mensagem(self, titulo, mensagem):
        # Janela de mensagem com estilo melhorado
        msg_window = ctk.CTkToplevel(self)
        msg_window.title(titulo)
        msg_window.geometry("350x200")
        msg_window.attributes("-topmost", True)
        
        # Ícone de acordo com o tipo de mensagem
        icon_frame = ctk.CTkFrame(msg_window, fg_color="transparent")
        icon_frame.pack(pady=(20, 0))
        
        if titulo == "Erro":
            icon_color = "#F44336"
        elif titulo == "Aviso":
            icon_color = "#FFC107"
        else:
            icon_color = "#4CAF50"
        
        icon = ctk.CTkFrame(
            icon_frame,
            width=50,
            height=50,
            corner_radius=25,
            fg_color=icon_color
        )
        icon.pack()
        
        # Mensagem
        msg_label = ctk.CTkLabel(
            msg_window,
            text=mensagem,
            font=self.barlow_font
        )
        msg_label.pack(pady=20)
        
        # Botão
        ok_button = ctk.CTkButton(
            msg_window,
            text="OK",
            command=msg_window.destroy,
            fg_color="#9D4EDD",
            hover_color="#7B2CBF",
            width=120,
            height=35,
            corner_radius=8
        )
        ok_button.pack(pady=10)
    
    def atualizar_tabela_agendamentos(self, novo_agendamento=None):
        # Limpar tabela atual
        for widget in self.table_content_frame.winfo_children():
            widget.destroy()
        
        # Dados de exemplo (simulação) com professor incluído
        dados = [
            {"data": "13/03/2025", "horario": "08:00", "professor": "João Silva", "tipo_aula": "Musculação", "aluno": "Carlos Mendes"},
            {"data": "13/03/2025", "horario": "10:00", "professor": "Maria Oliveira", "tipo_aula": "Pilates", "aluno": "Ana Pereira"},
            {"data": "14/03/2025", "horario": "15:00", "professor": "Carlos Pereira", "tipo_aula": "Yoga", "aluno": "Luiza Silva"},
            {"data": "14/03/2025", "horario": "17:00", "professor": "Ana Santos", "tipo_aula": "Funcional", "aluno": "Marcelo Costa"},
            {"data": "15/03/2025", "horario": "09:00", "professor": "Pedro Almeida", "tipo_aula": "CrossFit", "aluno": "Juliana Santos"}
        ]
        
        # Adicionar novo agendamento, se houver
        if novo_agendamento:
            dados.append(novo_agendamento)
        
        # Aplicar filtro de professor
        filtro_professor = self.filtro_professor_combobox.get()
        if filtro_professor != "Todos":
            dados = [d for d in dados if d["professor"] == filtro_professor]
        
        # Ordenar por data e horário
        dados.sort(key=lambda x: (x["data"], x["horario"]))
        
        # Mostrar os dados na tabela com estilo melhorado
        for i, dado in enumerate(dados):
            row_color = "#F8F8F8" if i % 2 == 0 else "white"
            row_frame = ctk.CTkFrame(self.table_content_frame, fg_color=row_color, corner_radius=8, height=40)
            row_frame.pack(fill="x", pady=2, ipady=5)
            row_frame.pack_propagate(False)  # Manter altura fixa
            
            data_label = ctk.CTkLabel(
                row_frame,
                text=dado["data"],
                font=self.small_font,
                text_color="#333333"
            )
            data_label.pack(side="left", expand=True, fill="both", padx=5)
            
            horario_label = ctk.CTkLabel(
                row_frame,
                text=dado["horario"],
                font=self.small_font,
                text_color="#333333"
            )
            horario_label.pack(side="left", expand=True, fill="both", padx=5)
            
            professor_label = ctk.CTkLabel(
                row_frame,
                text=dado["professor"],
                font=self.small_font,
                text_color="#333333"
            )
            professor_label.pack(side="left", expand=True, fill="both", padx=5)
            
            tipo_label = ctk.CTkLabel(
                row_frame,
                text=dado["tipo_aula"],
                font=self.small_font,
                text_color="#333333"
            )
            tipo_label.pack(side="left", expand=True, fill="both", padx=5)
            
            aluno_label = ctk.CTkLabel(
                row_frame,
                text=dado["aluno"],
                font=self.small_font,
                text_color="#333333"
            )
            aluno_label.pack(side="left", expand=True, fill="both", padx=5)
            
            # Adicionar botões de ação
            action_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=30)
            action_frame.pack(side="right", padx=5)
            
            # Botão para editar (apenas visual)
            edit_btn = ctk.CTkButton(
                action_frame,
                text="✏️",
                width=25,
                height=25,
                fg_color="#E0E0E0",
                text_color="#333333",
                hover_color="#CCCCCC",
                corner_radius=4
            )
            edit_btn.pack(side="left", padx=2)