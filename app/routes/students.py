from flask import request, Blueprint
from threading import Lock
from datetime import datetime
from dataclasses import asdict

from app.routes.utils.student_validator import StudentValidator
from app.routes.utils.responses import error_response, success_response
from app.routes.utils.student import students_data, get_next_id, Student
from app.routes.utils.ollama import OllamaService

students_bp = Blueprint('students', __name__)
students_lock = Lock()


@students_bp.route('/students', methods=["POST"])
def create_student():
    try:
        data = request.get_json()
        if not data:
            return error_response("No data Provided", 400)

        is_valid, error_message = StudentValidator.validate_student_data(data)
        if not is_valid:
            return error_response(error_message, 400)

        with students_lock:
            for student in students_data.values():
                if student["email"] == data["email"]:
                    return error_response("Email already exists", 409)

            student_id = get_next_id()

            student = Student(
                id=student_id,
                name=data['name'].strip(),
                age=data['age'],
                email=data['email'].strip().lower()
            )

            students_data[student_id] = asdict(student)

            return success_response(
                data=students_data[student_id],
                message="Student created successfully",
                status_code=201
            )

    except Exception as e:
        return error_response(str(e), 500)


@students_bp.route('/students', methods=['GET'])
def get_all_students():
    try:
        with students_lock:
            students_list = list(students_data.values())

        return success_response(
            data=students_list,
            message=f"Retrieved {len(students_list)} students"
        )

    except Exception as e:
        return error_response(f"Internal server error: {str(e)}", 500)


@students_bp.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id: int):
    try:
        with students_lock:
            if student_id not in students_data:
                return error_response("Student not found", 404)

            student = students_data[student_id]

        return success_response(data=student)

    except Exception as e:
        return error_response(f"Internal server error: {str(e)}", 500)


@students_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id: int):
    try:
        data = request.get_json()

        if not data:
            return error_response("No data provided")

        with students_lock:
            if student_id not in students_data:
                return error_response("Student not found", 404)

            current_student = students_data[student_id].copy()

            if 'name' in data:
                if not StudentValidator.validate_name(data['name']):
                    return error_response("Name must be a non-empty string")
                current_student['name'] = data['name'].strip()

            if 'age' in data:
                if not StudentValidator.validate_age(data['age']):
                    return error_response("Age must be an integer between 1 and 150")
                current_student['age'] = data['age']

            if 'email' in data:
                if not StudentValidator.validate_email(data['email']):
                    return error_response("Invalid email format")

                email_lower = data['email'].strip().lower()
                for sid, student in students_data.items():
                    if sid != student_id and student['email'] == email_lower:
                        return error_response("Email already exists", 409)

                current_student['email'] = email_lower

            current_student['updated_at'] = datetime.now().isoformat()

            students_data[student_id] = current_student

        return success_response(
            data=students_data[student_id],
            message="Student updated successfully"
        )

    except Exception as e:
        return error_response(f"Internal server error: {str(e)}", 500)


@students_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id: int):
    try:
        with students_lock:
            if student_id not in students_data:
                return error_response("Student not found", 404)

            deleted_student = students_data.pop(student_id)

        return success_response(
            data=deleted_student,
            message="Student deleted successfully"
        )

    except Exception as e:
        return error_response(f"Internal server error: {str(e)}", 500)


@students_bp.route('/students/<int:student_id>/summary', methods=['GET'])
def get_student_summary(student_id: int):
    try:
        with students_lock:
            if student_id not in students_data:
                return error_response("Student not found", 404)

            student = students_data[student_id]

        # Generate summary using Ollama
        summary = OllamaService.generate_student_summary(student)

        return success_response(
            data={
                'student': student,
                'summary': summary,
                'generated_at': datetime.now().isoformat()
            },
            message="Student summary generated successfully"
        )

    except Exception as e:
        return error_response(f"Internal server error: {str(e)}", 500)
