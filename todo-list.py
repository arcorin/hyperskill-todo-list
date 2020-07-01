# Work on project To-Do List. Stage 4/4: Bye, completed task
# https://hyperskill.org/projects/105/stages/571/implement

from sqlalchemy import create_engine

# create database file
# - use the create_engine() method
""" # - todo.db is the database file name """
# check_same_thread=False argument allows connecting to the database from another thread
engine = create_engine('sqlite:///todo.db?check_same_thread=False')


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

# create a model class that describes the table in the database
# all model classes should inherit from the DeclarativeMeta class
# DeclarativeMeta class is returned by declarative_base()
Base = declarative_base()

# Table:
# - name of the model class
# - used to access data from the table it describes
class Table(Base):
    # specifies the table name in the database:
    __tablename__ = "task"

    # define the columns in the table:
    id = Column(Integer, primary_key=True)
    task = Column(String, default="default_value")

    # column that stores the date
    # SQLAlchmey automatically converts SQL date into a Python datetime object
    deadline = Column(Date, default=datetime.today())

    # returns a string representation of the class object
    # ORM concept: each row in the table is an object of a class
    def __repr__(self):
        return self.string_field


# create table in the database:
# call create_all() method and pass engine to it:
# (creates table in the database by generating SQL queries according to the models described)
Base.metadata.create_all(engine)


from sqlalchemy.orm import sessionmaker

# access the database and store data in it:
# create a session to access database
Session = sessionmaker(bind=engine)

# session object is the only thing needed to manage the database
# create session object:
session = Session()

from datetime import datetime, timedelta

today = datetime.today()
# today_day = datetime.strptime('2020-24-04, %Y-%d-%m)')
today_month = today.strftime('%b')
today_day = today.strftime('%d')
# select all rows from Table where the date column equals today's date
rows = session.query(Table).filter(Table.deadline == today).all()


# 1) Prints all tasks for today
def today_tasks():
    print(f"Today {today_day} {today_month}:")
    rows = session.query(Table).filter(Table.deadline == today).all()
    if rows == []:
        print("Nothing to do!")
    for x in rows:
        print(x.task)
    print()

    main()


# 2) Prints all tasks for 7 days from today
def week_tasks():
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for n in range(7):
        day = datetime.today().date() + timedelta(days=n)
        print(weekdays[day.weekday() % 7], day.day, day.strftime('%b') + ":")

        rows = session.query(Table).filter(Table.deadline == day).all()
        if rows == []:
            print("Nothing to do!")
        for x in range(len(rows)):
            print(f"{x + 1}. {rows[x].task}")
        print()

    print()

    main()

# 3) Prints all tasks sorted by deadline
def all_tasks():
    print("All tasks:")
    rows = session.query(Table).order_by(Table.deadline).all()
    if rows == []:
        print("Nothing to do!")
    for x in range(len(rows)):
        print(f"{x + 1}. {rows[x].task}. {rows[x].deadline.day} {rows[x].deadline.strftime('%b')}")
    print()

    main()


# 4) Missed tasks: print the tasks ordered by the deadline date
def missed_tasks():
    print("Missed tasks:")
    rows = session.query(Table).filter(Table.deadline < datetime.today() - timedelta(days=1)).all()

    if rows == []:
        print("Nothing is missed!")

    for x in range(len(rows)):
        print(f"{x + 1}. {rows[x].task}. {rows[x].deadline.day} {rows[x].deadline.strftime('%b')}")
    print()

    main()


# 5) Add task : Asks for task description and saves it in the database
def add_task():
    print("Enter task")
    user_task = input()
    print("Enter deadline")
    user_deadline = datetime.strptime(input(), '%Y-%m-%d')

    new_row = Table(task=user_task,
                    deadline=user_deadline)
    session.add(new_row)
    session.commit()
    print("The task has been added!")
    print()

    main()


# 6) Delete task: print all the tasks sorted by the deadline and ...
# ... ask to enter the number of the task to delete
def delete_task():
    print("Choose the number of the task you want to delete:")
    rows = session.query(Table).order_by(Table.deadline).all()

    if rows == []:
        print("Nothing to delete!")

    for x in range(len(rows)):
        print(f"{x + 1}. {rows[x].task}. {rows[x].deadline.day} {rows[x].deadline.strftime('%b')}")

    task_to_delete = int(input()) - 1
    session.delete(rows[task_to_delete])
    session.commit()

    print("The task has been deleted!")
    print()

    main()


# A: first function to execute
def main():
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")

    choice = input()

    if choice == "0":
        print("\nBye!")
        exit()

    if choice == "1":
        today_tasks()

    if choice == "2":
        week_tasks()

    if choice == "3":
        all_tasks()

    if choice == "4":
        missed_tasks()

    if choice == "5":
        add_task()

    if choice == "6":
        delete_task()

    main()

main()
