from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

class DatabaseManager:
    def __init__(self, database_url="sqlite:///candidates.db"):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def init_db(self):
        Base.metadata.create_all(bind=self.engine)
        print("База даних ініціалізована")
        
    def get_session(self):
        return self.SessionLocal()
    
    def add_candidate(self, candidate_data):
        session = self.get_session()
        try:
            from .models import Candidate, Phone
            
            # Очищаємо пусті значення
            cleaned_data = {}
            for key, value in candidate_data.items():
                if value is not None and value != '':
                    if isinstance(value, str) and value.strip() == '':
                        continue
                    cleaned_data[key] = value
            
            # Створюємо кандидата
            candidate = Candidate(**cleaned_data)
            session.add(candidate)
            session.commit()
            
            # Додаємо телефони (якщо є)
            if 'phones' in cleaned_data:
                for phone_data in cleaned_data['phones']:
                    if phone_data.get('phone_number'):  # Додаємо тільки якщо є номер
                        phone = Phone(candidate_id=candidate.id, **phone_data)
                        session.add(phone)
            
            session.commit()
            return candidate.id
        except Exception as e:
            session.rollback()
            print(f"Помилка при додаванні кандидата: {e}")
            return None
        finally:
            session.close()
    
    def get_all_candidates(self):
        session = self.get_session()
        try:
            from .models import Candidate
            return session.query(Candidate).all()
        except Exception as e:
            print(f"Помилка при отриманні кандидатів: {e}")
            return []
        finally:
            session.close()
    
    def search_candidates(self, search_term):
        session = self.get_session()
        try:
            from .models import Candidate
            if not search_term:
                return self.get_all_candidates()
                
            return session.query(Candidate).filter(
                (Candidate.last_name.ilike(f"%{search_term}%")) |
                (Candidate.first_name.ilike(f"%{search_term}%")) |
                (Candidate.middle_name.ilike(f"%{search_term}%")) |
                (Candidate.tax_number.ilike(f"%{search_term}%")) |
                (Candidate.email.ilike(f"%{search_term}%"))
            ).all()
        except Exception as e:
            print(f"Помилка при пошуку кандидатів: {e}")
            return []
        finally:
            session.close()
    
    def delete_candidate(self, candidate_id):
        session = self.get_session()
        try:
            from .models import Candidate, Phone
            
            # Видаляємо телефони
            session.query(Phone).filter(Phone.candidate_id == candidate_id).delete()
            
            # Видаляємо кандидата
            candidate = session.query(Candidate).filter(Candidate.id == candidate_id).first()
            if candidate:
                session.delete(candidate)
            
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Помилка при видаленні кандидата: {e}")
            return False
        finally:
            session.close()
    
    def get_candidate_by_id(self, candidate_id):
        session = self.get_session()
        try:
            from .models import Candidate, Phone
            candidate = session.query(Candidate).filter(Candidate.id == candidate_id).first()
            if candidate:
                # Завантажуємо телефони кандидата
                phones = session.query(Phone).filter(Phone.candidate_id == candidate_id).all()
                return candidate, phones
            return None, []
        except Exception as e:
            print(f"Помилка при отриманні кандидата: {e}")
            return None, []
        finally:
            session.close()
    
    def update_candidate(self, candidate_id, candidate_data):
        session = self.get_session()
        try:
            from .models import Candidate, Phone
            
            # Оновлюємо дані кандидата
            candidate = session.query(Candidate).filter(Candidate.id == candidate_id).first()
            if candidate:
                for key, value in candidate_data.items():
                    if hasattr(candidate, key) and key != 'id' and key != 'phones':
                        setattr(candidate, key, value)
                
                # Оновлюємо телефони
                if 'phones' in candidate_data:
                    # Видаляємо старі телефони
                    session.query(Phone).filter(Phone.candidate_id == candidate_id).delete()
                    
                    # Додаємо нові телефони
                    for phone_data in candidate_data['phones']:
                        if phone_data.get('phone_number'):
                            phone = Phone(candidate_id=candidate_id, **phone_data)
                            session.add(phone)
                
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Помилка при оновленні кандидата: {e}")
            return False
        finally:
            session.close()