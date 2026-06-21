# FastAPI: The Complete Developer Guide — Every Module, Function & Feature Explained

> FastAPI has taken the Python backend world by storm. Whether you're coming from Flask, Django, or Express — this guide covers everything you need to build production-ready APIs. No fluff, all signal.

---

## What is FastAPI?

FastAPI is a modern, high-performance Python web framework for building APIs with Python 3.7+. It's built on top of **Starlette** (for web handling) and **Pydantic** (for data validation), and it uses standard Python type hints to do a lot of the heavy lifting for you.

Here's why developers love it:

- **Blazing fast** — on par with Node.js and Go
- **Automatic docs** — Swagger UI and ReDoc generated out of the box
- **Type-safe** — Python type hints drive validation, serialization, and documentation
- **Async-native** — built for `async/await` from the ground up
- **Less code, fewer bugs** — validation happens automatically, not manually

---

## Installation

```bash
pip install fastapi
pip install uvicorn[standard]

# Or install everything at once
pip install fastapi[all]
```

Run your app:

```bash
uvicorn main:app --reload
```

---

## 1. The FastAPI Application Class

Everything starts with instantiating `FastAPI`. This object holds your routes, middleware, event handlers, and configuration.

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="A production-ready API built with FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={"name": "Dev Team", "email": "dev@example.com"},
    license_info={"name": "MIT"},
)
```

**Key parameters:**

| Parameter | Purpose |
|---|---|
| `title` | API name shown in Swagger/ReDoc |
| `description` | Markdown-supported API description |
| `version` | API version string |
| `docs_url` | Path to Swagger UI (set `None` to disable) |
| `redoc_url` | Path to ReDoc |
| `openapi_url` | Path to the raw OpenAPI JSON |
| `debug` | Enable verbose error output |
| `contact` | Contact info dict |
| `license_info` | License info dict |

**Real-world tip:** Disable docs in production for security.

```python
import os

ENV = os.getenv("ENV", "dev")

app = FastAPI(
    docs_url="/docs" if ENV != "production" else None,
    redoc_url="/redoc" if ENV != "production" else None,
)
```

---

## 2. Routing & HTTP Methods

FastAPI exposes all standard HTTP methods as decorators.

```python
@app.get("/items")
@app.post("/items")
@app.put("/items/{id}")
@app.patch("/items/{id}")
@app.delete("/items/{id}")
@app.options("/items")
@app.head("/items")
```

A full CRUD example:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

@app.get("/items")
async def list_items():
    return [{"id": 1, "name": "Widget"}]

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"id": item_id}

@app.post("/items", status_code=201)
async def create_item(item: Item):
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"id": item_id, **item.dict()}

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    return None
```

**Route decorator parameters you should know:**

| Parameter | Purpose |
|---|---|
| `response_model` | Pydantic model to filter/validate the response |
| `status_code` | HTTP status code for success (default 200) |
| `tags` | Group routes in the docs |
| `summary` | Short label in the docs |
| `description` | Long Markdown description |
| `deprecated` | Mark as deprecated in docs |
| `include_in_schema` | Hide from OpenAPI schema |
| `response_class` | Custom response type |
| `dependencies` | List of `Depends()` for this route |
| `responses` | Document additional status codes |

---

## 3. Path Parameters

Path parameters are parts of the URL itself. FastAPI automatically type-casts them.

```python
from fastapi import FastAPI, Path

app = FastAPI()

# Basic — auto-cast to int
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

# With validation using Path()
@app.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(
        ...,
        title="Item ID",
        ge=1,       # must be >= 1
        le=1000,    # must be <= 1000
    )
):
    return {"item_id": item_id}

# String with regex
@app.get("/users/{username}")
async def get_by_username(
    username: str = Path(..., regex="^[a-zA-Z0-9_]+$", min_length=3, max_length=20)
):
    return {"username": username}
```

**`Path()` validation options:** `ge`, `gt`, `le`, `lt`, `min_length`, `max_length`, `regex`, `title`, `description`, `example`, `deprecated`

---

## 4. Query Parameters

Any function argument not matched to a path `{placeholder}` is automatically treated as a query parameter.

