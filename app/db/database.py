import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

Base = declarative_base()

logger.info("Initializing database engine...")
database_url = os.environ.get("DATABASE_URL")
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(e)
        raise e
    finally:
        db.close()
