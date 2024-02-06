""" name = input('What is your name?\n')
print(f'Hello {name}')
 """
while True:
    CBT = input('What is your cost before tip?')
    CBTf = float(CBT)
    Service = input('How was the service?') 
    if Service == ('Great'):
        print(f'Your total cost is: {CBTf * 1.25}')
    elif Service == ('Good'):
        print(f'Your total cost is: {CBTf * 1.2}')
    elif Service == ('Okay'):
        print(f'Your total cost is: {CBTf * 1.15}')
    elif Service == ('Bad'):
        print(f'Your total cost is: {CBTf * 1}')
    elif Service == ('great'):
        print(f'Your total cost is: {CBTf * 1.25}')
    elif Service == ('good'):
        print(f'Your total cost is: {CBTf * 1.2}')
    elif Service == ('okay'):
        print(f'Your total cost is: {CBTf * 1.15}')
    elif Service == ('bad'):
        print(f'Your total cost is: {CBTf * 1}')