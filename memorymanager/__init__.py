"""
Provides memory management support.

## Memory cleaning
The class `cleaner` flags the global references to erase them when commanded. References can be chosen to be excluded or included again in the process.

---
## Pointers
A safe implementation of pointers for Python. Written in pure Python, this module include two things:
### Class `Pointer`
Creates a `Pointer` instance. These pointers point to a reference, not to an object in memory.
If value for the reference is changed, so is the pointer value and *viceversa*.
### Decorator `pointerize`
Allows a function to receive pointers instead of values.

---
## Author
Ricardo Werner Rivas
"""
# Imports
from .cleaning import Cleaner
from .pointers import Pointer,pointerize

# Declare "__all__"
__all__=["Cleaner","Pointer","pointerize"]