# Python Interview Questions & Answers (Basic → Advanced)
### 100+ Questions covering Core Python, Collections, OOP, Problem Solving & Advanced Topics

---

## Section 1: Python Basics (Q1–Q20)

**Q1. What is Python? What are its key features?**

A. Python is a high-level, interpreted, dynamically-typed, general-purpose programming language. Key features: easy syntax, interpreted (no separate compile step), dynamically typed, supports multiple paradigms (OOP, functional, procedural), huge standard library, garbage collected, and cross-platform.

**Q2. What is the difference between a list and a tuple?**

A. Lists are mutable, tuples are immutable. Lists use more memory and are slightly slower to iterate. Tuples can be used as dictionary keys (if all elements are hashable); lists cannot. Syntax: `[1,2,3]` vs `(1,2,3)`.

**Q3. What are Python's built-in data types?**

A. Numeric (int, float, complex), Sequence (str, list, tuple, range), Mapping (dict), Set types (set, frozenset), Boolean (bool), Binary (bytes, bytearray, memoryview), and NoneType.

**Q4. Is Python interpreted or compiled?**

A. Both, technically. Python source is first compiled to bytecode (.pyc), which is then interpreted by the Python Virtual Machine (PVM). So it's compiled to bytecode and then interpreted, not compiled to native machine code like C.

**Q5. What is PEP 8?**

A. PEP 8 is the official style guide for Python code, covering naming conventions, indentation (4 spaces), line length (79 chars), whitespace usage, and other readability standards.

**Q6. Explain the difference between `==` and `is`.**

A. `==` compares values for equality. `is` compares object identity (whether two references point to the same object in memory). Example: `a = [1,2]; b = [1,2]; a == b` → True, `a is b` → False.

**Q7. What is the difference between mutable and immutable objects? Give examples.**

A. Mutable objects can be changed after creation (list, dict, set, bytearray). Immutable objects cannot be changed after creation (int, float, str, tuple, frozenset, bool). Modifying an immutable object creates a new object instead.

**Q8. What are Python's memory management mechanisms?**

A. Python uses a private heap for objects, an automatic garbage collector using reference counting plus a generational garbage collector to detect and clean up circular references, and object-specific allocators for small objects (pymalloc).

**Q9. What is the difference between `deepcopy` and `shallow copy`?**

A. A shallow copy (`copy.copy()`) creates a new object but inserts references to the same nested objects. A deep copy (`copy.deepcopy()`) recursively copies all nested objects, creating fully independent copies.
```
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)

# Modify a nested list in the shallow copy
shallow[0][0] = 999

print("Original:", original) # Output: [[999, 2], [3, 4]]
print("Shallow: ", shallow)  # Output: [[999, 2], [3, 4]]

import copy

original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)

# Modify a nested list in the deep copy
deep[0][0] = 999

print("Original:", original) # Output: [[1, 2], [3, 4]]
print("Deep:    ", deep)     # Output: [[999, 999], [3, 4]] -> Original stays intact!

```

**Q10. What are Python namespaces and scope (LEGB rule)?**

A. A namespace maps names to objects.
Scope resolution follows LEGB: Local → Enclosing → Global → Built-in. Python looks up a variable in that order.

**Q11. What is the difference between `append()` and `extend()` in lists?**

A. `append(x)` adds a single element (even if it's a list, it's added as one nested item). `extend(iterable)` adds each element of the iterable individually to the list.

**Q12. Explain `*args` and `**kwargs`.**

A. `*args` collects extra positional arguments into a tuple. `**kwargs` collects extra keyword arguments into a dictionary. They allow functions to accept variable numbers of arguments.

**Q13. What is a lambda function? When would you use one?**

A. An anonymous, single-expression function defined with `lambda args: expression`. Used for short throwaway functions, often as arguments to `map()`, `filter()`, `sorted(key=...)`.

```
# Regular function
def add(x, y):
    return x + y

# Equivalent Lambda function
add_lambda = lambda x, y: x + y

print(add_lambda(5, 3))  # Output: 8

# List of tuples: (Name, Age)
people = [("Alice", 25), ("Bob", 19), ("Charlie", 30)]

# Sort by age (the second element, index 1)
sorted_people = sorted(people, key=lambda person: person[1])

print(sorted_people)  
# Output: [('Bob', 19), ('Alice', 25), ('Charlie', 30)]

```

**Q14. What is the difference between `range()` and `xrange()`?**

A. `xrange()` existed only in Python 2 and returned a generator-like object (lazy). In Python 3, `range()` itself behaves lazily (returns a range object), so there is no `xrange` in Python 3.

**Q15. Explain Python's `pass`, `break`, and `continue` statements.**

A. `pass` is a no-op placeholder statement. `break` exits the nearest enclosing loop immediately. `continue` skips the rest of the current iteration and moves to the next one.

**Q16. What is type conversion vs type casting?**

A. Type conversion is implicit — Python automatically converts one type to another (e.g., int to float in `1 + 2.0`). Type casting is explicit — the programmer converts types manually using functions like `int()`, `str()`, `float()`.

**Q17. What does `if __name__ == "__main__":` do?**

