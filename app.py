from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
from funcoes import *
import webbrowser

app = Flask(__name__)
app.secret_key = 'chave_secreta_simples'
url = 'http://127.0.0.1:5000/'

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return view_func(*args, **kwargs)
    return wrapper

def campos_vazios(*campos):
    return any(not campo.strip() for campo in campos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == "admin" and senha == "1234":
            session['usuario'] = usuario
            return redirect(url_for('home'))
        return render_template('error.html')
    return render_template('login.html')

@app.route('/')
@login_required
def home():
    return render_template('home.html', usuario=session['usuario'])

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/system')
@login_required
def system():
    return render_template('system.html')

@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        codigo, nome, preco, descricao, categoria = map(request.form.get, ['codigo', 'name', 'price', 'description', 'category'])
        if campos_vazios(codigo, nome, preco, descricao, categoria) or float(preco) <= 0:
            return render_template('error2.html')
        add_produto(nome, codigo, float(preco), descricao, categoria)
    return render_template('add_produto.html')

@app.route('/edit_product', methods=['GET', 'POST'])
@login_required
def edit_product():
    if request.method == 'POST':
        codigo, nome, preco, descricao, categoria = map(request.form.get, ['codigo', 'name', 'price', 'description', 'category'])
        if campos_vazios(codigo, nome, preco, descricao, categoria) or float(preco) <= 0:
            return render_template('error2.html')
        edit_produto_por_codigo(codigo, nome, float(preco), descricao, categoria)
        return redirect(url_for('edit_product'))
    return render_template('edit_produtos.html')

@app.route('/del_product', methods=['GET', 'POST'])
@login_required
def del_product():
    if request.method == 'POST':
        codigo = request.form['codigo']
        if campos_vazios(codigo):
            return render_template('error2.html')
        delete_produto_por_codigo(codigo)
        return redirect(url_for('del_product'))
    return render_template('del_produto.html')

@app.route('/list_product')
@login_required
def list_product():
    return render_template('list_produtos.html', produtos=get_produtos())

@app.route('/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
    if request.method == 'POST':
        campos = [request.form.get(chave) for chave in ['name', 'cpf', 'email', 'phone', 'address', 'birth_date']]
        if campos_vazios(*campos):
            return render_template('error2.html')
        add_cliente(*campos)
        return redirect(url_for('add_client'))
    return render_template('add_cliente.html')

@app.route('/edit_client', methods=['GET', 'POST'])
@login_required
def edit_client():
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        campos = [request.form.get(chave) for chave in ['name', 'cpf', 'email', 'phone', 'address', 'birth_date']]
        if campos_vazios(*campos):
            return render_template('error2.html')
        edit_cliente(id_cliente, *campos)
        return redirect(url_for('edit_client'))
    return render_template('edit_cliente.html')

@app.route('/del_client', methods=['GET', 'POST'])
@login_required
def del_client():
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        if campos_vazios(id_cliente):
            return render_template('error2.html')
        delete_cliente(id_cliente)
        return redirect(url_for('del_client'))
    return render_template('del_cliente.html')

@app.route('/list_client')
@login_required
def list_client():
    return render_template('list_clientes.html', clientes=get_clientes())

@app.route('/add_sale', methods=['GET', 'POST'])
@login_required
def add_sale():
    if request.method == 'POST':
        produto_id, cliente_id, data_venda = map(request.form.get, ['produto_id', 'cliente_id', 'data_venda'])
        if campos_vazios(produto_id, cliente_id, data_venda):
            return render_template('error2.html')
        add_venda_por_codigo(cliente_id, produto_id, data_venda)
        return redirect(url_for('add_sale'))
    return render_template('add_venda.html')

@app.route('/search_sale', methods=['GET', 'POST'])
@login_required
def search_sale():
    if request.method == 'POST':
        cpf = request.form['cpf']
        codigo = request.form['codigo']
        if cpf and codigo:
            vendas = get_vendas_por_produto_e_cliente(codigo, cpf)
        elif cpf:
            vendas = get_vendas_por_cliente(cpf)
        elif codigo:
            vendas = get_vendas_por_produto(codigo)
        else:
            return render_template('error2.html')
        return render_template('list_vendas.html', vendas=vendas)
    return render_template('search.html')

@app.route('/list_sale')
@login_required
def list_sale():
    return render_template('list_vendas.html', vendas=get_vendas())

@app.route('/relatorios')
@login_required
def relatorios():
    return render_template('relatorios.html', resumo=gerar_resumo())

@app.route('/sobre')
@login_required
def sobre():
    return render_template('sobre.html')

if __name__ == '__main__':
    webbrowser.open(url)
    app.run(debug=True, use_reloader=False)
