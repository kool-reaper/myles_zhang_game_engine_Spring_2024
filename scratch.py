# This file was created by the one and only Myles Zhang

# Wrife a function that takes two arguments and multiplies them together
# Use a return statement
# Print is

# Write another function that converts the return from the first to a string and prints it out

# Write a while loop that uses both functions a finite number of times

i = 0

def myFunction(x, y):
    result = x*y
    return result

def printmyfunction(input):
    print(str(input))

while i < 10:
    i += 1
    printmyfunction(myFunction(3, 5))
