"""inp = int(input("Enter number of an array >> "))
results = list(range(10))
while inp!=0:
    results[inp]+=1
    inp = int(input("Enter number of an array >> "))"""

inp = input("Enter a sequence of numbers >> ")
inp = ( inp[:(inp.index("0")-1)] ).split(" ")
#cuts last 0 and splits string into list

results = [0]*9

for num in inp:
    results[int(num)-1]+=1

print(*results)