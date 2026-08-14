from app.database.database import SessionLocal
from app.models.academic import Program, Year, Semester, Branch, Subject


def seed_database():
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_program = db.query(Program).first()

        if existing_program:
            print("Database already contains academic data.")
            return

        # Program
        btech = Program(
            name="B.Tech"
        )
        db.add(btech)
        db.flush()

        # Years
        year1 = Year(name="Year 1", program_id=btech.id)
        year2 = Year(name="Year 2", program_id=btech.id)
        year3 = Year(name="Year 3", program_id=btech.id)
        year4 = Year(name="Year 4", program_id=btech.id)

        db.add_all([year1, year2, year3, year4])
        db.flush()

        # Semesters
        semesters = [
            Semester(name="Semester 1", year_id=year1.id),
            Semester(name="Semester 2", year_id=year1.id),
            Semester(name="Semester 3", year_id=year2.id),
            Semester(name="Semester 4", year_id=year2.id),
            Semester(name="Semester 5", year_id=year3.id),
            Semester(name="Semester 6", year_id=year3.id),
            Semester(name="Semester 7", year_id=year4.id),
            Semester(name="Semester 8", year_id=year4.id),
        ]

        db.add_all(semesters)
        db.flush()

        # Example branch
        aiml_branch = Branch(
            name="Artificial Intelligence and Machine Learning",
            semester_id=semesters[4].id
        )

        db.add(aiml_branch)
        db.flush()

        # Example subjects
        subjects = [
            Subject(
                name="Deep Learning",
                code="DL",
                branch_id=aiml_branch.id
            ),
            Subject(
                name="Machine Learning",
                code="ML",
                branch_id=aiml_branch.id
            ),
            Subject(
                name="Natural Language Processing",
                code="NLP",
                branch_id=aiml_branch.id
            ),
        ]

        db.add_all(subjects)

        db.commit()

        print("Academic data seeded successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()