from sqlalchemy import Column, Integer, String, Date, Boolean, Enum, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class GenderEnum(enum.Enum):
    MALE = "Чоловік"
    FEMALE = "Жінка"

class DocumentTypeEnum(enum.Enum):
    PASSPORT = "passport"
    ID_CARD = "id_card"

class ReligionEnum(enum.Enum):
    NONE = "Не вибрано"
    CHRISTIANITY = "Християнство"
    ISLAM = "Іслам"
    JUDAISM = "Юдаїзм"
    BUDDHISM = "Буддизм"
    HINDUISM = "Індуїзм"
    OTHER = "Інше"

class Candidate(Base):
    __tablename__ = 'candidates'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Основна інформація (обов'язкові поля)
    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    tax_number = Column(String(10), nullable=False)
    
    # Основна інформація (необов'язкові поля)
    middle_name = Column(String(100), nullable=True)
    birth_date = Column(Date, nullable=True)
    birth_place = Column(String(200), nullable=True)
    gender = Column(Enum(GenderEnum), nullable=True)
    
    # Документи (необов'язкові поля)
    document_type = Column(Enum(DocumentTypeEnum), nullable=True)
    passport_series = Column(String(2), nullable=True)
    passport_number = Column(String(6), nullable=True)
    passport_issued_by = Column(String(200), nullable=True)
    passport_issue_date = Column(Date, nullable=True)
    id_card_number = Column(String(9), nullable=True)
    id_card_issue_date = Column(Date, nullable=True)
    id_card_issued_by = Column(String(200), nullable=True)
    
    # Адреси (необов'язкові поля)
    registration_address = Column(Text, nullable=True)
    actual_address = Column(Text, nullable=True)
    
    # Контактна інформація (необов'язкові поля)
    email = Column(String(150), nullable=True)
    
    # Додаткова інформація (необов'язкові поля)
    nationality = Column(String(50), nullable=True)
    citizenship = Column(String(50), nullable=True)
    religion_forbids_weapons = Column(Boolean, nullable=True)
    religion = Column(Enum(ReligionEnum), nullable=True)
    alternative_religion = Column(String(50), nullable=True)
    vpo_status = Column(String(200), nullable=True)
    bank_name = Column(String(100), nullable=True)
    iban = Column(String(29), nullable=True)
    has_credit = Column(Boolean, nullable=True)
    driver_license = Column(String(100), nullable=True)
    personal_vehicle = Column(String(200), nullable=True)
    extreme_driving_experience = Column(Boolean, nullable=True)
    
    # Фото (необов'язкове поле)
    photo_path = Column(String(500), nullable=True)

class Phone(Base):
    __tablename__ = 'phones'
    
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, nullable=False)
    phone_number = Column(String(20), nullable=True)
    phone_type = Column(String(20), default="personal", nullable=True)