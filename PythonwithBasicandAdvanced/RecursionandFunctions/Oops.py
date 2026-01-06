# class student:
#     name="vishal"
#     age=22
#     cgpa=8.5
#     address="clement town,dehradun"
    
# s1=student()
# print(s1.name,s1.age,s1.cgpa,s1.address)





class car:
    color="red"
    company="bmw"
    price=1000000
    

factories=car()
print(factories.color,factories.company,factories.price)






# contructor in python
#  all classes have function called init_(),which is always executed when the classes bign initiated

# creating the classes with contructor


class phone:
    def __init__(self):
        print("Adding new phone in Database.....")
        pass
        # above contructor in default 
        
        
        # paramterized contructor
    def __init__(self,brand,price):
        self.brand=brand
        self.price=price
        
p1=phone("apple",100000)
p2=phone("samsung",200000)

print(p1.brand,p1.price)
print(p2.brand,p2.price)




# class and instances attributes


private attributes and methods in python


class Person:
    # a private methods
    __name="vishal"
    
    def __hello(self):
        print("hello ")
    def Welcome(self):
        self.__hello()
        # print("welcome to our app")
        
p1=Person()
p1.Welcome()













                        #    ___inheritance___
                        
#   single inheritance example                      
      
                        
class Car:
    @staticmethod 
    def Start():
        print("Car is started")
        
    @staticmethod
    def Stop():
        print("Car is stopped")
    
    
    
    
class Tayota(Car):
    def __init__(self,color,company,price):
        self.color=color
        self.company=company
        self.price=price
        
car1=Tayota("red","bmw",1000000)
print(car1.color,car1.company,car1.price)
car1.Start()
car1.Stop()


types of inheritance

1.single inheritance
2.multiple inheritance
3.multilevel inheritance
4.hierarchical inheritance
5.hybrid inheritance


# exmaple of mutililevel inheritance


class A:
    var1="vishal bhai"
class B(A):
    var2="Ankit bhai"
class C(A,B):
    var3="Anupam bhai"

C1=C()
print(C1.var1,C1.var2,C1.var3)




# Polymorphism is an example of a function with the same name but different implementation

# example of polymorphism
# with Addition and you practise many more with other operator loading



class Complex:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def ShowNumber(self):
        print(f"{self.a} + {self.b}i")

    def __add__(self, other):
        return Complex(self.a + other.a, self.b + other.b)

num1 = Complex(1, 2)
num1.ShowNumber()
num2 = Complex(3, 4)
num2.ShowNumber()
print("-----------------")
num3 = num1.__add__(num2)
num3.ShowNumber()


# super keywords example
class Vehicle:
    def __init__(self, brand, price):
        self.brand = brand
        self.price = price

    def ShowVehicle(self):
        print(self.brand, self.price)

class Car(Vehicle):
    def __init__(self, brand, price, color):
        super().__init__(brand, price)
        # it will caled the parent class constructor
        self.color = color

    def ShowCar(self):
        print(self.brand, self.price, self.color)


car1 = Car("bmw", 1000000, "red")
car1.ShowVehicle()
car1.ShowCar()

