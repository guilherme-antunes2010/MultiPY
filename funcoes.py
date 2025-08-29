import sqlite3
from collections import defaultdict

def add_produto(nome, codigo_barras, preco, descricao, categoria, grupo_id=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Inserir o produto individual na tabela (sem campo quantidade)
    cursor.execute('''
        INSERT INTO produtos (nome, codigo_barras, preco, descricao, categoria, produto_grupo_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, codigo_barras, preco, descricao, categoria, grupo_id))

    conn.commit()
    conn.close()

def edit_produto_por_codigo(codigo_barras, nome, preco, descricao, categoria):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE produtos
        SET nome = ?, preco = ?, descricao = ?, categoria = ?
        WHERE codigo_barras = ?
    ''', (nome, preco, descricao, categoria, codigo_barras))
    
    conn.commit()
    conn.close()


def delete_produto_por_codigo(codigo_barras):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM produtos
        WHERE codigo_barras = ?
    ''', (codigo_barras,))
    
    conn.commit()
    conn.close()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Excluir o produto da tabela
    cursor.execute('''
        DELETE FROM produtos
        WHERE id = ?
    ''', (id,))

    conn.commit()
    conn.close()

def get_produtos():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Selecionar todos os produtos da tabela
    cursor.execute('SELECT * FROM produtos WHERE ativo = 1')
    produtos = cursor.fetchall()

    conn.close()
    return produtos

def add_cliente(nome, cpf, email, telefone, endereco, data_nascimento=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO clientes (nome, cpf, email, telefone, endereco, data_nascimento)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, cpf, email, telefone, endereco, data_nascimento))

    conn.commit()
    conn.close()

def edit_cliente(id, nome, cpf, email, telefone, endereco, data_nascimento=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE clientes
        SET nome = ?, cpf = ?, email = ?, telefone = ?, endereco = ?, data_nascimento = ?
        WHERE id = ?
    ''', (nome, cpf, email, telefone, endereco, data_nascimento, id))

    conn.commit()
    conn.close()

def delete_cliente(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM clientes
        WHERE id = ?
    ''', (id,))

    conn.commit()
    conn.close()

def get_clientes():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()

    conn.close()
    return clientes

def add_venda_por_codigo(cliente_id, codigo_barras, data_venda=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Buscar o produto pelo código de barras
    cursor.execute('SELECT id, preco FROM produtos WHERE codigo_barras = ?', (codigo_barras,))
    resultado = cursor.fetchone()

    if not resultado:
        conn.close()
        raise ValueError("Produto com esse código de barras não encontrado.")

    produto_id, preco = resultado
    preco_total = float(preco)

    # Buscar o cliente pelo CPF
    cursor.execute('SELECT id FROM clientes WHERE cpf = ?', (cliente_id,))
    cliente_resultado = cursor.fetchone()

    if not cliente_resultado:
        conn.close()
        raise ValueError("Cliente com esse CPF não encontrado.")

    cliente_id_extraido = cliente_resultado[0]

    # Inserir a venda
    cursor.execute('''
        INSERT INTO vendas (id_cliente, id_produto, quantidade, data_venda, preco_total)
        VALUES (?, ?, ?, ?, ?)
    ''', (cliente_id_extraido, produto_id, 1, data_venda, preco_total))

    conn.commit()

    # Remover o produto vendido do estoque
    cursor.execute('UPDATE produtos SET ativo = 0 WHERE id = ?', (produto_id,))
    conn.commit()
    conn.close()


def get_vendas():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT v.id,
               COALESCE(c.nome, 'Cliente excluído') AS cliente_nome,
               COALESCE(p.nome, 'Produto excluído') AS produto_nome,
               v.quantidade, v.data_venda, v.preco_total
        FROM vendas v
        LEFT JOIN clientes c ON v.id_cliente = c.id
        LEFT JOIN produtos p ON v.id_produto = p.id
    ''')
    vendas = cursor.fetchall()
    conn.close()
    return vendas


def get_vendas_por_cliente(cpf):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM clientes WHERE cpf = ?', (cpf,))
    resultado = cursor.fetchone()

    if resultado is None:
        conn.close()
        return []  # Nenhum cliente com esse CPF

    cliente_id = resultado[0]  # extrai o ID do cliente da tupla

    cursor.execute('''
        SELECT v.id,
               COALESCE(c.nome, 'Cliente excluído') AS cliente_nome,
               COALESCE(p.nome, 'Produto excluído') AS produto_nome,
               v.quantidade, v.data_venda, v.preco_total
        FROM vendas v
        LEFT JOIN clientes c ON v.id_cliente = c.id
        LEFT JOIN produtos p ON v.id_produto = p.id
        WHERE v.id_cliente = ?
    ''', (cliente_id,))  # usa valor simples, não tupla

    vendas = cursor.fetchall()
    conn.close()
    return vendas

