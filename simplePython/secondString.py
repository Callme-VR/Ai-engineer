str1="this is the first string"
str2='this is the second string'
finalstr=str1+"\n" +str2
print (finalstr)
print(len(finalstr))
print(finalstr[3])
str="vishal"
print(str[1:4])
print(str.endswith("l"))
print(str.capitalize())
print(str.find("v"))
print(str.replace("vishal","vishnu"))
print(str.count("v"))


# conditional statements
Age=18
if(Age>=18):
    print("Y C Apply here!")
elif(Age==18):
    print("C Apply here!")
else:
    print("No you canot Apply here!")



# another exmaple of it
light="yellow"
if(light=="red"):
    print("stop")
elif(light=="green"):
    print("go")
elif(light=="yellow"):
    print("wait")
    
print("end of code")


# marks exmaple with grade example

marks=int(input("enter your marks"))

if(marks>=90):
    print("grade A")
elif(marks>=80 and marks<90):
    print("grade B")
elif(marks>=70 and marks<80):
    print("grade c")
elif(marks>=60 and marks<70):
    print("grade d")
elif(marks>=50 and marks<60):
    print("grade e")
    
else:
    print("fail")
    
    
    
    
 # nesting loops
age=int(input("enter your age"))

if(age>=18):
    if(age>=80):
        print("you can vote and also you are senior citizen")
    else:
        print("you can vote")
else:
    print("you cannot vote")
    
    

# practise question with odd and even number




# divisible number program
x=int(input("enter your number"))
if(x%9==0):
    print("divisible")
else:
    print("not divisible")