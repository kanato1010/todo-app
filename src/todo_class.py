import json
import time  #time.sleep使うため, エラー処理exceptのみで使用
from typing import List  #型ヒントでList使うためにtypingっていうモジュールから導入
from enum import Enum  #優先度設定のための列挙型導入、タイポ防止
from datetime import date  #日付のやつ、deadline実装のため

class Priority(Enum):  #優先度設定のためのclass、タイポ防止のためクラスにした
    HIGH = "★★★"
    MEDIUM = " ★★"
    LOW = "  ★"
    EMPTY = "   "

class TodoItem:
    def __init__(self, task: str, done: bool = False, priority: Priority = None, deadline: date = None) -> None:
        self.task = task
        self.done = done
        self.priority = priority
        self.deadline = deadline
    def toggle(self) -> None:  #完了と未完了を取り替え
        self.done = not self.done
    def to_dict(self) -> dict:
        return {"task" : self.task, "done" : self.done, "priority" : self.priority.value if self.priority else None, "deadline" : self.deadline.isoformat() if self.deadline else None}  #isoformatはdate型を文字列にする
    @classmethod
    def from_dict(cls, d: dict) -> "TodoItem":  # JSONから読み込んだdictをインスタンスに変換
        priority = Priority(d["priority"]) if d["priority"] else None  #文字列★からクラスPriority.LOWに変換してpriorityに格納
        deadline = date.fromisoformat(d["deadline"]) if d["deadline"] else None  #文字列(isoformat)からdateに変換してdeadlineへ格納
        return cls(d["task"], d["done"], priority, deadline)

try:
    todos: List["TodoItem"] = []
    with open("todos.json", "r") as f:
        loaded_todos = json.load(f)
        for x in loaded_todos:
            todos.append(TodoItem.from_dict(x))

except FileNotFoundError:
    todos = []

def display() -> int:

    print("")
    print("↓現在のリスト")

    for x,todo in enumerate(todos):
        #優先度表示のためのif
        if todo.priority == None:
            priority = Priority.EMPTY
        else:
            priority = todo.priority
        #締め切り表示のためのif
        if todo.deadline == None:
            deadline = ""
        else:
            deadline = "(〆" + str(todo.deadline) + ")"

        if todos[x].done == True:
            print(priority.value, x+1, ":", "✅", todo.task, deadline)
        else:
            print(priority.value, x+1, ":", " ▢", todo.task, deadline)

    print("")
    print("操作を選択してください")
    print("1:タスクを追加, 2:タスクを削除, 3:完了, 4:優先度設定, 5:締切設定, 0:セッションを終了")
    choice = int(input("数字を入力 : "))
    return choice

def todo_add(new_task: str) -> None:
    todos.append(TodoItem(new_task))

def todo_remove(remove_number: int) -> None:
    todos.pop(remove_number-1)

def get_len(d: "TodoItem"):
    p = d.priority.value if d.priority else ""
    return p.count("★")

#main----------------------------------
while True:
    try:
        choice = display()
        if choice == 0:  #セッション終了
            break

        if choice == 1:  #タスク追加
            new_task = input("追加するタスクを入力してください : ")
            todo_add(new_task)

        elif choice == 2:  #タスク削除
            remove_number = int(input("削除するタスクを入力してください : "))
            if remove_number < 1 or remove_number > len(todos):
                raise IndexError
            todo_remove(remove_number)

        elif choice == 3:  #完了, 取り消し
            number = int(input("完了するタスク番号を入力してください : "))
            if number < 1 or number > len(todos):
                raise IndexError
            todos[number-1].toggle()

        elif choice == 4:  #priorityの追加
            number = int(input("優先度を追加するタスクを選択してください : "))
            if number < 1 or number > len(todos):
                raise IndexError
            print("")
            print("1:優先度高め, 2:優先度中, 3:優先度低め")
            pri = int(input("優先度を選択してください : "))
            if pri == 1:
                priority = Priority.HIGH
            elif pri == 2:
                priority = Priority.MEDIUM
            elif pri == 3:
                priority = Priority.LOW
            else:
                raise ValueError
            todos[number-1].priority = priority
            todos.sort(key=get_len, reverse=True)  #優先度順に並び替え

        elif choice == 5:  #締め切りの設定
            number = int(input("締切を追加するタスクを選択してください : "))
            if number < 1 or number > len(todos):
                raise IndexError
            print("締め切りを設定します")
            year = int(input("年 : "))
            month = int(input("月 : "))
            day = int(input("日 : "))
            todos[number-1].deadline = date(year, month, day)

        with open("todos.json", "w") as f:
            saved_todos = []
            for x in todos:
                saved_todos.append(x.to_dict())
            json.dump(saved_todos, f, ensure_ascii=False, indent=2)

    except (ValueError, IndexError):
        print("")
        print("！！！！！！！！エラー！！！！！！！！")
        print("！！！！入力が正しくありません！！！！")
        time.sleep(3)