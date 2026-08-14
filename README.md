# 🍕 Pizzaria API

API REST desenvolvida com **FastAPI** para gerenciamento de produtos, usuários e pedidos de uma pizzaria.

O projeto foi desenvolvido com foco em boas práticas de desenvolvimento backend com Python, incluindo **autenticação JWT, arquitetura em camadas, SQLAlchemy, migrations com Alembic, testes automatizados, Docker, PostgreSQL e CI com GitHub Actions**.

A aplicação está publicada no **Render** e pode ser testada através da documentação interativa do Swagger.

## 🌐 Demo

**Swagger:**

https://pizzaria-api-rhwi.onrender.com/docs

**API:**

https://pizzaria-api-rhwi.onrender.com

> A aplicação utiliza uma instância gratuita no Render. Após um período de inatividade, o primeiro acesso pode levar alguns segundos enquanto o serviço é inicializado.

---

## 📑 Índice

- [🌐 Demo](#-demo)
- [🚀 Tecnologias](#-tecnologias)
- [📌 Funcionalidades](#-funcionalidades)
- [🏗️ Arquitetura](#️-arquitetura)
- [📁 Estrutura do projeto](#-estrutura-do-projeto)
- [⚙️ Variáveis de ambiente](#️-variáveis-de-ambiente)
- [▶️ Executando localmente](#️-executando-localmente)
- [🗄️ Banco de dados](#️-banco-de-dados)
- [🌱 Seeds](#-seeds)
- [🧪 Testes automatizados](#-testes-automatizados)
- [🔄 Integração contínua](#-integração-contínua)
- [☁️ Deploy](#️-deploy)
- [📚 Conceitos aplicados](#-conceitos-aplicados)
- [🔄 Próximas melhorias](#-próximas-melhorias)
- [📄 Licença](#-licença)

## 🚀 Tecnologias

### Backend

- Python 3.14
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- JWT (python-jose)
- pwdlib
- Uvicorn

### Banco de dados

- PostgreSQL — produção
- SQLite — desenvolvimento e testes
- Psycopg — driver PostgreSQL

### Testes e qualidade

- Pytest
- pytest-cov
- Ruff

### Infraestrutura e CI/CD

- Docker
- Docker Compose
- GitHub Actions
- Render

---

## 📌 Funcionalidades

### 👤 Usuários e autenticação

- Cadastro de usuários
- Login com JWT
- Autenticação via Bearer Token
- Proteção de rotas
- Controle de acesso por perfil
- Permissões administrativas

### 🍕 Produtos

- Cadastro de produtos
- Listagem de produtos
- Consulta de produto por ID
- Atualização de produtos
- Paginação
- Busca por nome
- Filtro por disponibilidade
- Filtro por produtos populares
- Filtro por faixa de preço
- Controle de acesso administrativo para operações protegidas

### 🛒 Pedidos

- Criação de pedidos
- Consulta de pedidos
- Consulta de pedido por ID
- Listagem de pedidos por usuário
- Atualização do status do pedido
- Adição de itens
- Remoção de itens
- Cálculo automático do valor total
- Controle do ciclo de status do pedido

### 🔐 Segurança

- Autenticação JWT
- Bearer Token
- Hash de senhas
- Rotas protegidas
- Controle de autorização
- Configurações sensíveis através de variáveis de ambiente

---

## 🏗️ Arquitetura

A aplicação utiliza separação de responsabilidades em camadas:

```text
HTTP Request
     │
     ▼
   Router
     │
     ▼
  Service
     │
     ▼
 SQLAlchemy
     │
     ▼
  Database
```

Os **routers** são responsáveis pela camada HTTP e definição dos endpoints.

Os **services** concentram as regras de negócio.

O **SQLAlchemy** realiza o mapeamento e acesso aos dados.

As sessões do banco são fornecidas através do sistema de **injeção de dependências do FastAPI**.

A aplicação também possui tratamento centralizado de exceções para padronizar respostas de erro.

---

## 📁 Estrutura do projeto

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── core/
│   ├── exception_handles.py
│   └── exceptions.py
│
├── db/
│   ├── base.py
│   ├── database.py
│   └── dependency.py
│
├── enums/
│   ├── order_status.py
│   └── product_category.py
│
├── models/
│   ├── order_models.py
│   ├── product_models.py
│   └── user_models.py
│
├── routers/
│   ├── auth_routes.py
│   ├── orders_routes.py
│   └── products_routes.py
│
├── schemas/
│   ├── auth_schemas.py
│   ├── order_schemas.py
│   ├── products_schemas.py
│   └── user_schemas.py
│
├── security/
│   ├── auth.py
│   └── config.py
│
├── seeds/
│   ├── products.py
│   ├── seed.py
│   └── seed_products.py
│
├── services/
│   ├── auth_service.py
│   ├── order_service.py
│   └── product_service.py
│
├── tests/
│
├── compose.dev.yaml
├── compose.yaml
├── Dockerfile
├── entrypoint.sh
├── alembic.ini
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

DATABASE_URL=sqlite:///banco.db
```

O arquivo `.env` não deve ser versionado.

---

## ▶️ Executando localmente

O ambiente de desenvolvimento utiliza **Docker Compose + SQLite**.

### 1. Clone o repositório

```bash
git clone git@github.com:johnealves/pizzaria-api.git
```

Entre no diretório:

```bash
cd pizzaria-api
```

### 2. Configure o `.env`

Crie o arquivo `.env` conforme descrito na seção de variáveis de ambiente.

### 3. Inicie o ambiente

Na primeira execução ou quando houver alterações que exijam reconstrução da imagem:

```bash
docker compose -f compose.dev.yaml up --build
```

Nas próximas execuções:

```bash
docker compose -f compose.dev.yaml up
```

A API ficará disponível em:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

Para encerrar:

```bash
docker compose -f compose.dev.yaml down
```

---

## 🗄️ Banco de dados

A aplicação utiliza configurações diferentes conforme o ambiente:

| Ambiente | Banco |
|---|---|
| Desenvolvimento | SQLite |
| Testes automatizados | SQLite isolado |
| Produção | PostgreSQL |

A conexão é definida através da variável de ambiente:

```env
DATABASE_URL=...
```

O **SQLAlchemy** abstrai o acesso ao banco e o **Alembic** é utilizado para versionamento do schema.

### Migrations

Para aplicar as migrations no ambiente local:

```bash
docker compose -f compose.dev.yaml exec api alembic upgrade head
```

---

## 🌱 Seeds

O projeto possui seeds para criação dos dados iniciais de produtos.

Para executar localmente:

```bash
docker compose -f compose.dev.yaml exec api python -m seeds.seed
```

O seed verifica se os produtos já existem antes da inserção, evitando duplicações.

No ambiente de deploy, o processo de inicialização é responsável por executar as etapas necessárias antes da inicialização da API.

---

## 🧪 Testes automatizados

Os testes são desenvolvidos com **Pytest**.

O ambiente de testes utiliza um banco SQLite independente, evitando alterações nos dados utilizados pela aplicação.

Para executar os testes:

```bash
pytest
```

Ou utilizando o container de desenvolvimento:

```bash
docker compose -f compose.dev.yaml exec api pytest
```

Entre os cenários testados estão:

- Listagem de produtos
- Consulta por ID
- Paginação
- Filtros
- Criação de produtos
- Autenticação de rotas protegidas

---

## 🔄 Integração contínua

O projeto utiliza **GitHub Actions** para executar automaticamente os testes.

A pipeline é executada em pushes e Pull Requests direcionados à branch principal.

```text
Push / Pull Request
        │
        ▼
     GitHub
        │
        ▼
 GitHub Actions
        │
        ├── Checkout
        ├── Setup Python
        ├── Instala dependências
        └── Executa Pytest
                │
                ▼
          Código validado
```

Isso permite detectar regressões automaticamente antes da integração de novas alterações.

---

## ☁️ Deploy

A aplicação está publicada no **Render** utilizando Docker.

Em produção, a API utiliza um banco **PostgreSQL** separado do container da aplicação.

```text
              Internet
                  │
                  ▼
        Render Web Service
                  │
                  ▼
          FastAPI / Docker
                  │
                  ▼
        PostgreSQL / Render
```

As configurações sensíveis de produção são fornecidas através de variáveis de ambiente no Render e não são armazenadas no repositório.

O fluxo do projeto é:

```text
Desenvolvimento
      │
      ▼
    GitHub
      │
      ├──── GitHub Actions
      │          │
      │        Pytest
      │
      ▼
    Render
      │
      ▼
 FastAPI + PostgreSQL
```

### Endpoints públicos

API:

https://pizzaria-api-rhwi.onrender.com

Swagger:

https://pizzaria-api-rhwi.onrender.com/docs

ReDoc:

https://pizzaria-api-rhwi.onrender.com/redoc

---

## 📚 Conceitos aplicados

Durante o desenvolvimento deste projeto foram aplicados conceitos como:

- Desenvolvimento de APIs REST
- Arquitetura em camadas
- Autenticação JWT
- Autorização baseada em perfil
- Hash de senhas
- Injeção de dependências
- ORM com SQLAlchemy
- Modelagem relacional
- Migrations com Alembic
- PostgreSQL
- Paginação
- Filtros e busca
- Tratamento centralizado de exceções
- Testes automatizados
- Isolamento do banco de testes
- Docker
- Docker Compose
- Variáveis de ambiente
- CI com GitHub Actions
- Deploy de aplicação containerizada

---

## 🔄 Próximas melhorias

- [ ] Ampliar a cobertura de testes
- [ ] Adicionar logging estruturado
- [ ] Adicionar testes de integração utilizando PostgreSQL
- [ ] Adicionar observabilidade e monitoramento
- [ ] Integrar a API ao frontend da pizzaria

---

## 📄 Licença

Projeto desenvolvido para fins de estudo e portfólio.