A. It checks whether the script is being run directly (in which case `__name__` equals `"__main__"`) versus being imported as a module (in which case `__name__` equals the module's name). Code inside this block only runs when the file is executed directly.

**Q18. What is the difference between `is None` and `== None`?**

A. `is None` checks identity against the singleton `None` object and is the recommended, PEP 8 approved way. `== None` checks equality and could theoretically be overridden by a custom `__eq__`, making it less reliable.

**Q19. What are Python decorators?**

A. A decorator is a function that takes another function (or class) and extends/modifies its behavior without permanently changing its source code, using the `@decorator_name` syntax above a function definition.

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before call")
        result = func(*args, **kwargs)
        print("After call")
        return result
    return wrapper

@my_decorator
def greet():
    print("Hello")
```

**Q20. What is the difference between a module and a package?**

A. A module is a single `.py` file containing Python code. A package is a directory containing multiple modules and an `__init__.py` file (making it importable as a namespace).

---

## Section 2: Collections & Data Structures (Q21–Q40)

**Q21. What is the difference between a `list`, `set`, and `dict` in terms of lookup time?**

A. List lookup by value is O(n) (linear scan). Set and dict lookups are O(1) average case because they use hash tables.

**Q22. How do you remove duplicates from a list while preserving order?**

```python
def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```

A. Using `dict.fromkeys(lst)` also works since Python 3.7+ dicts preserve insertion order: `list(dict.fromkeys(lst))`.

**Q23. What is a `frozenset`? Why would you use it?**

A. An immutable version of a `set`. Since it's hashable, it can be used as a dictionary key or added to another set, unlike a regular mutable set.

**Q24. Explain `collections.Counter` with an example.**

```python
from collections import Counter
words = ["a", "b", "a", "c", "b", "a"]
count = Counter(words)
print(count)              # Counter({'a': 3, 'b': 2, 'c': 1})
print(count.most_common(1))  # [('a', 3)]
```
A. `Counter` is a dict subclass for counting hashable objects; it supports arithmetic between counters and `.most_common(n)`.

**Q25. What is `collections.defaultdict` and how does it differ from a regular dict?**

A. `defaultdict` automatically creates a default value for a missing key instead of raising `KeyError`. Example: `d = defaultdict(list); d["x"].append(1)` works without pre-initializing `d["x"]`.

**Q26. What is `collections.OrderedDict`? Is it still needed in modern Python?**

A. It's a dict subclass that explicitly remembers insertion order and supports `move_to_end()`. Since Python 3.7, regular dicts preserve insertion order too, so `OrderedDict` is mainly useful now for its extra methods and explicit order-sensitive equality checks.

**Q27. What is `collections.namedtuple`? Give an example.**

```python
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)
print(p.x, p.y)   # 1 2
```
A. It creates tuple subclasses with named fields, giving readable, immutable, lightweight objects — useful as a simple alternative to a class.

**Q28. What is `collections.deque` and when would you use it over a list?**

A. A double-ended queue with O(1) appends/pops from both ends (vs O(n) for `list.insert(0, x)` or `list.pop(0)`). Ideal for queues, stacks, and sliding-window algorithms.

**Q29. How do dictionaries handle key collisions internally?**

A. Python dicts use open addressing with a hash table. When two keys hash to the same slot, probing (a specific sequence of alternate slots) is used to find the next available slot.

**Q30. How do you merge two dictionaries in Python?**

```python
d1 = {"a": 1}
d2 = {"b": 2}
merged = {**d1, **d2}          # Python 3.5+
merged2 = d1 | d2              # Python 3.9+
d1.update(d2)                  # in-place
```

**Q31. What is a list comprehension? Give an example with a condition.**

```python
squares_even = [x**2 for x in range(10) if x % 2 == 0]
```
A. A concise syntax to build a list from an iterable, optionally filtering/transforming elements in a single readable line.

**Q32. Explain dictionary and set comprehensions.**

```python
squares_dict = {x: x**2 for x in range(5)}
unique_lengths = {len(w) for w in ["cat", "dog", "elephant"]}
```

**Q33. What's the difference between `sort()` and `sorted()`?**

A. `list.sort()` sorts the list in place and returns `None`. `sorted(iterable)` returns a new sorted list, leaving the original unchanged, and works on any iterable (not just lists).

**Q34. How would you sort a list of dictionaries by a specific key?**

```python
data = [{"name": "Bob", "age": 25}, {"name": "Amy", "age": 22}]
sorted_data = sorted(data, key=lambda d: d["age"])
```

**Q35. What is the difference between `pop()`, `remove()`, and `del` for lists?**

A. `pop(index)` removes and returns the element at the given index (default last). `remove(value)` removes the first matching value (raises `ValueError` if absent). `del list[index]` deletes by index without returning it, and can also delete slices.

```
fruits = ["apple", "banana", "cherry", "date"]

# 1. Pop without an index (defaults to last element)
last_fruit = fruits.pop()
print(last_fruit)  # Output: 'date'
print(fruits)      # Output: ['apple', 'banana', 'cherry']

