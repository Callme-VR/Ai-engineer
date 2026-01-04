cities=["Delhi","Mumbai","Pune","Bangalore"]
heroes=["ironman","spiderman","captainAmerica"]

def calculate_len(cities,heroes):
    print("Length of cities:",len(cities))
    print("Length of heroes:",len(heroes))
    
calculate_len(cities,heroes) 




def convertDollarto_Inr(dollars):
    inr=dollars*90.01
    print(inr)
    
convertDollarto_Inr(2)






# 
# Recursion is an example of a function calling itself and it is used to solve problems that can be broken down into smaller, similar problems.




def fact(n):
    if(n==0 or n==1):
        return 1
    else:
        return n*fact(n-1)
        
print(fact(5))