# Simplipy-Python

## How to use

### **Command**

```python
from simplipy_python import Command

def PrintArgs(Arguments):
    print(Arguments)

CommandHandler = Command(CommandMessage="Run> ", StarterMessage=None) # StarterMessage is Optional.
CommandHandler.AddCommand(command_name="Print Arguments", command_function=PrintArgs)
CommandHandler.SetupCommands() # Setup Command Module.
```

It should look like this:
<br>
![Image of what it'll look like](https://i.imgur.com/9Za6hxE.png "Image of Simplipy")

### **Category**

```python
from simplipy_python import Command, Category

def PrintArgs(Arguments):
    print(Arguments)

def PrintArgsCategory(Arguments):
    print(f"Category {Arguments}")

CommandHandler = Command(CommandMessage="Run> ", StarterMessage="Category Test!!!")
CommandHandler.AddCommand(command_name="Print Arguments", command_function=PrintArgs)

Category1 = Category(category_name="Other Functions") # Create Category
Category1.AddCommand(command_name="Print Arguments 1", command_function=PrintArgsCategory) # Add Function

CommandHandler.SetupCommands(Categories=[Category1]) # Inject the Categories into the Setup
```

**BEFORE TRYING THIS, PLEASE TYPE IN THE CATEGORY NAME**
<br>
_Case Sensitive_

```
Commands Run> Other-Functions
```

Should look like this:
<br>
![Image of what it'll look like](https://i.imgur.com/7jHtD8r.png "Image of Simplipy Category")

### Help Command
```cmd
$ python filename.py -h

usage: prog.py [-h] [--changelog]

options:
  -h, --help     show this help message and exit
  -cl, --changelog      The python package's changelog
```

## Exceptions

### NotValidCommand
Is raised when you input an invalid Command.

### CommandNameAlreadyExists
Is raised when you make a Command have the same name as another.

### FunctionAlreadyExists
Is raised when you try to pass the same function into a different Command.