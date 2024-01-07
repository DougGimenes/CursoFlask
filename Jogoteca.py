from flask import Flask, render_template, request, redirect, session, flash, url_for
import Titulos
import Usuarios

app = Flask(__name__)
app.secret_key = 'dimmadomme'

jogos = [Titulos.titulo('Dungeons & Dragons 5e', 'RPG, Medieval Fantastico', '300'), Titulos.titulo('Tormenta 20', 'RPG, Medieval Fantastico', '400'), Titulos.titulo('Pathfinder 2e', 'RPG, Medieval Fantastico', '250')]
usu1 = Usuarios.usuario('doug', 'Douglas Gimenes', 'segredo')
usu2 = Usuarios.usuario('carol', 'Carolina Gimenes', 'peridoto')
usuarios = {usu1.id : usu1, usu2.id : usu2}

@app.route('/')
def index():
    return render_template('lista.html', cabecalho = 'Biblioteca', titulos = jogos)
    
@app.route('/incluir')
def incluir():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('incluir')))
    return render_template('incluir.html', cabecalho='Incluir titulos')
    
@app.route('/criar', methods=['POST',])
def criar():
    jogos.append(Titulos.titulo(request.form['nome'], request.form['genero'], request.form['numPaginas']))
    return redirect(url_for('index'))
    
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima or '/')
    
@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(request.form['usuario'] + ' logou com sucesso!')
            proxima_pagina =  request.form['proxima']
            return redirect(proxima_pagina)
        else :
            flash('Não logado, tente de novo!')
            return redirect (url_for('login'))
        
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

app.run(debug=True)