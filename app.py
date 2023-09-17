from fastapi import FastAPI
import uvicorn
import os
from routers import oauth2_router


app = FastAPI()

# Add routers
app.include_router(oauth2_router, prefix='/api/oauth2', tags=['OAuth2'])


if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=4567, reload=True, log_level='info', workers=os.cpu_count())
