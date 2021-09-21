from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        to_do = todo(title=title, desc=desc)
        db.session.add(to_do)
        db.session.commit()
    allTodo = todo.query.all()
    return render_template('index.html', allTodo=allTodo)


@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        task = todo.query.filter_by(sno=sno).first()
        task.title = title
        task.desc = desc
        db.session.add(task)
        db.session.commit()
        return redirect("/")
    to_update = todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=to_update)


@app.route("/delete/<int:sno>")
def delete(sno):
    to_delete = todo.query.filter_by(sno=sno).first()
    db.session.delete(to_delete)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)