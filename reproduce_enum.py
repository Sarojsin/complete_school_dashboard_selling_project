from sqlalchemy import Column, Integer, Enum as SQLEnum, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import enum

class UserRole(str, enum.Enum):
    PARENT = "parent"

Base = declarative_base()

class User(Base):
    __tablename__ = "users_test"
    id = Column(Integer, primary_key=True)
    role = Column(SQLEnum(UserRole))

# Use sqlite for reproduction if possible, but error was Postgres specific.
# But I can check what value is bound.
engine = create_engine("sqlite:///:memory:", echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

u = User(role=UserRole.PARENT)
session.add(u)
session.commit()