```python
from fastapi import FastAPI, Query
from typing import Optional, List

app = FastAPI()

# Simple optional query params
@app.get("/items")
async def list_items(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    active: bool = True,
):
    return {"skip": skip, "limit": limit, "search": search}

# With full validation
@app.get("/products")
async def list_products(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort: str = Query("created_at", regex="^(name|price|created_at)$"),
    q: Optional[str] = Query(None, min_length=2, max_length=50),
):
    return {"page": page, "size": size, "sort": sort}

# List query param — /filter?tag=python&tag=fastapi
@app.get("/filter")
async def filter_items(
    tags: List[str] = Query(default=[]),
):
    return {"tags": tags}
```

---

## 5. Request Body & Pydantic Models

This is where FastAPI truly shines. Define your request shape as a Pydantic model and get validation, serialization, and docs for free.

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class StatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"
    pending = "pending"

class Address(BaseModel):
    street: str
    city: str
    country: str = "India"
    pincode: str = Field(..., regex=r"^[0-9]{6}$")

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, example="Alice")
    email: str = Field(..., example="alice@example.com")
    age: Optional[int] = Field(None, ge=18, le=120)
    status: StatusEnum = StatusEnum.active
    address: Optional[Address] = None
    tags: List[str] = []

    @validator("email")
    def email_must_be_valid(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email")
        return v.lower()

    class Config:
        schema_extra = {
            "example": {"name": "Alice", "email": "alice@example.com", "age": 25}
        }
```

**`Field()` parameters:**

| Parameter | Purpose |
|---|---|
| `...` | Makes the field required |
| `default` | Default value |
| `default_factory` | Callable that returns the default |
| `min_length / max_length` | String length bounds |
| `ge / gt / le / lt` | Numeric bounds |
| `regex` | String must match this pattern |
| `alias` | Alternative JSON key name |
| `example` | Shown in Swagger docs |
| `exclude` | Exclude from serialization |

---

## 6. Response Handling

### response_model

Use `response_model` to filter what gets returned — this is how you prevent sensitive fields like passwords from leaking.

```python
class UserIn(BaseModel):
    name: str
    email: str
    password: str  # sensitive

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    # password is intentionally absent

@app.post("/users", response_model=UserOut, status_code=201)
async def create_user(user: UserIn):
    # password is stripped automatically by response_model
    return {"id": 42, "name": user.name, "email": user.email, "password": user.password}
```

### Response Classes

| Class | Use Case |
|---|---|
| `JSONResponse` | Default JSON output |
| `HTMLResponse` | Serve HTML pages |
| `PlainTextResponse` | Plain text output |
| `RedirectResponse` | Redirect to another URL |
| `FileResponse` | Serve a file for download |
| `StreamingResponse` | Stream large data or live feeds |
| `Response` | Raw response with full control |
| `ORJSONResponse` | Faster JSON via `orjson` |

```python
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse, RedirectResponse

@app.get("/html", response_class=HTMLResponse)
async def html_page():
    return "<html><body><h1>Hello</h1></body></html>"

@app.get("/redirect")
async def redirect():
    return RedirectResponse(url="/home", status_code=302)

@app.get("/download")
async def download():
    return FileResponse("report.pdf", filename="report.pdf")

@app.get("/stream")
async def stream():
    def generate():
        for i in range(100):
            yield f"data: {i}\n"
    return StreamingResponse(generate(), media_type="text/plain")
```

### Custom Headers & Cookies

```python
from fastapi import Response
from fastapi.responses import JSONResponse

@app.get("/custom")
async def custom(response: Response):
    response.headers["X-Custom-Header"] = "my-value"
    response.set_cookie(key="session", value="abc123", httponly=True, secure=True)
    return {"message": "Done"}

@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie("session")
    return {"message": "Logged out"}
```

---

## 7. Headers, Cookies, Form Data & File Uploads

### Headers

```python
from fastapi import Header
from typing import Optional

@app.get("/secure")
async def secure(
    x_api_key: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None),
):
    return {"key": x_api_key}
```

FastAPI auto-converts `X-API-Key` → `x_api_key` (Header-Case to snake_case).

### Cookies

```python
from fastapi import Cookie

@app.get("/profile")
async def profile(
    session_id: Optional[str] = Cookie(None),
    theme: str = Cookie(default="light"),
):
    return {"session_id": session_id, "theme": theme}
```

### Form Data

```python
from fastapi import Form

@app.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    remember_me: bool = Form(False),
):
    return {"username": username}
```

### File Uploads

```python
from fastapi import File, UploadFile
from typing import List

# Small file (loaded into memory)
@app.post("/upload/small")
async def upload_small(file: bytes = File(...)):
    return {"size": len(file)}

