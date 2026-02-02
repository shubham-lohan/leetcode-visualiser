from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles

from app.routers import compare, profile

app = FastAPI(title="LeetCode Visualiser")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(profile.router)
app.include_router(compare.router)


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    return """User-agent: *
Allow: /
Sitemap: https://leetcode-visualiser.vercel.app/sitemap.xml
"""


@app.get("/sitemap.xml", response_class=Response)
def sitemap():
    content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://leetcode-visualiser.vercel.app/</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://leetcode-visualiser.vercel.app/compare</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
"""
    return Response(content=content, media_type="application/xml")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
