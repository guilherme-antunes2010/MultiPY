import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS produto_grupo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        codigo_barras TEXT UNIQUE NOT NULL,
        preco REAL NOT NULL,
        descricao TEXT,
        categoria TEXT NOT NULL,
        produto_grupo_id INTEGER,
        ativo BOOLEAN DEFAULT 1,
        data_adicionado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (produto_grupo_id) REFERENCES produto_grupo(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL,
        email TEXT,
        telefone TEXT,
        endereco TEXT,
        data_nascimento DATE,
        data_adicionado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_total REAL NOT NULL,
        data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id),
        FOREIGN KEY (id_produto) REFERENCES produtos(id)
    )
''')

conn.commit()
conn.close()

print("Banco de dados atualizado com sucesso!")
