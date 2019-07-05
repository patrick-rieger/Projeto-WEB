from flask import render_template, flash, redirect, url_for, request, Session
from app import app, db, lm
from app.models.forms import LoginForm, RegisterForm
from app.models.tables import User, Permission, Role, Noticia
from flask_login import login_user, logout_user, login_required, current_user
from app.decorators import admin_required, permission_required
import requests
from bs4 import BeautifulSoup


@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@app.route("/lista")
@login_required
@admin_required
def lista():
    usuarios = User.query.all()
    return render_template("users.html", usuarios=usuarios)


@app.route("/login", methods=["GET", "POST"])
def login():
    form_login = LoginForm()
    if form_login.validate_on_submit():
        user = User.query.filter_by(username=form_login.username.data).first()
        if user and user.password == form_login.password.data:
            login_user(user)
            flash("Logado com sucesso")
            return redirect(url_for('index'))
        else:
            flash("Senha errada!")
    return render_template('login.html', form_login=form_login, navbar="")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html', navpage=True)


@app.route("/teste")
def teste():
    return render_template('teste.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Até a próxima')
    return redirect(url_for('index'))


@app.route("/origem", methods=["GET", "POST"])
def origem():
    return render_template('origem.html', navpage=True)


@app.route("/campeonatosFIBA")
def campeonatosFIBA():
    return render_template('campeonatosFIBA.html', navpage=True)


@app.route("/campeonatosNBA")
def campeonatosNBA():
    return render_template('campeonatosNBA.html', navpage=True)


@app.route("/regras")
def regras():
    return render_template('regras.html', navpage=True)


@app.route("/register", methods=["GET", "POST"])
def register():
    form_register = RegisterForm()
    if form_register.validate_on_submit():
        user = User.query.filter_by(username=form_register.username.data).first()
        if user:
            flash("Usuário já cadastrado")
        else:
            cadastrando = User(username=form_register.username.data, password=form_register.password.data,
                               name=form_register.name.data, email=form_register.email.data)
            db.session.add(cadastrando)
            db.session.commit()
            login_user(cadastrando)
            flash("Usuário cadastrado e logado com sucesso")
            mensagem = "Seja bem vindo(a), " + cadastrando.name + "!"
            flash(mensagem)
            return redirect(url_for('index'))
    return render_template('register.html',
                           form_register=form_register, navbar="")


@app.errorhandler(404)
def not_found(error):
    n = 404
    return render_template('erro.html', erro=error, n=n), 404


@app.errorhandler(403)
def not_found(error):
    n = 403
    return render_template('erro.html', erro=error, n=n), 403


@app.errorhandler(401)
def not_found(error):
    n = 401
    return render_template('erro.html', erro=error, n=n), 401


@app.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"


@app.route('/noticias')
def noticias():
    noticias = Noticia.query.all()
    return render_template("noticias.html", noticias=noticias)


@app.route('/montandoNoticias')
def montandoNoticias():
    page = requests.get("https://globoesporte.globo.com/basquete/")
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.find_all('div', class_='_ie')
    lista_links = []
    for x in range(0, 10):
        tag = links[x].find('a')
        if tag is not None:
            link = tag['href']
            if link not in lista_links:
                lista_links.append(link)
                page2 = requests.get(link)
                soup2 = BeautifulSoup(page2.content, 'html.parser')
                resumo = soup2.find('h2', class_='content-head__subtitle')
                if resumo:
                    resumo = resumo.get_text()
                titulo = soup2.find('title').get_text()
                TAGimage = soup2.find('div', class_='progressive-img')
                TAGimage = str(TAGimage)
                image = TAGimage.split('data-max-size-url="', 1)[1]
                image = image.split('" data-min-size=', 1)[0]
                noticia = Noticia(link=link, titulo=titulo, resumo=resumo, imagem=image)
                tem = Noticia.query.filter_by(titulo=titulo).first()
                if not tem:
                    db.session.add(noticia)
                    db.session.commit()
    return redirect(url_for('noticias'))


@app.route('/moderator')
@login_required
@permission_required(Permission.FOLLOW)
def for_moderators_only():
    return "For comment moderators!"


@login_required
@admin_required
@app.route("/excluir/<int:id>")
def excluir(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    flash('Usuário removido com sucesso')
    return redirect(url_for('lista'))
