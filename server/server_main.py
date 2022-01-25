from fastapi import FastAPI
import os
from starlette.responses import FileResponse

app = FastAPI()

# path 설정 필요
BASE_DIR = '/home/bigdata/work'
IMG_DIR = os.path.join(BASE_DIR,'ramdisk/Img/')
MAL_DIR = os.path.join(BASE_DIR, 'ramdisk/')

@app.get('/Img/img/{file}')
def show(file:str):
    path = ''.join([IMG_DIR,file])
    return FileResponse(path)

@app.get('/Img/mal/{file}')
def show(file:str):
    path = ''.join([MAL_DIR,file])
    return FileResponse(path)
