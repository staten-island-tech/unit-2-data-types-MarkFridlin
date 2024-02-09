""" name = input('What is your name?\n')
print(f'Hello {name}')
 """
while True:
    CBT = input('What is your cost before tip?')
    CBTf = float(CBT) 
    print(f'Your total cost is: {round(CBTf * 1.2, 2)}')