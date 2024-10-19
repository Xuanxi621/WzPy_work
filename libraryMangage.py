import time

import pywebio.input
from pywebio import start_server, session
from pywebio.output import put_error, put_markdown, put_tabs, put_table
from pywebio.input import input_group, PASSWORD
import sqlite3

connect = sqlite3.connect("./library.db", check_same_thread=False)
cur = connect.cursor()


def sqlTest():
    # cur.execute("insert into login values(1,'admin','admin123')")
    # cur.execute("insert into books values (2,'Opencv',200,'视觉')")
    cur.execute("select * from books")
    outcome = cur.fetchall()
    print(outcome)
    # for i in list(map(list, outcome)):
    #     print(i)
    connect.commit()


def database():
    cur.execute(
        "create table if not exists books(id integer primary key,book_name TEXT,book_price integer,book_describe TEXT)"
    )

    cur.execute(
        "create table if not exists login(id integer primary key,username TEXT,password TEXT)"
    )


def login():
    put_markdown("# 图书馆管理系统")

    info = input_group("User Login", [
        pywebio.input.input('请输入您的用户名:', name='name'),
        pywebio.input.input('请输入您的密码:', name='password', type=PASSWORD)
    ])
    # print(info['name'], info['password'])

    cur.execute("select * from login where username='%s' and password = '%s'" % (info['name'], info['password']))
    outcome = cur.fetchall()
    if not outcome:
        put_error("您输入的用户或者密码错误")
        time.sleep(1)
        session.run_js('window.location.reload()')
    else:
        cur.execute("select * from books")
        outcome = cur.fetchall()
        outcome_li = list(map(list, outcome))
        outcome_li.insert(0, ['Id', 'Name', 'Price', 'Describe'])
        put_tabs([
            {'title': 'Books', 'content': [
                put_table(outcome_li)
            ]}
        ])


if __name__ == '__main__':
    # database()
    # sqlTest()
    start_server(login, port=8080)
