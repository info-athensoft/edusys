import pytest
import mysql.connector
from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables from .env_test
dotenv_path = Path(__file__).resolve().parent.parent / ".env_test"
load_dotenv(dotenv_path=dotenv_path)

@pytest.fixture(scope="session")
def db_connection():
    """Provides a DB connection for all tests in the session."""
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    yield connection
    connection.close()


@pytest.fixture(autouse=True)
def reset_database(db_connection):
    """Reset the DB state before each test."""
    cursor = db_connection.cursor()

    # Read and execute each SQL statement individually (no multi=True)
    with open('tests/sql_tests/create_tables.sql', 'r') as f:
        sql_script = f.read()
        statements = sql_script.split(';')
        for statement in statements:
            stmt = statement.strip()
            if stmt:
                try:
                    cursor.execute(stmt)
                except mysql.connector.Error as err:
                    print(f"Error executing statement: {stmt}\n{err}")
                    raise

    # Insert initial data
    cursor.execute("""
        INSERT INTO course_profile(course_name, course_code, course_desc, target_audience, duration_in_weeks,
                                   credit_hours, profile_status)
        VALUES ('Introduction to Computer Science', 'COMP 250', 'Searching/sorting algorithms, data structures', 2, 15, 3.0, 1),
               ('Theory of Computation', 'COMP 330', NULL, 2, 12, 3.0, 1),
               ('Sampling Theory and Applications', 'MATH 525', 'Horvitz-Thompson estimator', 1, 10, 3.0, 1)
    """)

    cursor.execute("""
        INSERT INTO student_profile(student_id, first_name, middle_name, last_name, birth_date, phone_number,
                                    email_address, home_address, registration_date, enrollment_status,
                                    guardian_status, profile_status)
        VALUES ('2025050001', 'Daniel', 'Ziyang', 'Luo', '1998-12-10', '5141234567', 'daniel.luo@mail.mcgill.ca', '123 rue Street', '2025-03-27', 1, 0, 1),
               ('2025050002', 'Brian', 'Harold', 'May', '1947-07-19', '4381234567', 'brianmay@gmail.com', '1975 rue Queen', '2024-10-31', 0, 0, 0),
               ('2025050003', 'Farrokh', '', 'Bulsara', '1946-09-05', '4501234567', 'freddiemercury@gmail.com', '1975 rue Bohemian', '2024-01-31', 1, 1, 1)
    """)

    db_connection.commit()
    cursor.close()