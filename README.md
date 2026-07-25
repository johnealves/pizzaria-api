# 🍕 Pizzaria API

API REST desenvolvida com **FastAPI** para simular o gerenciamento de pedidos de uma pizzaria.

O projeto foi desenvolvido com foco em boas práticas de desenvolvimento backend utilizando Python, incluindo autenticação JWT, arquitetura em camadas, modelagem relacional com SQLAlchemy e versionamento de banco de dados com Alembic.

---

## 🚀 Tecnologias

- Python 3.14
- FastAPI
- SQLAlchemy
- Alembic
- SQLite
- Pydantic
- JWT (python-jose)
- Passlib
- Uvicorn

---

## 📌 Funcionalidades

### Usuários

- Cadastro de usuários
- Login com JWT
- Autenticação de rotas
- Controle de acesso por perfil (Administrador e Cliente)

### Pedidos

- Criar pedidos
- Consultar pedidos
- Consultar pedido por ID
- Listar pedidos de um usuário
- Atualizar status do pedido
- Adicionar itens
- Remover itens
- Cálculo automático do valor total

### Segurança

- Autenticação via Bearer Token
- Rotas protegidas
- Validação de permissões para administradores e clientes

---

## 📁 Estrutura do projeto

```text
.
├── alembic/
├── db/
│   ├── base.py
│   ├── database.py
│   └── dependency.py
│
├── enums/
│   └── order_status.py
│
├── models/
│   ├── order_model.py
│   └── user_model.py
│
├── routers/
│   ├── auth_router.py
│   └── orders_router.py
│
├── schemas/
│
├── .env
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalação

Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/pizzaria-api.git
```

Entre na pasta

```bash
cd pizzaria-api
```

Crie um ambiente virtual

Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 🔐 Variáveis de ambiente

Crie um arquivo `.env`

```env
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🗄️ Banco de dados

Execute as migrations

```bash
alembic upgrade head
```

---

## ▶️ Executando

```bash
uvicorn main:app --reload
```

---

## 📖 Documentação

Após iniciar a aplicação:

Swagger

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

## 📚 Conceitos praticados

- Desenvolvimento de APIs REST
- Autenticação JWT
- SQLAlchemy ORM
- Relacionamentos entre entidades
- Migrations com Alembic
- Organização de projetos FastAPI
- Injeção de Dependências
- Pydantic
- Arquitetura em camadas
- Controle de autorização

---

## 🔄 Próximas melhorias

- [ ] Docker
- [ ] Testes automatizados
- [ ] Paginação
- [ ] Histórico de alterações dos pedidos
- [ ] Filtros de consulta
- [ ] Logging
- [ ] CI/CD com GitHub Actions

---

## 📄 Licença

Projeto desenvolvido para fins de estudo.