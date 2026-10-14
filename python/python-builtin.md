# Python Built-in Functions — Complete Guide with Examples

Python ships with dozens of built-in functions available globally without any import. Grouped below by category.

---

## 1. Type Conversion Functions

**`int(x)`** – converts to integer
```python
print(int("42"))      # 42
print(int(3.9))        # 3 (truncates, doesn't round)
print(int("101", 2))   # 5 (binary string to int)
```

**`float(x)`** – converts to float
```python
print(float("3.14"))   # 3.14
print(float(5))         # 5.0
```

**`str(x)`** – converts to string
```python
print(str(42))       # '42'
print(str([1, 2]))   # '[1, 2]'
```

**`bool(x)`** – converts to boolean (truthy/falsy evaluation)
```python
print(bool(0))       # False
print(bool(""))      # False
print(bool([]))      # False
print(bool("hi"))    # True
```

**`list(x)` / `tuple(x)` / `set(x)` / `dict(x)`** – convert between collection types
```python
print(list("abc"))          # ['a', 'b', 'c']
print(tuple([1, 2, 3]))     # (1, 2, 3)
print(set([1, 1, 2, 3]))    # {1, 2, 3}
print(dict([("a", 1), ("b", 2)]))   # {'a': 1, 'b': 2}
```

**`complex(real, imag)`** – creates a complex number
```python
print(complex(2, 3))   # (2+3j)
```

**`bytes()` / `bytearray()`** – create byte sequences
```python
print(bytes("hi", "utf-8"))       # b'hi'
print(bytearray([104, 105]))       # bytearray(b'hi')
```

---

## 2. Math & Numeric Functions

**`abs(x)`** – absolute value
```python
print(abs(-7))     # 7
print(abs(-3.5))   # 3.5
```

**`round(x, n)`** – rounds to n decimal places (default 0)
```python
print(round(3.14159, 2))   # 3.14
print(round(2.5))          # 2 (banker's rounding - rounds to even)
print(round(3.5))          # 4
```

**`pow(x, y, z)`** – x raised to power y, optionally modulo z
```python
print(pow(2, 3))        # 8
print(pow(2, 10, 1000))  # 24 (equivalent to (2**10) % 1000, but faster for large numbers)
```

**`divmod(x, y)`** – returns (quotient, remainder) as a tuple
```python
print(divmod(17, 5))   # (3, 2)
```

**`sum(iterable, start)`** – sums elements
```python
print(sum([1, 2, 3]))         # 6
print(sum([1, 2, 3], 10))     # 16 (with a starting value)
```

**`min(iterable)` / `max(iterable)`** – smallest/largest value
```python
print(min([3, 1, 4]))               # 1
print(max([3, 1, 4]))               # 4
print(max("apple", "banana", key=len))   # 'banana' (custom key function)
```

---

## 3. Iterable & Sequence Functions

**`len(x)`** – length of a sequence/collection
```python
print(len("hello"))     # 5
print(len([1, 2, 3]))   # 3
```

**`range(start, stop, step)`** – generates a sequence of numbers (lazy)
```python
print(list(range(5)))          # [0, 1, 2, 3, 4]
print(list(range(2, 10, 2)))   # [2, 4, 6, 8]
```

**`enumerate(iterable, start)`** – pairs elements with an index
```python
for i, val in enumerate(["a", "b", "c"], start=1):
    print(i, val)
# 1 a
# 2 b
# 3 c
```

**`zip(*iterables)`** – combines multiple iterables element-wise
```python
names = ["Sam", "Alex"]
scores = [90, 85]
print(list(zip(names, scores)))   # [('Sam', 90), ('Alex', 85)]
```

**`sorted(iterable, key, reverse)`** – returns a new sorted list
```python
print(sorted([3, 1, 2]))                       # [1, 2, 3]
print(sorted([3, 1, 2], reverse=True))          # [3, 2, 1]
print(sorted(["bb", "a", "ccc"], key=len))      # ['a', 'bb', 'ccc']
```

**`reversed(seq)`** – returns a reverse iterator
```python
print(list(reversed([1, 2, 3])))   # [3, 2, 1]
```

**`map(func, iterable)`** – applies a function to every element
```python
print(list(map(str, [1, 2, 3])))          # ['1', '2', '3']
print(list(map(lambda x: x * 2, [1, 2, 3])))   # [2, 4, 6]
```

**`filter(func, iterable)`** – filters elements where func returns True
```python
print(list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])))   # [2, 4]
```

**`any(iterable)` / `all(iterable)`** – True if any/all elements are truthy
```python
print(any([False, False, True]))   # True
print(all([True, True, False]))    # False
```

**`iter(x)` / `next(x)`** – get an iterator / fetch the next value
```python
it = iter([1, 2, 3])
print(next(it))   # 1
print(next(it))   # 2
print(next(it, "done"))   # 3 (default value avoids StopIteration if exhausted after this)
```

---

## 4. Object Inspection & Introspection

**`type(x)`** – returns the type of an object
```python
print(type(5))        # <class 'int'>
print(type("hi"))     # <class 'str'>
```

**`isinstance(obj, class)`** – checks if object is an instance of a class (or tuple of classes)
```python
print(isinstance(5, int))              # True
print(isinstance(5, (int, float)))      # True
```

**`issubclass(cls, classinfo)`** – checks class inheritance relationship
```python
class Animal: pass
class Dog(Animal): pass
print(issubclass(Dog, Animal))   # True
```

**`id(x)`** – returns the unique memory identifier of an object
```python
a = [1, 2]
print(id(a))   # some integer, e.g. 140234883935808
```

**`dir(obj)`** – lists valid attributes/methods of an object
```python
print(dir([]))   # ['append', 'clear', 'copy', 'count', ...]
```

**`vars(obj)`** – returns an object's `__dict__` (attribute mapping)
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print(vars(p))   # {'x': 1, 'y': 2}
```

**`hasattr(obj, name)` / `getattr(obj, name, default)` / `setattr(obj, name, value)`**
```python
class Person:
    def __init__(self):
        self.name = "Sam"

p = Person()
print(hasattr(p, "name"))          # True
print(getattr(p, "age", "N/A"))    # 'N/A' (default, since age doesn't exist)
setattr(p, "age", 25)
print(p.age)   # 25
```

**`callable(obj)`** – checks if object can be called like a function
```python
print(callable(len))     # True
print(callable(5))       # False
```

---

## 5. Input / Output Functions

**`print(*values, sep, end)`** – prints to console
```python
print("Hello", "World", sep="-")     # Hello-World
print("no newline", end="")           # doesn't add trailing \n
```

**`input(prompt)`** – reads a line of user input as a string
```python
name = input("Enter your name: ")
print(f"Hello, {name}")
```

**`format(value, format_spec)`** – formats a value according to a spec
```python
print(format(3.14159, ".2f"))   # '3.14'
print(format(255, "x"))          # 'ff' (hex)
print(format(255, "b"))          # '11111111' (binary)
```

**`repr(x)`** – returns the "official" string representation of an object
```python
print(repr("hello"))   # "'hello'" (includes quotes)
print(repr([1, 2]))    # '[1, 2]'
```

---

## 6. Functional Programming Helpers

**`lambda`** – anonymous function (keyword, not a function, but worth including)
```python
square = lambda x: x ** 2
print(square(5))   # 25
```

**`eval(expr)`** – evaluates a string as a Python expression (use with caution — security risk on untrusted input)
```python
print(eval("2 + 3 * 4"))   # 14
```

**`exec(code)`** – executes a string as Python code (statements, not just expressions)
```python
exec("x = 5\nprint(x)")   # 5
```

**`compile(source, filename, mode)`** – compiles source into a code object (used before `eval`/`exec` for performance)
```python
code = compile("2 + 2", "<string>", "eval")
print(eval(code))   # 4
```

---

## 7. Class/Object Creation Helpers

**`object()`** – creates a bare, featureless object (the base of all classes)
```python
obj = object()
print(type(obj))   # <class 'object'>
```

**`super()`** – accesses methods of a parent class
```python
class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    def speak(self):
        return super().speak() + " -> Woof"

