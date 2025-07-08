import re


class StudentValidator:
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_age(age: int) -> bool:
        return isinstance(age, int) and 1 <= age <= 150

    @staticmethod
    def validate_name(name: str) -> bool:
        return isinstance(name, str) and len(name.strip()) > 0

    @staticmethod
    def validate_student_data(data: dict) -> tuple[bool, str]:
        if not isinstance(data, dict):
            return False, "Invalid data format"

        # Check required fields
        required_fields = ['name', 'age', 'email']
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"

        # Validate name
        if not StudentValidator.validate_name(data['name']):
            return False, "Name must be a non-empty string"

        # Validate age
        if not StudentValidator.validate_age(data['age']):
            return False, "Age must be an integer between 1 and 150"

        # Validate email
        if not StudentValidator.validate_email(data['email']):
            return False, "Invalid email format"

        return True, "Valid"
