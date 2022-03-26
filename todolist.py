# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta

# Create engine
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


# Create task Table
class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def new_session(self, engine):
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def todo_menu(self, menu_option):
        if menu_option == 'main':
            print(
                '',
                '1) Today\'s tasks',
                '2) Week\'s tasks',
                '3) All tasks',
                '4) Missed tasks',
                '5) Add a task',
                '6) Delete a task',
                '0) Exit',
                '',
                sep='\n'
            )
            menu_option = int(input())
            return menu_option
        elif menu_option == 'menu_new':
            print('\nEnter task')
            task_input = input()
            print('\nEnter a deadline')
            dateline_input = input()
            return [task_input, datetime.strptime(dateline_input, '%Y-%m-%d')]

    def today_task(self):
        today = datetime.today().strftime('%Y-%m-%d')
        all_tasks = self.session.query(Table).filter(Table.deadline == today)
        if all_tasks.count() > 0:
            print('Today:')
            for tsk in all_tasks:
                print(tsk.task)
        else:
            print(
                'Today:',
                'Nothing to do!',
                sep='\n'
            )

    def week_task(self):
        today = datetime.today()
        for day in range(7):
            current_day = today + timedelta(day)
            current_day_tasks = self.session.query(Table).filter(Table.deadline == current_day.strftime('%Y-%m-%d'))
            print(f'\n{current_day.strftime("%A %d %b")}')
            task_count = 1
            if current_day_tasks.count() > 0:
                for tsk in current_day_tasks:
                    print(
                        f'{task_count}. {tsk.task}'
                    )
                    task_count += 1
            else:
                print('Nothing to do!')

    def all_task(self):
        all_tasks = self.session.query(Table).order_by(Table.deadline)
        if all_tasks.count() > 0:
            task_count = 1
            print('\nAll tasks:')
            for tsk in all_tasks:
                print(f'{task_count}. {tsk.task}. {tsk.deadline.strftime("%d %b")}')
                task_count += 1
        else:
            print(
                '',
                'Nothing to do!',
                sep='\n'
            )

    def missed_task(self):
        rows = self.session.query(Table). \
            filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
        print('\nMissed tasks:')
        if len(rows) > 0:
            row_number = 1
            for row in rows:
                print(f'{row_number}) {row.task} {row.deadline.strftime("%d %b")}')
                row_number += 1
        else:
            print('All tasks have been completed!')

    def add_task(self, new_task, task_deadline=datetime.today()):
        new_task = new_task
        task_deadline = task_deadline
        new_row = Table(
            task=new_task,
            deadline=task_deadline.date()
        )
        self.session.add(new_row)
        self.session.commit()

    def delete_task(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print('\nChoose the number of the task you want to delete:')
        if len(rows) > 0:
            row_number = 1
            for row in rows:
                print(f'{row_number}) {row.task} {row.deadline.strftime("%d %b")}')
                row_number += 1
            self.session.delete(rows[int(input()) - 1])
            self.session.commit()
            print('The task has been deleted!')
        else:
            print('Nothing to delete')

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

# Start Session
todo_list = Table()
todo_list.new_session(engine)

# Run todo list menu option
option = todo_list.todo_menu('main')
while option > 0:
    if option == 1:
        todo_list.today_task()
    elif option == 2:
        todo_list.week_task()
    elif option == 3:
        todo_list.all_task()
    elif option == 4:
        todo_list.missed_task()
    elif option == 5:
        task = todo_list.todo_menu('menu_new')
        todo_list.add_task(task[0], task[1])
        print('The task has been added!\n')
    elif option == 6:
        todo_list.delete_task()
    elif option == 0:
        option = 0
        break
    option = todo_list.todo_menu('main')

print('Bye!')