def get_vendas_por_produto(codigo_barras):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    #buscar produto pelo codigo de barras
    cursor.execute('SELECT id FROM produtos WHERE codigo_barras = ?', (codigo_barras,))
    resultado = cursor.fetchone()

    if resultado is None:
        conn.close()
        return []  # Nenhum produto com esse codigo de barras

    produto_id = resultado[0]  # extrai o ID do produto da tupla

    cursor.execute('''
        SELECT v.id,
               COALESCE(c.nome, 'Cliente excluído') AS cliente_nome,
               COALESCE(p.nome, 'Produto excluído') AS produto_nome,
               v.quantidade, v.data_venda, v.preco_total
        FROM vendas v
        LEFT JOIN clientes c ON v.id_cliente = c.id
        LEFT JOIN produtos p ON v.id_produto = p.id
        WHERE v.id_produto = ?
    ''', (produto_id,))  # usa valor simples, não tupla

    vendas = cursor.fetchall()
    print(vendas)
    conn.close()
    return vendas

def get_vendas_por_produto_e_cliente(codigo_barras, cpf):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    #buscar produto pelo codigo de barras
    cursor.execute('SELECT id FROM produtos WHERE codigo_barras = ?', (codigo_barras,))
    resultado = cursor.fetchone()

    if resultado is None:
        conn.close()
        return []  # Nenhum produto com esse codigo de barras

    produto_id = resultado[0]  # extrai o ID do produto da tupla

    cursor.execute('SELECT id FROM clientes WHERE cpf = ?', (cpf,))
    resultado = cursor.fetchone()

    if resultado is None:
        conn.close()
        return []  # Nenhum cliente com esse CPF

    cliente_id = resultado[0]  # extrai o ID do cliente da tupla

    cursor.execute('''
        SELECT v.id,
               COALESCE(c.nome, 'Cliente excluído') AS cliente_nome,
               COALESCE(p.nome, 'Produto excluído') AS produto_nome,
               v.quantidade, v.data_venda, v.preco_total
        FROM vendas v
        LEFT JOIN clientes c ON v.id_cliente = c.id
        LEFT JOIN produtos p ON v.id_produto = p.id
        WHERE v.id_produto = ? AND v.id_cliente = ?
    ''', (produto_id, cliente_id))  # usa valor simples, não tupla

    vendas = cursor.fetchall()
    print(vendas)
    conn.close()
    return vendas
def gerar_resumo():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT SUM(preco_total) as total FROM vendas")
    total_vendas = cur.fetchone()['total'] or 0

    cur.execute("SELECT COUNT(*) as total FROM vendas")
    total_pedidos = cur.fetchone()['total']

    ticket_medio = total_vendas / total_pedidos if total_pedidos else 0

    cur.execute('''
        SELECT p.nome, SUM(v.quantidade) as total_vendido
        FROM vendas v
        JOIN produtos p ON v.id_produto = p.id
        GROUP BY v.id_produto
        ORDER BY total_vendido DESC
        LIMIT 1
    ''')
    produto = cur.fetchone()
    produto_mais_vendido = (produto['nome'], produto['total_vendido']) if produto else ("-", 0)

    cur.execute('''
        SELECT p.nome, SUM(v.quantidade) as total_vendido
        FROM vendas v
        JOIN produtos p ON v.id_produto = p.id
        GROUP BY v.id_produto
        ORDER BY total_vendido DESC
    ''')
    grafico_produtos = {row['nome']: row['total_vendido'] for row in cur.fetchall()}

    cur.execute('''
        SELECT c.nome, SUM(v.preco_total) as total_gasto
        FROM vendas v
        JOIN clientes c ON v.id_cliente = c.id
        GROUP BY v.id_cliente
        ORDER BY total_gasto DESC
        LIMIT 1
    ''')
    cliente = cur.fetchone()
    cliente_top = (cliente['nome'], cliente['total_gasto']) if cliente else ("-", 0)


    cur.execute('''
        SELECT c.nome, SUM(v.preco_total) as total
        FROM vendas v
        JOIN clientes c ON v.id_cliente = c.id
        GROUP BY v.id_cliente
        ORDER BY total DESC
    ''')
    grafico_clientes = {row['nome']: row['total'] for row in cur.fetchall()}

    conn.close()

    return {
        'total_vendas': total_vendas,
        'total_pedidos': total_pedidos,
        'ticket_medio': ticket_medio,
        'produto_mais_vendido': produto_mais_vendido,
        'cliente_top': cliente_top,
        'grafico_produtos': grafico_produtos,
        'grafico_clientes': grafico_clientes
    }
