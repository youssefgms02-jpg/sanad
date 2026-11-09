
import os
import secrets

from datetime import datetime, timezone
from urllib.parse import urlparse

from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Header,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import Service
from schemas import ServiceCreate, ServiceUpdate


# =====================================
# إعداد التطبيق
# =====================================

app = FastAPI(
    title="SANAD API",
    description="منصة سَنَد للخدمات والمعلومات المصرية",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)


# =====================================
# الاتصال بقاعدة البيانات
# =====================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================================
# حماية الإدارة
# =====================================

def verify_admin_token(
    x_admin_token: str = Header(..., alias="X-Admin-Token")
):
    # اقرأ المفتاح وقت وصول الطلب، وليس عند تشغيل التطبيق.
    expected_token = os.environ.get("SANAD_ADMIN_TOKEN")

    # نطبع حالة وجود المفتاح فقط، ولا نطبع قيمته حفاظًا على سريته.
    print("ADMIN TOKEN CONFIGURED:", bool(expected_token), flush=True)

    if not expected_token:
        raise HTTPException(
            status_code=503,
            detail="Admin authentication is not configured",
        )

    if not secrets.compare_digest(x_admin_token, expected_token):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )

    return True


# =====================================
# تحويل الخدمة إلى JSON
# =====================================

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


# =====================================
# التحقق من المصدر الرسمي
# =====================================

def validate_official_source(source):
    if not source:
        raise HTTPException(
            status_code=400,
            detail="يجب إضافة رابط المصدر الرسمي قبل النشر",
        )

    parsed = urlparse(source)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise HTTPException(
            status_code=400,
            detail="رابط المصدر غير صالح",
        )


# =====================================
# إعدادات CORS
# =====================================

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


# =====================================
# المسارات العامة
# =====================================

@app.get("/")
def home():
    return {
        "message": "أهلاً بيك في سَنَد",
        "status": "API is running",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


# عرض الخدمات المنشورة فقط
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


# تفاصيل خدمة منشورة
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


# =====================================
# لوحة الإدارة - الإحصائيات
# =====================================

@app.get("/admin/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    admin: bool = Depends(verify_admin_token),
):
    total = db.query(Service).count()

    published = db.query(Service).filter(
        Service.status == "published"
    ).count()

    drafts = db.query(Service).filter(
        Service.status == "draft"
    ).count()

    return {
        "total_services": total,
        "published_services": published,
        "draft_services": drafts,
    }


# =====================================
# لوحة الإدارة - عرض جميع الخدمات
# =====================================

@app.get("/admin/services")
def get_admin_services(
    status: str | None = None,
    db: Session = Depends(get_db),
    admin: bool = Depends(verify_admin_token),
):
    query = db.query(Service)

    if status:
        if status not in ("draft", "published"):
            raise HTTPException(
                status_code=400,
                detail="حالة الخدمة غير صحيحة",
            )

        query = query.filter(Service.status == status)

    services = query.order_by(
        Service.id.desc()
    ).all()

    return {
        "services": [
            service_to_dict(service)
            for service in services
        ]
    }


# =====================================
# لوحة الإدارة - تفاصيل أي خدمة
# =====================================

@app.get("/admin/services/{service_id}")
def get_admin_service(
    service_id: int,
    db: Session = Depends(get_db),
    admin: bool = Depends(verify_admin_token),
):
    service = db.query(Service).filter(
        Service.id == service_id
    ).first()

    if not service:
        raise HTTPException(
            status_code=404,
            detail="الخدمة غير موجودة",
        )

    return service_to_dict(service)


# =====================================
# لوحة الإدارة - إضافة خدمة
# =====================================

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


# =====================================
# لوحة الإدارة - تعديل خدمة
# =====================================

@app.patch("/admin/services/{service_id}")
def update_service(
    service_id: int,
    service_data: ServiceUpdate,
    db: Session = Depends(get_db),
    admin: bool = Depends(verify_admin_token),
):
    service = db.query(Service).filter(
        Service.id == service_id
    ).first()

    if not service:
        raise HTTPException(
            status_code=404,
            detail="الخدمة غير موجودة",
        )

    updates = service_data.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="لم يتم إرسال أي بيانات للتعديل",
        )

    for field in ("name", "description", "category"):
        if field in updates and updates[field] is None:
            raise HTTPException(
                status_code=400,
                detail=f"الحقل {field} لا يمكن أن يكون فارغًا",
            )

    try:
        for field, value in updates.items():
            setattr(service, field, value)

        # أي تعديل يحتاج مراجعة جديدة قبل إعادة النشر
        service.status = "draft"
        service.last_reviewed = None

        db.commit()
        db.refresh(service)

        return service_to_dict(service)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="تعذر تعديل الخدمة",
        )


# =====================================
# لوحة الإدارة - نشر خدمة
# =====================================

@app.patch("/admin/services/{service_id}/publish")
def publish_service(
    service_id: int,
    db: Session = Depends(get_db),
    admin: bool = Depends(verify_admin_token),
):
    service = db.query(Service).filter(
        Service.id == service_id
    ).first()

    if not service:
        raise HTTPException(
            status_code=404,
            detail="الخدمة غير موجودة",
        )

    validate_official_source(service.official_source)

    service.status = "published"
    service.last_reviewed = datetime.now(timezone.utc)

    db.commit()
    db.refresh(service)

    return service_to_dict(service)


# =====================================
# لوحة الإدارة - إلغاء نشر خدمة
# =====================================

@app.patch("/admin/services/{service_id}/unpublish")
def unpublish_service(
    service_id: int,
    db: Session = Depends(get_db),
    admin: bool = Depends(verify_admin_token),
):
    service = db.query(Service).filter(
        Service.id == service_id
    ).first()

    if not service:
        raise HTTPException(
            status_code=404,
            detail="الخدمة غير موجودة",
        )

    service.status = "draft"
    service.last_reviewed = None

    db.commit()
    db.refresh(service)

    return service_to_dict(service)


# =====================================
# لوحة الإدارة - حذف خدمة
# =====================================

@app.delete("/admin/services/{service_id}")
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    admin: bool = Depends(verify_admin_token),
):
    service = db.query(Service).filter(
        Service.id == service_id
    ).first()

    if not service:
        raise HTTPException(
            status_code=404,
            detail="الخدمة غير موجودة",
        )

    try:
        db.delete(service)
        db.commit()

        return {
            "message": "تم حذف الخدمة بنجاح",
            "service_id": service_id,
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="تعذر حذف الخدمة",
        )
