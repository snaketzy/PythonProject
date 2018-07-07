#name = input('what is your name'+'\n')
#print('hello '+name+'!')
#str = "hello world"

def power(x,n):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s
#print(name in str)
print(power(3,10))
input('Press<Enter>')
