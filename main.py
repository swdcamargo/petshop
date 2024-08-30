from enum import Enum
from typing import List
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Categoria(Enum):
    ALIMENTO = "ALIMENTO"
    MEDICAMENTO = "MEDICAMENTO"
    ACESSORIO = "ACESSORIO"

class Produto(BaseModel):
    id: int
    nome: str
    categoria: Categoria
    preco: float

produto_guardado: List[Produto] = []

@app.get("/", response_class=HTMLResponse)
async def read_products(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "produtos": produto_guardado})

@app.post("/cadastroproduto/")
async def create_product(request: Request, id: int = Form(...), nome: str = Form(...), categoria: Categoria = Form(...), preco: float = Form(...)):
    produto = Produto(id=id, nome=nome, categoria=categoria, preco=preco)
    produto_guardado.append(produto)
    return templates.TemplateResponse("index.html", {"request": request, "produtos": produto_guardado})

@app.get("/edit/{produto_id}", response_class=HTMLResponse)
async def edit_product(request: Request, produto_id: int):
    produto = next((p for p in produto_guardado if p.id == produto_id), None)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return templates.TemplateResponse("edit.html", {"request": request, "produto": produto})

@app.post("/updateproduto/")
async def update_product(request: Request, id: int = Form(...), nome: str = Form(...), categoria: Categoria = Form(...), preco: float = Form(...)):
    for index, p in enumerate(produto_guardado):
        if p.id == id:
            produto_guardado[index] = Produto(id=id, nome=nome, categoria=categoria, preco=preco)
            break
    return templates.TemplateResponse("index.html", {"request": request, "produtos": produto_guardado})

@app.get("/delete/{produto_id}", response_class=HTMLResponse)
async def delete_product(request: Request, produto_id: int):
    global produto_guardado
    produto_guardado = [p for p in produto_guardado if p.id != produto_id]
    return templates.TemplateResponse("index.html", {"request": request, "produtos": produto_guardado})
