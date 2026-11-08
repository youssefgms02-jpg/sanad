
import os
import secrets

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import Service
from schemas import ServiceCreate


# إنشاء التطبيق
app = FastAPI(
    title="SANAD API",
    description="منصة سَنَد للخدمات والمعلومات المصرية",
    version="1.0.0",
)


# إنشاء جداول قاعدة البيانات
Base.metadata.create_all(bind=engine)


# الاتصال بقاعدة البيانات
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# التحقق من المفتاح الإداري
def verify_admin_token(
    x_admin_token: str = Header(..., alias="X-Admin-Token")
):
    expected_token = os.getenv("SANAD_ADMIN_TOKEN")

    if not expected_token:
        raise HTTPException(
            status_code=503,
            detail="Admin authentication is not configured",
        )

    if not secrets.compare_digest(
        x_admin_token,
        expected_token,
    ):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )

    return True


# تحويل الخدمة إلى JSON
def service_to_dict(service):
    return {
        "id": service.id,
        "name": service.name,
        "description": service.description,
        "category": service.category,
        "authority": service.authority,
        "eligibility": service.eligibility,
        "documents": service.documents,
        "steps": service.steps,
        "official_source": service.official_source,
        "last_reviewed": (
            service.last_reviewed.isoformat()
            if service.last_reviewed
            else None
        ),
        "status": service.status,
        "created_at": (
            service.created_at.isoformat()
            if service.created_at
            else None
        ),
    }


# إعدادات CORS
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "SANAD_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# الصفحة الرئيسية
@app.get("/")
def home():
    return {
        "message": "أهلاً بيك في سَنَد",
        "status": "API is running",
    }


# فحص حالة الخادم
@app.get("/health")
def health():
    return {"status": "ok"}


# عرض الخدمات المنشورة
@app.get("/services")
def get_services(
    category: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Service).filter(
        Service.status == "published"
    )

    if category:
        query = query.filter(
            Service.category.ilike(category)
        )

    services = query.order_by(Service.id).all()

    return {
        "services": [
            service_to_dict(service)
            for service in services
        ]
    }


# عرض تفاصيل خدمة منشورة
@app.get("/services/{service_id}")
def get_service(
    service_id: int,
    db: Session = Depends(get_db),
):
    service = (
        db.query(Service)
        .filter(
            Service.id == service_id,
            Service.status == "published",
        )
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="الخدمة غير موجودة أو غير منشورة",
        )

    return service_to_dict(service)


# إضافة خدمة جديدة كمسودة
@app.post("/admin/services", status_code=201)
def create_service(
    service_data: ServiceCreate,
    db: Session = Depends(get_db),
    admin: bool = Depends(verify_admin_token),
):
    new_service = Service(
        **service_data.model_dump(),
        status="draft",
    )

    try:
        db.add(new_service)
        db.commit()
        db.refresh(new_service)

        return service_to_dict(new_service)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="تعذر حفظ الخدمة",
        )