print(Dog().speak())   # Some sound -> Woof
```

**`property(fget, fset, fdel)`** – creates a managed attribute (usually used via `@property` decorator instead)
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    def get_radius(self):
        return self._radius

    radius = property(get_radius)

c = Circle(5)
print(c.radius)   # 5
```

**`classmethod(func)` / `staticmethod(func)`** – usually used as decorators, but callable directly too
```python
class MyClass:
    @classmethod
    def create(cls):
        return cls()

    @staticmethod
    def helper():
        return "helper called"
```

---

## 8. Miscellaneous but Frequently Used

**`open(filename, mode)`** – opens a file
```python
with open("example.txt", "w") as f:
    f.write("Hello, file!")
```

**`help(obj)`** – shows documentation for an object/function
```python
help(str.upper)   # prints docstring/usage info
```

**`globals()` / `locals()`** – return dictionaries of global/local variables
```python
x = 10
print("x" in globals())   # True

def foo():
    y = 5
    print(locals())   # {'y': 5}
foo()
```

**`hash(x)`** – returns the hash value of a hashable object
```python
print(hash("hello"))   # some integer (consistent within a run)
print(hash((1, 2)))     # tuples are hashable if their elements are
```

**`slice(start, stop, step)`** – creates a slice object (usable in indexing)
```python
lst = [0, 1, 2, 3, 4, 5]
s = slice(1, 4)
print(lst[s])   # [1, 2, 3]
```

**`memoryview(obj)`** – creates a memory view object for buffer protocol access (advanced, used for zero-copy slicing of bytes)
```python
data = bytearray(b"hello")
mv = memoryview(data)
print(mv[0])   # 104 (byte value of 'h')
```

**`ascii(obj)`** – returns a string with non-ASCII characters escaped
```python
print(ascii("café"))   # "'caf\\xe9'"
```

**`chr(i)` / `ord(c)`** – convert between Unicode code point and character
```python
print(chr(65))    # 'A'
print(ord("A"))   # 65
```

**`bin(n)` / `oct(n)` / `hex(n)`** – convert integer to binary/octal/hex string
```python
print(bin(10))   # '0b1010'
print(oct(10))   # '0o12'
print(hex(255))  # '0xff'
```

**`frozenset(iterable)`** – creates an immutable set
```python
fs = frozenset([1, 2, 3])
print(fs)   # frozenset({1, 2, 3})
```

**`delattr(obj, name)`** – deletes an attribute from an object
```python
class Foo:
    def __init__(self):
        self.x = 5

f = Foo()
delattr(f, "x")
print(hasattr(f, "x"))   # False
```

**`__import__(name)`** – programmatically imports a module (rarely used directly; prefer `import` statement or `importlib`)
```python
math_module = __import__("math")
print(math_module.sqrt(16))   # 4.0
```

---

## Quick Reference Table

| Function | Purpose |
|---|---|
| `int()`, `float()`, `str()`, `bool()` | Type conversion |
| `list()`, `tuple()`, `set()`, `dict()` | Collection conversion |
| `abs()`, `round()`, `pow()`, `divmod()` | Numeric operations |
| `sum()`, `min()`, `max()` | Aggregation |
| `len()`, `range()`, `enumerate()`, `zip()` | Sequence operations |
| `sorted()`, `reversed()` | Ordering |
| `map()`, `filter()` | Functional transforms |
| `any()`, `all()` | Boolean aggregation |
| `iter()`, `next()` | Iterator protocol |
| `type()`, `isinstance()`, `issubclass()` | Type checking |
| `id()`, `dir()`, `vars()` | Introspection |
| `hasattr()`, `getattr()`, `setattr()`, `delattr()` | Dynamic attribute access |
| `callable()` | Callability check |
| `print()`, `input()`, `format()`, `repr()` | I/O and representation |
| `eval()`, `exec()`, `compile()` | Dynamic code execution |
| `super()`, `property()`, `classmethod()`, `staticmethod()` | OOP helpers |
| `open()` | File handling |
| `help()`, `globals()`, `locals()` | Debugging/introspection |
| `hash()`, `slice()`, `memoryview()` | Low-level utilities |
| `chr()`, `ord()`, `bin()`, `oct()`, `hex()` | Character/number base conversion |
| `frozenset()` | Immutable set creation |


Python strings have a large set of built-in methods. Here's a comprehensive list grouped by category, each with an example.

## Case Conversion

- **`upper()`** – converts to uppercase
  `"hello".upper()` → `'HELLO'`
- **`lower()`** – converts to lowercase
  `"HELLO".lower()` → `'hello'`
- **`title()`** – capitalizes first letter of each word
  `"hello world".title()` → `'Hello World'`
- **`capitalize()`** – capitalizes only the first character
  `"hello world".capitalize()` → `'Hello world'`
- **`swapcase()`** – swaps upper/lower case
  `"Hello".swapcase()` → `'hELLO'`
- **`casefold()`** – aggressive lowercase for caseless matching (handles special Unicode cases better than `lower()`)
  `"Straße".casefold()` → `'strasse'`

## Searching & Checking

- **`find(sub)`** – returns index of first occurrence, or `-1` if not found
  `"hello world".find("world")` → `6`
- **`rfind(sub)`** – like `find()` but searches from the right
  `"hello world hello".rfind("hello")` → `12`
- **`index(sub)`** – same as `find()` but raises `ValueError` if not found
  `"hello".index("l")` → `2`
- **`count(sub)`** – counts non-overlapping occurrences
  `"banana".count("a")` → `3`
- **`startswith(prefix)`** – checks prefix match
  `"hello.py".startswith("hello")` → `True`
- **`endswith(suffix)`** – checks suffix match
  `"hello.py".endswith(".py")` → `True`
- **`in` operator** – substring membership test
  `"lo" in "hello"` → `True`

## Type/Content Checks

- **`isalpha()`** – all characters are alphabetic
  `"Hello".isalpha()` → `True`
- **`isdigit()`** – all characters are digits
  `"123".isdigit()` → `True`
- **`isalnum()`** – all characters are alphanumeric
  `"abc123".isalnum()` → `True`
- **`isspace()`** – all characters are whitespace
  `"   ".isspace()` → `True`
- **`isupper()`** – all cased characters are uppercase
  `"HELLO".isupper()` → `True`
- **`islower()`** – all cased characters are lowercase
  `"hello".islower()` → `True`
- **`istitle()`** – string follows title-case rules
  `"Hello World".istitle()` → `True`
- **`isnumeric()`** – all characters are numeric (includes fractions, superscripts, etc.)
  `"½".isnumeric()` → `True`
- **`isdecimal()`** – all characters are decimal digits (stricter than `isdigit`)
  `"123".isdecimal()` → `True`
- **`isidentifier()`** – valid as a Python identifier
  `"my_var".isidentifier()` → `True`
