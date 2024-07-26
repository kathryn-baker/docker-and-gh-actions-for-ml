from fastapi import FastAPI
from .text_generation import TextGenerator
from functools import cache
import logging

import os

app = FastAPI()

@app.get("/")
async def health():
    return {"health": "OK", 'env': os.getenv('TEST')}

@cache
def get_model() -> TextGenerator:
    # this stores a dictionary of calls and results rather than actually calling the function
    # every time
    logging.info('Loading model')
    return TextGenerator()


@app.get("/{prompt}")
async def generate_text(
    prompt: str,
    max_new_tokens: int=50,
    num_return_sequences: int=1,
) -> dict:
    model = get_model()
    sequences = model.generate(prompt, max_new_tokens=max_new_tokens, num_return_sequences=num_return_sequences)
    return {"generated_sequences": sequences}

@app.on_event('startup')
async def on_startup():
    # this calls the function when the app first starts rather than when we do the first
    # prompt 
    get_model()