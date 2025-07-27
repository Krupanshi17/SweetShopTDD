from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routes import auth # adjust this to your project structure

app = FastAPI()

# ✅ Register routes first
app.include_router(auth.router)

# ✅ Custom OpenAPI schema for global "Authorize" button
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Sweet Shop API",
        version="1.0.0",
        description="API for Sweet Shop Management",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # 🔥 Inject BearerAuth globally
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi