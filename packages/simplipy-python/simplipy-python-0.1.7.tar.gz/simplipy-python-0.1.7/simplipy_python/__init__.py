__version__ = '0.1.1'

from os import system as OsSystem
from termcolor import colored as Color
from time import sleep as Wait
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-cl', '--changelog', help="The python package's changelog", required=False, action="store_true")

args = parser.parse_args()

arged = False

if args.changelog:
  arged = True
  log = [
    f"[+] - Added Parse-Args (--changelog)",
    f"[+] - Fixed some Errors",
    f"[+] - Fixed errors when adding multiple categories",
    f"[=] - https://pypi.org/project/simplipy-python/"
  ]
  print(',\n'.join(log))

def _printCommands(commands, Categories, _startMessage):
  global Category
  OsSystem("cls")
  print(_startMessage)
  print(Color("Commands", "yellow", attrs=["bold"]))
  for x in range(len(commands)):
    print(f"  [{str(x + 1)}] - {commands[str(x + 1)]['name']}")

  if Categories != None:
    if len(Categories) > 0:
      for i,x in enumerate(Categories):
        x._setupCategory()


class Exceptions():

  class NotValidCommand(Exception):
    """Raised when a Command isn't found in the Command List."""

    def __init__(self, cmdNum: str):
      self.cmdNum = cmdNum

    def __str__(self):
      return f"The command you tried to run isn't in the \"Command List\" The Error Ran: \"{self.cmdNum}\"."

  class FunctionAlreadyExists(Exception):
    """Raised when a function already exists in a Command."""

    def __init__(self, function):
      self._funcId = function

    def __str__(self):
      return f"The function ({self._funcId}) already exists within a Command."

  class CommandNameAlreadyExists(Exception):
    """Raised when a Command Name already exists."""

    def __init__(self, name):
      self._name = name

    def __str__(self):
      return f"The function ({self._name}) already exists within a Command."


_commands = {}


def GetArguments(message: str):
  arguments = [arg for arg in message.split(' ')]

  arguments.remove(arguments[0])
  arguments.remove(arguments[-1])

  return arguments


categories = {}


class Category():

  def __init__(self, category_name: str):
    """Create a Category with a name."""
    category_name = category_name.replace(' ', '-', len(category_name))
    self._cName = category_name

    categories[category_name] = {'commands': {}}

  def AddCommand(self, command_name: str, command_function):
    """Add command into the Category"""
    categories[self._cName]['commands'][str(
      len(categories[self._cName]['commands']) + 1)] = {
        'name': command_name,
        'func': command_function,
        'id': str(len(categories[self._cName]['commands']) + len(_commands))
      }

  def _setupCategory(self):
    # for _, j in enumerate(categories):
    print('')
    print(Color(self._cName, 'green', attrs=['bold']))

    for x in range(len(categories[self._cName]['commands'])):
      print(
        f"  [{categories[self._cName]['commands'][str(x + 1)]['id']}] - {categories[self._cName]['commands'][str(x + 1)]['name']}"
      )


isCategory = False
cc = "Commands"


class Command():

  def __init__(self, CommandMessage: str, StarterMessage: str = None):
    """Setup the main Command Handler."""
    self._runnerMessage = CommandMessage
    self._startMessage = StarterMessage

    if (self._startMessage == None):
      self._startMessage = f"Thank you for using {Color('Simplipy', 'green', attrs=['bold', 'blink'])}!"
    else:
      self._startMessage = self._startMessage + Color(
        ' - Simplipy', 'green', attrs=['dark'])

  def AddCommand(self, command_name: str, command_function):
    """Add command into the main Command Handler."""
    self._name = command_name
    self._func = command_function

    self._commands = _commands

    for x in range(len(self._commands)):
      if (self._commands[str(x + 1)]['func'] == self._func):
        raise Exceptions.FunctionAlreadyExists(self._func)
        return
      elif (self._commands[str(x + 1)]['name'] == self._name):
        raise Exceptions.CommandNameAlreadyExists(self._name)
        return

    self._commands[str(len(_commands) + 1)] = {
      'name': self._name,
      'func': self._func
    }

  def SetupCommands(self, Categories: list = None):
    global categories, cc

    if arged:
      return 

    _printCommands(self._commands, Categories, self._startMessage)

    def startUp(chosenCategory):
      global isCategory
      ranInfo = input(
        Color(chosenCategory, 'white', attrs=['dark']) + ' ' +
        self._runnerMessage)
      ranInfo = ranInfo + ' '

      if ranInfo.split(' ')[0] in categories:
        isCategory = True
        OsSystem('cls')
        _printCommands(self._commands, Categories, self._startMessage)

        startUp(ranInfo.split(' ')[0])
      elif ranInfo.split(' ')[0] == "Commands":
        isCategory = False
        _printCommands(self._commands, Categories, self._startMessage)
        startUp('Commands')

      if chosenCategory == "Commands" and not isCategory:
        if (ranInfo.split(' ')[0] in self._commands):
          Arguments = GetArguments(ranInfo)
          self._commands[str(ranInfo.split(' ')[0])]['func'](Arguments)
        else:
          OsSystem('cls')
          raise Exceptions.NotValidCommand(ranInfo.split(' ')[0])
      elif chosenCategory in categories:
        if str(int(ranInfo.split(' ')[0]) -
               len(_commands) + 1) in categories[chosenCategory]['commands']:
          Arguments = GetArguments(ranInfo)
          categories[chosenCategory]['commands'][str(
            int(ranInfo.split(' ')[0]) - len(_commands) + 1)]['func'](Arguments)
        else:
          OsSystem("cls")
          raise Exceptions.NotValidCommand(ranInfo.split(' ')[0])

    if cc != "":
      startUp(cc)
      cc = ""
