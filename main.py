from flask import Flask, render_template
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

from db.db_commands import get_data

app = Flask(__name__)

# Настройки
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245w'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test:test@localhost:5433/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)

# Инспектор создан для проверки наличия таблицы в БД, используется в строке 49
inspector = inspect(db.engine)


# БД
class DataTable(db.Model):
    __tablename__ = 'data_table'
    id = db.Column(db.Integer, primary_key=True)
    rep_dt = db.Column(db.Date, nullable=False)
    delta = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'id: {self.id}, rep_dt: {self.rep_dt}, delta: {self.delta}'


# Представления
@app.route('/')
def index():
    """
    Главная страница с кнопкой 'Получить данные из файла'
    """
    return render_template('index.html')


@app.route('/import/xlsx/')
def import_xlsx():
    """
    Функция имортирует данные из .xlsx файла, после чего проверяет существует ли таблица в БД,
    если существует - очищает, если нет - создает. Полученные из файла данные построчно записываются в БД
    :return: рендер полученных данных из файла .xlsx в шаблон 'data_in_db.html
    """
    data = get_data()
    has_table = inspector.has_table('data_table')
    if has_table:
        DataTable.query.delete()
    else:
        db.create_all()
    for dt in data:
        row = DataTable(rep_dt=dt[0], delta=dt[1])
        db.session.add(row)
    db.session.commit()
    context = DataTable.query.order_by(DataTable.rep_dt)
    return render_template('data_in_db.html', context=context)


from resource import DataListResourceSql, DataListResourcePandas

api.add_resource(DataListResourceSql, '/export/sql/')
api.add_resource(DataListResourcePandas, '/export/pandas/')

if __name__ == '__main__':
    app.run(debug=True)
