from enum import Enum
from typing import Union
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI()

class Categoria(Enum):
    ALIMENTO = "ALIMENTO"
    MEDICAMENTO = "MEDICAMENTO"
    ACESSORIO = "ACESSORIO"

class Produto(BaseModel):
    id: int
    nome: str
    categoria: Categoria
    preco: float

produto_guardado = []


@app.post("/cadastroproduto")
def cad_prod(produto:Produto):
    produto_guardado.append(produto)
    return {"message": "Produto cadastrado com sucesso!"}
    


@app.get("/cadastroproduto")
def read_prod():
    if not produto_guardado:
        raise HTTPException(status_code=404, detail="Nenhum produto cadastrado")
    
    return produto_guardado

    

@app.put("/cadastroproduto")
def att_produto(produto:Produto):
    global produto_guardado
    if produto_guardado is None:
        raise HTTPException(status_code=404, detail="Nenhum produto cadastrado para atualizar")

    produto_guardado += produto

    return {"message": "Produto atualizado com sucesso!", "produto_atualizado": produto_guardado}

@app.delete("/cadastroproduto")
def delete_produto(produto:Produto):
    global produto_guardado
    if produto_guardado == None: 
        raise HTTPException(status_code=404, detail="Nenhum produto cadastrado para excluir")
    else: produto_guardado.remove(produto)
    return {"message":"Produto excluido com sucesso!"}