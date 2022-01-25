import uvicorn

if __name__ == '__main__':
    uvicorn.run("server_main:app",
                host="0.0.0.0",
                port=8443,
                reload=True,
                )