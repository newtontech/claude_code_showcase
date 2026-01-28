import random

def guess_number():
    number = random.randint(1, 100)
    attempts = 0
    print("欢迎来到猜数字游戏！我已经想好了一个1到100之间的数字。")
    while True:
        try:
            guess = int(input("请输入你的猜测: "))
            attempts += 1
            if guess < number:
                print("太小了！再试一次。")
            elif guess > number:
                print("太大了！再试一次。")
            else:
                print(f"恭喜你！你猜对了数字 {number}，用了 {attempts} 次尝试。")
                break
        except ValueError:
            print("请输入一个有效的整数！")

if __name__ == "__main__":
    guess_number()
