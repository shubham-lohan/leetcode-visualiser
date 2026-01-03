from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import profile, compare

app = FastAPI(title="LeetCode Visualiser")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(profile.router)
app.include_router(compare.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
