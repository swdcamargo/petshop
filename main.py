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
    


def cad_prod(produto: Produto):
    for p in produto_guardado:
        if p.id == produto.id:
            raise HTTPException(status_code=400, detail="Produto com esse ID já existe")
    
    produto_guardado.append(produto)
    return {"message": "Produto cadastrado com sucesso!"}

    

@app.put("/cadastroproduto/{produto_id}")
def att_produto(produto_id: int, produto: Produto):
    for index, pdnalista in enumerate(produto_guardado):
        if pdnalista.id == produto_id:
            produto_guardado[index] = produto
            return {"message": "Produto atualizado com sucesso!", "produto_atualizado": produto}
    
    raise HTTPException(status_code=404, detail="Produto não encontrado para atualizar")

@app.delete("/cadastroproduto/{produto_id}")
def delete_produto(produto_id: int):
    for pdnalista in produto_guardado:
        if pdnalista.id == produto_id:
            produto_guardado.remove(pdnalista)
            return {"message": "Produto excluído com sucesso!"}
    
    raise HTTPException(status_code=404, detail="Produto não encontrado para excluir")