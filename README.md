# 🚀 API REST de Contatos - FastAPI & Azure

API REST desenvolvida em Python utilizando **FastAPI** e **SQLite**, implantada na nuvem Microsoft Azure através do **Azure Container Instances (ACI)**. Este projeto foi desenvolvido para atender aos requisitos acadêmicos da **FIAP**.

---

## 👨‍💻 Autor

* **Nome:** Felipe de Sousa Gomes
* **RM:** 565085
* **Instituição:** FIAP (Faculdade de Informática e Administração Paulista)

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12
* **Framework Web:** FastAPI
* **Validação de Dados:** Pydantic
* **Banco de Dados:** SQLite (Embarcado)
* **Containerização:** Docker
* **Infraestrutura em Nuvem:** Azure Container Instances (ACI)
* **Região de Deploy:** Brazil South (`brazilsouth`)

---

## 📌 Endpoints da API

* `POST /contatos/` — Cadastra um novo contato.
* `GET /contatos/` — Lista todos os contatos cadastrados.
* `GET /contatos/{item_id}` — Busca um contato específico pelo ID.

---

## 💻 Como Executar o Projeto Localmente

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/felipesousg/api-contatos.git](https://github.com/felipesousg/api-contatos.git)
   cd api-contatos
