from fastapi import FastAPI


app = FastAPI()

@app.get('/')
def hello():
    return {'message':'Hello Fast_API'}


@app.get('/about')
def about():
    return {'message':'I currently learning FastAPI at 12:40'}