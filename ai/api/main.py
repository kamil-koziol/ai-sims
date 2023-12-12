from fastapi import FastAPI

app = FastAPI()


@app.get('/personas')
def index():
    return 'cos'


