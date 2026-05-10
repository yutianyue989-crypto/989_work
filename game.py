import random
import sys


"""
一个简单的终端小游戏合集
包含：
1. 猜数字
2. 掷骰子对战
3. 简易冒险

运行：python game.py
"""

def clear():
    print("\n" * 50)


def menu():
    print("=== 终端小游戏 ===")
    print("1. 猜数字")
    print("2. 掷骰子对战")
    print("3. 简易冒险")
    print("4. 退出")


def guess_number():
    clear()
    print("🎯 猜数字游戏")
    target = random.randint(1, 100)
    attempts = 0

    while True:
        try:
            guess = int(input("猜一个1-100的数字: "))
            attempts += 1

            if guess < target:
                print("太小了")
            elif guess > target:
                print("太大了")
            else:
                print(f"🎉 猜对了！用了 {attempts} 次")
                break
        except ValueError:
            print("请输入数字")

    input("回车返回菜单")


def dice_battle():
    clear()
    print("🎲 掷骰子对战")

    player = 0
    computer = 0

    for i in range(3):
        input("回车掷骰子")
        p = random.randint(1, 6)
        c = random.randint(1, 6)

        print(f"你掷出了 {p}, 电脑掷出了 {c}")
        player += p
        computer += c

    print(f"最终比分: 你 {player} : 电脑 {computer}")

    if player > computer:
        print("你赢了 🎉")
    elif player < computer:
        print("你输了 💀")
    else:
        print("平局 🤝")

    input("回车返回菜单")


def adventure():
    clear()
    print("🗡️ 简易冒险游戏")

    hp = 10

    print("你进入了地牢...")

    while hp > 0:
        print(f"当前血量: {hp}")
        print("1. 前进")
        print("2. 休息")
        print("3. 退出")

        choice = input("> ")

        if choice == "1":
            event = random.choice(["怪物", "宝箱", "空"])

            if event == "怪物":
                dmg = random.randint(1, 4)
                hp -= dmg
                print(f"你遇到怪物，受伤 {dmg} 点")

            elif event == "宝箱":
                heal = random.randint(1, 3)
                hp += heal
                print(f"你找到药水，恢复 {heal} 点")

            else:
                print("什么都没有发生")

        elif choice == "2":
            hp += 2
            print("你休息了一下，恢复2点")

        elif choice == "3":
            break

        else:
            print("无效输入")

        if hp <= 0:
            print("你死了 💀")
            break

    input("回车返回菜单")


def main():
    while True:
        clear()
        menu()
        choice = input("选择: ")

        if choice == "1":
            guess_number()
        elif choice == "2":
            dice_battle()
        elif choice == "3":
            adventure()
        elif choice == "4":
            print("再见 👋")
            sys.exit()
        else:
            print("无效选择")


if __name__ == "__main__":
    main()
