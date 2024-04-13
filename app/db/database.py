from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from shared.logger import get_logger


logger = get_logger(__name__)

SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/dbname"

logger.info("Initializing database engine...")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


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
