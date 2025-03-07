from datetime import datetime

class AdminController:
    def __init__(self, gerenciador_db):
        self.db = gerenciador_db

    def adicionar_cliente(self, cliente_data):
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
        query = "SELECT * FROM clientes"
        resultados = self.db.executar_consulta(query)
        return self._parse_clientes(resultados)

    def buscar_cliente(self, termo):
        query = """
        SELECT * FROM clientes 
        WHERE nome LIKE %s OR telefone LIKE %s OR email LIKE %s
        """
        termo = f"%{termo}%"
        resultados = self.db.executar_consulta(query, (termo, termo, termo))
        return self._parse_clientes(resultados)

    def buscar_cliente_por_id(self, cliente_id):
        query = "SELECT * FROM clientes WHERE id = %s"
        resultados = self.db.executar_consulta(query, (cliente_id,))
        return self._parse_clientes(resultados)[0] if resultados else None

    def atualizar_cliente(self, cliente_id, novos_dados):
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
        query = "DELETE FROM clientes WHERE id = %s"
        return self.db.executar_comando(query, (cliente_id,))

    def formatar_data_para_sql(self, data_str):
        try:
            return datetime.strptime(data_str, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            return None

    def _parse_clientes(self, resultados):
        if resultados:
            colunas = ['id', 'nome', 'telefone', 'email', 'endereco', 
                      'data_nascimento', 'data_inicio', 'plano']
            return [dict(zip(colunas, cliente)) for cliente in resultados]
        return []