# 2. Pop with a specific index
second_fruit = fruits.pop(1)
print(second_fruit) # Output: 'banana'
print(fruits)       # Output: ['apple', 'cherry']

numbers = [10, 20, 30, 20, 40]

# Removes the FIRST occurrence of 20
numbers.remove(20)
print(numbers)  # Output: [10, 30, 20, 40]

# Trying to remove a value that doesn't exist raises an error:
# numbers.remove(99)  # Raises ValueError: list.remove(x): x not in list

colors = ["red", "green", "blue", "yellow", "purple"]

# 1. Delete a single item by index
del colors[0]
print(colors)  # Output: ['green', 'blue', 'yellow', 'purple']

# 2. Delete a range using slicing
del colors[1:3]
print(colors)  # Output: ['green', 'purple']

# 3. Clear the entire list
del colors[:]
print(colors)  # Output: []
```

**Q36. How do you flatten a nested list in Python?**

```python
nested = [[1, 2], [3, 4], [5]]
flat = [item for sublist in nested for item in sublist]
# or: import itertools; list(itertools.chain.from_iterable(nested))
```

**Q37. What is the difference between `array` module and `list`?**

A. `array` stores elements of a single, fixed numeric type more compactly than a `list` (which stores generic Python objects/pointers), making arrays more memory-efficient for large numeric datasets, though less flexible.

**Q38. How does Python's `heapq` module work? Give a use case.**

A. `heapq` implements a min-heap on top of a regular list. Useful for priority queues, finding k smallest/largest elements efficiently.

```python
import heapq
nums = [5, 1, 8, 3, 2]
heapq.heapify(nums)
print(heapq.heappop(nums))   # 1 (smallest)
print(heapq.nsmallest(2, [5,1,8,3,2]))  # [1, 2]

```

**Q39. What is the difference between `set` and `frozenset` operations like union/intersection?**
A. Both support `union()`, `intersection()`, `difference()`, `symmetric_difference()`. The difference is mutability: `set` also supports in-place operators like `|=`, `add()`, `remove()`; `frozenset` does not, since it's immutable.

```
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Operator
print(a | b)         # Output: {1, 2, 3, 4, 5, 6}

# Method
print(a.union(b))    # Output: {1, 2, 3, 4, 5, 6}

# Operator
print(a & b)                # Output: {3, 4}

# Method
print(a.intersection(b))   # Output: {3, 4}

# Elements in 'a' but not in 'b'
print(a - b)                # Output: {1, 2}
print(a.difference(b))      # Output: {1, 2}

# Elements in 'b' but not in 'a'
print(b - a)                # Output: {5, 6}

# Operator
print(a ^ b)                          # Output: {1, 2, 5, 6}

# Method
print(a.symmetric_difference(b))      # Output: {1, 2, 5, 6}

s1 = {1, 2}
s2 = {2, 3}

s1.add(4)             # Adds a single item: {1, 2, 4}
s1.remove(2)          # Removes item (raises KeyError if missing): {1, 4}
s1.discard(99)        # Removes item safely (no error if missing)

s1 |= s2              # In-place union (or s1.update(s2)): {1, 3, 4}
s1 &= {3, 4, 5}       # In-place intersection: {3, 4}

```
**Q40. How do you check if two lists have any common elements efficiently?**

```python
def has_common(a, b):
    return bool(set(a) & set(b))
```
A. Converting to sets makes the intersection check O(n+m) instead of O(n*m) with nested loops.

---

## Section 3: Strings & String Manipulation (Q41–Q50)

**Q41. How do you reverse a string in Python?**

```python
s = "hello"
reversed_s = s[::-1]
```

**Q42. How do you check if a string is a palindrome?**

```python
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]
```

**Q43. What's the difference between `str.format()`, `%` formatting, and f-strings?**

A. `%` is the oldest, C-style formatting. `.format()` is more flexible and readable, introduced in Python 2.6/3. f-strings (Python 3.6+) are the fastest and most readable, embedding expressions directly: `f"{name} is {age}"`.

**Q44. How do you check if a string contains only digits/alphabets?**

A. `s.isdigit()`, `s.isalpha()`, `s.isalnum()`, `s.isspace()` — all built-in string methods.

**Q45. How would you count the frequency of each character in a string?**

```python
from collections import Counter
freq = Counter("mississippi")
```

**Q46. How do you split a string and join it back?**

```python
words = "a,b,c".split(",")     # ['a', 'b', 'c']
joined = "-".join(words)       # 'a-b-c'
```

**Q47. Write a function to check if two strings are anagrams.**

```python
def is_anagram(s1, s2):
    return sorted(s1.lower()) == sorted(s2.lower())
```

**Q48. What is string interning in Python?**

A. Python caches ("interns") certain small/simple string literals (and identifiers) so identical strings can share the same memory object, making `is` comparisons True for them — an optimization, not a guarantee for all strings.

**Q49. How do you find the first non-repeating character in a string?**

```python
from collections import Counter
def first_unique(s):
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return ch
    return None