- **`isprintable()`** – all characters are printable
  `"hello\n".isprintable()` → `False`

## Trimming & Padding

- **`strip()`** – removes leading/trailing whitespace (or given characters)
  `"  hello  ".strip()` → `'hello'`
- **`lstrip()`** – removes from the left only
  `"  hello".lstrip()` → `'hello'`
- **`rstrip()`** – removes from the right only
  `"hello  ".rstrip()` → `'hello'`
- **`strip(chars)`** – removes specified characters
  `"xxhelloxx".strip("x")` → `'hello'`
- **`ljust(width)`** – left-justify, pad on the right
  `"hi".ljust(5, "*")` → `'hi***'`
- **`rjust(width)`** – right-justify, pad on the left
  `"hi".rjust(5, "*")` → `'***hi'`
- **`center(width)`** – center the string, pad both sides
  `"hi".center(6, "-")` → `'--hi--'`
- **`zfill(width)`** – pad with leading zeros (useful for numbers)
  `"42".zfill(5)` → `'00042'`

## Splitting & Joining

- **`split(sep)`** – splits into a list on a delimiter (default: whitespace)
  `"a,b,c".split(",")` → `['a', 'b', 'c']`
- **`rsplit(sep, maxsplit)`** – splits from the right
  `"a,b,c".rsplit(",", 1)` → `['a,b', 'c']`
- **`splitlines()`** – splits on line boundaries
  `"line1\nline2".splitlines()` → `['line1', 'line2']`
- **`join(iterable)`** – joins elements with the string as separator
  `"-".join(["a", "b", "c"])` → `'a-b-c'`
- **`partition(sep)`** – splits into a 3-tuple (before, sep, after) on first occurrence
  `"key=value".partition("=")` → `('key', '=', 'value')`
- **`rpartition(sep)`** – like `partition()` but splits on last occurrence
  `"a=b=c".rpartition("=")` → `('a=b', '=', 'c')`

## Replacing & Modifying

- **`replace(old, new)`** – replaces all occurrences
  `"hello world".replace("world", "there")` → `'hello there'`
- **`replace(old, new, count)`** – replaces only first `count` occurrences
  `"aaa".replace("a", "b", 2)` → `'bba'`
- **`translate(table)`** – maps characters using a translation table
  `"hello".translate(str.maketrans("el", "ip"))` → `'hippo'`
- **`maketrans(x, y)`** – builds a translation table (used with `translate()`, shown above)

## Formatting

- **f-strings** – embed expressions directly (Python 3.6+)
  `name = "Sam"; f"Hello, {name}!"` → `'Hello, Sam!'`
- **`format(*args)`** – template-based formatting
  `"Hello, {}!".format("Sam")` → `'Hello, Sam!'`
- **`format_map(dict)`** – like `format()` but takes a mapping directly
  `"Hello, {name}!".format_map({"name": "Sam"})` → `'Hello, Sam!'`
- **`%` operator** – old-style C printf formatting
  `"Hello, %s!" % "Sam"` → `'Hello, Sam!'`

## Encoding & Conversion

- **`encode(encoding)`** – converts string to bytes
  `"hello".encode("utf-8")` → `b'hello'`
- **`str(bytes_obj, encoding)`** / **`bytes.decode()`** – converts bytes back to string
  `b"hello".decode("utf-8")` → `'hello'`

## Other Useful Ones

- **`len(s)`** – gets string length (built-in function, not a method)
  `len("hello")` → `5`
- **`s[::-1]`** – reverse via slicing (not a method, but a very common idiom)
  `"hello"[::-1]` → `'olleh'`
- **`expandtabs(tabsize)`** – replaces tabs with spaces
  `"a\tb".expandtabs(4)` → `'a   b'`
- **`format_spec` mini-language in f-strings** – e.g. number formatting
  `f"{3.14159:.2f}"` → `'3.14'`


# Python Built-in Features: List & Dict (with Examples)

---

## PART 1: LIST

Lists are ordered, mutable, allow duplicates, and can hold mixed data types.

### Adding Elements

**`append(x)`** – adds a single element to the end
```python
lst = [1, 2, 3]
lst.append(4)
print(lst)   # [1, 2, 3, 4]
```

**`extend(iterable)`** – adds each element of an iterable to the end
```python
lst = [1, 2]
lst.extend([3, 4])
print(lst)   # [1, 2, 3, 4]
```

**`insert(index, x)`** – inserts an element at a specific position
```python
lst = [1, 2, 4]
lst.insert(2, 3)
print(lst)   # [1, 2, 3, 4]
```

### Removing Elements

**`remove(x)`** – removes the first matching value (raises `ValueError` if not found)
```python
lst = [1, 2, 3, 2]
lst.remove(2)
print(lst)   # [1, 3, 2]
```

**`pop(index)`** – removes and returns element at index (default: last element)
```python
lst = [1, 2, 3]
val = lst.pop()
print(val, lst)   # 3 [1, 2]
```

**`clear()`** – removes all elements
```python
lst = [1, 2, 3]
lst.clear()
print(lst)   # []
```

**`del` statement** – deletes by index or slice (not a method, but essential)
```python
lst = [1, 2, 3, 4]
del lst[1]
print(lst)   # [1, 3, 4]
```

### Searching & Counting

**`index(x)`** – returns index of first occurrence (raises `ValueError` if absent)
```python
lst = [10, 20, 30, 20]
print(lst.index(20))   # 1
```

**`count(x)`** – counts occurrences of a value
```python
lst = [1, 2, 2, 3, 2]
print(lst.count(2))   # 3
```

**`in` operator** – membership test
```python
lst = [1, 2, 3]
print(2 in lst)   # True
```

### Ordering

**`sort()`** – sorts the list in place (ascending by default)
```python
lst = [3, 1, 2]
lst.sort()
print(lst)   # [1, 2, 3]
```

**`sort(reverse=True)`** – sorts in descending order
```python
lst = [3, 1, 2]
lst.sort(reverse=True)
print(lst)   # [3, 2, 1]
```

**`sort(key=...)`** – sorts using a custom key function
```python
words = ["banana", "kiwi", "apple"]
words.sort(key=len)
print(words)   # ['kiwi', 'apple', 'banana']
```

**`sorted(lst)`** – built-in function; returns a new sorted list (original unchanged)
```python
lst = [3, 1, 2]
new_lst = sorted(lst)
print(new_lst, lst)   # [1, 2, 3] [3, 1, 2]
```

**`reverse()`** – reverses the list in place
```python
lst = [1, 2, 3]
lst.reverse()
print(lst)   # [3, 2, 1]
```

**`reversed(lst)`** – built-in function; returns a reverse iterator
```python
lst = [1, 2, 3]
print(list(reversed(lst)))   # [3, 2, 1]
```

### Copying

**`copy()`** – returns a shallow copy
```python
lst = [1, 2, 3]
new_lst = lst.copy()
new_lst.append(4)
print(lst, new_lst)   # [1, 2, 3] [1, 2, 3, 4]
```

**`list[:]`** – slicing also creates a shallow copy
```python
lst = [1, 2, 3]
copy_lst = lst[:]
```

**`copy.deepcopy(lst)`** – deep copy (from the `copy` module), for nested lists
```python
import copy
lst = [[1, 2], [3, 4]]
deep = copy.deepcopy(lst)
deep[0][0] = 99
print(lst)    # [[1, 2], [3, 4]] (unchanged)
```

### Other Built-in Functions Used with Lists

