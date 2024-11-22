from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_sqlalchemy import SQLAlchemy
import os
import json
import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'seu_segredo_aqui'  # Necessário para usar o flash

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///albuns_musicais.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    artista = db.Column(db.String(100), nullable=False)
    data_lancamento = db.Column(db.String(10), nullable=False)
    musicas = db.Column(db.JSON, nullable=False)  # Agora é um campo JSON

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        genero = request.form['genero']
        artista = request.form['artista']
        data_lancamento = request.form['data_lancamento']
        musicas = request.form.getlist('musicas')  # Usando 'getlist' para capturar múltiplas músicas como lista

        novo_album = Album(
            nome=nome,
            genero=genero,
            artista=artista,
            data_lancamento=data_lancamento,
            musicas=musicas  # Aqui estamos passando uma lista de músicas
        )
        db.session.add(novo_album)
        db.session.commit()
        flash("Álbum cadastrado com sucesso!", "success")
        return redirect(url_for('home'))

    return render_template('cadastro.html')

@app.route('/pesquisa', methods=['GET', 'POST'])
def pesquisa():
    albuns = []
    if request.method == 'POST':
        nome_pesquisa = request.form['nome']
        albuns = Album.query.filter(Album.nome.ilike(f'%{nome_pesquisa}%')).all()
    return render_template('pesquisa.html', albuns=albuns)

@app.route('/importacao', methods=['GET', 'POST'])
def importacao():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("Nenhum arquivo selecionado.", "danger")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("Nenhum arquivo selecionado.", "danger")
            return redirect(request.url)
        if file and file.filename.endswith('.json'):
            try:
                data = json.load(file)
                for item in data:
                    novo_album = Album(
                        nome=item['nome'],
                        genero=item['genero'],
                        artista=item['artista'],
                        data_lancamento=item['data_lancamento'],
                        musicas=item['musicas']  # Assumindo que 'musicas' seja uma lista
                    )
                    db.session.add(novo_album)
                db.session.commit()
                flash("Álbuns importados com sucesso!", "success")
            except Exception as e:
                flash(f"Erro ao importar dados: {e}", "danger")
            return redirect(url_for('home'))

    return render_template('importacao.html')

@app.route('/exportacao', methods=['GET', 'POST'])
def exportacao():
    if request.method == 'POST':
        nome_arquivo = request.form['nome_arquivo']
        albuns = Album.query.all()
        if not albuns:
            flash("Nenhum dado disponível para exportação.", "warning")
            return redirect(url_for('home'))
        data = [{
            'Nome': album.nome,
            'Gênero': album.genero,
            'Artista': album.artista,
            'Data de Lançamento': album.data_lancamento,
            'Músicas': album.musicas  # 'musicas' agora é uma lista, será exportado diretamente
        } for album in albuns]
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Álbuns Musicais')
        output.seek(0)
        nome_arquivo_com_extensao = f"{nome_arquivo}.xlsx"
        return send_file(output, as_attachment=True, download_name=nome_arquivo_com_extensao, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    return render_template('exportacao.html')

@app.route('/download_files')
def download_files():
    files = [
        {"name": "Exemplo de Álbum", "filename": "exemplo_album.zip"},
        {"name": "Lista de Álbuns", "filename": "albuns_musicais.json"}
    ]
    return render_template('download_files.html', files=files)

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True, threaded=True)