```

**Q50. What is the difference between `str.strip()`, `lstrip()`, and `rstrip()`?**

A. `strip()` removes leading and trailing whitespace (or specified characters). `lstrip()` removes only from the left/start. `rstrip()` removes only from the right/end.

---

## Section 4: Functions, OOP & Advanced Concepts (Q51–Q70)

**Q51. What is the difference between a shallow function argument default of a mutable object being a common bug? Explain "mutable default argument" pitfall.**

```python
def add_item(item, lst=[]):   # BAD: default list is shared across calls
    lst.append(item)
    return lst
```
A. Default arguments are evaluated once at function definition time, not each call. So a mutable default (like `[]`) persists and accumulates state across calls. Fix: use `None` as default and initialize inside the function.

**Q52. Explain Python's `@staticmethod` vs `@classmethod` vs instance methods.**

A. Instance methods take `self` and operate on instance data. `@classmethod` takes `cls` and operates on the class itself (useful for alternate constructors). `@staticmethod` takes neither — it's a regular function namespaced inside a class, with no access to instance or class state.

Method Type,Decorator,First Parameter,Access/Capabilities
Instance Method,None,self,Can access and modify instance state (self.x) and class state (self.__class__).
Class Method,@classmethod,cls,"Can access and modify class state (cls.x), but cannot access instance state. Often used for factory constructors."
Static Method,@staticmethod,None,Utility function. Cannot access or modify instance state or class state. Lives inside the class namespace for logical grouping.

```python

class Employee:
    # Class attribute (shared by all instances)
    company_name = "TechCorp"

    def __init__(self, name, salary):
        # Instance attributes (unique to each instance)
        self.name = name
        self.salary = salary

    # -------------------------------------------------------------
    # 1. Instance Method
    # Operates on a specific instance (uses `self`)
    # -------------------------------------------------------------
    def get_details(self):
        return f"Employee: {self.name}, Salary: ${self.salary}"

    def give_raise(self, amount):
        self.salary += amount

    # -------------------------------------------------------------
    # 2. Class Method
    # Operates on the class itself (uses `cls`), often used as factory constructors
    # -------------------------------------------------------------
    @classmethod
    def from_string(cls, emp_str):
        """Factory constructor: Creates an instance from a string like 'John-50000'."""
        name, salary = emp_str.split("-")
        return cls(name, int(salary))

    @classmethod
    def set_company_name(cls, new_name):
        cls.company_name = new_name

    # -------------------------------------------------------------
    # 3. Static Method
    # Standard utility function that doesn't need self or cls
    # -------------------------------------------------------------
    @staticmethod
    def is_valid_salary(salary):
        """Checks if a proposed salary is valid."""
        return salary > 0

```

**Q53. What is method resolution order (MRO) in Python?**

A. MRO defines the order in which base classes are searched when executing a method with multiple inheritance. Python uses the C3 linearization algorithm; you can inspect it via `ClassName.__mro__` or `ClassName.mro()`.

**Q54. What is multiple inheritance? What problems can arise (diamond problem)?**

A. A class inheriting from more than one parent class. The "diamond problem" occurs when two parent classes share a common ancestor, causing ambiguity in method resolution — Python resolves this deterministically using MRO/C3 linearization.

`     A  (Top Ancestor)
      / \
     B   C  (Parent Classes)
      \ /
       D  (Child Class)
`

```
class A:
    def show(self):
        print("A's show() called")

class B(A):
    def show(self):
        print("B's show() called")
        super().show()

class C(A):
    def show(self):
        print("C's show() called")
        super().show()

class D(B, C):
    def show(self):
        print("D's show() called")
        super().show()


# --- Execution ---
d = D()
d.show()


```
**Q55. What are Python's magic/dunder methods? Give 3 examples.**

A. Special methods surrounded by double underscores that let objects support built-in operations. Examples: `__init__` (constructor), `__str__` (string representation), `__len__` (support for `len()`), `__eq__` (equality comparison), `__add__` (operator overloading for `+`).


**Q56. What is the difference between `__str__` and `__repr__`?**

A. `__str__` returns a readable, user-friendly string (used by `print()` and `str()`). `__repr__` returns an unambiguous, developer-facing representation (ideally one that could recreate the object), used by the interpreter and `repr()`. If `__str__` is undefined, Python falls back to `__repr__`.

**Q57. What is encapsulation, and how is it achieved in Python?**

A. Encapsulation bundles data and methods together while restricting direct access. Python uses naming conventions: single underscore `_var` (protected, convention only) and double underscore `__var` (name-mangled to `_ClassName__var`, harder to access accidentally) — Python doesn't have true private members.

**Q58. What is polymorphism? Give a Python example.**

```python
class Dog:
    def speak(self): return "Woof"
class Cat:
    def speak(self): return "Meow"

for animal in [Dog(), Cat()]:
    print(animal.speak())
