from fastapi import FastAPI

from contextos.glicemias.pontos_de_entrada.api import router as router_glicemias

app = FastAPI()

app.include_router(router_glicemias)
