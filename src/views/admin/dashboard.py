import customtkinter as ctk
from tkinter import StringVar
import datetime

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F0F0F0", corner_radius=0)
        
        self.controller = controller
        
        # Configuração da fonte
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
        
        # Layout principal: sidebar e área de conteúdo
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
        self.criar_botao_menu("Dashboard", 0, True)
        self.criar_botao_menu("Membros", 1)
        self.criar_botao_menu("Planos", 2)
        self.criar_botao_menu("Pagamentos", 3)
        self.criar_botao_menu("Agenda", 4)
        self.criar_botao_menu("Funcionários", 5)
        self.criar_botao_menu("Relatórios", 6)
        self.criar_botao_menu("Configurações", 7)
        
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
        
        # Área de conteúdo principal
        self.content_frame = ctk.CTkFrame(
            self,
            fg_color="#F0F0F0",
            corner_radius=0
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=1)
        
        # Cabeçalho da área de conteúdo
        header_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 30))
        
        # Data atual
        current_date = datetime.datetime.now().strftime("%d/%m/%Y")
        date_label = ctk.CTkLabel(
            header_frame,
            text=f"Hoje: {current_date}",
            font=self.small_font,
            text_color="black"
        )
        date_label.pack(side="left")
        
        # Título do dashboard
        dashboard_title = ctk.CTkLabel(
            header_frame,
            text="Dashboard",
            font=self.title_font,
            text_color="black"
        )
        dashboard_title.pack(side="right")
        
        # Redesign: Cards grandes e vistosos para as duas métricas principais
        # Container para os cards
        metrics_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        metrics_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
        metrics_frame.grid_rowconfigure(0, weight=1)
        
        # Card de Total de Membros - Esquerda
        self.create_large_metric_card(
            metrics_frame, 
            0, 0, 
            "Total de Membros", 
            "342", 
            "Membros ativos na academia", 
            "#5A189A",
            "user"
        )
        
        # Card de Receita Mensal - Direita
        self.create_large_metric_card(
            metrics_frame, 
            0, 1, 
            "Receita Mensal", 
            "R$ 24.850,00", 
            "Faturamento do mês atual", 
            "#7B2CBF",
            "money"
        )
        
        # Container para gráfico de evolução
        chart_container = ctk.CTkFrame(
            self.content_frame,
            fg_color="white",
            corner_radius=15
        )
        chart_container.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=20, pady=(0, 20))
        
        chart_title = ctk.CTkLabel(
            chart_container,
            text="Evolução Anual",
            font=self.subtitle_font,
            text_color="black"
        )
        chart_title.pack(anchor="w", padx=20, pady=(20, 10))
        
        chart_subtitle = ctk.CTkLabel(
            chart_container,
            text="Comparativo de membros e receita nos últimos 12 meses",
            font=self.small_font,
            text_color="gray"
        )
        chart_subtitle.pack(anchor="w", padx=20, pady=(0, 20))
        
        # Simples visualização de tendência
        trend_frame = ctk.CTkFrame(
            chart_container,
            fg_color="transparent",
            height=250
        )
        trend_frame.pack(fill="x", padx=20, pady=10)
        trend_frame.pack_propagate(False)
        
        # Criar uma linha de tendência simulada
        months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        line_canvas = ctk.CTkCanvas(
            trend_frame,
            bg="#FFFFFF",
            highlightthickness=0
        )
        line_canvas.pack(fill="both", expand=True)
        
        # Desenhar linhas de referência horizontais
        for i in range(5):
            y = 200 - i * 40
            line_canvas.create_line(50, y, 700, y, fill="#E0E0E0", dash=(4, 4))
            label = f"{i * 25}%" if i > 0 else "0%"
            line_canvas.create_text(30, y, text=label, fill="#808080", font=("Arial", 9))
        
        # Desenhar rótulos dos meses
        for i, month in enumerate(months):
            x = 50 + i * (650 / 11)
            line_canvas.create_text(x, 220, text=month, fill="#808080", font=("Arial", 9))
        
        # Dados da linha de membros (dados simulados com tendência de crescimento)
        member_data = [120, 145, 165, 160, 180, 210, 240, 255, 270, 290, 310, 342]
        
        # Normalização para o espaço do canvas
        max_value = max(member_data)
        normalized_data = [(val / max_value) * 160 for val in member_data]
        
        # Desenhar linha de membros
        for i in range(len(normalized_data) - 1):
            x1 = 50 + i * (650 / 11)
            y1 = 200 - normalized_data[i]
            x2 = 50 + (i + 1) * (650 / 11)
            y2 = 200 - normalized_data[i + 1]
            line_canvas.create_line(x1, y1, x2, y2, fill="#5A189A", width=3, smooth=True)
            line_canvas.create_oval(x1-4, y1-4, x1+4, y1+4, fill="#5A189A", outline="")
        
        # Último ponto
        x, y = 50 + 11 * (650 / 11), 200 - normalized_data[-1]
        line_canvas.create_oval(x-4, y-4, x+4, y+4, fill="#5A189A", outline="")
        
        # Legenda
        legend_frame = ctk.CTkFrame(
            chart_container,
            fg_color="transparent"
        )
        legend_frame.pack(anchor="w", padx=20, pady=(0, 20))
        
        legend_indicator = ctk.CTkFrame(
            legend_frame,
            width=15,
            height=15,
            corner_radius=7,
            fg_color="#5A189A"
        )
        legend_indicator.pack(side="left", padx=(0, 5))
        
        legend_text = ctk.CTkLabel(
            legend_frame,
            text="Crescimento de Membros",
            font=self.small_font,
            text_color="black"
        )
        legend_text.pack(side="left")
        
        # Rodapé com mensagem de boas-vindas
        footer_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        footer_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        
        footer_text = ctk.CTkLabel(
            footer_frame,
            text="Bem-vindo ao Sistema de Gestão de Academia",
            font=self.small_font,
            text_color="gray"
        )
        footer_text.pack()
    
    def criar_botao_menu(self, texto, indice, ativo=False):
        """Cria um botão na sidebar com estilização adequada"""
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
            command=lambda t=texto: print(f"Menu {t} clicado")
        )
        btn.pack(pady=5, padx=15)
        return btn
    
    def create_large_metric_card(self, parent, row, column, title, value, subtitle, color, icon_type=None):
        """Cria um card grande para métricas principais"""
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=15,
            height=200
        )
        card.grid(row=row, column=column, padx=15, pady=15, sticky="nsew")
        card.grid_propagate(False)
        
        # Layout interno do card
        card.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=self.subtitle_font,
            text_color="black"
        )
        title_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            card,
            text=subtitle,
            font=self.small_font,
            text_color="gray"
        )
        subtitle_label.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 15))
        
        # Valor com tamanho grande
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=self.large_value_font,
            text_color=color
        )
        value_label.grid(row=2, column=0, sticky="w", padx=20)
        
        # Ícone simulado (círculo com um símbolo ou inicial)
        if icon_type:
            # Usar uma cor mais clara em vez de transparência
            icon_color = "#E8DAEF" if color == "#5A189A" else "#D6C5E8"
            
            icon_frame = ctk.CTkFrame(
                card,
                width=60,
                height=60,
                corner_radius=30,
                fg_color=icon_color
            )
            icon_frame.place(relx=0.9, rely=0.5, anchor="e")
            
            # Texto do ícone baseado no tipo
            icon_text = "U" if icon_type == "user" else "$"
            
            icon_label = ctk.CTkLabel(
                icon_frame,
                text=icon_text,
                font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
                text_color=color
            )
            icon_label.place(relx=0.5, rely=0.5, anchor="center")


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Sistema de Gestão de Academia")
    app.geometry("1200x700")
    
    class MockController:
        def mostrar_frame(self, frame_name):
            print(f"Mudando para tela: {frame_name}")
    
    dashboard = DashboardFrame(app, MockController())
    dashboard.pack(fill="both", expand=True)
    
    app.mainloop()