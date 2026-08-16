# 🍕 Pizzaria API

API REST para gerenciamento de produtos, usuários e pedidos de uma pizzaria, desenvolvida com **FastAPI**, **PostgreSQL** e **Docker**.

O projeto aplica autenticação JWT, persistência com SQLAlchemy, migrations com Alembic, testes automatizados e integração contínua com GitHub Actions.

## 🌐 Demo

A aplicação está publicada no Render.

**Swagger:**
https://pizzaria-api-rhwi.onrender.com/docs

**API:**
https://pizzaria-api-rhwi.onrender.com

> A aplicação utiliza uma instância gratuita no Render. Após um período de inatividade, o primeiro acesso pode levar alguns segundos.

---

## 🚀 Tecnologias

### Backend

* Python 3.14
* FastAPI
* Pydantic
* SQLAlchemy
* Alembic
* PostgreSQL
* Psycopg
* JWT
* pwdlib
* Uvicorn

### Testes e qualidade

* Pytest
* pytest-cov
* Ruff

### Infraestrutura

* Docker
* Docker Compose
* GitHub Actions
* Render

---

## 📌 Funcionalidades

### Usuários e autenticação

* Cadastro de usuários
* Login com JWT
* Autenticação via Bearer Token
* Hash de senhas
* Rotas protegidas
* Controle de acesso administrativo

### Produtos

* Cadastro, consulta e atualização de produtos
* Paginação
* Busca por nome
* Filtro por disponibilidade
* Filtro por produtos populares
* Filtro por faixa de preço

### Pedidos

* Criação e consulta de pedidos
* Listagem de pedidos por usuário
* Adição e remoção de itens
* Cálculo automático do valor total
* Atualização e controle do status do pedido

---

## ▶️ Executando o projeto

### Pré-requisitos

É necessário ter instalado:

* Git
* Docker
* Docker Compose

Não é necessário instalar Python ou PostgreSQL localmente.

### 1. Clone o repositório

```bash
git clone git@github.com:johnealves/pizzaria-api.git
cd pizzaria-api
```

### 2. Configure as variáveis de ambiente

Crie o arquivo `.env.docker` na raiz do projeto:

```env
POSTGRES_USER=pizzaria
POSTGRES_PASSWORD=pizzaria
POSTGRES_DB=pizzaria

DATABASE_URL=postgresql+psycopg://pizzaria:pizzaria@postgres:5432/pizzaria

SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

O arquivo `.env.docker` não deve ser versionado.

### 3. Inicie a aplicação

```bash
docker compose up --build
```

O Docker irá iniciar a API e o PostgreSQL. As migrations do Alembic são aplicadas automaticamente durante a inicialização.

A aplicação ficará disponível em:

```text
API:     http://localhost:8000
Swagger: http://localhost:8000/docs
ReDoc:   http://localhost:8000/redoc
```

Para encerrar:

```bash
docker compose down
```

---

## 🌱 Dados iniciais

Para popular o banco com os dados iniciais:

```bash
docker compose exec api python -m seeds.seed
```

Os seeds criam os dados necessários para utilização da aplicação e verificam a existência dos registros antes da inserção.

### Resetar o banco

Para apagar completamente os dados, recriar o banco e executar os seeds:

```bash
docker compose down -v
docker compose up -d --build
docker compose exec api python -m seeds.seed
```

> O comando `docker compose down -v` remove o volume do PostgreSQL e apaga todos os dados armazenados localmente.

---

## 🗄️ Migrations

O schema do PostgreSQL é versionado utilizando Alembic.

Para aplicar migrations manualmente:

```bash
docker compose exec api alembic upgrade head
```

Para criar uma nova migration:

```bash
docker compose exec api alembic revision --autogenerate -m "descricao da migration"
```

---

## 🧪 Testes

Os testes automatizados são desenvolvidos com Pytest.

Para executar pelo container:

```bash
docker compose exec api pytest
```

Para verificar a cobertura:

```bash
docker compose exec api pytest --cov
```

Entre os cenários testados estão autenticação, produtos, paginação, filtros e rotas protegidas.

---

## 📚 Conceitos aplicados

* APIs REST
* Arquitetura em camadas
* Autenticação e autorização com JWT
* Hash de senhas
* Injeção de dependências
* SQLAlchemy ORM
* Modelagem relacional
* PostgreSQL
* Alembic migrations
* Tratamento centralizado de exceções
* Testes automatizados
* Docker e Docker Compose
* Integração contínua
* Deploy de aplicação containerizada

---

## 🔄 Próximas melhorias

* [ ] Ampliar a cobertura de testes
* [ ] Adicionar logging estruturado
* [ ] Adicionar observabilidade e monitoramento
* [ ] Integrar a API ao frontend da pizzaria

---

## 📄 Licença

Projeto desenvolvido para fins de estudo e portfólio.
