from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.application.auth.cleanup_tokens_use_case import CleanupTokensUseCase
from app.infrastructure.db.repositories.refresh_token_repository import SqlAlchemyRefreshTokenRepository
import logging
import traceback

from app.core.database import SessionLocal 

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

scheduler = AsyncIOScheduler()

def cleanup_job():
    print("--- INICIANDO CLEANUP JOB ---")
    
    db = SessionLocal() 
    
    try:
        repo = SqlAlchemyRefreshTokenRepository(db)
        use_case = CleanupTokensUseCase(repo)
        
        use_case.execute()
        
        print("---cCLEANUP JOB FINALIZADO CON ÉXITO ---")
    except Exception as e:
        print(f"--- ERROR FATAL EN CLEANUP JOB: {e} ---")
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()
        print("--- DB CERRADA ---")

def start_scheduler():
    scheduler.add_job(cleanup_job, 'interval', hours=24)
    scheduler.start()
    print("--- SCHEDULER INICIADO (esperando el intervalo pactado)---")