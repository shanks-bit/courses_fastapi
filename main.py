from fastapi import FastAPI
from routes.courses import courses_root
from routes.entry import entry_root

app = FastAPI()

app.include_router(entry_root)
app.include_router(courses_root)


