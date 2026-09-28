import json
import time  #time.sleep使うため, エラー処理exceptのみで使用

class TodoItem:
    def __init__(self, task, done=False):
        self.task = task
        self.done = done
    def toggle(self):  #完了と未完了を取り替え
        self.done = not self.done
    def to_dict(self):
        return {"task" : self.task, "done" : self.done}
    @classmethod
    def from_dict(cls, d):     # JSONから読み込んだdictをインスタンスに変換
        return cls(d["task"], d["done"])

try:
    todos = []
    with open("todos.json", "r") as f:
        loaded_todos = json.load(f)
        for x in loaded_todos:
            todos.append(TodoItem.from_dict(x))

except FileNotFoundError:
    todos = []

def display():

    print("")
    print("↓現在のリスト")

    for x,y in enumerate(todos):
        if todos[x].done == True:
            print(x+1, ":", "✅", todos[x].task)
        else:
            print(x+1, ":", " ▢", todos[x].task)

    print("")
    print("操作を選択してください")
    print("1:タスクを追加, 2:タスクを削除, 3:完了, 4:セッションを終了")
    choice = int(input("数字を入力 : "))
    return choice

def todo_add(new_task):
    todos.append(TodoItem(new_task))

def todo_remove(remove_number):
    todos.pop(remove_number-1)

#main----------------------------------
while True:
    try:
        choice = display()
        if choice == 4:  #セッション終了
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