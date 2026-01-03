# count=1
# while count<=6:
#     print("count")
#     count=count+1
# print("while loop ended")

i=5
while i>=1:
    print(i)
    i-=1
    
print("while loop ended")




# first question is done using by mine own mind logic



counter=0
while counter<=100:
    print(counter)
    counter+=1;
    
print("while loop ended")



# next question print number from 100 to 1;

i=100
while i>=1:
    print(i)
    i-=1
    


# for the mutliplw of an table by using the input from the User


n=int(input("Enter The Number:"))

i=1
while(i<=10):
    print(n*i)
    i+=1
    
    
# for printing the indexing of an Squeare numbers

list=[1,4,9,16,25,36,49,64,81,100]


idx=0
while idx <len(list):
    print(list[idx])
    idx+=1;










list=(1,4,9,16,25,36,49,64,81,100)

x=81
i=0
while i<len(list):
    if(list[i]==x):
        print("Element FOund on the Index:",i)
        break
    else:
        print("Element Not Found")
    i+=1
    
    
    
# for Continue

i=1
while i<=10:
    if(i%2==0):
        i+=1
        continue
    print(i)
    i+=1
    