**`len(lst)`** – returns number of elements
```python
print(len([1, 2, 3]))   # 3
```

**`sum(lst)`** – sums numeric elements
```python
print(sum([1, 2, 3]))   # 6
```

**`min(lst)` / `max(lst)`** – smallest/largest element
```python
print(min([3, 1, 2]), max([3, 1, 2]))   # 1 3
```

**`any(lst)` / `all(lst)`** – True if any/all elements are truthy
```python
print(any([0, 0, 1]))   # True
print(all([1, 1, 1]))   # True
```

**`enumerate(lst)`** – pairs each element with its index
```python
for i, val in enumerate(["a", "b", "c"]):
    print(i, val)
# 0 a
# 1 b
# 2 c
```

**`zip(lst1, lst2)`** – pairs elements from multiple lists
```python
names = ["Sam", "Alex"]
ages = [25, 30]
print(list(zip(names, ages)))   # [('Sam', 25), ('Alex', 30)]
```

**`map(func, lst)`** – applies a function to every element
```python
print(list(map(str.upper, ["a", "b"])))   # ['A', 'B']
```

**`filter(func, lst)`** – filters elements matching a condition
```python
print(list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4])))   # [2, 4]
```

**List comprehension** – concise way to build/transform lists
```python
squares = [x**2 for x in range(5)]
print(squares)   # [0, 1, 4, 9, 16]
```

### Slicing

**`lst[start:stop:step]`** – extract a sub-list
```python
lst = [0, 1, 2, 3, 4, 5]
print(lst[1:4])     # [1, 2, 3]
print(lst[::2])     # [0, 2, 4]
print(lst[::-1])    # [5, 4, 3, 2, 1, 0]
```

### Nesting & Flattening

**Nested lists**
```python
matrix = [[1, 2], [3, 4]]
print(matrix[1][0])   # 3
```

**Flattening with comprehension**
```python
flat = [item for row in matrix for item in row]
print(flat)   # [1, 2, 3, 4]
```

---

## PART 2: DICT

Dictionaries store key-value pairs, are mutable, and (since Python 3.7) preserve insertion order.

### Creating & Accessing

**Dict literal / `dict()` constructor**
```python
d = {"a": 1, "b": 2}
d2 = dict(a=1, b=2)
```

**Accessing by key**
```python
d = {"name": "Sam", "age": 25}
print(d["name"])   # Sam
```

**`get(key, default)`** – safe access; returns `default` (or `None`) if key missing
```python
d = {"name": "Sam"}
print(d.get("age"))         # None
print(d.get("age", 0))      # 0
```

### Adding & Updating

**Assignment** – add or overwrite a key
```python
d = {"name": "Sam"}
d["age"] = 25
print(d)   # {'name': 'Sam', 'age': 25}
```

**`update(other_dict)`** – merges another dict (or iterable of pairs) into this one
```python
d = {"a": 1}
d.update({"b": 2, "c": 3})
print(d)   # {'a': 1, 'b': 2, 'c': 3}
```

**`setdefault(key, default)`** – returns value if key exists, else sets and returns default
```python
d = {"a": 1}
d.setdefault("b", 2)
print(d)   # {'a': 1, 'b': 2}
```

**Merge operator `|` (Python 3.9+)** – merges two dicts into a new one
```python
d1 = {"a": 1}
d2 = {"b": 2}
merged = d1 | d2
print(merged)   # {'a': 1, 'b': 2}
```

**In-place merge operator `|=`**
```python
d1 = {"a": 1}
d1 |= {"b": 2}
print(d1)   # {'a': 1, 'b': 2}
```

### Removing

**`pop(key, default)`** – removes key and returns its value (or default if missing)
```python
d = {"a": 1, "b": 2}
val = d.pop("a")
print(val, d)   # 1 {'b': 2}
```

**`popitem()`** – removes and returns the last inserted key-value pair (as a tuple)
```python
d = {"a": 1, "b": 2}
print(d.popitem())   # ('b', 2)
```

**`del d[key]`** – deletes a specific key
```python
d = {"a": 1, "b": 2}
del d["a"]
print(d)   # {'b': 2}
```

**`clear()`** – removes all key-value pairs
```python
d = {"a": 1, "b": 2}
d.clear()
print(d)   # {}
```

### Viewing Keys, Values, Items

**`keys()`** – returns a view of all keys
```python
d = {"a": 1, "b": 2}
print(list(d.keys()))   # ['a', 'b']
```

**`values()`** – returns a view of all values
```python
print(list(d.values()))   # [1, 2]
```

**`items()`** – returns a view of (key, value) pairs
```python
print(list(d.items()))   # [('a', 1), ('b', 2)]
```

**Iterating over a dict**
```python
d = {"a": 1, "b": 2}
for key, value in d.items():
    print(key, value)
# a 1
# b 2
```

### Checking Membership

**`in` operator** – checks if a key exists
```python
d = {"a": 1}
print("a" in d)      # True
print(1 in d.values())  # True
```

### Copying

**`copy()`** – shallow copy
```python
d = {"a": 1}
d2 = d.copy()
```

**`copy.deepcopy(d)`** – deep copy for nested dicts
```python
import copy
d = {"a": {"nested": 1}}
d2 = copy.deepcopy(d)
```

### Dict Comprehension

```python
squares = {x: x**2 for x in range(5)}
print(squares)   # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# with condition
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
```

### Class Methods

**`dict.fromkeys(iterable, value)`** – creates a dict with given keys, all set to the same value
```python
keys = ["a", "b", "c"]
d = dict.fromkeys(keys, 0)
print(d)   # {'a': 0, 'b': 0, 'c': 0}
```

### Useful Built-in Functions with Dicts

**`len(d)`** – number of key-value pairs
```python
d = {"a": 1, "b": 2}
print(len(d))   # 2
```

**`sorted(d)`** – sorts keys (returns a list)
```python
d = {"b": 2, "a": 1}
print(sorted(d))   # ['a', 'b']
```

**`sorted(d.items(), key=...)`** – sort by value
```python
d = {"a": 3, "b": 1, "c": 2}
print(sorted(d.items(), key=lambda x: x[1]))
# [('b', 1), ('c', 2), ('a', 3)]
```

**`max(d, key=d.get)` / `min(d, key=d.get)`** – find key with max/min value
```python
d = {"a": 3, "b": 1, "c": 2}
print(max(d, key=d.get))   # a
```

**`**` unpacking operator** – spreads dict as keyword arguments or merges dicts
```python
def greet(name, age):
    print(f"{name} is {age}")

d = {"name": "Sam", "age": 25}
greet(**d)   # Sam is 25

merged = {**{"a": 1}, **{"b": 2}}
print(merged)   # {'a': 1, 'b': 2}
```

### Related Specialized Dict Types (from `collections`)

**`defaultdict`** – auto-initializes missing keys
```python
from collections import defaultdict
d = defaultdict(int)
d["x"] += 1
print(d)   # defaultdict(<class 'int'>, {'x': 1})
```

**`Counter`** – dict subclass for counting hashable items
```python
from collections import Counter
c = Counter(["a", "b", "a"])
print(c)   # Counter({'a': 2, 'b': 1})
```

**`OrderedDict`** – dict that explicitly supports reordering
```python
from collections import OrderedDict
d = OrderedDict(a=1, b=2)
d.move_to_end("a")
print(d)   # OrderedDict([('b', 2), ('a', 1)])
```

---

## Quick Reference Tables

