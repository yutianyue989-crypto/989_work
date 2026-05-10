import random

def game():
    print("🎮 欢迎来到猜数字游戏！")
    print("我已经想好了一个 1 到 1000 的数字")

    number = random.randint(1, 1000)
    attempts = 0

    while True:
        try:
            guess = int(input("请输入你的猜测（1-1000）："))
            attempts += 1

            if guess < 1 or guess > 1000:
                print("⚠️ 请输入 1 到 1000 之间的数字")
                continue

            if guess < number:
                print("📉 太小了！")
            elif guess > number:
                print("📈 太大了！")
            else:
                print(f"🎉 猜对了！答案是 {number}")
                print(f"你一共猜了 {attempts} 次")
                break

        except ValueError:
            print("❗ 请输入有效数字")

def menu():
    while True:
        print("\n====== 猜数字游戏 ======")
        print("1. 开始游戏")
        print("2. 退出")

        choice = input("请选择：")

        if choice == "1":
            game()
        elif choice == "2":
            print("👋 再见！")
            break
        else:
            print("❗ 无效选项")

if __name__ == "__main__":
    menu()