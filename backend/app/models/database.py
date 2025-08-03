from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class User(Base):
    """Kullanıcı modeli"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    role = Column(String, default="patient")  # patient, doctor, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # İlişkiler
    patients = relationship("Patient", back_populates="user")
    analyses = relationship("Analysis", back_populates="user")

class Patient(Base):
    """Hasta modeli"""
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    patient_id = Column(String, unique=True, index=True)  # Hastane hasta ID'si
    age = Column(Integer)
    gender = Column(String)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    blood_type = Column(String, nullable=True)
    medical_history = Column(JSON, default=list)
    current_medications = Column(JSON, default=list)
    allergies = Column(JSON, default=list)
    emergency_contact = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # İlişkiler
    user = relationship("User", back_populates="patients")
    test_results = relationship("TestResult", back_populates="patient")
    analyses = relationship("Analysis", back_populates="patient")

class TestResult(Base):
    """Test sonucu modeli"""
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    test_name = Column(String, index=True)
    test_code = Column(String, index=True)  # LOINC kodu
    value = Column(Float)
    unit = Column(String)
    reference_range_min = Column(Float, nullable=True)
    reference_range_max = Column(Float, nullable=True)
    reference_range_text = Column(String, nullable=True)
    status = Column(String)  # normal, high, low, critical
    test_date = Column(DateTime)
    lab_name = Column(String, nullable=True)
    doctor_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # İlişkiler
    patient = relationship("Patient", back_populates="test_results")
    analysis_results = relationship("AnalysisResult", back_populates="test_result")

class Analysis(Base):
    """AI Analiz modeli"""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    analysis_type = Column(String)  # blood_test, risk_assessment, doctor_insights
    status = Column(String, default="pending")  # pending, completed, failed
    input_data = Column(JSON)
    output_data = Column(JSON)
    llm_model_used = Column(String)
    processing_time = Column(Float, nullable=True)  # saniye
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)
    
    # İlişkiler
    user = relationship("User", back_populates="analyses")
    patient = relationship("Patient", back_populates="analyses")
    analysis_results = relationship("AnalysisResult", back_populates="analysis")

class AnalysisResult(Base):
    """Analiz sonuç detayları"""
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"))
    test_result_id = Column(Integer, ForeignKey("test_results.id"), nullable=True)
    result_type = Column(String)  # anomaly, risk, recommendation
    result_data = Column(JSON)
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # İlişkiler
    analysis = relationship("Analysis", back_populates="analysis_results")
    test_result = relationship("TestResult", back_populates="analysis_results")

class DoctorNote(Base):
    """Doktor notları"""
    __tablename__ = "doctor_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("users.id"))
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=True)
    note_type = Column(String)  # diagnosis, treatment, follow_up
    content = Column(Text)
    diagnosis = Column(String, nullable=True)
    treatment_plan = Column(JSON, nullable=True)
    medications = Column(JSON, nullable=True)
    follow_up_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class PatientEducation(Base):
    """Hasta eğitim materyalleri"""
    __tablename__ = "patient_education"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=True)
    education_type = Column(String)  # diagnosis, treatment, lifestyle
    language = Column(String, default="tr")
    content = Column(JSON)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

class AuditLog(Base):
    """Audit log - HIPAA uyumluluğu için"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    action = Column(String)  # view, create, update, delete
    resource_type = Column(String)  # patient, test_result, analysis
    resource_id = Column(Integer, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())

# Enum değerleri için sabitler
class TestStatus:
    NORMAL = "normal"
    HIGH = "high"
    LOW = "low"
    CRITICAL = "critical"

class AnalysisStatus:
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class UserRole:
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"

class AnalysisType:
    BLOOD_TEST = "blood_test"
    RISK_ASSESSMENT = "risk_assessment"
    DOCTOR_INSIGHTS = "doctor_insights"
    PATIENT_EDUCATION = "patient_education" 