### List Methods
| Method | Purpose |
|---|---|
| `append(x)` | Add single element to end |
| `extend(iter)` | Add multiple elements to end |
| `insert(i, x)` | Insert at position |
| `remove(x)` | Remove first matching value |
| `pop(i)` | Remove & return element by index |
| `clear()` | Remove all elements |
| `index(x)` | Find index of value |
| `count(x)` | Count occurrences |
| `sort()` | Sort in place |
| `reverse()` | Reverse in place |
| `copy()` | Shallow copy |

### Dict Methods
| Method | Purpose |
|---|---|
| `get(k, default)` | Safe key access |
| `update(other)` | Merge another dict |
| `setdefault(k, default)` | Get or set default |
| `pop(k, default)` | Remove & return value |
| `popitem()` | Remove last inserted pair |
| `clear()` | Remove all pairs |
| `keys()` | View of keys |
| `values()` | View of values |
| `items()` | View of key-value pairs |
| `copy()` | Shallow copy |
| `fromkeys(keys, value)` | Build dict from keys |


# Python `collections` Module — Complete Guide with Use Cases

The `collections` module provides specialized container datatypes as alternatives to Python's general-purpose `dict`, `list`, `set`, and `tuple`.

```python
import collections
```

---

## 1. `Counter`

A dict subclass for counting hashable objects. Elements are stored as keys, counts as values.

### Basic Usage
```python
from collections import Counter

c = Counter(["apple", "banana", "apple", "orange", "banana", "apple"])
print(c)   # Counter({'apple': 3, 'banana': 2, 'orange': 1})
```

### Counting characters in a string
```python
c = Counter("mississippi")
print(c)   # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})
```

### Counting words in text
```python
text = "the quick brown fox jumps over the lazy dog the fox runs"
word_counts = Counter(text.split())
print(word_counts.most_common(2))
# [('the', 3), ('fox', 2)]
```

### Key Methods
```python
c = Counter(a=3, b=1, c=2)

print(c.most_common())        # [('a', 3), ('c', 2), ('b', 1)] - sorted by count
print(c.most_common(1))       # [('a', 3)] - top N
print(list(c.elements()))     # ['a', 'a', 'a', 'b', 'c', 'c'] - expand counts
c.update(["a", "d"])          # increment counts
print(c)                      # Counter({'a': 4, 'c': 2, 'b': 1, 'd': 1})
c.subtract(["a", "a"])        # decrement counts
print(c["a"])                 # 2
```

### Arithmetic Between Counters
```python
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)

print(c1 + c2)   # Counter({'a': 4, 'b': 3})
print(c1 - c2)   # Counter({'a': 2}) - negative/zero counts dropped
print(c1 & c2)   # Counter({'a': 1, 'b': 1}) - min of each
print(c1 | c2)   # Counter({'a': 3, 'b': 2}) - max of each
```

### Real Use Case: Finding the most common element / majority check
```python
def most_frequent(nums):
    return Counter(nums).most_common(1)[0][0]

print(most_frequent([1, 3, 2, 3, 3, 1]))   # 3
```

### Real Use Case: Anagram check
```python
def is_anagram(s1, s2):
    return Counter(s1) == Counter(s2)

print(is_anagram("listen", "silent"))   # True
```

---

## 2. `defaultdict`

A dict subclass that auto-initializes a default value for missing keys instead of raising `KeyError`.

### Basic Usage
```python
from collections import defaultdict

d = defaultdict(int)   # default value 0
d["apple"] += 1
d["apple"] += 1
d["banana"] += 1
print(d)   # defaultdict(<class 'int'>, {'apple': 2, 'banana': 1})
```

### Grouping Data (very common use case)
```python
words = ["apple", "bat", "bar", "atom", "book"]
groups = defaultdict(list)

for word in words:
    groups[word[0]].append(word)

print(dict(groups))
# {'a': ['apple', 'atom'], 'b': ['bat', 'bar', 'book']}
```

### Nested defaultdict (auto-vivification of multi-level structures)
```python
tree = lambda: defaultdict(tree)
graph = tree()
graph["a"]["b"]["c"] = 1   # no need to pre-create nested dicts
print(graph)
```

### With `set` as default (deduplicated grouping)
```python
d = defaultdict(set)
d["fruits"].add("apple")
d["fruits"].add("apple")   # duplicate ignored
d["fruits"].add("banana")
print(d)   # defaultdict(<class 'set'>, {'fruits': {'apple', 'banana'}})
```

### Real Use Case: Building an adjacency list for a graph
```python
edges = [("A", "B"), ("A", "C"), ("B", "C")]
graph = defaultdict(list)

for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)

print(dict(graph))
# {'A': ['B', 'C'], 'B': ['A', 'C'], 'C': ['A', 'B']}
```

---

## 3. `OrderedDict`

A dict subclass that remembers insertion order explicitly and provides extra order-related methods. (Regular dicts preserve order since Python 3.7, but `OrderedDict` still offers `move_to_end()` and stricter order-sensitive equality.)

### Basic Usage
```python
from collections import OrderedDict

d = OrderedDict()
d["banana"] = 3
d["apple"] = 4
d["orange"] = 2
print(d)   # OrderedDict([('banana', 3), ('apple', 4), ('orange', 2)])
```

### `move_to_end()`
```python
d = OrderedDict(a=1, b=2, c=3)
d.move_to_end("a")
print(d)   # OrderedDict([('b', 2), ('c', 3), ('a', 1)])

d.move_to_end("c", last=False)   # move to the front instead
print(d)   # OrderedDict([('c', 3), ('b', 2), ('a', 1)])
```

### Order-sensitive equality (key difference vs regular dict)
```python
d1 = OrderedDict(a=1, b=2)
d2 = OrderedDict(b=2, a=1)
print(d1 == d2)          # False (order matters)

reg1 = {"a": 1, "b": 2}
reg2 = {"b": 2, "a": 1}
print(reg1 == reg2)      # True (regular dict ignores order in equality)
```

### Real Use Case: Implementing an LRU Cache
```python
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
            self.cache.popitem(last=False)   # evict least recently used

cache = LRUCache(2)
cache.put(1, "a")
cache.put(2, "b")
cache.get(1)          # marks 1 as recently used
cache.put(3, "c")     # evicts 2 (least recently used)
print(dict(cache.cache))   # {1: 'a', 3: 'c'}
```

---

## 4. `namedtuple`

Creates tuple subclasses with named fields — lightweight, immutable, readable objects (a simple alternative to a full class).

### Basic Usage
```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)     # 3 4
print(p)            # Point(x=3, y=4)
print(p[0], p[1])   # still supports index access -> 3 4
```

### Field names as a string (alternative syntax)
```python
Person = namedtuple("Person", "name age city")
p = Person("Sam", 25, "NYC")
print(p.name, p.age, p.city)   # Sam 25 NYC
```

### Immutability
```python
p = Point(1, 2)
# p.x = 5   # AttributeError: can't set attribute
p2 = p._replace(x=5)   # create a modified copy instead
print(p2)   # Point(x=5, y=2)
```

### Converting to/from dict
```python
p = Point(1, 2)
print(p._asdict())    # {'x': 1, 'y': 2}

d = {"x": 10, "y": 20}
p2 = Point(**d)
print(p2)   # Point(x=10, y=20)
```

### Default values
```python
Employee = namedtuple("Employee", ["name", "role", "salary"], defaults=["Unassigned", 0])
e = Employee("Sam")
print(e)   # Employee(name='Sam', role='Unassigned', salary=0)
```

