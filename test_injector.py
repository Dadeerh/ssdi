from .Injector import Injector
import abc
import pytest


class A(abc.ABC):
    def __init__(self):
        print("A init")
    
    def foo(self):
        print("A foo")

class B(A):
    def __init__(self):
        print("B init")
    
    def foo(self):
        print("B foo")

class C(A):
    def __init__(self):
        print("C init")
    
    def foo(self):
        print("C foo")

class D(B,C):
    def __init__(self):
        print("D init")
    
    def bar(self):
        print("D bar")

class E():
    def __init__(self, cls_b_or_c: A):
        self.cls_b_or_c = cls_b_or_c
    
    def foo(self):
        print("E foo")
        self.cls_b_or_c.foo()

class BaseClass():
    def __init__(self):
        print("Baseclass init")
    
    def foo(self):
        print("Baseclass foo")

class ChildClass(BaseClass):
    def __init__(self):
        print("Childclass init")
    
    def foo(self):
        print("Childclass foo")

class DepChildClass():
    def __init__(self, bc:BaseClass):
        self.bc = bc
    
    def foo(self):
        print("Depchildclass foo")
        self.bc.foo()

class DepChildClassNoAnnotation():
    def __init__(self, bc):
        self.bc = bc
    
    def foo(self):
        print("DepChildClassNoAnnotation foo")
        self.bc.foo()

class ChildClassWithParameters(BaseClass):
    def __init__(self, a:int,b:int,c:int,param:str=""):
        print(f"{a}{b}{c}{param}")
        
class AnotherChildClassWithParameters(BaseClass):
    # Note: classes to be used with Injector must be positional (for now)
    def __init__(self, a:int,b:int ,c:int, bc:BaseClass=None,param:str=""):
        bc.foo()
        print(f"{a}{b}{c}{param}")


class SomeClass():
    def __init__(self,bc:ChildClassWithParameters=None):
        print("SomeClass init")


def singleton(cls):
    obj = cls()
    # Always return the same object
    cls.__new__ = staticmethod(lambda cls: obj)
    # Disable __init__
    try:
        del cls.__init__
    except AttributeError:
        pass
    return cls

@singleton
class Singleton():
    pass


def test_truth():
    assert A is A

def test_instance_get(capsys):
    injector = Injector()
    injector.add(A)

    a_obj = injector.get(A)

    assert isinstance(a_obj, A)
    a_obj.foo()
    captured = capsys.readouterr()
    assert captured.out == "A init\nA foo\n"

def test_instance_get_with_dependency_and_abc(capsys):
    injector = Injector()
    injector.add(E)
    injector.add(C)
    e_obj = injector.get(E)
    assert isinstance(e_obj, E)

    e_obj.foo()
    capture = capsys.readouterr()
    assert capture.out == "C init\nE foo\nC foo\n"

def test_instance_get_with_dependency(capsys):
    injector = Injector()
    injector.add(DepChildClass)
    injector.add(ChildClass)
    e_obj = injector.get(DepChildClass)
    assert isinstance(e_obj, DepChildClass)

    e_obj.foo()
    capture = capsys.readouterr()
    assert capture.out == "Childclass init\nDepchildclass foo\nChildclass foo\n"

def test_instance_get_with_dependency_without_annotation(capsys):
    injector = Injector()
    injector.add(DepChildClassNoAnnotation)
    injector.add(ChildClass)
    with pytest.raises(Exception):
        injector.get(DepChildClassNoAnnotation)

def test_instance_get_with_dependency_missing(capsys):
    injector = Injector()
    injector.add(DepChildClass)
    with pytest.raises(Exception):
        injector.get(DepChildClass)

def test_instance_get_with_variables(capsys):
    injector = Injector()
    injector.add(ChildClassWithParameters, 1,2,3,param="123")
    injector.get(ChildClassWithParameters)
    capture = capsys.readouterr()
    assert capture.out == "123123\n"


def test_instance_get_with_dependency_variables(capsys):
    injector = Injector()
    injector.add(ChildClassWithParameters, 1,2,3,param="123")
    injector.add(DepChildClass)
    dcc = injector.get(DepChildClass)
    dcc.foo()

    capture = capsys.readouterr()
    assert capture.out == "123123\nDepchildclass foo\nBaseclass foo\n"

def test_instance_get_with_dependency_variables_and_class(capsys):
    injector = Injector()
    injector.add(ChildClassWithParameters, 1,2,3,param="123")
    injector.add(AnotherChildClassWithParameters, 1,2,3,param="123")
    dcc = injector.get(AnotherChildClassWithParameters)

    capture = capsys.readouterr()
    assert capture.out == "123123\nBaseclass foo\n123123\n"

def test_singleton():
    s1 = Singleton()
    s2 = Singleton()

    assert s1 is s2

def test_singleton_2():
    s1 = Singleton()
    s1.counter = 0
    s1.counter += 1

    s2 = Singleton()
    s2.counter += 1

    assert s1.counter == 2
    assert s2.counter == 2


def test_singleton_di():
    injector = Injector()
    injector.add(Singleton)

    s1 = injector.get(Singleton)
    s2 = injector.get(Singleton)

    assert s1 is s2