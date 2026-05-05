import warnings
from sqlalchemy.exc import SAWarning

def warning_handler(message, category, filename, lineno, file=None, line=None):
    print(f"WARNING: {category.__name__}: {message}")

warnings.showwarning = warning_handler
warnings.simplefilter('always')

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, Session

Base = declarative_base()

class SchoolCourse(Base):
    __tablename__ = 'school_courses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    assignments = relationship("Assignment", cascade="all, delete-orphan")

class Assignment(Base):
    __tablename__ = 'assignments'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    course_id = Column(Integer, ForeignKey('school_courses.id'))
    course = relationship("SchoolCourse")

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
print("Created tables")
