from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, List, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
import time
from datetime import datetime

from app.services.llm_service import llm_service
from app.services.reference_range_service import reference_range_service
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

# Pydantic modelleri
class TestResult(BaseModel):
    test_name: str
    value: float
    unit: str
    reference_range: Optional[str] = None
    status: Optional[str] = None  # normal, high, low, critical

class PatientInfo(BaseModel):
    age: int
    gender: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    medical_history: List[str] = []
    current_medications: List[str] = []
    allergies: List[str] = []

class BloodTestRequest(BaseModel):
    test_results: List[TestResult]
    patient_info: PatientInfo
    symptoms: Optional[List[str]] = []
    previous_results: Optional[List[TestResult]] = []

class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    results: Dict
    created_at: str

class ReferenceRangeResponse(BaseModel):
    test_name: str
    reference_range: Dict
    evaluation: Dict

@router.post("/analyze/blood-test", response_model=AnalysisResponse)
async def analyze_blood_test(
    request: BloodTestRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """
    Kan tahlili sonuçlarını AI ile analiz eder
    """
    try:
        logger.info(f"Kan tahlili analizi başlatıldı - Kullanıcı: {current_user.id}")
        
        # Test sonuçlarını dict formatına çevir
        test_results = [result.dict() for result in request.test_results]
        patient_info = request.patient_info.dict()
        
        # LLM analizi yap
        analysis_result = await llm_service.analyze_blood_test(
            test_results=test_results,
            patient_info=patient_info
        )
        
        # Background task olarak veritabanına kaydet
        background_tasks.add_task(
            save_analysis_to_db,
            user_id=current_user.id,
            analysis_result=analysis_result,
            test_data={"test_results": test_results, "patient_info": patient_info}
        )
        
        return AnalysisResponse(
            analysis_id=f"analysis_{current_user.id}_{int(time.time())}",
            status="completed",
            results=analysis_result,
            created_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Kan tahlili analizi hatası: {e}")
        raise HTTPException(status_code=500, detail="Analiz sırasında bir hata oluştu")

@router.post("/analyze/risk-assessment", response_model=Dict)
async def assess_health_risks(
    request: BloodTestRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Sağlık risklerini değerlendirir
    """
    try:
        logger.info(f"Risk değerlendirmesi başlatıldı - Kullanıcı: {current_user.id}")
        
        test_results = [result.dict() for result in request.test_results]
        patient_info = request.patient_info.dict()
        
        risk_assessment = await llm_service.assess_health_risks(
            test_results=test_results,
            patient_info=patient_info
        )
        
        return {
            "status": "success",
            "risk_assessment": risk_assessment,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Risk değerlendirmesi hatası: {e}")
        raise HTTPException(status_code=500, detail="Risk değerlendirmesi sırasında bir hata oluştu")

@router.post("/analyze/doctor-insights", response_model=Dict)
async def generate_doctor_insights(
    request: BloodTestRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Doktorlar için klinik değerlendirme desteği
    """
    try:
        logger.info(f"Doktor insights oluşturuluyor - Kullanıcı: {current_user.id}")
        
        test_results = [result.dict() for result in request.test_results]
        patient_info = request.patient_info.dict()
        
        doctor_insights = await llm_service.generate_doctor_insights(
            test_results=test_results,
            symptoms=request.symptoms or [],
            patient_info=patient_info
        )
        
        return {
            "status": "success",
            "doctor_insights": doctor_insights,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Doktor insights hatası: {e}")
        raise HTTPException(status_code=500, detail="Doktor insights oluşturulurken bir hata oluştu")

@router.post("/analyze/patient-education", response_model=Dict)
async def generate_patient_education(
    request: Dict,
    current_user: User = Depends(get_current_user)
):
    """
    Hasta eğitim materyali oluşturur
    """
    try:
        logger.info(f"Hasta eğitimi oluşturuluyor - Kullanıcı: {current_user.id}")
        
        diagnosis = request.get("diagnosis", "")
        treatment_plan = request.get("treatment_plan", {})
        patient_language = request.get("patient_language", "tr")
        
        education_material = await llm_service.generate_patient_education(
            diagnosis=diagnosis,
            treatment_plan=treatment_plan,
            patient_language=patient_language
        )
        
        return {
            "status": "success",
            "education_material": education_material,
            "language": patient_language,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Hasta eğitimi hatası: {e}")
        raise HTTPException(status_code=500, detail="Hasta eğitimi oluşturulurken bir hata oluştu")

@router.get("/analysis/{analysis_id}", response_model=Dict)
async def get_analysis_result(
    analysis_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Daha önce yapılan analiz sonucunu getirir
    """
    try:
        # Veritabanından analiz sonucunu getir
        analysis_result = await get_analysis_from_db(analysis_id, current_user.id)
        
        if not analysis_result:
            raise HTTPException(status_code=404, detail="Analiz sonucu bulunamadı")
        
        return {
            "status": "success",
            "analysis": analysis_result
        }
        
    except Exception as e:
        logger.error(f"Analiz sonucu getirme hatası: {e}")
        raise HTTPException(status_code=500, detail="Analiz sonucu getirilirken bir hata oluştu")

@router.post("/evaluate-test", response_model=ReferenceRangeResponse)
async def evaluate_single_test(
    test_name: str,
    value: float,
    age: int,
    gender: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Tek bir test sonucunu referans aralıklarına göre değerlendirir
    """
    try:
        # Referans aralığını getir
        reference_data = reference_range_service.get_test_reference_range(
            test_name=test_name,
            age=age,
            gender=gender
        )
        
        if not reference_data:
            raise HTTPException(status_code=404, detail=f"Test için referans aralığı bulunamadı: {test_name}")
        
        # Test sonucunu değerlendir
        evaluation = reference_range_service.evaluate_test_result(
            test_name=test_name,
            value=value,
            age=age,
            gender=gender
        )
        
        return ReferenceRangeResponse(
            test_name=test_name,
            reference_range=reference_data,
            evaluation=evaluation
        )
        
    except Exception as e:
        logger.error(f"Test değerlendirme hatası: {e}")
        raise HTTPException(status_code=500, detail="Test değerlendirmesi sırasında bir hata oluştu")

@router.get("/reference-ranges/tests", response_model=List[Dict])
async def get_available_tests():
    """
    Mevcut testleri listeler
    """
    try:
        tests = reference_range_service.get_all_tests()
        return tests
    except Exception as e:
        logger.error(f"Test listesi getirme hatası: {e}")
        raise HTTPException(status_code=500, detail="Test listesi getirilirken bir hata oluştu")

@router.get("/reference-ranges/categories", response_model=List[str])
async def get_test_categories():
    """
    Test kategorilerini listeler
    """
    try:
        categories = list(reference_range_service.reference_data.get('blood_tests', {}).keys())
        return categories
    except Exception as e:
        logger.error(f"Kategori listesi getirme hatası: {e}")
        raise HTTPException(status_code=500, detail="Kategori listesi getirilirken bir hata oluştu")

@router.get("/reference-ranges/category/{category}", response_model=List[Dict])
async def get_tests_by_category(category: str):
    """
    Kategoriye göre testleri listeler
    """
    try:
        tests = reference_range_service.get_tests_by_category(category)
        return tests
    except Exception as e:
        logger.error(f"Kategori testleri getirme hatası: {e}")
        raise HTTPException(status_code=500, detail="Kategori testleri getirilirken bir hata oluştu")

# Helper fonksiyonlar
async def save_analysis_to_db(user_id: int, analysis_result: Dict, test_data: Dict):
    """Analiz sonucunu veritabanına kaydeder"""
    # TODO: Veritabanı kayıt işlemi
    logger.info(f"Analiz sonucu veritabanına kaydedildi - Kullanıcı: {user_id}")

async def get_analysis_from_db(analysis_id: str, user_id: int) -> Optional[Dict]:
    """Veritabanından analiz sonucunu getirir"""
    # TODO: Veritabanı sorgu işlemi
    return None 