from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import json
import pandas as pd
from io import BytesIO

app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aplicativos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para o banco de dados
class Aplicativo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(20), nullable=False)
    artista = db.Column(db.String(20), nullable=False)
    data_lancamento = db.Date(db.String(10), nullable=False)
    musicas = db.Column(db.String(1000), nullable=False) 

# Criação do banco de dados
with app.app_context():
    db.create_all()

@app.route('cadastro.html')
def home():
    return render_template('index.html')

@app.route('cadastro.html', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Obter dados do formulário
        nome = request.form['nome']
        genero = request.form['genero']
        artista = request.form['artista']
        data_lancamento = request.form['data_lancamento']
        musicas = request.form['musicas']

        # Criar uma nova instância de Aplicativo
        novo_aplicativo = Aplicativo(
            nome = nome,
            genero = genero,
            artista = artista,
            data_lancamento = data_lancamento,
            musicas = musicas
        )

        # Adicionar e salvar no banco de dados
        db.session.add(novo_aplicativo)
        db.session.commit()

        # Redireciona para a tela principal após o cadastro
        return redirect(url_for('home'))

    return render_template('cadastro.html')

@app.route('/pesquisa', methods=['GET', 'POST'])
def pesquisa():
    aplicativos = []
    if request.method == 'POST':
        nome_pesquisa = request.form['nome']
        # Buscar no banco de dados pelo nome do aplicativo
        aplicativos = Aplicativo.query.filter(Aplicativo.nome.like(f'%{nome_pesquisa}%')).all()

    return render_template('pesquisa.html', aplicativos=aplicativos)

# Rota para Carga de Dados
@app.route('/carga', methods=['GET', 'POST'])
def carga():
    if request.method == 'POST':
        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            return "Nenhum arquivo selecionado.", 400

        file = request.files['file']
        if file.filename == '':
            return "Nenhum arquivo selecionado.", 400

        # Lê o arquivo JSON e carrega os dados no banco
        if file and file.filename.endswith('.json'):
            data = json.load(file)
            for item in data:
                novo_aplicativo = Aplicativo(
                    nome=item['nome'],
                    descricao=item['descricao'],
                    versao=item['versao'],
                    desenvolvedor=item['desenvolvedor'],
                    data_lancamento=item['data_lancamento']
                )
                db.session.add(novo_aplicativo)
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('carga.html')

@app.route('/exportacao', methods=['GET', 'POST'])
def exportacao():
    if request.method == 'POST':
        nome_arquivo = request.form['nome_arquivo']

        # Obter dados do banco de dados
        aplicativos = Aplicativo.query.all()
        data = [{
            'Nome': app.nome,
            'Descrição': app.descricao,
            'Versão': app.versao,
            'Desenvolvedor': app.desenvolvedor,
            'Data de Lançamento': app.data_lancamento
        } for app in aplicativos]

        # Checar se os dados estão corretos
        if not data:
            return "Nenhum dado disponível para exportação.", 500

        try:
            # Criar DataFrame e exportar para BytesIO
            df = pd.DataFrame(data)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Aplicativos')
            output.seek(0)  # Colocar o ponteiro no início

            # Definir o nome do arquivo de download
            nome_arquivo_com_extensao = f"{nome_arquivo}.xlsx"

            return send_file(
                output,
                as_attachment=True,
                download_name=nome_arquivo_com_extensao,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        except Exception as e:
            print(f"Erro durante a exportação: {e}")
            return "Erro ao exportar os dados.", 500

    return render_template('exportacao.html')

@app.route('/download/<path:filename>')
def download(filename):
    # Diretorio onde os arquivos de download estão localizados
    directory = os.path.join(app.root_path, 'static/files')
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/download_files')
def download_files():
    # Lista de arquivos disponíveis para download
    files = [
        {"name": "Exemplo do Site", "filename": "exemplo.zip"},
        {"name": "Bibliotecas instaladas", "filename": "biblioteca.txt"},
        {"name": "Exemplo de JSON", "filename": "dados_aplicativos.json"}
    ]
    return render_template('download_files.html', files=files)





if __name__ == '__main__':
    cert_path = 'cert.pem'
    key_path = 'key.pem'

    if os.path.exists(cert_path) and os.path.exists(key_path):
        app.run(host='0.0.0.0', port=443, ssl_context=(cert_path, key_path))
    else:
        print("Certificados SSL não encontrados. Execute com HTTP para testes.")
        app.run(host='0.0.0.0', port=5000)