# UploadFile — streamed, good for large files
@app.post("/upload")
async def upload(file: UploadFile):
    content = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
    }

# Multiple files
@app.post("/upload/multiple")
async def upload_multiple(files: List[UploadFile]):
    return [{"filename": f.filename} for f in files]

# File + form fields together
@app.post("/upload/with-meta")
async def upload_meta(
    file: UploadFile,
    description: str = Form(...),
):
    return {"filename": file.filename, "description": description}
```

---

## 8. Dependency Injection — `Depends()`

Dependency injection is one of FastAPI's killer features. Share logic across routes cleanly — no globals, no repetition.

### Basic Function Dependency

```python
from fastapi import Depends
from typing import Optional

def common_params(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
):
    return {"skip": skip, "limit": limit, "search": search}

@app.get("/items")
async def get_items(params: dict = Depends(common_params)):
    return params

@app.get("/products")
async def get_products(params: dict = Depends(common_params)):
    return params  # same logic, zero repetition
```

### Class-Based Dependency

```python
class Pagination:
    def __init__(self, page: int = 1, size: int = 20):
        self.page = page
        self.size = min(size, 100)
        self.offset = (page - 1) * self.size

@app.get("/users")
async def get_users(pg: Pagination = Depends(Pagination)):
    return {"page": pg.page, "size": pg.size, "offset": pg.offset}
```

### Yield Dependency (Resource Management)

The most important pattern for database sessions — resource is always cleaned up even on error.

```python
from sqlalchemy.orm import Session
from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db          # provide the session to the route
    finally:
        db.close()        # always runs, even on exception

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()
```

### Auth Dependency

```python
from fastapi import HTTPException, Header

async def verify_token(x_api_key: Optional[str] = Header(None)):
    if x_api_key != "my-secret-key":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

# Apply to a single route
@app.get("/protected", dependencies=[Depends(verify_token)])
async def protected():
    return {"message": "Access granted"}

# Apply to all routes in a router
router = APIRouter(dependencies=[Depends(verify_token)])
```

---

## 9. Exception Handling

### HTTPException

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in db:
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} not found",
            headers={"X-Error": "item-not-found"},
        )
    return db[item_id]
```

### Custom Exception Handlers

```python
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class AppException(Exception):
    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=400,
        content={"error": exc.name, "message": exc.message},
    )

# Override FastAPI's default 422 handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": str(exc.body)},
    )
```

---

## 10. Middleware

Middleware wraps every single request and response. Perfect for logging, CORS, timing, and request tracing.

### Custom Middleware

```python
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time() - start)
    return response

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"→ {request.method} {request.url}")
    response = await call_next(request)
    print(f"← {response.status_code}")
    return response
```

### CORS Middleware

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["X-Total-Count"],
    max_age=600,
)
```

### Other Built-in Middleware

| Middleware | Purpose |
|---|---|
| `GZipMiddleware` | Compress responses above a size threshold |
| `HTTPSRedirectMiddleware` | Force all traffic to HTTPS |
| `TrustedHostMiddleware` | Reject requests with invalid `Host` headers |
| `SessionMiddleware` | Server-side session management |

```python
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"])
```

---

## 11. APIRouter — Modular Project Structure

As your project grows, you don't want all routes in `main.py`. `APIRouter` lets you split routes across files.

```python
# routers/users.py
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "User not found"}},
)

@router.get("/")
async def list_users():
    return [{"id": 1, "name": "Alice"}]

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"id": user_id}
```

```python
# main.py
from fastapi import FastAPI
from routers import users, products, orders

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router, prefix="/v1")
app.include_router(orders.router, prefix="/orders", tags=["orders"])
```

**`APIRouter` parameters:**

| Parameter | Purpose |
|---|---|
| `prefix` | URL prefix for all routes in this router |
| `tags` | Tag group for docs |
| `dependencies` | Shared `Depends()` for all routes |
| `responses` | Default response docs for all routes |
| `default_response_class` | Default response class |
| `include_in_schema` | Toggle schema inclusion |

---

## 12. Security & Authentication

### OAuth2 + JWT (Full Example)

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(400, "Wrong credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
async def read_me(user=Depends(get_current_user)):
    return {"username": user}
```

### API Key Authentication

