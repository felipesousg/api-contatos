from datetime import datetime
import os
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI(title="API de Contatos", version="1.0.0")

# Define o caminho do banco (usa a variável de ambiente do Azure ou local)
DB_PATH = os.getenv("DB_PATH", "contatos.db")


def get_db():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  return conn


def init_db():
  dir_name = os.path.dirname(DB_PATH)
  if dir_name and not os.path.exists(dir_name):
    os.makedirs(dir_name, exist_ok=True)
  conn = get_db()
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT,
            favorito INTEGER DEFAULT 0,
            criado_em TEXT
        )
    """)
  conn.commit()
  conn.close()


@app.on_event("startup")
def startup_event():
  init_db()


class ContatoCreate(BaseModel):
  nome: str
  email: EmailStr
  telefone: str | None = None
  favorito: bool = False


class ContatoResponse(BaseModel):
  id: int
  nome: str
  email: str
  telefone: str | None = None
  favorito: bool
  criado_em: str


@app.post("/contatos", response_model=ContatoResponse, status_code=201)
def criar_contato(contato: ContatoCreate):
  if not contato.nome or not contato.nome.strip():
    raise HTTPException(status_code=422, detail="O campo nome é obrigatório.")

  criado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  favorito_int = 1 if contato.favorito else 0

  conn = get_db()
  cursor = conn.cursor()
  cursor.execute(
      """
        INSERT INTO contatos (nome, email, telefone, favorito, criado_em)
        VALUES (?, ?, ?, ?, ?)
    """,
      (contato.nome, contato.email, contato.telefone, favorito_int, criado_em),
  )
  conn.commit()
  contato_id = cursor.lastrowid
  conn.close()

  return {
      "id": contato_id,
      "nome": contato.nome,
      "email": contato.email,
      "telefone": contato.telefone,
      "favorito": contato.favorito,
      "criado_em": criado_em,
  }


@app.get("/contatos", response_model=list[ContatoResponse])
def listar_contatos():
  conn = get_db()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM contatos")
  rows = cursor.fetchall()
  conn.close()

  resultado = []
  for row in rows:
    resultado.append({
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "telefone": row["telefone"],
        "favorito": bool(row["favorito"]),
        "criado_em": row["criado_em"],
    })
  return resultado


@app.get("/contatos/{item_id}", response_model=ContatoResponse)
def obter_contato(item_id: int):
  conn = get_db()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM contatos WHERE id = ?", (item_id,))
  row = cursor.fetchone()
  conn.close()

  if not row:
    raise HTTPException(status_code=404, detail="Contato não encontrado")

  return {
      "id": row["id"],
      "nome": row["nome"],
      "email": row["email"],
      "telefone": row["telefone"],
      "favorito": bool(row["favorito"]),
      "criado_em": row["criado_em"],
  }


@app.put("/contatos/{item_id}", response_model=ContatoResponse)
def atualizar_contato(item_id: int, contato: ContatoCreate):
  conn = get_db()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM contatos WHERE id = ?", (item_id,))
  row = cursor.fetchone()

  if not row:
    conn.close()
    raise HTTPException(status_code=404, detail="Contato não encontrado")

  favorito_int = 1 if contato.favorito else 0
  cursor.execute(
      """
        UPDATE contatos SET nome = ?, email = ?, telefone = ?, favorito = ?
        WHERE id = ?
    """,
      (contato.nome, contato.email, contato.telefone, favorito_int, item_id),
  )
  conn.commit()
  conn.close()

  return {
      "id": item_id,
      "nome": contato.nome,
      "email": contato.email,
      "telefone": contato.telefone,
      "favorito": contato.favorito,
      "criado_em": row["criado_em"],
  }


@app.delete("/contatos/{item_id}")
def deletar_contato(item_id: int):
  conn = get_db()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM contatos WHERE id = ?", (item_id,))
  row = cursor.fetchone()

  if not row:
    conn.close()
    raise HTTPException(status_code=404, detail="Contato não encontrado")

  cursor.execute("DELETE FROM contatos WHERE id = ?", (item_id,))
  conn.commit()
  conn.close()
  return {"detail": "Contato deletado com sucesso"}