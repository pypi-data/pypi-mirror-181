# made with <3 by vyzv
# current version : 1.0


import time, os
from sys import platform
from os import system, name, get_terminal_size as _terminal_size


class Signipy:

  def Sleep(xtime):
     return time.sleep(xtime)

  def Clear():
     return os.system("cls" if os.name == "nt" else "clear")

  def Title(xtitle: str):
     if name == 'nt':
        return system(f"title {xtitle}")

  def Size(a: int, b: int): # standard size -> 120, 32
     if name == 'nt':
        return system(f"mode {a}, {b}")

  def Center(text: str, spaces: int = None, icon: str = " "):
     if spaces is None:
         spaces = Signipy._xspaces(text=text)
     return "\n".join((icon * spaces) + text for text in text.splitlines())

  def _xspaces(text: str):
      try:
          col = _terminal_size().columns
      except OSError:
          return 0
      textl = text.splitlines()
      ntextl = max((len(v) for v in textl if v.strip()), default = 0)
      return int((col - ntextl) / 2)

  def _yspaces(text: str):
      try:
          lin = _terminal_size().lines
      except OSError:
          return 0
      textl = text.splitlines()
      ntextl = len(textl)
      return int((lin - ntextl) / 2)