### Real Use Case: Representing rows from a database/CSV without full class overhead
```python
Employee = namedtuple("Employee", ["id", "name", "dept"])
rows = [(1, "Sam", "Eng"), (2, "Alex", "Sales")]
employees = [Employee(*row) for row in rows]

for emp in employees:
    print(f"{emp.name} works in {emp.dept}")
```

---

## 5. `deque` (Double-Ended Queue)

Provides O(1) appends and pops from BOTH ends (unlike `list`, where `insert(0, x)`/`pop(0)` are O(n)).

### Basic Usage
```python
from collections import deque

d = deque([1, 2, 3])
d.append(4)          # add to right
d.appendleft(0)       # add to left
print(d)   # deque([0, 1, 2, 3, 4])

d.pop()               # remove from right -> 4
d.popleft()           # remove from left -> 0
print(d)   # deque([1, 2, 3])
```

### Rotating
```python
d = deque([1, 2, 3, 4, 5])
d.rotate(2)     # rotate right by 2
print(d)        # deque([4, 5, 1, 2, 3])

d.rotate(-2)    # rotate left by 2
print(d)        # deque([1, 2, 3, 4, 5])
```

### Bounded deque (fixed-size, auto-discards oldest)
```python
d = deque(maxlen=3)
for i in range(5):
    d.append(i)
print(d)   # deque([2, 3, 4], maxlen=3) - oldest values dropped
```

### Real Use Case: Implementing a queue (FIFO) for BFS
```python
graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}

def bfs(start):
    visited = {start}
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

print(bfs("A"))   # ['A', 'B', 'C', 'D']
```

### Real Use Case: Sliding window (last N items seen)
```python
def moving_average(stream, window_size):
    window = deque(maxlen=window_size)
    averages = []
    for val in stream:
        window.append(val)
        averages.append(sum(window) / len(window))
    return averages

print(moving_average([1, 2, 3, 4, 5], 3))
# [1.0, 1.5, 2.0, 3.0, 4.0]
```

### Real Use Case: Undo/Redo history with bounded size
```python
history = deque(maxlen=5)   # keep only last 5 actions
history.append("action1")
history.append("action2")
```

---

## 6. `ChainMap`

Groups multiple dictionaries (or mappings) into a single view, searching them in order without merging/copying data.

### Basic Usage
```python
from collections import ChainMap

defaults = {"theme": "light", "language": "en"}
user_settings = {"theme": "dark"}

combined = ChainMap(user_settings, defaults)
print(combined["theme"])       # dark (found in first dict)
print(combined["language"])    # en (falls back to second dict)
```

### Updates only affect the first mapping
```python
combined["language"] = "fr"
print(user_settings)   # {'theme': 'dark', 'language': 'fr'}
print(defaults)        # {'theme': 'light', 'language': 'en'} - unchanged
```

### Adding a new layer
```python
cli_args = {"theme": "solarized"}
combined2 = combined.new_child(cli_args)
print(combined2["theme"])   # solarized (cli_args takes priority)
```

### Real Use Case: Layered configuration (CLI args > env vars > config file > defaults)
```python
import os

defaults = {"debug": False, "port": 8080}
config_file = {"port": 9090}
env_vars = {k: v for k, v in os.environ.items() if k in defaults}
cli_args = {}   # e.g., parsed from argparse

settings = ChainMap(cli_args, env_vars, config_file, defaults)
print(settings["port"])   # 9090 (from config_file, since cli_args/env don't override it)
```

---

## 7. `UserDict`, `UserList`, `UserString`

Wrapper classes designed to be subclassed when you want to customize dict/list/string behavior — safer than subclassing `dict`/`list`/`str` directly because internal methods consistently call your overridden methods.

### `UserDict` – Example: a dict with case-insensitive keys
```python
from collections import UserDict

class CaseInsensitiveDict(UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super().__getitem__(key.lower())

d = CaseInsensitiveDict()
d["Name"] = "Sam"
print(d["name"])   # Sam
print(d["NAME"])   # Sam
```

### `UserList` – Example: a list that logs changes
```python
from collections import UserList

class LoggingList(UserList):
    def append(self, item):
        print(f"Adding: {item}")
        super().append(item)

lst = LoggingList([1, 2, 3])
lst.append(4)
# Output: Adding: 4
print(lst)   # [1, 2, 3, 4]
```

### `UserString` – Example: a string that tracks modification count
```python
from collections import UserString

class TrackedString(UserString):
    def __init__(self, value):
        super().__init__(value)
        self.modifications = 0

    def upper(self):
        self.modifications += 1
        return super().upper()

s = TrackedString("hello")
print(s.upper())          # HELLO
print(s.modifications)    # 1
```

---

## Quick Reference Table

| Class | Purpose | Common Use Case |
|---|---|---|
| `Counter` | Count hashable items | Word frequency, majority element, anagram check |
| `defaultdict` | Dict with auto-default values | Grouping data, adjacency lists, avoiding `KeyError` |
| `OrderedDict` | Order-aware dict with extra methods | LRU cache, order-sensitive comparisons |
| `namedtuple` | Lightweight immutable objects with named fields | Representing rows/records, readable tuples |
| `deque` | Double-ended queue, O(1) both ends | BFS queues, sliding windows, undo history |
| `ChainMap` | View over multiple dicts, no merging | Layered configuration (CLI > env > file > defaults) |
| `UserDict/List/String` | Base classes for safe subclassing | Custom dict/list/string behaviors |

---

## Summary: When to Use What

- **Need to count things?** → `Counter`
- **Need a dict that "just works" without checking key existence?** → `defaultdict`
- **Need to remember/manipulate insertion order explicitly (e.g., LRU)?** → `OrderedDict`
- **Need a simple, readable, immutable record type?** → `namedtuple`
- **Need fast appends/pops from both ends (queue/stack behavior)?** → `deque`
- **Need to search across multiple config sources without merging them?** → `ChainMap`
- **Need to safely customize dict/list/str behavior?** → `UserDict` / `UserList` / `UserString`


  # Python `functools`, `itertools`, `heapq` & `deque` — Complete Guide with Examples

---

## PART 1: `functools`

Tools for working with functions and higher-order operations (functions that act on/return other functions).

```python
import functools
```

### `functools.lru_cache` — Memoization Cache

Automatically caches function results based on arguments, avoiding recomputation.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(30))          # fast, thanks to caching
print(fib.cache_info())  # CacheInfo(hits=28, misses=31, maxsize=None, currsize=31)
fib.cache_clear()        # clear the cache manually
```
**Use case:** Speeding up recursive algorithms (Fibonacci, DP problems), expensive API/database calls with repeated arguments.

### `functools.cache` (Python 3.9+) — Simpler unlimited cache
```python
from functools import cache

@cache
def square(x):
    return x * x
```

### `functools.wraps` — Preserving Metadata in Decorators

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)   # preserves func.__name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet():
    """Greets the user"""
    print("Hello")

print(greet.__name__)   # 'greet' (without @wraps it would be 'wrapper')
print(greet.__doc__)    # 'Greets the user'
```
**Use case:** Always use in custom decorators — prevents losing introspection/debugging info of the original function.

### `functools.reduce` — Cumulative Reduction

```python
from functools import reduce

nums = [1, 2, 3, 4]
product = reduce(lambda x, y: x * y, nums)
print(product)   # 24

# with initial value
total = reduce(lambda acc, x: acc + x, nums, 100)
print(total)   # 110
```
**Use case:** Aggregating a list into a single value (product, running max, merging dicts) when a simple loop/sum() isn't expressive enough.

