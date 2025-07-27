from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routes import auth, sweet  # Import route modules
from app.services.auth_service import seed_admin  # Admin seeding logic
from fastapi.middleware.cors import CORSMiddleware  # Middleware for CORS handling

# Initialize FastAPI application with debug enabled
app = FastAPI(debug=True)

# Add CORS middleware to allow cross-origin requests (for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routers for authentication and sweet management
app.include_router(auth.router)
app.include_router(sweet.router)

# Define custom OpenAPI schema to include global JWT bearer authentication
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    # Generate default OpenAPI schema
    openapi_schema = get_openapi(
        title="Sweet Shop API",
        version="1.0.0",
        description="API for Sweet Shop Management",
        routes=app.routes,
    )

    # Add security scheme for Bearer token (JWT)
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Apply BearerAuth globally to all routes
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Override FastAPI's default OpenAPI schema generation with custom one
app.openapi = custom_openapi

# Event triggered on application startup to seed admin user
@app.on_event("startup")
async def startup_event():
    await seed_admin()
