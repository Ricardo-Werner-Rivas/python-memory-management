#*===============================================================================================================================
#* LEGEND
#*-------------------------------------------------------------------------------------------------------------------------------
#! Missing
#? Question
#* Section
#^ Important
# Normal comment
#// Alternative or deprecated code
#*===============================================================================================================================

#^ The different types of comments require the "Colorful Comments Refreshed" extension for VSCode to be properly distinguished

#* IMPORTS
# Import "TypeVar" and "Generic"
from typing import TypeVar,Generic
# Import "modules" from "sys" package
from sys import modules
# Import "currentframe" from "inspect" package
from inspect import currentframe

#* MAIN CLASS
# Define the class "Pointer" with generic type
class Pointer(Generic[TypeVar("Any")]):
    """
    Implements pointers in Python for both mutable (though unneded) and non-mutable objects.
    These pointers are completely safe and do not work internally as C's pointers, they are just an imitation of their behaviour.
    
    When a Pointer instance is created, though it stores a value, it "points" to an specific reference, not the value in a memory adress.
    This way, all references pointing to the same non-mutable object don't change when the pointer is updated, avoiding a potential mess.
    
    Non-mutable objects still change their memory adresses when re-referenced but the reference and the value stored in the pointer are forced to share memory adress.
    
    Value and memory adress updates are not made in real-time, but the methods update the non-coincident values:
        * **Getter**: it updates its own value to the variable's one (if variable was given instead of literal).
        * **Setter**: it updates the value of the variable to its own (if variable was given instead of literal).
        * **Deleter**: it also deletes the original variable (if variable was given instead of literal).
    ---
    Attributes:
        value (`Any`, Hidden): Object to point to.
        attr (`str`|`None`, Hidden): Attribute of class instance. Only if `value` is a class instance.
        name (`str`, Hidden): Name of the global variable to which the pointer is pointing.
            Could require an input from the user to introduce the name of the variable if more than one is found.
        vars_dict (`dict[str,Any]`, Hidden): Dictionary of variables.
            `vars(modules["__main__"])` if pointing to a global variable and `inspect.currentframe().f_back.f_locals` if pointing to a local variable.
    ---
    
    ## Methods
        1. **Value getter**: Gets the value.
        2. **Value setter**: Sets a new value.
        3. **Value deleter**: Deletes the value.
        4. **Reference getter**: Gets the pointed reference
        5. **Reference setter**: Changes the pointed reference
    ---
    ## Properties
        :value: *`MethodType`*
        Points to `value` (or `value.attr`). Called through `<instance>.value`. All three possible objects (getter, setter and deleter) have been declared.
        :reference: *`MethodType`*
        Pointed reference. Called through `<instance>.reference`. Deleter **not** defined.
    ---
    
    ## Currently supported
    Both global and local variables can be pointed at.
    
    Literals are **not** supported because of it being useless. If you create a `Pointer` instance for a literal and works,
    keep in mind that it is merely by accident and it is **not** the intended use it was designed for.
    Currently, the only use for inserting a literal instead of a referenced value could be for the class code to display all the references pointing to that literal
    and bind the instance to the desired reference.
    """
    def __init__(self,value=None,reference:str|None=None,*,attr:str|None=None,local:bool=False):
        """
        Arguments:
            value (`Any`, Optional): Object to point to. If want to point to a class instance atribute, introduce the class instance without the atribute.
            reference (`str`|`None`, Optional): Reference to point to. Useful in case there are multiple references pointing to the same value.
            attr (`str`|`None`, Optional): Atribute of the class instance to which you want to point. Leave empty if `value` is not a class instance.
            local (`bool`, Optional): Indicates if the value to point to is a local variable (`True` for yes and `False` for no). `False` by default.
        """
        if local:
            vars_dict=currentframe().f_back.f_locals
        else:
            vars_dict=vars(modules["__main__"])
        self._value=value
        self._vars_dict=vars_dict
        self._attr=attr
        if reference:
            name=reference
        else:
            name=[]
            for key,v in vars_dict.items():
                try:
                    if v is value:
                        name.append(key)
                except ValueError:
                    pass
            if len(name)>1:
                print(f"{name}\nMultiple references found for the \"value\" parameter. First one was chosen")
                name=name[0]
                #// while True:
                #//     name_aux=input()
                #//     if name_aux in name:
                #//         break
                #//     else:
                #//         print("Error, introduce the correct variable name for the 'value' parameter:")
                #// name=name_aux
                #// del name_aux
            elif len(name)==1:
                name=name[0]
            elif len(name)==0:
                name=None
        self._name=name
    
    #* PROPERTIES
    # Value
    @property
    # Getter
    def value(self):
        if self._attr:
            #? Take name checking out in favor of the reference property
            if self._name and self._name not in list(self._vars_dict):
                del self._value,self._attr
                raise KeyError("The class instance has already been deleted, so the pointer no longer has access to it.")
            elif self._attr not in dir(self._value):
                raise AttributeError(f"The atribute '{self._attr}' has already been deleted, so the pointer no longer has access to it.")
            return getattr(self._value,self._attr)
        else:
            if self._name:
                if self._name not in list(self._vars_dict):
                    del self._value
                    raise KeyError("The variable has already been deleted, so the pointer no longer has access to it.")
                if self._value is not self._vars_dict[self._name]:
                    self._value=self._vars_dict[self._name]
            return self._value
    # Setter
    @value.setter
    def value(self,value):
        if self._attr:
            setattr(self._value,self._attr,value)
        else:
            self._value=value
            if self._name and value is not self._vars_dict[self._name]:
                self._vars_dict[self._name]=value
    # Deleter
    @value.deleter
    def value(self):
        if self._attr:
            delattr(self._value,self._attr)
        else:
            del self._value
            if self._name:
                del self._vars_dict[self._name]
    
    # Reference
    @property
    # Getter
    def reference(self):
        #? Raise error if reference was already purged
        return self._name
    # Setter
    @reference.setter
    def reference(self,var_name):
        if var_name not in self._vars_dict:
            raise ValueError(f"Reference \"{var_name}\" not in enviroment variables")
        elif self._vars_dict[var_name] is not self.value:
            raise ValueError(f"Reference \"{var_name}\" doesn't point to pointer value ({self.value})")
        else:
            self._name=var_name
    #^ No deleter
    
    #* INDEXATION
    # Getter
    def __getitem__(self,index):
        return self.value[index]
    # Setter
    def __setitem__(self,index,value):
        self.value[index]=value
        return
    # Deleter
    def __delitem__(self,index):
        del self.value[index]
        return
    
    #* ARITHMETIC OPERATIONS
    # Addition
    def __add__(self,value):
        if isinstance(value,Pointer):
            return self.value+value.value
        else:
            return self.value+value
    # Difference
    def __sub__(self,value):
        if isinstance(value,Pointer):
            return self.value-value.value
        else:
            return self.value-value
    # Multiplication
    def __mul__(self,value):
        if isinstance(value,Pointer):
            return self.value*value.value
        else:
            return self.value*value
    # Fraction
    def __truediv__(self,value):
        if isinstance(value,Pointer):
            return self.value/value.value
        else:
            return self.value/value
    # Integer division
    def __floordiv__(self,value):
        if isinstance(value,Pointer):
            return self.value//value.value
        else:
            return self.value//value
    # Module
    def __mod__(self,value):
        if isinstance(value,Pointer):
            return self.value%value.value
        else:
            return self.value%value
    # Power
    def __pow__(self,value):
        if isinstance(value,Pointer):
            return self.value**value.value
        else:
            return self.value**value
    
    #* REFLEXED ARITHMETIC METHODS
    # Addition
    def __radd__(self,value):
        return value+self.value
    # Difference
    def __rsub__(self,value):
        return value-self.value
    # Multiplication
    def __rmul__(self,value):
        return value*self.value
    # Fraction
    def __rtruediv__(self,value):
        return value/self.value
    # Integer division
    def __rfloordiv__(self,value):
        return value//self.value
    # Module
    def __rmod__(self,value):
        return value%self.value
    # Power
    def __rpow__(self,value):
        return value**self.value
    
    #* IN-PLACE ARITHMETIC METHODS
    # Addition
    def __iadd__(self,value):
        self.value=self.value+value
        return self
    # Difference
    def __isub__(self,value):
        self.value=self.value-value
        return self
    # Multiplication
    def __imul__(self,value):
        self.value=self.value*value
        return self
    # Fraction
    def __itruediv__(self,value):
        self.value=self.value/value
        return self
    # Integer division
    def __ifloordiv__(self,value):
        self.value=self.value//value
        return self
    # Module
    def __imod__(self,value):
        self.value=self.value%value
        return self
    def __ipow__(self,value):
        self.value=self.value**value
        return self
    
    #* COMPARATIVE METHODS
    # Equality
    def __eq__(self,value):
        if isinstance(value,Pointer):
            return self.value==value.value
        else:
            return self.value==value
    # Inequality
    def __ne__(self,value):
        if isinstance(value,Pointer):
            return self.value!=value.value
        else:
            return self.value!=value
    # Lower than
    def __lt__(self,value):
        if isinstance(value,Pointer):
            return self.value<value.value
        else:
            return self.value<value
    # Lower or equal
    def __le__(self,value):
        if isinstance(value,Pointer):
            return self.value<=value.value
        else:
            return self.value<=value
    # Greater than
    def __gt__(self,value):
        if isinstance(value,Pointer):
            return self.value>value.value
        else:
            return self.value>value
    # Greater or equal
    def __ge__(self,value):
        if isinstance(value,Pointer):
            return self.value>=value.value
        else:
            return self.value>=value
    
    #* UNARY METHODS
    # Negative
    def __neg__(self):
        return Pointer(-self.value)
    # Positive
    def __pos__(self):
        return Pointer(+self.value)
    # Absolute value
    def __abs__(self):
        return Pointer(abs(self.value))
    
    #* LENGTH
    # Length
    def __len__(self):
        return len(self.value)
    
    #* TRANSFORMATION METHODS
    # __int__
    def __int__(self):
        return int(self.value)
    def __float__(self):
        return float(self.value)
    def __index__(self):
        return self.value
    
    #* SCREEN
    # Representation
    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"
    # HTML representation
    def _repr_html_(self):
        return f"<p>{self.value}</p>"
    # Printing
    def __str__(self):
        return str(self.value)