```python
from fastapi.security import APIKeyHeader
from fastapi import Security

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_api_key(key: str = Security(api_key_header)):
    if key != "valid-secret-key":
        raise HTTPException(403, "Forbidden")
    return key

@app.get("/data")
async def secure_data(api_key: str = Security(get_api_key)):
    return {"data": "confidential"}
```

**Security classes reference:**

| Class | Purpose |
|---|---|
| `OAuth2PasswordBearer` | Extract Bearer token from Authorization header |
| `OAuth2PasswordRequestForm` | Parse username/password from form body |
| `HTTPBasic` | HTTP Basic authentication |
| `HTTPBearer` | Raw Bearer token extraction |
| `APIKeyHeader` | API key from a header |
| `APIKeyQuery` | API key from a query param |
| `APIKeyCookie` | API key from a cookie |
| `SecurityScopes` | Fine-grained OAuth2 scope control |

---

## 13. Background Tasks

Background tasks run after the response is returned to the client. No waiting, no blocking.

```python
from fastapi import BackgroundTasks

def send_welcome_email(email: str, name: str):
    # simulate slow email sending
    print(f"Sending email to {email}...")

async def process_report(report_id: int):
    await some_heavy_computation(report_id)

@app.post("/users")
async def create_user(user: UserCreate, background_tasks: BackgroundTasks):
    # Save user to DB...
    background_tasks.add_task(send_welcome_email, user.email, user.name)
    background_tasks.add_task(process_report, 1)
    return {"message": "User created. Email is on its way."}
    # Response returns IMMEDIATELY — tasks run after
```

> **When to use Background Tasks vs Celery:** Background tasks are great for lightweight work (emails, logs, notifications) that can tolerate a failure. Use Celery + Redis for retries, scheduling, and distributed task queues.

---

## 14. Startup & Shutdown — Lifespan

Use lifespan events to initialize DB connections, load ML models, or run cleanup on shutdown.

### Modern Way (Recommended)

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    await database.connect()
    ml_model["clf"] = load_model("model.pkl")
    print("App is starting...")

    yield  # app runs here

    # SHUTDOWN
    await database.disconnect()
    print("App is shutting down...")

app = FastAPI(lifespan=lifespan)
```

### Legacy Event Handlers

```python
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
```

---

## 15. WebSockets

FastAPI supports real-time, full-duplex communication via WebSockets.

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import List

# Simple echo
@app.websocket("/ws")
async def websocket_echo(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

# Broadcast to all connected clients
class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.connections.remove(ws)

    async def broadcast(self, message: str):
        for conn in self.connections:
            await conn.send_text(message)

manager = ConnectionManager()

@app.websocket("/chat/{room}")
async def chat(ws: WebSocket, room: str):
    await manager.connect(ws)
    try:
        while True:
            msg = await ws.receive_text()
            await manager.broadcast(f"[{room}] {msg}")
    except WebSocketDisconnect:
        manager.disconnect(ws)
        await manager.broadcast(f"A user left {room}")
```

**WebSocket methods:** `ws.accept()`, `ws.send_text()`, `ws.send_bytes()`, `ws.send_json()`, `ws.receive_text()`, `ws.receive_bytes()`, `ws.receive_json()`, `ws.close()`

---

## 16. Database Integration

### SQLAlchemy (Sync)

```python
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "postgresql://user:password@localhost/mydb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

### Async SQLAlchemy

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/mydb"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/users")
async def list_users(db: AsyncSession = Depends(get_async_db)):
    from sqlalchemy import select
    result = await db.execute(select(User))
    return result.scalars().all()
```

### MongoDB with Motor

```python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.mydb

@app.post("/documents")
async def create_doc(data: dict):
    result = await db.items.insert_one(data)
    return {"id": str(result.inserted_id)}

@app.get("/documents")
async def list_docs():
    return await db.items.find().to_list(100)
```

---

## 17. Testing

### TestClient (Sync)

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1}

def test_create_item():
    response = client.post("/items", json={"name": "Widget", "price": 9.99})
    assert response.status_code == 201

def test_invalid_type():
    response = client.get("/items/abc")  # should be int
    assert response.status_code == 422
```

### Testing with Auth

```python
def test_protected():
    # No auth
    assert client.get("/protected").status_code == 401

    # With auth
    response = client.get("/protected", headers={"X-API-Key": "valid-key"})
    assert response.status_code == 200
```

### Override Dependencies in Tests

```python
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
```

### Async Testing

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_async():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/1")
    assert response.status_code == 200
```

---

## 18. Advanced Features

