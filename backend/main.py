
import os
import secrets
import re
from difflib import SequenceMatcher

from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse

from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Header,
    Request,
    Response,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import Service, ServiceReport, User, AuthSession, UserFavorite
from schemas import ServiceCreate, ServiceUpdate, ServiceReportCreate, ServiceReportStatusUpdate, AuthRegister, AuthLogin, FavoriteSync
from source_utils import extract_http_urls, valid_http_url, normalize_arabic_text
from auth_utils import hash_password, verify_password, hash_session_token, new_session_token


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
        "source_urls": extract_http_urls(service.official_source),
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
    urls = extract_http_urls(source)
    if not urls:
        raise HTTPException(
            status_code=400,
            detail="أضف رابطًا رسميًا كاملًا يبدأ بـ https:// قبل النشر",
        )

    invalid_urls = [
        url for url in urls
        if not valid_http_url(url) or urlparse(url).scheme.lower() != "https"
    ]
    if invalid_urls:
        raise HTTPException(
            status_code=400,
            detail="كل روابط المصادر يجب أن تكون روابط HTTPS صالحة",
        )


def validate_service_for_publish(service):
    required = {
        "authority": "الجهة المسؤولة",
        "eligibility": "شروط الاستفادة",
        "documents": "المستندات أو توضيح أن المتطلبات تختلف حسب الحالة",
        "steps": "خطوات الحصول على الخدمة",
    }
    missing = [label for field, label in required.items() if not str(getattr(service, field, "") or "").strip()]
    if missing:
        raise HTTPException(
            status_code=400,
            detail="لا يمكن نشر الخدمة قبل استكمال: " + "، ".join(missing),
        )
    validate_official_source(service.official_source)


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
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "X-Admin-Token", "Authorization"],
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



# =====================================
# حسابات مستخدمي سَنَد والمفضلة المتزامنة
# =====================================

AUTH_COOKIE_NAME = "sanad_session"
AUTH_SESSION_DAYS = 30


def user_to_dict(user):
    return {
        "id": user.id,
        "display_name": user.display_name,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


def check_request_origin(request: Request):
    origin = request.headers.get("origin")
    if origin and origin not in allowed_origins:
        raise HTTPException(status_code=403, detail="مصدر الطلب غير مسموح")


def set_auth_cookie(response: Response, token: str):
    secure = os.getenv("SANAD_COOKIE_SECURE", "false").lower() == "true"
    same_site = os.getenv("SANAD_COOKIE_SAMESITE", "lax").lower()
    if same_site not in ("lax", "strict", "none"):
        same_site = "lax"
    if same_site == "none" and not secure:
        raise HTTPException(status_code=500, detail="إعدادات ملفات تعريف الارتباط غير آمنة")
    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=token,
        max_age=AUTH_SESSION_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=secure,
        samesite=same_site,
        path="/",
    )


def find_auth_session(request: Request, db: Session):
    token = request.cookies.get(AUTH_COOKIE_NAME)
    if not token:
        return None, None
    session = db.query(AuthSession).filter(
        AuthSession.token_hash == hash_session_token(token),
        AuthSession.revoked_at.is_(None),
    ).first()
    if not session:
        return None, None
    expires_at = session.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at <= datetime.now(timezone.utc):
        return None, None
    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        return None, None
    return session, user


def get_current_user(request: Request, db: Session = Depends(get_db)):
    _, user = find_auth_session(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="سجّل الدخول للمتابعة")
    return user


def create_auth_session(user: User, db: Session, response: Response):
    token = new_session_token()
    session = AuthSession(
        user_id=user.id,
        token_hash=hash_session_token(token),
        expires_at=datetime.now(timezone.utc) + timedelta(days=AUTH_SESSION_DAYS),
    )
    db.add(session)
    db.commit()
    set_auth_cookie(response, token)


@app.post("/auth/register", status_code=201)
def register_account(data: AuthRegister, request: Request, response: Response, db: Session = Depends(get_db)):
    check_request_origin(request)
    email = data.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="البريد الإلكتروني مسجل بالفعل")
    user = User(
        email=email,
        display_name=data.display_name,
        password_hash=hash_password(data.password),
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        create_auth_session(user, db, response)
        return {"user": user_to_dict(user)}
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="تعذر إنشاء الحساب حاليًا")


@app.post("/auth/login")
def login_account(data: AuthLogin, request: Request, response: Response, db: Session = Depends(get_db)):
    check_request_origin(request)
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="البريد الإلكتروني أو كلمة المرور غير صحيحة")
    try:
        create_auth_session(user, db, response)
        return {"user": user_to_dict(user)}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="تعذر تسجيل الدخول حاليًا")


@app.get("/auth/me")
def current_account(user: User = Depends(get_current_user)):
    return {"user": user_to_dict(user)}


@app.post("/auth/logout")
def logout_account(request: Request, response: Response, db: Session = Depends(get_db)):
    check_request_origin(request)
    session, _ = find_auth_session(request, db)
    if session:
        session.revoked_at = datetime.now(timezone.utc)
        db.commit()
    response.delete_cookie(
        key=AUTH_COOKIE_NAME,
        path="/",
        httponly=True,
        secure=os.getenv("SANAD_COOKIE_SECURE", "false").lower() == "true",
        samesite=os.getenv("SANAD_COOKIE_SAMESITE", "lax").lower(),
    )
    return {"message": "تم تسجيل الخروج"}


