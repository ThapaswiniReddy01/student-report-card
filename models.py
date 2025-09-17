import json
import uuid

class Student:
    def __init__(self, name, subjects=None, student_id=None):
        self.id = student_id or str(uuid.uuid4())[:8]
        self.name = name
        self.subjects = subjects or {}

    def add_subject(self, subject, score):
        self.subjects[subject] = score

    def calculate_average(self):
        if not self.subjects:
            return 0
        return sum(self.subjects.values()) / len(self.subjects)

    def get_grade(self):
        avg = self.calculate_average()
        if avg >= 90: return "A"
        elif avg >= 75: return "B"
        elif avg >= 50: return "C"
        else: return "Fail"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "subjects": self.subjects}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["subjects"], data["id"])


class GradeManager:
    def __init__(self, filename="grades.json"):
        self.filename = filename
        self.students = []
        self.load_from_file()

    def add_student(self, student):
        self.students.append(student)
        self.save_to_file()

    def delete_student(self, student_id):
        self.students = [s for s in self.students if s.id != student_id]
        self.save_to_file()

    def get_student(self, student_id):
        return next((s for s in self.students if s.id == student_id), None)

    def save_to_file(self):
        with open(self.filename, "w") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=4)

    def load_from_file(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.students = [Student.from_dict(d) for d in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.students = []
