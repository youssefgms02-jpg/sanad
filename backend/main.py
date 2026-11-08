from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SANAD API",
    description="منصة سَنَد للخدمات والمعلومات المصرية",
    version="1.0.0",
)

# بيانات تجريبية فقط؛ يجب استبدالها بمعلومات موثقة من مصادر رسمية قبل النشر.
services = [
    {
        "id": 1,
        "name": "خدمة حكومية تجريبية",
        "description": "وصف توضيحي لخدمة حكومية.",
        "category": "government",
        "authority": "لم تُحدد بعد",
        "eligibility": "لم تُحدد بعد",
        "documents": "لم تُحدد بعد",
        "steps": "لم تُحدد بعد",
    },
    {
        "id": 2,
        "name": "خدمة تعليمية تجريبية",
        "description": "وصف توضيحي لخدمة تعليمية.",
        "category": "education",
        "authority": "لم تُحدد بعد",
        "eligibility": "لم تُحدد بعد",
        "documents": "لم تُحدد بعد",
        "steps": "لم تُحدد بعد",
    },
    {
        "id": 3,
        "name": "خدمة دعم تجريبية",
        "description": "وصف توضيحي لخدمة الدعم.",
        "category": "support",
        "authority": "لم تُحدد بعد",
        "eligibility": "لم تُحدد بعد",
        "documents": "لم تُحدد بعد",
        "steps": "لم تُحدد بعد",
    },
    {
        "id": 4,
        "name": "خدمة لذوي الإعاقة وكبار السن",
        "description": "وصف توضيحي للخدمة.",
        "category": "accessibility",
        "authority": "لم تُحدد بعد",
        "eligibility": "لم تُحدد بعد",
        "documents": "لم تُحدد بعد",
        "steps": "لم تُحدد بعد",
    },
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "أهلاً بيك في سَنَد",
        "status": "API is running",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/services")
def get_services(category: str | None = None):
    if category:
        filtered_services = [
            service for service in services
            if service["category"].lower() == category.lower()
        ]
    else:
        filtered_services = services

    return {"services": filtered_services}


@app.get("/services/{service_id}")
def get_service(service_id: int):
    for service in services:
        if service["id"] == service_id:
            return service

    raise HTTPException(
        status_code=404,
        detail="الخدمة غير موجودة",
    )
