def print_factors(x):
    factors_list = []
    for i in range(1, x + 1):
       if x % i  == 0:
           factors_list.append(i)
    return factors_list
num1 = int(input("What is your first number: "))
factors_num1 = print_factors(num1)
num2 = int(input("What is your second number: "))
factors_num2 = print_factors(num2)
gcf = 1
for num in factors_num1:
    if num in factors_num2 and gcf < num:
        gcf = num 
print("The greatest common factor of ", num1 , ' and', num2, "are: ", gcf)