# .......................задание 1............................................
# создание файла базы данных с именем файла базы данных todo.db

from sqlalchemy import create_engine

engine = create_engine('sqlite:///todo.db?check_same_thread=False')


# .......................задание 2 ............................................
# Cоздайте таблицу в этой базе данных. Имя таблицы должно быть task.
#   В табличной задаче должны быть следующие столбцы:
#       1.Целочисленный столбец с именем id. Это должен быть первичный ключ.
#       2.Строковый столбец с именем task.
#       3.Столбец даты с названием крайний срок. По умолчанию в нем должна быть указана дата создания задачи. Вы можете использовать метод datetime.today ().


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'  # Имя таблицы должно быть task
    id = Column(Integer, primary_key=True)  # id - целочисленный столбец таблицы; primary_key=True говорит, что этот столбец является первичным ключом.
    task = Column(String)  # task - это строковый столбец;
    deadline = Column(Date, default=datetime.today())  # deadline - это столбец, в котором хранится дата. SQLAlchemy автоматически преобразует дату SQL в объект date и времени Python.

    def __repr__(self):
        return self.task
# .......................задание 3 ............................................
# Также нужно реализовать меню, которое сделает вашу программу более удобной. В меню должны быть следующие пункты:
#       1.Today's tasks(Сегодняшние задачи_. Распечатывает все задачи на сегодня.
#       2.Add task(Добавить задачу). Запрашивает описание задачи и сохраняет его в базе данных.
#       3.Exit (Выход).


# После того, как мы описали нашу таблицу, самое время создать ее в нашей базе данных. Все, что нам нужно, это вызвать метод create_all () и передать ему движок:
Base.metadata.create_all(engine)
# Этот метод создает таблицу в нашей базе данных путем генерации SQL-запросов в соответствии с описанными нами моделями.
# Теперь мы можем получить доступ к базе данных и хранить в ней данные. Для доступа к базе данных нам нужно создать сеанс:

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# Чтобы создать строку в нашей таблице, вам необходимо создать объект класса модели и передать его методу add ():

# new_row = Table(task='This is string field!', deadline=datetime.strptime('01-24-2020', '%m-%d-%Y').date())
# session.add(new_row)
# session.commit()


rows = session.query(Table).all()  # Метод all () возвращает все строки из таблицы в виде списка Python.

# Вы можете получить доступ к полям строк по их именам:
#if len(rows) > 0:
#    first_row = rows[0]  # Если список строк не пустой


# print(first_row.deadline)  # Распечатает значение deadline
# print(first_row.id)  # Напечатает идентификатор строки.
# print(first_row)  # Распечатает строку, возвращенную методом __repr__, a именно task

status = True
while status:
    act = input("\n1) Today's tasks\n2) Add task\n0) Exit\n")
    if act == "0":
        status = False
        print("Bye!")
    elif act == "2":
        add_task =input("Enter task")

        new_row = Table(task=add_task, deadline=datetime.now().date())
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    elif act == "1":
        print("Today:")
        rows = session.query(Table).all()
        print(len(rows))
        for row in rows:
            # Если список строк не пустой
            print(str(row.id) + ".", row)  # Распечатает строку, возвращенную методом __repr__, a именно task

        if len(rows) == 0:
            print("Nothing to do!")
