# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.middleware import AdminAuthMiddleware

from .api.v1.routes.admin import auth as admin_auth
from .api.v1.routes.admin import whitelist as admin_whitelist

from .api.v1.routes.public import whitelist as public_whitelist

app = FastAPI(title="Meganacci API")

# Register middleware
app.add_middleware(AdminAuthMiddleware)

# Register CORS middleware
origins = [
    # "http://localhost:3000",   # Next.js dev server
    # "http://127.0.0.1:3000",   # sometimes browsers resolve localhost differently
    "https://meganacci.xyz"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # which origins can call your API
    allow_credentials=True,
    allow_methods=["*"],          # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # allow all headers
)

# Admin routers
app.include_router(admin_auth.router, prefix="/v1/admin/auth", tags=["admin-auth"])
app.include_router(admin_whitelist.router, prefix="/v1/admin/whitelist", tags=["admin-whitelist"])

# Public router
app.include_router(public_whitelist.router, prefix="/v1/whitelist", tags=["public-whitelist"])