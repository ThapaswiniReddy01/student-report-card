from flask import Flask, render_template, request, redirect, url_for
from models import Student, GradeManager

app = Flask(__name__)
manager = GradeManager()

@app.route('/')
def index():
    return render_template('index.html', students=manager.students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        subjects = {}
        subjects_list = request.form.getlist('subject')
        scores_list = request.form.getlist('score')
        for sub, score in zip(subjects_list, scores_list):
            if sub and score:
                subjects[sub] = float(score)
        student = Student(name, subjects)
        manager.add_student(student)
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/report/<student_id>')
def view_report(student_id):
    student = manager.get_student(student_id)
    if not student:
        return "Student not found", 404
    return render_template('view_report.html', student=student)

@app.route('/delete/<student_id>')
def delete_student(student_id):
    manager.delete_student(student_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)