```
A. Polymorphism allows objects of different classes to be treated through a common interface, each responding to the same method call in its own way.

**Q59. What is a generator? How does it differ from a normal function?**

A. A generator uses `yield` instead of `return` to produce a sequence of values lazily, one at a time, pausing/resuming state between calls — saving memory versus building an entire list upfront.

```python
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1
```

**Q60. What is the difference between an iterator and an iterable?**

A. An iterable is any object implementing `__iter__()` that returns an iterator (e.g., list, string). An iterator implements both `__iter__()` and `__next__()`, maintaining state about its current position and raising `StopIteration` when exhausted.

**Q61. What are Python context managers? How does `with` work?**

A. Context managers manage setup/teardown (like opening/closing a file) via `__enter__` and `__exit__` methods, ensuring cleanup happens even if an exception occurs. `with open('f.txt') as f:` automatically closes the file afterward.

**Q62. How do you create a custom context manager?**

```python
from contextlib import contextmanager

@contextmanager
def my_context():
    print("Enter")
    yield
    print("Exit")

with my_context():
    print("Inside")
```

**Q63. What is the Global Interpreter Lock (GIL)? How does it affect multithreading?**

A. The GIL is a mutex in CPython that allows only one thread to execute Python bytecode at a time, even on multi-core systems. This means CPU-bound multithreaded programs don't get true parallelism (use multiprocessing instead), though I/O-bound tasks still benefit from threading since the GIL is released during I/O waits.

**Q64. What is the difference between multithreading and multiprocessing in Python?**

A. Multithreading runs multiple threads within one process, sharing memory, but limited by the GIL for CPU-bound work. Multiprocessing spawns separate processes with separate memory and interpreters, achieving true parallelism for CPU-bound tasks at the cost of higher memory usage and inter-process communication overhead.

**Q65. What are Python decorators with arguments? Show an example.**

```python
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hi():
    print("Hi")
```

**Q66. What is monkey patching?**

A. Dynamically modifying or extending a class or module at runtime (e.g., replacing a method on an object/class after it's defined). Powerful but risky — can make code harder to debug and maintain.

**Q67. Explain Python's `property` decorator and its use case.**

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def area(self):
        return 3.14159 * self._radius ** 2
```
A. `@property` lets a method be accessed like an attribute (`circle.area` instead of `circle.area()`), often used with setters/getters to control attribute access while keeping a clean interface.

**Q68. What is the difference between abstract classes and interfaces in Python?**

A. Python doesn't have formal interfaces; it uses abstract base classes (ABCs) via the `abc` module. An abstract class can have both abstract methods (must be overridden) and concrete methods, using `@abstractmethod` decorators, and cannot be instantiated directly.

```
from abc import ABC, abstractmethod

# 1. Define the Abstract Base Class inheriting from ABC
class Shape(ABC):
    
    # Concrete method (shared logic available to all shapes)
    def describe(self):
        return "I am a geometric shape."

    # Abstract method (MUST be overridden by subclasses)
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass


# 2. Define Subclasses implementing the abstract methods

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * (self.radius ** 2)

    def perimeter(self):
        return 2 * 3.14159 * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


```
**Q69. What is duck typing?**

A. A dynamic typing philosophy: "If it walks like a duck and quacks like a duck, it's a duck." Python doesn't check an object's type, only whether it has the required methods/attributes, allowing flexible, type-agnostic code.

**Q70. What is the difference between composition and inheritance? When would you prefer one?**

A. Inheritance models an "is-a" relationship (a `Dog` is an `Animal`). Composition models a "has-a" relationship (a `Car` has an `Engine`). Composition is generally preferred for flexibility and to avoid tight coupling/fragile base class problems, unless there's a genuine hierarchical relationship.

---

## Section 5: Error Handling, File I/O & Standard Library (Q71–Q80)

**Q71. How does exception handling work in Python? Explain try/except/else/finally.**

A. `try` holds code that might raise an exception. `except` catches and handles specific (or general) exceptions. `else` runs only if no exception occurred. `finally` always runs, used for cleanup (like closing resources), regardless of whether an exception occurred.

**Q72. How do you create a custom exception?**

```python
class InsufficientFundsError(Exception):
    def __init__(self, message="Insufficient funds"):
        super().__init__(message)

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError()
```

**Q73. What is the difference between `Exception` and `BaseException`?**

A. `BaseException` is the root of all exceptions, including `SystemExit`, `KeyboardInterrupt`, and `GeneratorExit` — things you usually shouldn't catch. `Exception` is a subclass of `BaseException` and is the base for all "normal" errors you should catch (e.g., `ValueError`, `TypeError`).

**Q74. How do you handle multiple exceptions in one except block?**

```python
try:
    risky()
except (ValueError, TypeError) as e:
    print(f"Error: {e}")
```

**Q75. What is the difference between reading a file with `read()`, `readline()`, and `readlines()`?**

A. `read()` returns the entire file content as one string. `readline()` reads a single line at a time. `readlines()` returns a list of all lines. For large files, iterating over the file object directly (`for line in f:`) is most memory-efficient.

**Q76. Why should you use `with open(...) as f:` instead of manually calling `open()`/`close()`?**

A. `with` guarantees the file is properly closed even if an exception occurs during processing, since `close()` is called automatically inside `__exit__`, preventing resource leaks.

**Q77. What is `pickle` used for? What are its risks?**

A. `pickle` serializes Python objects to bytes (for storage/transmission) and deserializes them back. Risk: unpickling data from an untrusted source can execute arbitrary code, so it should never be used with untrusted input.

