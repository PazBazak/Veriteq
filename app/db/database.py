from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker
from utils.config import read_config
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

logger.info("Initializing database engine")
database_url = (
    f"postgresql://"
    f"{read_config('database', 'username')}:{read_config('database', 'password')}@"
    f"{read_config('database', 'host')}/{read_config('database', 'database_name')}"
)
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
