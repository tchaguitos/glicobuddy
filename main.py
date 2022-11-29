from fastapi import FastAPI

from contextos.usuarios.pontos_de_entrada.api import router as router_usuarios
from contextos.glicemias.pontos_de_entrada.api import router as router_glicemias


app = FastAPI()

app.include_router(router_usuarios)
app.include_router(router_glicemias)
