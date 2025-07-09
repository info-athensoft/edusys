from app.dao.base_dao import BaseDAO
from app.models.student_profile import StudentProfile
from app.utils.db_utils import DBUtils
from app.utils.student_utils import StudentUtils
from app.enums.enrollment_status import EnrollmentStatus
from app.enums.guardian_status import GuardianStatus
from app.enums.profile_status import ProfileStatus

class StudentProfileDAO(BaseDAO):

    def __init__(self):
        super().__init__("student_profile")

    def get_student_by_id(self, student_id: int) -> StudentProfile | None:
        result = self.get_rows_by_column_value(student_id, "student_id")
        if result:
            return self.build_entity_object(result[0])
        return None

    def get_student_by_email(self, email: str) -> StudentProfile | None:
        result = self.get_rows_by_column_value(email, "email_address")
        if result:
            return self.build_entity_object(result[0])
        return None

    def get_max_student_id(self):
        return self.get_max_element_in_column("student_id")

    def create_student_profile(self, student_profile: StudentProfile):
        new_student_id = StudentUtils.generate_unique_student_id()
        query = """
        INSERT INTO student_profile 
        (student_id, first_name, middle_name, last_name, birth_date, phone_number, email_address, home_address, registration_date, enrollment_status, guardian_status, profile_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            new_student_id,
            student_profile.get_first_name(),
            student_profile.get_middle_name(),
            student_profile.get_last_name(),
            student_profile.get_birth_date(),
            student_profile.get_phone_number(),
            student_profile.get_email_address(),
            student_profile.get_home_address(),
            student_profile.get_registration_date(),
            student_profile.get_enrollment_status().value,
            student_profile.get_guardian_status().value,
            student_profile.get_profile_status().value
        )
        connection = None
        cursor = None
        try:
            connection = DBUtils().get_connection()
            cursor = connection.cursor()
            cursor.execute(query, values)
            connection.commit()
            return cursor.lastrowid
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def read_student_profiles(self, filter_column=None, filter_value=None):
        query = "SELECT * FROM student_profile"
        connection = None
        cursor = None
        try:
            connection = DBUtils().get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            students = cursor.fetchall()

            for student in students:
                student["enrollment_status"] = EnrollmentStatus(student["enrollment_status"]).name.title()
                student["guardian_status"] = GuardianStatus(student["guardian_status"]).name.title().replace("_", " ")
                student["profile_status"] = ProfileStatus(student["profile_status"]).name.title()

            if filter_column and filter_value:
                filter_value_lower = filter_value.lower()
                students = [
                    student for student in students
                    if filter_column in student and filter_value_lower in str(student[filter_column]).lower()
                ]

            return students

        except Exception as e:
            return f"Error fetching students: {e}"

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def update_student_profile(self, student_profile: StudentProfile):
        query = """
        UPDATE student_profile SET
            first_name = %s,
            middle_name = %s,
            last_name = %s,
            birth_date = %s,
            phone_number = %s,
            email_address = %s,
            home_address = %s,
            registration_date = %s,
            enrollment_status = %s,
            guardian_status = %s,
            profile_status = %s
        WHERE student_id = %s
        """
        values = (
            student_profile.get_first_name(),
            student_profile.get_middle_name(),
            student_profile.get_last_name(),
            student_profile.get_birth_date(),
            student_profile.get_phone_number(),
            student_profile.get_email_address(),
            student_profile.get_home_address(),
            student_profile.get_registration_date(),
            student_profile.get_enrollment_status().value,
            student_profile.get_guardian_status().value,
            student_profile.get_profile_status().value,
            student_profile.get_student_id()
        )
        connection = None
        cursor = None
        try:
            connection = DBUtils().get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, values)
            connection.commit()
            if cursor.rowcount == 0:
                raise ValueError(f"Student ID {student_profile.get_student_id()} does not exist in the database.")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def build_entity_object(row: dict) -> StudentProfile:
        return StudentProfile(
            student_id=row['student_id'],
            first_name=row['first_name'],
            middle_name=row['middle_name'],
            last_name=row['last_name'],
            birth_date=row['birth_date'],
            phone_number=row['phone_number'],
            email_address=row['email_address'],
            home_address=row['home_address'],
            registration_date=row['registration_date'],
            enrollment_status=EnrollmentStatus(row['enrollment_status']),
            guardian_status=GuardianStatus(row['guardian_status']),
            profile_status=ProfileStatus(row['profile_status'])
        )
