import json
import time  #time.sleep使うため, エラー処理exceptのみ

try:
    with open("todos.json", "r") as f:
        todos = json.load(f)
except FileNotFoundError:
    todos = []

def display():

    print("")
    print("↓現在のリスト")

    for x,y in enumerate(todos):
        if y["done"] == True:
            print(x+1, ":", "✅", y["task"])
        else:
            print(x+1, ":", " ▢", y["task"])

    print("")
    print("操作を選択してください")
    print("1:タスクを追加, 2:タスクを削除, 3:完了, 4:完了取り消し, 5:セッションを終了")
    choice = int(input("数字を入力 : "))
    return choice

def todo_add(new_task):
    ntask = {"task" : new_task, "done" : False}
    todos.append(ntask)

def todo_remove(remove_task):
    todos.pop(remove_task-1)
#main----------------------------------
while True:
    try:
        choice = display()
        if choice == 5:  #セッション終了
            break

        if choice == 1:  #タスク追加
            new_task = input("追加するタスクを入力してください : ")
            todo_add(new_task)

        elif choice == 2:  #タスク削除
            remove_task = int(input("削除するタスクを入力してください : "))
            if remove_task < 1 or remove_task > len(todos):
                raise IndexError
            todo_remove(remove_task)

        elif choice == 3:  #完了にマーク
            number = int(input("完了するタスク番号を入力してください : "))
            if number < 1 or number > len(todos):
                raise IndexError
            d = todos[number-1]
            d["done"] = True

        elif choice == 4:  #完了取り消し
            number = int(input("完了を取り消しするタスク番号を入力してください : "))
            if number < 1 or number > len(todos):
                raise IndexError
            d = todos[number-1]
            d["done"] = False

        with open("todos.json", "w") as f:
            json.dump(todos, f, ensure_ascii=False, indent=2)

    except (ValueError, IndexError):
        print("")
        print("！！！！！！！！エラー！！！！！！！！")
        print("！！！！入力が正しくありません！！！！")
        time.sleep(3)