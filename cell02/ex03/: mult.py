first_number = float(input("Enter the first number: "))
second_number = float(input("Enter the second number: "))
result = first_number * second_number
print(f"{first_number} x {second_number} = {result}")
if result > 0:
    print("The result is positive.")
elif result < 0:
    print("The result is negative.")
else:
    print("The result is both positive and negative.")