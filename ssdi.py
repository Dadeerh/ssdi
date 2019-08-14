
class Injector():
    
    def __init__(self):
        self._classes = {}

    def add(self, cls, *args, **kwargs):
        self._classes[cls.__name__] = {
            "class": cls,
            "args": args,
            "kwargs": kwargs
        }
        pass

    def get(self,cls):
        instantiated_classes = {}
        if hasattr(cls.__init__, "__annotations__"):
            for variable, variable_type in cls.__init__.__annotations__.items():
                for _clsname, _cls_dict in self._classes.items():
                    if self.__is_candidate(_cls_dict["class"], variable_type):
                        instantiated_classes[variable] = self.get(_cls_dict["class"])
                        break

        try:
            return cls(*self._classes[cls.__name__]["args"], **self._classes[cls.__name__]["kwargs"], **instantiated_classes)
        except Exception as e:
            raise Exception(f"Could not instantiate {cls.__name__}. Either dependency is missing, type annotations are not being used, a named parameter was given and could thus not be injected, or needed parameters were missing. Exception: {e}")


    def __is_candidate(self, cls, variable_type):
        if (cls.__name__ == variable_type.__name__) or (issubclass(cls,variable_type)):
            return True
        
        return False