### The Request Object

```python
from fastapi import Request

@app.get("/info")
async def request_info(request: Request):
    return {
        "method": request.method,
        "url": str(request.url),
        "client_ip": request.client.host,
        "headers": dict(request.headers),
        "cookies": request.cookies,
        "query_params": dict(request.query_params),
    }

# Read raw body
@app.post("/raw")
async def raw_body(request: Request):
    body = await request.body()
    json_data = await request.json()
    return {"size": len(body)}
```

### status Module

```python
from fastapi import status

@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: dict):
    return item

@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(id: int):
    return None
```

Common constants: `HTTP_200_OK`, `HTTP_201_CREATED`, `HTTP_204_NO_CONTENT`, `HTTP_400_BAD_REQUEST`, `HTTP_401_UNAUTHORIZED`, `HTTP_403_FORBIDDEN`, `HTTP_404_NOT_FOUND`, `HTTP_422_UNPROCESSABLE_ENTITY`, `HTTP_429_TOO_MANY_REQUESTS`, `HTTP_500_INTERNAL_SERVER_ERROR`

### StaticFiles

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
# Access: http://localhost:8000/static/logo.png

# Serve a React/Vue SPA
app.mount("/", StaticFiles(directory="dist", html=True), name="frontend")
```

### Jinja2 Templates

```python
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/page/{name}")
async def render_page(request: Request, name: str):
    return templates.TemplateResponse(
        "page.html",
        {"request": request, "name": name, "items": [1, 2, 3]},
    )
```

### url_path_for — Reverse URL Lookup

```python
@app.get("/users/{user_id}", name="get_user")
async def get_user(user_id: int):
    return {"id": user_id}

@app.get("/generate-link")
async def generate_link(request: Request):
    url = request.url_for("get_user", user_id=42)
    return {"url": str(url)}  # http://localhost:8000/users/42
```

---

## 19. OpenAPI Customization

### Tags and Metadata

```python
tags_metadata = [
    {"name": "users", "description": "User management operations"},
    {"name": "items", "description": "Item catalog operations"},
    {
        "name": "auth",
        "description": "Authentication",
        "externalDocs": {"url": "https://docs.example.com/auth"},
    },
]

app = FastAPI(title="My API", openapi_tags=tags_metadata)
```

### Custom OpenAPI Schema

```python
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(title="My API", version="3.0.0", routes=app.routes)
    schema["info"]["x-logo"] = {"url": "/static/logo.png"}
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi
```

### Multiple Response Status Codes

```python
@app.get(
    "/items/{item_id}",
    responses={
        200: {"description": "Item found", "model": ItemOut},
        404: {"description": "Item not found"},
        403: {"description": "Insufficient permissions"},
    },
)
async def get_item(item_id: int):
    pass
```

---

## 20. Deployment

### Uvicorn

```bash
# Development
uvicorn main:app --reload

# Production — multiple workers with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# With SSL
uvicorn main:app --ssl-keyfile key.pem --ssl-certfile cert.pem
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Configuration

```python
# pip install pydantic-settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My API"
    database_url: str
    secret_key: str
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)
```

---

## Complete Import Cheat Sheet

```python
# Core
from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request, Response
from fastapi import BackgroundTasks
from fastapi import status
from fastapi import WebSocket, WebSocketDisconnect

# Parameters
from fastapi import Body, Form, File, UploadFile
from fastapi import Header, Cookie, Path, Query
from fastapi import Security

# Responses
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from fastapi.responses import ORJSONResponse

# Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Security
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import HTTPBasic, HTTPBearer
from fastapi.security import APIKeyHeader, APIKeyQuery, APIKeyCookie
from fastapi.security import SecurityScopes

# Static & Templates
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Testing
from fastapi.testclient import TestClient

# Exceptions
from fastapi.exceptions import RequestValidationError
```

---

## Closing Thoughts

FastAPI has a well-designed API that rewards you for writing clean, type-annotated Python. Once you internalize the dependency injection system and Pydantic models, your code becomes self-documenting and self-validating at the same time.

The framework is genuinely production-ready — used by Microsoft, Uber, Netflix, and Explosion AI. It gets out of your way when you're building simple endpoints and scales gracefully to complex, authenticated, async, multi-service architectures.

Start with the basics, lean on `Depends()` heavily, and let Pydantic models be your contract between frontend and backend. That's the FastAPI way.

---

*Happy building. 🚀*
