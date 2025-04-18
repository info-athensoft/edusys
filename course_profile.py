from audience_type import AudienceType
from profile_status import ProfileStatus

class CourseProfile(object):

    def __init__(self, course_id, course_name, course_code, course_desc,
                 target_audience, duration_in_weeks, credit_hours, profile_status):
        self.__course_id = course_id
        self.__course_name = course_name
        self.__course_code = course_code
        self.__course_desc = course_desc
        if isinstance(target_audience, AudienceType):
            self.__target_audience = target_audience
        else:
            raise Exception("target_audience must be of type AudienceType")
        self.__duration_in_weeks = duration_in_weeks
        self.__credit_hours = credit_hours
        if isinstance(profile_status, ProfileStatus):
            self.__profile_status = profile_status

    def __eq__(self, other):
        if not isinstance(other, CourseProfile):
            return False
        return self.__course_id == other.__course_id

    def __hash__(self):
        return hash((self.__course_id, self.__course_code, self.__course_name))

    def __repr__(self):
        return (f"Course({self.__course_id}), {self.__course_name}, {self.__course_code}, " +
                f"{self.__course_desc}, {self.__target_audience}, {self.__duration_in_weeks}, " +
                f"{self.__credit_hours}, {self.__profile_status})")

    def __str__(self):
        return f"{self.__course_code}: {self.__course_name}"

    def get_name(self):
        return self.__course_name

    def set_name(self, course_name):
        self.__course_name = course_name

    def get_code(self):
        return self.__course_code

    def set_code(self, course_code):
        self.__course_code = course_code

    def get_description(self):
        return self.__course_desc

    def set_description(self, course_desc):
        self.__course_desc = course_desc

    def get_target_audience(self):
        return self.__target_audience

    def set_target_audience(self, target_audience):
        if isinstance(target_audience, AudienceType):
            self.__target_audience = target_audience
        else:
            raise Exception("target_audience must be of type AudienceType")

    def get_duration_in_weeks(self):
        return self.__duration_in_weeks

    def set_duration_in_weeks(self, duration_in_weeks):
        self.__duration_in_weeks = duration_in_weeks

    def get_credits(self):
        return self.__credit_hours

    def set_credits(self, credit_hours):
        self.__credit_hours = credit_hours


if __name__ == '__main__':
    course_1 = CourseProfile(250, "Introduction to Computer Science", "COMP 250", "Stacks, queues, etc.",
                      AudienceType.ADULT, 15, 3.0, ProfileStatus.ACTIVE)
    course_2 = CourseProfile(250, "Introduction to Computer Science", "COMP 250", "Recurrences",
                      AudienceType.YOUTH, 15, 3.0, ProfileStatus.INACTIVE)
    print(course_1.__dict__)
    print(course_1 == course_2)