**Q78. What is the difference between `json.dumps()` and `pickle.dumps()`?**

A. `json` serializes to a human-readable, language-agnostic text format but only supports basic types (dict, list, str, number, bool, None). `pickle` serializes to a Python-specific binary format supporting almost any Python object, but is unsafe with untrusted data and not portable across languages.

**Q79. What is a virtual environment, and why is it used?**

A. An isolated Python environment with its own installed packages, separate from the system Python and other projects. Prevents dependency version conflicts between different projects. Created via `venv` or tools like `virtualenv`/`conda`.

**Q80. What is the difference between `is_alive()`, `join()`, and daemon threads in the `threading` module?**

A. `is_alive()` checks if a thread is still running. `join()` blocks the calling thread until the target thread finishes. A daemon thread runs in the background and is killed automatically when the main program exits, regardless of whether it finished.

---

## Section 6: Problem-Solving / Coding Questions (Q81–Q100)

**Q81. Write a function to check if a number is prime.**

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_prime_recursive(n, d=2):
    # Base Cases
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % d == 0:
        return False
    if d * d > n:  # No divisors found up to sqrt(n)
        return True
    
    # Recursive Case: check the next divisor
    return is_prime_recursive(n, d + 1)

```

**Q82. Write a function to compute the Fibonacci sequence up to n terms (iterative).**

```python
def fibonacci(n):
    a, b = 0, 1
    result = []
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result


def fibonacci_recursive(n):
    # Base cases
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    # Recursive case
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

# Example: Get the 7th Fibonacci number
print(fibonacci_recursive(7))  # Output: 13


```

**Q83. Write a function to find the factorial of a number (recursive).**

```python
def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)
```

**Q84. Write a function to check if two arrays/lists are rotations of each other.**

```python
def is_rotation(a, b):
    if len(a) != len(b):
        return False
    return " ".join(map(str, b)) in " ".join(map(str, a + a))
```

**Q85. Implement binary search.**

```python
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```

**Q86. Write a function to find the second largest number in a list without using `sorted()` twice.**

```python
def second_largest(nums):
    first = second = float('-inf')
    for n in nums:
        if n > first:
            first, second = n, first
        elif first > n > second:
            second = n
    return second
```

**Q87. Write a function that finds the missing number in a list of 1 to n.**

```python
def missing_number(nums, n):
    expected_sum = n * (n + 1) // 2
    return expected_sum - sum(nums)
```

**Q88. Implement a function to check if a linked list has a cycle (Floyd's algorithm).**

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```


**Q89. Write a function to find the two numbers in a list that sum to a target value (Two Sum).**

```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

**Q90. Write a function to check if a given string has balanced parentheses.**
```python
def is_balanced(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack
```

**Q91. Implement a function to merge two sorted lists into one sorted list.**

```python
def merge_sorted(a, b):
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result
```

**Q92. Write a function to find the majority element in a list (Boyer-Moore voting algorithm).**

```python
def majority_element(nums):
    count = 0
    candidate = None
    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1
    return candidate

from collections import Counter

def majority_element(nums):
    # Counter(nums).most_common(1) returns [ (candidate, count) ]
    return Counter(nums).most_common(1)[0][0]

# Example Usage
print(majority_element([2, 2, 1, 1, 1, 2, 2]))  # Output: 2

from collections import Counter

def majority_element(nums):
    counts = Counter(nums)
    return max(counts, key=counts.get)

# Example Usage
print(majority_element([3, 3, 4, 2, 4, 4, 2, 4, 4]))  # Output: 4


```

**Q93. Write a function to rotate a list by k positions.**

```python
def rotate(lst, k):
    k = k % len(lst)
    return lst[-k:] + lst[:-k]
```

**Q94. Implement quicksort.**

```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + mid + quicksort(right)
```

**Q95. Write a function to detect the first duplicate in a list.**

```python
def first_duplicate(lst):
    seen = set()
    for item in lst:
        if item in seen:
            return item
        seen.add(item)
    return None
```

**Q96. Write a function to check if two strings are one edit apart (insert, remove, replace).**

```python
def one_edit_away(s1, s2):
    if abs(len(s1) - len(s2)) > 1:
        return False
    if len(s1) == len(s2):
        return sum(a != b for a, b in zip(s1, s2)) <= 1
    shorter, longer = (s1, s2) if len(s1) < len(s2) else (s2, s1)
    i = j = 0
    found_diff = False
    while i < len(shorter) and j < len(longer):
        if shorter[i] != longer[j]:
            if found_diff:
                return False
            found_diff = True
            j += 1
        else:
            i += 1
            j += 1
    return True
```

**Q97. Write a function to find all permutations of a string.**

```python
from itertools import permutations
def all_permutations(s):
    return ["".join(p) for p in permutations(s)]
```

**Q98. Implement a function to find the longest common prefix among a list of strings.**

```python
def longest_common_prefix(strs):
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix
```

**Q99. Write a function to determine if a list contains a subarray with a given sum (using sliding window, positive numbers).**
```python
def has_subarray_sum(nums, target):
    left = 0
    current_sum = 0
    for right in range(len(nums)):
        current_sum += nums[right]
        while current_sum > target and left <= right:
            current_sum -= nums[left]
            left += 1
        if current_sum == target:
            return True
    return False
```

**Q100. Write a function to implement an LRU (Least Recently Used) Cache.**
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

---

## Section 7:

**Q101. What are metaclasses in Python?**
A. A metaclass is "the class of a class" — it defines how a class itself behaves/is constructed. By default, classes are instances of `type`. Custom metaclasses (via `class Meta(type):`) let you control class creation, commonly used in ORMs and frameworks like Django.

**Q102. What is the difference between `__new__` and `__init__`?**
A. `__new__` is responsible for creating and returning a new instance (called before `__init__`), useful for immutable types or singleton patterns. `__init__` initializes the already-created instance's attributes; it doesn't return anything.

**Q103. What is a Python descriptor?**
A. An object implementing `__get__`, `__set__`, or `__delete__` that customizes attribute access on another class. `property` is implemented internally as a descriptor.

**Q104. Explain the difference between `@lru_cache` and manual memoization.**
A. `functools.lru_cache` is a built-in decorator that automatically caches function results based on arguments, with configurable size limits and eviction of least-recently-used entries — saving you from writing a manual dictionary-based cache.
```python
from functools import lru_cache
@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)
```

**Q105. What is the difference between `asyncio`'s `async`/`await` and threading?**

A. `asyncio` uses a single-threaded event loop with cooperative multitasking — coroutines voluntarily yield control at `await` points, ideal for I/O-bound concurrency without thread-switching overhead or GIL contention. Threading uses OS-level preemptive context switching across multiple threads.

**Q106. What is the walrus operator (`:=`)? Give an example.**

* variable := expression
  

```python
data = [1, 2, 3, 4, 5]
if (n := len(data)) > 3:
    print(f"List has {n} items")
