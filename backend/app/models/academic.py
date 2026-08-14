from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    years = relationship(
        "Year",
        back_populates="program",
        cascade="all, delete-orphan"
    )


class Year(Base):
    __tablename__ = "years"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)

    program = relationship("Program", back_populates="years")

    semesters = relationship(
        "Semester",
        back_populates="year",
        cascade="all, delete-orphan"
    )


class Semester(Base):
    __tablename__ = "semesters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    year_id = Column(Integer, ForeignKey("years.id"), nullable=False)

    year = relationship("Year", back_populates="semesters")

    branches = relationship(
        "Branch",
        back_populates="semester",
        cascade="all, delete-orphan"
    )


class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=False)

    semester = relationship("Semester", back_populates="branches")

    subjects = relationship(
        "Subject",
        back_populates="branch",
        cascade="all, delete-orphan"
    )


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False)

    branch = relationship("Branch", back_populates="subjects")

    documents = relationship(
        "Document",
        back_populates="subject",
        cascade="all, delete-orphan"
    )


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)

    subject = relationship("Subject", back_populates="documents")