```python
# Real use: find the max via reduce
max_val = reduce(lambda a, b: a if a > b else b, [3, 7, 2, 9, 4])
print(max_val)   # 9
```

### `functools.partial` — Partial Function Application

Creates a new function with some arguments pre-filled.

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))   # 25
print(cube(2))     # 8
```
**Use case:** Simplifying repeated calls with fixed arguments — common in callbacks, GUI event handlers, or configuring library functions.

```python
# Real use: pre-configuring a function for map()
nums = [1, 2, 3, 4]
add_10 = partial(lambda x, y: x + y, y=10)
print(list(map(add_10, nums)))   # [11, 12, 13, 14]
```

### `functools.total_ordering` — Auto-generate Comparison Methods

Given `__eq__` and one ordering method (e.g. `__lt__`), fills in the rest (`__le__`, `__gt__`, `__ge__`).

```python
from functools import total_ordering

@total_ordering
class Employee:
    def __init__(self, salary):
        self.salary = salary

    def __eq__(self, other):
        return self.salary == other.salary

    def __lt__(self, other):
        return self.salary < other.salary

e1 = Employee(50000)
e2 = Employee(60000)
print(e1 < e2, e1 > e2, e1 <= e2)   # True False True
```
**Use case:** Custom classes needing full comparison support (sorting, `min()`/`max()`) without writing all 5 dunder methods manually.

### `functools.cmp_to_key` — Using Old-Style Comparator Functions with `sorted()`

```python
from functools import cmp_to_key

def compare(a, b):
    return a - b   # negative, zero, positive

nums = [5, 2, 4, 1]
sorted_nums = sorted(nums, key=cmp_to_key(compare))
print(sorted_nums)   # [1, 2, 4, 5]
```
**Use case:** Complex custom sort logic that's hard to express as a simple `key=` function (e.g., sort strings by comparing concatenations, like "largest number formed by arranging list").

### `functools.singledispatch` — Function Overloading Based on Argument Type

```python
from functools import singledispatch

@singledispatch
def process(value):
    print(f"Default: {value}")

@process.register
def _(value: int):
    print(f"Integer: {value * 2}")

@process.register
def _(value: str):
    print(f"String: {value.upper()}")

process(10)        # Integer: 20
process("hello")   # String: HELLO
process(3.14)       # Default: 3.14
```
**Use case:** Writing type-specific logic cleanly instead of long `isinstance()` chains — common in serialization/formatting libraries.

### `functools.reduce` vs Built-in Alternatives (Quick Comparison)
```python
nums = [1, 2, 3, 4]
print(sum(nums))                              # 10 (built-in, preferred for sums)
print(reduce(lambda a, b: a + b, nums))        # 10 (equivalent, more general purpose)
```

---

## PART 2: `itertools`

Efficient, memory-friendly building blocks for constructing iterators.

```python
import itertools
```

### `itertools.count` — Infinite Counter
```python
from itertools import count, islice

counter = count(start=10, step=2)
print(list(islice(counter, 5)))   # [10, 12, 14, 16, 18]
```
**Use case:** Generating IDs, or as a counter in combination with `zip()` for indexing.

### `itertools.cycle` — Infinite Repeating Cycle
```python
from itertools import cycle, islice

colors = cycle(["red", "green", "blue"])
print(list(islice(colors, 7)))
# ['red', 'green', 'blue', 'red', 'green', 'blue', 'red']
```
**Use case:** Round-robin task assignment, repeating patterns.

### `itertools.repeat` — Repeat a Value N Times (or infinitely)
```python
from itertools import repeat
print(list(repeat("x", 3)))   # ['x', 'x', 'x']

# common with map() for fixed second argument
print(list(map(pow, [1, 2, 3], repeat(2))))   # [1, 4, 9]
```

### `itertools.chain` — Combine Multiple Iterables
```python
from itertools import chain

a = [1, 2]
b = [3, 4]
c = [5]
print(list(chain(a, b, c)))   # [1, 2, 3, 4, 5]
```
**Use case:** Flattening a list of lists / iterating over multiple collections as if they were one.
```python
nested = [[1, 2], [3, 4], [5]]
flat = list(chain.from_iterable(nested))
print(flat)   # [1, 2, 3, 4, 5]
```

### `itertools.compress` — Filter by a Boolean Mask
```python
from itertools import compress

data = ["a", "b", "c", "d"]
mask = [1, 0, 1, 0]
print(list(compress(data, mask)))   # ['a', 'c']
```

### `itertools.dropwhile` / `takewhile`
```python
from itertools import dropwhile, takewhile

nums = [1, 2, 3, 10, 4, 5]
print(list(takewhile(lambda x: x < 5, nums)))   # [1, 2, 3]
print(list(dropwhile(lambda x: x < 5, nums)))   # [10, 4, 5]
```
**Use case:** Extracting a prefix/suffix from data based on a condition (e.g., parsing log lines until an error appears).

### `itertools.groupby` — Group Consecutive Items by Key
```python
from itertools import groupby

data = [1, 1, 2, 2, 2, 3, 1, 1]
for key, group in groupby(data):
    print(key, list(group))
# 1 [1, 1]
# 2 [2, 2, 2]
# 3 [3]
# 1 [1, 1]
```
**Important:** `groupby` only groups *consecutive* items, so data usually needs sorting first for full grouping.
```python
words = ["apple", "banana", "avocado", "blueberry", "cherry"]
words.sort(key=lambda w: w[0])
for key, group in groupby(words, key=lambda w: w[0]):
    print(key, list(group))
# a ['apple', 'avocado']
# b ['banana', 'blueberry']
# c ['cherry']
```
**Use case:** Grouping log entries by date, grouping records by category after sorting.

### `itertools.permutations` — All Orderings
```python
from itertools import permutations

print(list(permutations([1, 2, 3])))
# [(1,2,3), (1,3,2), (2,1,3), (2,3,1), (3,1,2), (3,2,1)]

print(list(permutations([1, 2, 3], 2)))   # length-2 permutations
# [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]
```
**Use case:** Brute-force problems (traveling salesman on small inputs), generating all possible arrangements (anagram generation, password guessing for CTFs/security testing).

### `itertools.combinations` / `combinations_with_replacement`
```python
from itertools import combinations, combinations_with_replacement

print(list(combinations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 3)]

print(list(combinations_with_replacement([1, 2, 3], 2)))
# [(1,1), (1,2), (1,3), (2,2), (2,3), (3,3)]
```
**Use case:** Choosing subsets (e.g., pairs of teams, lottery combinations), generating test case combinations.

### `itertools.product` — Cartesian Product
```python
from itertools import product

print(list(product([1, 2], ["a", "b"])))
# [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

# with repeat for exponentiation-style combos
print(list(product([0, 1], repeat=3)))
# all 8 combinations of 3 binary digits
```
**Use case:** Generating all combinations of settings/parameters for testing, building coordinate grids, brute-forcing small search spaces.

### `itertools.accumulate` — Running Totals
```python
from itertools import accumulate
import operator

nums = [1, 2, 3, 4]
print(list(accumulate(nums)))                     # [1, 3, 6, 10] (running sum)
print(list(accumulate(nums, operator.mul)))       # [1, 2, 6, 24] (running product)
print(list(accumulate(nums, max)))                # [1, 2, 3, 4] (running max)
```
**Use case:** Prefix sums for range-sum queries, running balances/totals in financial data.

### `itertools.islice` — Slice an Iterator
```python
from itertools import islice

