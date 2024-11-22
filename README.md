
# **SOMZERA - Web Application de Álbuns Musicais**

![image](https://github.com/user-attachments/assets/385e35a4-781e-4bb3-9336-f6968276e0ce)

**SOMZERA** é uma aplicação web para cadastrar, pesquisar, importar e exportar álbuns musicais. Desenvolvido utilizando o **Flask**, um framework web em Python, o projeto oferece uma interface simples e intuitiva para gerenciar álbuns de música, seus artistas, gêneros, datas de lançamento e músicas.

## **Funcionalidades**

- **Cadastro de Álbuns**: Permite cadastrar álbuns com informações como nome, gênero, artista, data de lançamento e lista de músicas.
- **Pesquisa de Álbuns**: Possibilita pesquisar álbuns pelo nome, permitindo buscar facilmente álbuns existentes no banco de dados.
- **Importação de Dados**: Permite importar álbuns a partir de arquivos **JSON** para o banco de dados.
- **Exportação de Dados**: Permite exportar todos os álbuns cadastrados para um arquivo **Excel (.xlsx)**.
- **Download de Arquivos**: A aplicação oferece arquivos para download, como exemplos de dados e álbuns.

## **Tecnologias Utilizadas**

- **Flask**: Framework web em Python para desenvolvimento da aplicação.
- **SQLAlchemy**: ORM (Object-Relational Mapping) para interagir com o banco de dados **SQLite**.
- **SQLite**: Banco de dados utilizado para armazenar os álbuns musicais.
- **Pandas**: Biblioteca Python utilizada para exportar os dados para arquivos **Excel**.
- **Jinja2**: Motor de templates utilizado para renderizar as páginas HTML.

## **Instalação**

Para rodar a aplicação localmente, siga os passos abaixo:

### 1. Clonar o Repositório

No terminal, execute o seguinte comando para clonar o repositório:

```bash
git clone https://github.com/seu-usuario/somzera.git
