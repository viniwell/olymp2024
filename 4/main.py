def check_if_ideal(num) -> bool:
    #  Checks if a number is an ideal
    sum = 0
    for i in range(1, num):
        if num%i==0:
            sum+=i
    return num==sum

if __name__=="__main__":
    nums=[]
    for i in range(3):
        nums.append(int(input("Input number >> ")))

    for num in nums:
        print(check_if_ideal(num))