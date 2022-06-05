# Lox Langauge Project

The purpose of this project is to implement a basic programing langauge named "Lox" and write both an interpreter and compiler.

This is based on the book, [Crafting Interpreters](http://craftinginterpreters.com/) by Robert Nystrom.

My goal here is to build an intuitive sense for programming langauges, compilers, etc. I'll be building the interpreter in python (instead of java) and the virtual machine in c++ (instead of c).

## How to Run

```bash
# Initialize Environment
python3 -m venv .venv
source .venv/bin/activate
pip3 install pip --upgrade
pip3 install -r requirements.txt
```

## Language Specification

Lox is a super simple, dynamically typed OOP with single inheritance. It has C-like syntax (for familiarity).

Keywords List:

| Keyword     | Type       |
| ----------- | ---------- |
| `var`       | variable   |
| `true`      | variable   |
| `false`     | variable   |
| `.`         | variable   |
| `+`         | expression |
| `-`         | expression |
| `*`         | expression |
| `/`         | expression |
| `>`         | expression |
| `>=`        | expression |
| `<`         | expression |
| `<=`        | expression |
| `==`        | expression |
| `!=`        | expression |
| `!`         | operator   |
| `and`       | operator   |
| `or`        | operator   |
| `print`     | statement  |
| `{` and `}` | scope      |
| `(` and `)` | grouping   |
| `if`        | control    |
| `else`      | control    |
| `while`     | control    |
| `for`       | control    |
| `fun`       | functional |
| `,`         | functional |
| `return`    | functional |
| `;`         | functional |
| `class`     | classes    |
| `super`     | classes    |
| `this`      | classes    |
| `nil`       | variable   |

### Datatypes

| Datatype | Example         |
| -------- | --------------- |
| bool     | `true`, `false` |
| int      | `1337`          |
| double   | `1.337`         |
| string   | `"Hello"`       |
| nil      | `nil`           |

### Expressions

| Expression | Description    |
| ---------- | -------------- |
| `a + b`    | addition       |
| `a - b`    | subtraction    |
| `a * b`    | multiplication |
| `a / b`    | division       |
| `-a`       | negate         |

### Comparison and Equality

| Expression | Description           |
| ---------- | --------------------- |
| `a < b`    | less than             |
| `a <= b`   | less than or equal    |
| `a > b`    | greater than          |
| `a >= b`   | greater than or equal |
| `a == b`   | equal                 |
| `a != b`   | not equal             |

### Logical Operators

| Expression | Description  |
| ---------- | ------------ |
| `!a`       | not operator |
| `a and b`  | and operator |
| `a or b`   | or operator  |

### Precedence and Grouping

| Expression  | Description          |
| ----------- | -------------------- |
| `(` and `)` | grouping expressions |

### Statements and Scope

| Expression  | Description                  |
| ----------- | ---------------------------- |
| `print`     | prints string expression     |
| `{` and `}` | creates a "block" or "scope" |

### Variables

| Expression | Description        |
| ---------- | ------------------ |
| `var`      | declare a variable |

### Control Flow

| Expression   | Description            |
| ------------ | ---------------------- |
| `if`, `else` | if and else statements |
| `while`      | c-style while loops    |
| `for`        | c-style for loops      |

### Functions

Functions are real values that you can get a reference to, store in variables, pass around, etc.

| Expression           | Description                             |
| -------------------- | --------------------------------------- |
| `fun` foo`(a, b, c)` | function declaration and arguement list |
| `return`             | return a variable from a function       |

Examples:

```js
fun addPair(a, b)
{
    return a + b;
}

fun identity(a)
{
    return a;
}

print identity(addPair)(1, 2); // prints "3"

fun outer(a, b)
{
    var outside = "outer variable";
    
    // prints "outer variable" and "inner"
    fun inner()
    {
        print outside;
        print "inner";
    }

    // Returns the internal function
    return inner;
}

var fn = someFunc();
fn();
```

### Classes

Classes are very js or python like. They have an `init` function that can be overriden as the constructor to the class. Class methods do not use the `fun` function keyword, you just define them 

```js
class Animal
{
    init(name)
    {
        this.name = name;
    }

    name()
    {
        return this.name;
    }

    speak()
    {
        return "The " + name() + " says ";  
    }
}

// Inheritance
class Dog < Animal
{
    init()
    {
        super.init("dog");
    }

    // override
    speak()
    {
        // Call to the superclass's implementation
        return super.speak() + "bark";
    }
}

// Store class as a variable
var classAsVariable = Animal;

// Pass a class into a function
foo(Animal);

// Instantiate class
var animal = Dog();
print animal.speak(); // prints "The dog says bark"
```
