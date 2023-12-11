# OOPs start
# The quantitiy calculate_price in the below example are called methods which are called on the instance of the class.
# The price and quantity are called attributes of the class.
# The class is the blueprint of the object.
# The object is the instance of the class.
# The self is the instance of the class.
# __init__ is called a constructor and has a name which needs to be called by the same name in order to be used.

import csv

class item:
    all =[] # class attribute
    pay_rate = 0.8 # class attribute

    def __init__(self , name: str , price : float, quantity = 0.0 ): # executed when the object is created
        # Run validations to the received arguments

        assert price >=0 , f"Price {price} is not greater than equal to zero"
        assert quantity >=0 , f"Quantity {quantity} is not greater than equal to zero"

        # Assign to self object
        self.name = _name # Added an extra underscore to the name to make it private
        self.price = price
        self.quantity = quantity

        # Actions to execute
        item.all.append(self) # appending the instance to the list
        
    @property # This is sort of a getter method which can be used to get the value of the attribute
    def name(self):
        return self._name # underscore is used to make the attribute private
        # use double underscore to make the attribute private and not accessible outside the class

    @name.setter # This is sort of a setter method which can be used to set the value of the attribute
    def name(self , value):
        if len(value) > 10:
            raise Exception("The name is too long")
        else:
            self._name = value

    def calculate_price(self):
        return self.price * self.quantity
    
    def apply_discount(self):
        self.price = self.price * self.pay_rate # only pay_rate won't work here but item.pay_rate will work (but then wont be able to change 
        # discount for the specific instance.

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.name}" , {self.price} , {self.quantity})' # this is a string representation of the object
        # self.__class__.__name__ --> this will give the name of the class of the object so the item problem in the Phone thing is solved here.

    @classmethod # calls this method before the __init__ method  ; this is allowed using the decorator @classmethod
    def instantiate_from_csv(cls):
        with open('items.csv' , 'r') as f:
            reader = csv.DictReader(f)
            items = list(reader)

        # Iterating over a list of dictionaries
        for item_data in items:
            # print (item)
            item(
                name= item_data.get('name'),
                price= float(item_data.get('price')),
                quantity= float(item_data.get('quantity'))
            )

    @staticmethod 
    def is_integer(num):
        # We will count out the floats that are point zero
        if isinstance(num , float):
            # Count out the floats that are point zero
            return num.is_integer()
        elif isinstance(num , int):
            return True
        else:
            return False
            

# item_1 = item('Pen' , 9 , 3)
# item_2 = item('Pencil' , 5 , 2)

# item_2.has_eraser = True # adding a new attribute to the object
# item_2.pay_rate = 0.7 # changing the class attribute for the specific instance
# print (item.pay_rate == item_2.pay_rate) # Can be accessed both ways ; doesnt need to be passed in compulsorily 

# item_1 first searches the above attribute from the instance level and then the class level.

# print(item.__dict__) # prints the attributes of the class in dictionary format
# print(item_1.__dict__)

# Let us say we have multiple items :
# Now we want sort of a list and we want instance to be appended to it each time we create an object.

# item_a = item('Phone' ,100, 1)
# item_b = item('Laptop' ,1000, 4)
# item_c = item('TV' ,2000, 2)
# item_d = item('Tablet' ,700, 3)
# item_e = item('Headphones' ,100, 6)

# print (item.all) --> Does not represent the object in list well
# so for above we will use __repr__ method

# print (item.all) # with __repr__

# for instance in item.all :
#     print (instance.name)

# Now here we have data and the code in the same .py file and we will look to change that next.

# class method :
# item.instantiate_from_csv() # this is a class method and is called on the class and not on the instance.
# print (item.all)

# print (item.is_integer(5.0)) # static method

# Remember when to use class and when to us static methods!!
# static methods are used when we want to use a method but dont want to pass the instance or the class as an argument (sort of like an outside function).
# class methods are used when we want to use a method but want to pass the class as an argument.
# both of these can be called on an instance as well but this is rarely used.

# Inherited Classes, Parent Classes and Child Classes

class Phone(item): # Phone is the child class and item is the parent class
    # all =[] # Not required as we have already done this in the parent class
    def __init__(self, name : str , price : float, quantity = 0.0 , broken_phones = 0):
        super().__init__(
            name, price, quantity # these are the attributes obtained from the parent class
        )
        self.broken_phones = broken_phones 
        # Phone.all.append(self)  # Not required as we have already done this in the parent class


Phone_1 = Phone("jscPhonev", 100, 1, 2)
# Phone_2 = Phone('jscPhonev2' ,1000, 4 , 1)
# Phone_1.broken_phones = 2
# Phone_2.broken_phones = 1

# can remove the hardcoded broken_phones from above and then copy the whole init from item and and put it in phone along with the broken_phones attribute as additional
# instead of doing this we can use super() method which will call the init method of the parent class and then we can add the additional attribute to the child class.

# print (Phone.all) # This gives the name item(jscphonev.....) as we have not defined the __repr__ method for the child class.
# print (item.all) # This also gives phone(....) now , since the Phone instance creation calls the init from the parent class which appends the instance to the list.
# So Item.all is the list of all the instances of the parent class and the child class.


# Preferably create instances in main.py and keep separate python files for the parent and the child classes.

# ENCAPSULARTION or restriting the users to only reading the attributes and not changing them.

# can basically add the following to allow a new option while printing the name of the instance.
# @property
# def read_only_name(self):
#     return 'AAA'
# so wont be able to change this property now but can change the Phone_1.name property still.

# 4 Key Pillars of OOPs: Encapsulation, Abstraction, Inheritance, Polymorphism