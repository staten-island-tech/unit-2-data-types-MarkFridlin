import math

def print_factors(x):
   for i in range(1, x + 1):
       if x % i == 0:
           print(i)

num1 = int(input("What is your first number: "))

print_factors(num1)

num2 = int(input("What is your second number: "))

print_factors(num2)

gcf = (math.gcd(num1, num2))

print("The greatest common factor of ", num1 , ' and', num2, "are: ", gcf)

