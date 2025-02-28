from datetime import datetime

class AdminController:
    def __init__(self, gerenciador_db):
        """
        Inicializa o AdminController com uma instância de GerenciadorBancoDados.
        
        Args:
            gerenciador_db (GerenciadorBancoDados): Instância do gerenciador de banco de dados.
        """
        self.db = gerenciador_db
    
    def adicionar_cliente(self, cliente_data):
        """
        Adiciona um novo cliente ao banco de dados.
        
        Args:
            cliente_data (dict): Dados do cliente a serem inseridos.
        
        Returns:
            bool: True se o cliente foi adicionado com sucesso, False caso contrário.
        """
        query = """
        INSERT INTO clientes 
        (nome, telefone, email, endereco, data_nascimento, data_inicio, plano)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            cliente_data['nome'],
            cliente_data['telefone'],
            cliente_data['email'],
            cliente_data['endereco'],
            cliente_data['data_nascimento'],
            cliente_data['data_inicio'],
            cliente_data['plano']
        )
        return self.db.executar_comando(query, valores)
    
    def obter_todos_clientes(self):
        """
        Obtém todos os clientes cadastrados no banco de dados.
        
        Returns:
            list: Lista de dicionários com os dados dos clientes.
        """
        query = "SELECT * FROM clientes"
        resultados = self.db.executar_consulta(query)
        
        if resultados:
            # Converte os resultados em uma lista de dicionários
            colunas = ['id', 'nome', 'telefone', 'email', 'endereco', 'data_nascimento', 'data_inicio', 'plano']
            clientes = [dict(zip(colunas, cliente)) for cliente in resultados]
            return clientes
        return []
    
    def buscar_cliente_por_nome(self, nome):
        """
        Busca clientes pelo nome (ou parte do nome).
        
        Args:
            nome (str): Nome ou parte do nome a ser buscado.
        
        Returns:
            list: Lista de dicionários com os dados dos clientes encontrados.
        """
        query = "SELECT * FROM clientes WHERE nome LIKE %s"
        resultados = self.db.executar_consulta(query, (f"%{nome}%",))
        
        if resultados:
            colunas = ['id', 'nome', 'telefone', 'email', 'endereco', 'data_nascimento', 'data_inicio', 'plano']
            clientes = [dict(zip(colunas, cliente)) for cliente in resultados]
            return clientes
        return []
    
    def atualizar_cliente(self, cliente_id, novos_dados):
        """
        Atualiza os dados de um cliente existente.
        
        Args:
            cliente_id (int): ID do cliente a ser atualizado.
            novos_dados (dict): Dados atualizados do cliente.
        
        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário.
        """
        query = """
        UPDATE clientes 
        SET nome = %s, telefone = %s, email = %s, endereco = %s, 
            data_nascimento = %s, data_inicio = %s, plano = %s
        WHERE id = %s
        """
        valores = (
            novos_dados['nome'],
            novos_dados['telefone'],
            novos_dados['email'],
            novos_dados['endereco'],
            novos_dados['data_nascimento'],
            novos_dados['data_inicio'],
            novos_dados['plano'],
            cliente_id
        )
        return self.db.executar_comando(query, valores)
    
    def excluir_cliente(self, cliente_id):
        """
        Exclui um cliente do banco de dados.
        
        Args:
            cliente_id (int): ID do cliente a ser excluído.
        
        Returns:
            bool: True se a exclusão foi bem-sucedida, False caso contrário.
        """
        query = "DELETE FROM clientes WHERE id = %s"
        return self.db.executar_comando(query, (cliente_id,))
    
    def formatar_data_para_sql(self, data_str):
        """
        Converte uma data no formato DD/MM/AAAA para o formato SQL (AAAA-MM-DD).
        
        Args:
            data_str (str): Data no formato DD/MM/AAAA.
        
        Returns:
            str: Data no formato SQL ou None se a data for inválida.
        """
        try:
            data_obj = datetime.strptime(data_str, "%d/%m/%Y")
            return data_obj.strftime("%Y-%m-%d")
        except ValueError:
            return None