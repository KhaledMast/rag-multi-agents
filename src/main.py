from fastapi import FastAPI
from lifespan import lifespan
from routes import base, data, nlp


# Initialisation of FastAPI with the lifespan
app = FastAPI(lifespan=lifespan)

# TODO: Add middleware

# Inclusion of routers
app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)