@app.get("/me/favorites")
def get_account_favorites(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.query(UserFavorite.service_id).filter(UserFavorite.user_id == user.id).all()
    return {"service_ids": [row[0] for row in rows]}


@app.put("/me/favorites")
def sync_account_favorites(data: FavoriteSync, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    check_request_origin(request)
    service_ids = sorted(set(data.service_ids))
    if service_ids:
        valid_count = db.query(Service).filter(
            Service.id.in_(service_ids),
            Service.status == "published",
        ).count()
        if valid_count != len(service_ids):
            raise HTTPException(status_code=400, detail="تتضمن المفضلة خدمة غير منشورة أو غير موجودة")
    try:
        db.query(UserFavorite).filter(UserFavorite.user_id == user.id).delete(synchronize_session=False)
        db.add_all([UserFavorite(user_id=user.id, service_id=service_id) for service_id in service_ids])
        db.commit()
        return {"service_ids": service_ids, "total": len(service_ids)}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="تعذرت مزامنة المفضلة")



def normalize_search_text(value: str | None) -> str:
    return normalize_arabic_text(value)


def search_score(service, normalized_query: str) -> int:
    name = normalize_search_text(service.name)
    description = normalize_search_text(service.description)
    authority = normalize_search_text(service.authority)
    eligibility = normalize_search_text(service.eligibility)
    documents = normalize_search_text(service.documents)
    steps = normalize_search_text(service.steps)
    searchable = f"{name} {description} {authority} {eligibility} {documents} {steps}"

    score = 100 if normalized_query in name else (45 if normalized_query in searchable else 0)
    query_words = normalized_query.split()
    matched_words = 0
    candidates = [part for part in searchable.split() if len(part) >= 3]

    for word in query_words:
        if len(word) < 2:
            continue
        if word in name:
            score += 24
            matched_words += 1
        elif word in searchable:
            score += 10
            matched_words += 1
        elif len(word) >= 3 and any(
            SequenceMatcher(None, word, part).ratio() >= 0.82
            for part in candidates
        ):
            score += 5
            matched_words += 1

    meaningful_words = [word for word in query_words if len(word) >= 2]
    if meaningful_words and matched_words == len(meaningful_words):
        score += 12
    return score


# عرض الخدمات المنشورة مع بحث عربي فوري ونتائج مرتبة حسب الصلة
@app.get("/services")
def get_services(
    category: str | None = None,
    q: str | None = None,
    authority: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Service).filter(Service.status == "published")
    if category:
        query = query.filter(Service.category.ilike(category.strip()))
    if authority:
        query = query.filter(Service.authority.ilike(f"%{authority.strip()}%"))

    services = query.order_by(Service.id).all()
    normalized_query = normalize_search_text(q)

    if normalized_query:
        ranked = [
            (search_score(service, normalized_query), service)
            for service in services
        ]
        ranked = [(score, service) for score, service in ranked if score > 0]
        ranked.sort(key=lambda item: (-item[0], item[1].id))
        services = [service for _, service in ranked]

    return {
        "services": [service_to_dict(service) for service in services],
        "total": len(services),
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
# بلاغات مراجعة معلومات الخدمات
# =====================================

def report_to_dict(report):
    return {
        "id": report.id,
        "service_id": report.service_id,
        "kind": report.kind,
        "message": report.message,
        "status": report.status,
        "created_at": report.created_at.isoformat() if report.created_at else None,
    }


@app.post("/reports", status_code=201)
def create_service_report(
    report_data: ServiceReportCreate,
    db: Session = Depends(get_db),
):
    if report_data.service_id is not None:
        service = db.query(Service).filter(
            Service.id == report_data.service_id,
            Service.status == "published",
        ).first()
        if not service:
            raise HTTPException(status_code=404, detail="الخدمة غير موجودة أو غير منشورة")

    report = ServiceReport(
        service_id=report_data.service_id,
        kind=report_data.kind,
        message=report_data.message,
        status="new",
    )
    try:
        db.add(report)
        db.commit()
        db.refresh(report)
        return {"message": "تم استلام البلاغ للمراجعة. شكرًا لمساعدتك.", "report_id": report.id}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="تعذر إرسال البلاغ حاليًا")


@app.get("/admin/reports")
def get_service_reports(
    db: Session = Depends(get_db),
    admin: bool = Depends(verify_admin_token),
):
    reports = db.query(ServiceReport).order_by(ServiceReport.id.desc()).limit(100).all()
    return {"reports": [report_to_dict(report) for report in reports]}


@app.patch("/admin/reports/{report_id}")
def update_service_report(
    report_id: int,
    status_data: ServiceReportStatusUpdate,
    db: Session = Depends(get_db),
    admin: bool = Depends(verify_admin_token),
):
    report = db.query(ServiceReport).filter(ServiceReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="البلاغ غير موجود")
    report.status = status_data.status
    db.commit()
    db.refresh(report)
    return report_to_dict(report)


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

    validate_service_for_publish(service)

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
