from flask import Flask, render_template, request, jsonify, session
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    salt = bcrypt.gensalt()
    usuario = request.args.get('usuario')
    session['username'] = usuario
    senha = request.args.get('senha')
    hashed_password = bcrypt.hashpw(senha.encode('utf-8'), salt)
    
    conexao = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "paguemais"
    )

    consulta = "SELECT usuario, senha FROM funcionario WHERE usuario = %s"
    valores = (usuario, )
    cursor = conexao.cursor()
    cursor.execute(consulta, valores)
    resultado = cursor.fetchall()
    dados = []

    for linha in resultado:
        dicionario = {"usuario": linha[0],
                      "senha": linha[1]}
        dados.append(dicionario)
        
    cursor.close()
    conexao.close()
    if len(dados) == 0:
        mensagem = 'Usuário não encontrado'
        return render_template('login.html', mensagem=mensagem)
    else:
        usuario_armazenado = dados[0]['usuario']
        senha_armazenada = dados[0]['senha'].encode('utf-8')
        if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada) and usuario_armazenado == usuario:
            print("Senha correta!") 
            return render_template('home.html', usuario=usuario)
        else:
            mensagem = 'Usuário ou senha incorretos'
            return render_template('login.html', mensagem=mensagem)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    nome = session.get('username')
    return render_template('home.html', usuario=nome)

@app.route('/cancelarcadastrousuario', methods=['GET', 'POST'])
def cancelarcadastrousuario():
    nome = session.get('username')
    return render_template('home.html', usuario=nome)

@app.route('/pagecaduser', methods=['GET', 'POST'])
def pagecaduser():
    return render_template('cadastrarusuario.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('Login.html')

@app.route('/trocasenha', methods=['GET', 'POST'])
def trocasenha():
    return render_template('trocasenha.html')

@app.route('/changepassword', methods=['GET', 'POST'])
def atualizasenha():
    salt = bcrypt.gensalt()
    usuario = request.args.get('usuario')
    senha = request.args.get('senha')
    novasenha = request.args.get('novasenha')
    hashed_password = bcrypt.hashpw(novasenha.encode('utf-8'), salt)

    conexao = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "paguemais"
    )

    consulta = "SELECT senha FROM funcionario WHERE usuario = %s"

    valores = (usuario, )
    cursor = conexao.cursor()
    cursor.execute(consulta, valores)
    resultado = cursor.fetchall()

    dados = []

    for linha in resultado:
        dicionario = {"senha": linha[0]}
        dados.append(dicionario)
    
    cursor.close()

    conexao.close()

    senha_armazenada = dados[0]['senha'].encode('utf-8')
    if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada):

        conexao = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "paguemais"
        )

        mycursor = conexao.cursor()

        sql = "UPDATE funcionario SET senha = %s where usuario = %s"
        valores = (hashed_password, usuario)
        mycursor.execute(sql, valores)
        conexao.commit()

        nome = session.get('username')
        return render_template('home.html', usuario=nome)
    else:
        mensagem = 'Senha atual incorreta'
        return render_template('trocasenha.html', mensagem=mensagem)    

@app.route('/cancelatrocasenha', methods=['GET', 'POST'])
def cancelatrocasenha():
    nome = session.get('username')
    return render_template('home.html', usuario=nome)

@app.route('/cadastrarusuario', methods=['GET', 'POST'])
def cadastrarusuario():
    if request.method == 'POST':
        salt = bcrypt.gensalt()
        usuario = request.form['usuario']
        senha = request.form['senha']
        hashed_password = bcrypt.hashpw(senha.encode('utf-8'), salt)
     
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="paguemais"
        )
        cursor = conexao.cursor()
    
        sql = "INSERT INTO funcionario (usuario, senha) VALUES (%s, %s)"
        
        valores = (usuario, hashed_password)
        
        cursor.execute(sql, valores)
        
        conexao.commit()
        conexao.close()
        return render_template('home.html', usuario='master')
    else:
        return render_template('home.html', usuario='master')

@app.route('/consultausuarios')
def consultausuarios():
    conexao = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "paguemais"
    )

    consulta = "SELECT * FROM funcionario where usuario <> 'master'"

    cursor = conexao.cursor()
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    
    cursor.close()

    conexao.close()
    return render_template('consultausuarios.html', dados=resultado)

@app.route('/consultaprodutos')
def consultaprodutos():
    conexao = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "paguemais"
    )

    consulta = "SELECT * FROM produtos"

    cursor = conexao.cursor()
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    
    cursor.close()

    conexao.close()
    return render_template('consultaprodutos.html', dados=resultado)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
