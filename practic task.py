class Animal:
    kind = "warm-blooded"
    counter = 0
    
    def __init__(self, name, speed):
        self.__name = name  #зммінна стала приватною
        self.speed = speed
        Animal.counter += 1
        Animal.__printAmount(self.__name)  #використання статичного методу
        
    def __del__(self):
        Animal.counter -= 1
        print("Now ", Animal.counter, " animals left")
        
    def sayHello(self):
        print("Hello, I am ", self.__name, ", my speed is ", self.speed)
        
    def speedUp(self, delta):
        self.speed = self.speed + delta
        
    def speedDown(self, delta):
        if (self.speed >= delta):
            self.speed = self.speed - delta
            
    def stop(self):
        self.speed = 0
        
    def getName(self):
        return self.__name
        
    def __sayPrivate(self):  #приватний метод
        print("This is private method")

    @staticmethod
    def __printAmount(startMess):
        print(startMess, ": now ", Animal.counter, " animals exist")

#створення екземплярів класу
an1 = Animal("Kitty", 1)
an2 = Animal("Puppy", 2)
an3 = Animal("Big dog", 5)

#виклик методів екземплярів класу
an3.sayHello()
an3.speedUp(20)
an3.speedDown(15)
an3.sayHello()

an2.stop()
an2.sayHello()

print(an1.getName())
print(an1.counter) 

#спроба викликати приватний метод
try:
    an1.__sayPrivate()
except AttributeError:
    print("Неможливо викликати приватний метод ззовні класу")

#виведення параметрів екземпляра класу
print(an1.__dict__)

#видалення екземплярів класу
del an1
del an2
del an3

