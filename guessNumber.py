import random

number_to_guess = random.randint(1, 6)

attempts = 0

print("欢迎来到猜数字游戏，请猜一个1到6的数字")

while True:
  # 获取用户的猜测
  guess = int(input("请输入您的猜测： "))
  attempts += 1

  # 判断用户的猜测
  if guess < number_to_guess:
    print("太小了，再试一次")
  elif guess > number_to_guess:
    print("太大了，再试一次")
  else:
    print(f"恭喜你，找到了{number_to_guess},总共尝试了{attempts} 次")
    break
