# SSDI (Super Simple Dependency Injector)

SSDI is an incredibly simple class that uses Python 3 type annotations to give simple dependency injection.
It provides an injector class that automatically resolves dependencies based on type.
It works with base classes and abstract base classes.

In case of multiple of the same type it will chose the first added type.

It is, as the name indicates, really a very simple injector!

# Requirements
As the class uses type annotations, it is required to use Python 3.x+

There are further requirements to how you code your classes. This will be covered in usage and examples.

# Installation
## pip installation
```
pip install ssdi
```
or
```
python -m pip install ssdi
```

# Usage

There are some simple requirements for using ssdi:

* Type annotations must be used for parameters
* Named parameters given must not be the same name as the classes to be injected
* There cannot be more than one of a type in the injector
    * *truth be told* there can, but then only the first presented class will be used.

Below you see a simple example of using the Injector class.
It is shown that you can pass parameters and named parameters to the classes.

For a more real life example see the *examples* section of this document. 

```python
from ssdi import Injector

class BaseClass():
    def logic(self) -> None:
        print("BaseClass logic")
        pass

class ChildClass(BaseClass):
    def __init__(self, param: int)
        self.param = param

    def logic(self) -> None:
        super().logic()
        print("ChildClass logic: ", self.param)
        pass

class OtherClass():
    def __init__(self, param: int, some_class:  BaseClass, named_param: str = "foo") -> None:
        self.some_class = some_class
        self.param = param
        self.named_param = named_param

    def logic(self) -> None:
        self.some_class.logic()
        print("OtherClass logic: ", self.param, self.named_param)

if __name__ == "__main__":
    injector = Injector()

    injector.add(ChildClass, 123)
    injector.add(OtherClass, 456, named_param="bar")

    other_class = injector.get(OtherClass)
    other_class.logic()
```

gives output:

```
BaseClass logic
ChildClass logic 123
OtherClass logic 456 bar
```

# Examples
## Logging classes

Imagine you have a larger application. For this you have implemented custom logging logic. For this you have a logging object that can be given an instance of various classes. To begin with you just log to stdout using print statements. 

Then after some months you find a need to log to a database. This will require new logic. 
Now instead of replacing all the instances of TestLogger - you instead use SSDI and simply need to replace it once - the place where you have given the injector your class. 
The rest of the class instantiations - all your 100's of classes of business logic - will now automatically be instantiated with the new DatabaseLogger class instead, saving you time and reducing chances of bugs.


First we have our loggers defined:


File *logger.py*
```python
import ABC

class Logger(ABC.abc):
    @abstractmethod
    def log(message: str) -> None:
        """ 
        This functions implementation will log a message
        """
        pass

class TestLogger(Logger):
    def log(message: str) -> None:
        """
        This function logs to a debug interface, f.x. to stdout
        """
        print(message)

class DatabaseLogger(Logger):
    def log(message: str) -> None:
        """
        This function logs to a database
        """
        # Logic to log to database
        pass


```

Then we have all our business logic:

File *business.py*
```python
from logger import Logger

class BusinessLogicOne():
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
    
    def logic(self):
        self.logger.log("Some log message")
        
class BusinessLogicTwo():
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
    
    def logic(self):
        self.logger.log("Some log message")
        
class BusinessLogicN():
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
    
    def logic(self):
        self.logger.log("Some log message")
```

And then finally we have a class that uses SSDI. See here that no matter how many classes uses the logger class instantiation, we still only need to change it one place when we instead implement out database logger. See if you can change the code below to use the new logger - the promise is that it really is *super simple*.

File main.py

```python
from ssdi import Injector

from business import *
from logger import *

if __name__ == "__main__":
    injector = Injector()
    injector.add(BusinessLogicOne)
    injector.add(BusinessLogicTwo)
    injector.add(BusinessLogicN)
    injector.add(TestLogger)

    business_logic_one = injector.get(BusinessLogicOne)
    business_logic_one.logic()
    
    business_logic_two = injector.get(BusinessLogicTwo)
    business_logic_two.logic()
    
    business_logic_n = injector.get(BusinessLogicN)
    business_logic_n.logic()
```


# Tests
Several unit tests have been created. These are created to be tested using pytest. Please see the file test_injector.py on github () for all the tests.

# Contact
Comment on github () or email to dadeerh91@gmail.com