```
A. Introduced in Python 3.8, it allows assignment within an expression, reducing the need for redundant computation or separate assignment lines.

**Q107. What is the difference between `__slots__` and regular class attributes?**
A. By default, instances store attributes in a `__dict__`, which uses extra memory. `__slots__` restricts instances to a fixed set of attributes stored in a more memory-efficient structure, disallowing dynamic attribute addition and reducing per-instance memory overhead — useful when creating many instances.

**Q108. What is the difference between a shallow understanding of "everything is an object" in Python and what that means practically?**

A. In Python, functions, classes, modules, and even types are all first-class objects — they can be assigned to variables, passed as arguments, stored in data structures, and have attributes. This underpins features like decorators, higher-order functions, and dynamic introspection (`type()`, `dir()`, `getattr()`).

---

## Section 8: More Problem-Solving / Coding Questions (Q109–Q140)

**Q109. Write a function to find the maximum subarray sum (Kadane's Algorithm).**

```python
def max_subarray_sum(nums):
    max_sum = current_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum
```

**Q110. Write a function to check if a number is a power of two.**

```python
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0
```

**Q111. Write a function to reverse an integer (e.g., 123 → 321).**

```python
def reverse_integer(x):
    sign = -1 if x < 0 else 1
    x = abs(x)
    reversed_num = int(str(x)[::-1])
    return sign * reversed_num
```

**Q112. Implement merge sort.**

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Q113. Write a function to find the depth (height) of a binary tree.**

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def max_depth(root):
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

**Q114. Write a function to check if a binary tree is a valid binary search tree (BST).**

```python
def is_valid_bst(root, low=float('-inf'), high=float('inf')):
    if root is None:
        return True
    if not (low < root.val < high):
        return False
    return (is_valid_bst(root.left, low, root.val) and
            is_valid_bst(root.right, root.val, high))
```

**Q115. Write a function to perform level-order (BFS) traversal of a binary tree.**

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
```

**Q116. Implement Depth-First Search (DFS) on a graph represented as an adjacency list.**
```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited
```

**Q117. Implement Breadth-First Search (BFS) on a graph.**
```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order
```

**Q118. Write a function to find the number of islands in a 2D grid (DFS flood-fill).**
```python
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])

    def sink(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        sink(r+1, c); sink(r-1, c); sink(r, c+1); sink(r, c-1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                sink(r, c)
    return count
```

**Q119. Write a dynamic programming solution for the classic "Climbing Stairs" problem (n steps, 1 or 2 at a time).**
```python
def climb_stairs(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b
```

**Q120. Write a function to solve the coin change problem (minimum coins to make an amount).**
```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
```

**Q121. Write a function to find the longest increasing subsequence (LIS) length.**
```python
def length_of_lis(nums):
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

**Q122. Write a function to compute the edit distance (Levenshtein distance) between two strings.**
```python
def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]
```

**Q123. Write a function to rotate an N x N matrix 90 degrees clockwise in place.**
```python
def rotate_matrix(matrix):
    matrix.reverse()
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    return matrix
```

**Q124. Write a function to transpose a matrix.**
```python
def transpose(matrix):
    return [list(row) for row in zip(*matrix)]