def infinite_numbers():
    n = 0
    while True:
        yield n
        n += 1

print(list(islice(infinite_numbers(), 5)))       # [0, 1, 2, 3, 4]
print(list(islice(infinite_numbers(), 2, 8, 2)))  # [2, 4, 6]
```
**Use case:** Taking a limited number of items from an infinite/large generator without consuming it all.

### `itertools.tee` — Split an Iterator into Multiple Independent Ones
```python
from itertools import tee

nums = iter([1, 2, 3])
it1, it2 = tee(nums, 2)
print(list(it1))   # [1, 2, 3]
print(list(it2))   # [1, 2, 3] (independent copy)
```
**Use case:** Iterating the same data stream for two different purposes without re-fetching from source.

### `itertools.zip_longest` — Zip Without Truncating to the Shortest
```python
from itertools import zip_longest

a = [1, 2, 3]
b = ["x", "y"]
print(list(zip_longest(a, b, fillvalue="-")))
# [(1, 'x'), (2, 'y'), (3, '-')]
```
**Use case:** Aligning unequal-length datasets (e.g., merging columns of different lengths, padding for CSV export).

---

## PART 3: `heapq`

Implements a binary min-heap on top of a regular Python list. Provides O(log n) push/pop.

```python
import heapq
```

### Basic Heap Operations
```python
nums = [5, 1, 8, 3, 2]
heapq.heapify(nums)          # convert list into a heap in place, O(n)
print(nums)                  # [1, 2, 8, 3, 5] (heap-ordered, not fully sorted)

heapq.heappush(nums, 0)      # push a new item, O(log n)
print(heapq.heappop(nums))   # 0 (removes & returns smallest), O(log n)
```

### `heappushpop` and `heapreplace`
```python
nums = [2, 4, 6]
heapq.heapify(nums)

print(heapq.heappushpop(nums, 1))   # 1 - pushes then pops (efficient if new item is smaller)
print(heapq.heapreplace(nums, 5))   # 2 - pops then pushes (always removes something)
```

### `nlargest` / `nsmallest` — Top-K Elements
```python
nums = [5, 1, 8, 3, 2, 9, 4]
print(heapq.nlargest(3, nums))    # [9, 8, 5]
print(heapq.nsmallest(3, nums))   # [1, 2, 3]

# with a key function
data = [{"name": "A", "score": 50}, {"name": "B", "score": 90}, {"name": "C", "score": 70}]
print(heapq.nlargest(2, data, key=lambda x: x["score"]))
# [{'name': 'B', 'score': 90}, {'name': 'C', 'score': 70}]
```
**Use case:** Finding top-K largest/smallest elements more efficiently than sorting the entire list — O(n log k) instead of O(n log n).

### Real Use Case: Priority Queue (task scheduling by priority)
```python
tasks = []
heapq.heappush(tasks, (2, "Write report"))
heapq.heappush(tasks, (1, "Fix critical bug"))
heapq.heappush(tasks, (3, "Attend meeting"))

while tasks:
    priority, task = heapq.heappop(tasks)
    print(f"Priority {priority}: {task}")
# Priority 1: Fix critical bug
# Priority 2: Write report
# Priority 3: Attend meeting
```

### Real Use Case: Max-Heap (Python's heapq is min-heap only — negate values)
```python
nums = [5, 1, 8, 3]
max_heap = [-n for n in nums]
heapq.heapify(max_heap)
print(-heapq.heappop(max_heap))   # 8 (the actual max)
```

### Real Use Case: Merging K Sorted Lists
```python
def merge_k_sorted(lists):
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    result = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    return result

print(merge_k_sorted([[1, 4, 7], [2, 5, 8], [3, 6, 9]]))
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Real Use Case: Finding the Median from a Data Stream (two-heap technique)
```python
class MedianFinder:
    def __init__(self):
        self.small = []   # max-heap (negated) for lower half
        self.large = []   # min-heap for upper half

    def add_num(self, num):
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def find_median(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2

mf = MedianFinder()
for n in [5, 15, 1, 3]:
    mf.add_num(n)
print(mf.find_median())   # 4.0
```

---

## PART 4: `deque` (Deep Dive)

Already introduced in the collections guide — here's a focused deep-dive on `deque` specifically, since it's central to many interview problems.

```python
from collections import deque
```

### Why `deque` over `list`?
| Operation | `list` | `deque` |
|---|---|---|
| Append/pop from right | O(1) | O(1) |
| Append/pop from left | O(n) | O(1) |
| Random access by index | O(1) | O(n) |

**Rule of thumb:** Use `list` when you mostly need indexing/random access. Use `deque` when you mostly append/pop from both ends (queues, stacks, sliding windows).

### Core Operations
```python
d = deque([1, 2, 3])
d.append(4)            # [1, 2, 3, 4]
d.appendleft(0)         # [0, 1, 2, 3, 4]
d.pop()                 # removes 4 -> [0, 1, 2, 3]
d.popleft()             # removes 0 -> [1, 2, 3]
d.extend([4, 5])        # [1, 2, 3, 4, 5]
d.extendleft([0, -1])   # [-1, 0, 1, 2, 3, 4, 5] (note: reversed order!)
```

### Real Use Case: Implementing a Stack and a Queue with the Same Structure
```python
# As a stack (LIFO)
stack = deque()
stack.append(1)
stack.append(2)
print(stack.pop())   # 2

# As a queue (FIFO)
queue = deque()
queue.append(1)
queue.append(2)
print(queue.popleft())   # 1
```

### Real Use Case: Sliding Window Maximum (classic hard interview problem)
```python
def sliding_window_max(nums, k):
    dq = deque()   # stores indices, values in decreasing order
    result = []
    for i, n in enumerate(nums):
        while dq and nums[dq[-1]] < n:
            dq.pop()
        dq.append(i)
        if dq[0] == i - k:
            dq.popleft()
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result

print(sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))
# [3, 3, 5, 5, 6, 7]
```

### Real Use Case: Palindrome Check Using Deque
```python
def is_palindrome(s):
    d = deque(s)
    while len(d) > 1:
        if d.popleft() != d.pop():
            return False
    return True

print(is_palindrome("racecar"))   # True
```

### Real Use Case: Fixed-Size History / Recent Items Buffer
```python
recent_searches = deque(maxlen=3)
for term in ["python", "java", "sql", "rust"]:
    recent_searches.append(term)
print(list(recent_searches))   # ['java', 'sql', 'rust'] - oldest auto-dropped
```

---

## Quick Reference Summary

| Module | Best For |
|---|---|
| `functools.lru_cache` / `cache` | Memoizing expensive/recursive function calls |
| `functools.partial` | Pre-filling function arguments |
| `functools.reduce` | Cumulative aggregation of an iterable |
| `functools.wraps` | Preserving metadata in decorators |
| `functools.total_ordering` | Auto-generating comparison operators |
| `functools.singledispatch` | Type-based function overloading |
| `itertools.chain` | Combining/flattening multiple iterables |
| `itertools.groupby` | Grouping consecutive items by key |
| `itertools.permutations`/`combinations`/`product` | Generating arrangements/subsets/cartesian products |
| `itertools.islice` | Slicing generators/infinite iterators |
| `itertools.accumulate` | Running totals/prefix sums |
| `heapq` | Priority queues, top-K elements, merging sorted data, streaming median |
| `deque` | O(1) queue/stack operations, sliding windows, bounded history buffers |




