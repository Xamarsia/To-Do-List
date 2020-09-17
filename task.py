# .......................задание 1............................................
# создание файла базы данных с именем файла базы данных todo.db

from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'  # Имя таблицы должно быть task
    id = Column(Integer,
                primary_key=True)  # id - целочисленный столбец таблицы; primary_key=True говорит, что этот столбец является первичным ключом.
    task = Column(String)  # task - это строковый столбец;
    deadline = Column(Date,
                      default=datetime.today())

    def __repr__(self):
        return self.task


# После того, как мы описали нашу таблицу, самое время создать ее в нашей базе данных. Все, что нам нужно, это вызвать метод create_all () и передать ему движок:
Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


rows = session.query(Table).all()

status = True
while status:
    act = input(
        "\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    if act == "0":
        status = False
        print("\nBye!")

    elif act == "1":
        date_time = datetime.today().date()  # текущая дата без времени
        print(date_time.strftime("\nToday " "%d %b" ":"))
        today = datetime.today()
        rows = session.query(Table).filter(Table.deadline == today.date()).all()  # вибрать все строки по дате
        ro = [i for i in range(1, len(rows) + 1)]
        i = 0
        for row in rows:
            if len(rows) != 0:
                print(str(ro[i]) + ".", row)
                i += 1
        if len(rows) == 0:
            print("Nothing to do!")

    elif act == "2":
        today = datetime.today()
        day = 0
        counter = 0

        while counter < 7:
            today = today + timedelta(days=day)
            rows = session.query(Table).filter(Table.deadline == today.date()).all()  # вибрать все строки по дате
            ro = [i for i in range(1, len(rows) + 1)]
            i = 0
            print()
            print(str(datetime.strftime(today, "%A %d %b")) + ":")
            for row in rows:
                if len(rows) != 0:
                    print(str(ro[i]) + ".", row)
                    i += 1
            if len(rows) == 0:
                print("Nothing to do!")
            day = 1
            counter += 1

    elif act == "3":
        rows = session.query(Table).order_by(Table.deadline).all()
        ro = [i for i in range(1, len(rows) + 1)]
        i = 0
        print("\nAll tasks:")
        for row in rows:
            if len(rows) != 0:
                print(str(ro[i]) + ".", str(row) + ".", datetime.strftime(row.deadline, "%d %b"))
                i += 1

    elif act == "4":
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        today = datetime.today().date()
        ro = [i for i in range(1, len(rows) + 1)]
        i = 0
        print("\nMissed tasks:")
        for row in rows:
            if row.deadline < today:
                if len(rows) != 0:
                    print(str(ro[i]) + ".", str(row) + ".", datetime.strftime(row.deadline, "%d %b"))
                    i += 1
        if len(rows) == 0:
            print("Nothing is missed!")

    elif act == "5":
        add_task = input("\nEnter task")
        deadline = input("Enter deadline")  # 2020-04-28
        new_row = Table(task=add_task, deadline=datetime.strptime(deadline, '%Y-%m-%d'))
        session.add(new_row)
        session.commit()
        print("The task has been added!")

    elif act == "6":
        rows = session.query(Table).order_by(Table.deadline).all()
        ro = [i for i in range(1, len(rows) + 1)]
        i = 0
        print("\nChoose the number of the task you want to delete:")
        for row in rows:
            if len(rows) != 0:
                print(str(ro[i]) + ".", str(row) + ".", datetime.strftime(row.deadline, "%d %b"))
                i += 1
        deleted_task = int(input())
        print(rows[0])
        specific_row = rows[deleted_task - 1]
        session.delete(specific_row)
        session.commit()

        print("The task has been deleted!")