```

**Q125. Write a function to find all pairs in a list that sum to a target (return unique pairs).**
```python
def pairs_with_sum(nums, target):
    seen, pairs = set(), set()
    for num in nums:
        complement = target - num
        if complement in seen:
            pairs.add((min(num, complement), max(num, complement)))
        seen.add(num)
    return list(pairs)
```

**Q126. Write a function to check if a number is a "happy number" (repeatedly summing squares of digits eventually reaches 1).**
```python
def is_happy(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(d) ** 2 for d in str(n))
    return n == 1
```

**Q127. Write a function to find the kth largest element in an unsorted list without fully sorting (using heapq).**
```python
import heapq
def kth_largest(nums, k):
    return heapq.nlargest(k, nums)[-1]
```

**Q128. Write a function to implement a basic Trie (prefix tree) with insert and search.**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end
```

**Q129. Write a function to determine the maximum profit from buying/selling a stock once (best time to buy/sell stock).**
```python
def max_profit(prices):
    min_price = float('inf')
    profit = 0
    for price in prices:
        min_price = min(min_price, price)
        profit = max(profit, price - min_price)
    return profit
```

**Q130. Write a function to find the union and intersection of two linked lists (using values).**
```python
def union_intersection(list1, list2):
    s1, s2 = set(list1), set(list2)
    return sorted(s1 | s2), sorted(s1 & s2)
```

**Q131. Write a function to count the number of set bits (1s) in the binary representation of an integer.**
```python
def count_set_bits(n):
    count = 0
    while n:
        n &= (n - 1)   # clears the lowest set bit
        count += 1
    return count
```

**Q132. Write a function to generate all subsets (the power set) of a list.**
```python
def power_set(nums):
    result = [[]]
    for num in nums:
        result += [subset + [num] for subset in result]
    return result
```

**Q133. Write a function to find the longest palindromic substring in a string.**
```python
def longest_palindrome(s):
    if not s:
        return ""
    start, end = 0, 0
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        return r - l - 1
    for i in range(len(s)):
        len1 = expand(i, i)
        len2 = expand(i, i + 1)
        max_len = max(len1, len2)
        if max_len > end - start:
            start = i - (max_len - 1) // 2
            end = i + max_len // 2
    return s[start:end + 1]
```

**Q134. Write a function to find the intersection point of two singly linked lists.**
```python
def get_intersection_node(headA, headB):
    a, b = headA, headB
    while a is not b:
        a = a.next if a else headB
        b = b.next if b else headA
    return a
```

**Q135. Write a function to implement a basic producer-consumer pattern using `queue.Queue` and threading.**
```python
import threading, queue, time

def producer(q):
    for i in range(5):
        q.put(i)
        time.sleep(0.1)
    q.put(None)  # sentinel to signal completion

def consumer(q):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"Consumed: {item}")

q = queue.Queue()
t1 = threading.Thread(target=producer, args=(q,))
t2 = threading.Thread(target=consumer, args=(q,))
t1.start(); t2.start()
t1.join(); t2.join()
```

**Q136. Write a function to validate whether a Sudoku board (partially filled 9x9 grid) is valid so far.**
```python
def is_valid_sudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == ".":
                continue
            b = (r // 3) * 3 + c // 3
            if val in rows[r] or val in cols[c] or val in boxes[b]:
                return False
            rows[r].add(val); cols[c].add(val); boxes[b].add(val)
    return True
```

**Q137. Write a function to find all triplets in a list that sum to zero (3Sum).**
```python
def three_sum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            total = nums[i] + nums[l] + nums[r]
            if total == 0:
                result.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l + 1]: l += 1
                while l < r and nums[r] == nums[r - 1]: r -= 1
                l += 1; r -= 1
            elif total < 0:
                l += 1
            else:
                r -= 1
    return result
```

**Q138. Write a function to implement a min-stack (a stack that supports `getMin()` in O(1)).**
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        min_val = val if not self.min_stack else min(val, self.min_stack[-1])
        self.min_stack.append(min_val)

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def get_min(self):
        return self.min_stack[-1]
```

**Q139. Write a function to find the shortest path in an unweighted graph between two nodes (BFS).**
```python
from collections import deque

def shortest_path(graph, start, end):
    queue = deque([[start]])
    visited = {start}
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == end:
            return path
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None
```

**Q140. Write a function to check if a string can be segmented into space-separated dictionary words (Word Break problem).**
```python
def word_break(s, word_dict):
    word_set = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[len(s)]
```

---

### How to Use This Guide
- **Basics (Q1–20):** Warm-up / screening round questions.
- **Collections (Q21–40):** Core for roles needing data manipulation.
- **Strings (Q41–50):** Common in coding rounds.
- **OOP/Advanced (Q51–70):** Mid-to-senior level conceptual depth.
- **Error Handling/Stdlib (Q71–80):** Practical, production-code awareness.
- **Problem Solving (Q81–100):** Coding round / whiteboard practice.
- **Bonus Advanced (Q101–108):** Senior/staff-level or Python-internals-focused interviews.
- **More Problem Solving (Q109–140):** DP, trees, graphs, tries, bit manipulation, and data-structure design (LRU cache, min-stack, producer-consumer) — great for advanced coding rounds.
