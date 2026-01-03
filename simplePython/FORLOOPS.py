# for loop in python 
#  it used for the sequesntial iteration of condition

array=[1,2,3,4,5,6,7,8,9,10]
x=7
i=0
for i in array:
    if(i==x):
        print("Element Found on the Index:",i)
        break
    else:
        print("Element Not Found")
    i+=1
    
# fruits=["apple","banana","cherry"]
# for i in fruits:
#     print(i)
    
    

# range in for loop

# number=range(10)
# for i in number:
#     print(i)
    

# more example of it for using range function

# for j in range(2,4,13):
#     print(j)


# for i in range(1,101,2):
#     print(i)
    
    
    
# n=int(input("Enter the Number"))

# for i in range(1,11):
#     print(n*i)
    

# factorial find question

n=int(input("Enter the Number"))
fact=1
for i in range(1,n+1):
    fact*=(i)
print(fact)


