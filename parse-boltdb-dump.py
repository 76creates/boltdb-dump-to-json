from sys import stdin
from json import loads, dumps

# Author: Dusan Gligoric
# Email: 7six@protonmail.com 
# Licence: GPL v2.0
# Usage: boltdb-dump my.db | python3 parse-boltdb-dump.py 

# this refers to indentation that is used on the dump
# this is default per https://github.com/chilts/boltdb-dump
DELIMITER="  "
# holder of our dictionarized DB
DB={}
# levelized stack of the reference points in the DB
STACK=[DB]
# used for calculating lvl of the DB
LVL=0
# these two are used for fetching keys and values
GETKEY=False
KEYSTACK=""

# prints debug messages, does not include step_debugger and vice versa
DEBUG = False
# prints DB every step of the way, would be good to implement input blocker
STEP_DEBUG = False

# findLvl finds the indendtation lvl of the line
def findLvl(line:str, lvl:int) -> int:
  if line.startswith(DELIMITER):
    return findLvl(line[len(DELIMITER):], lvl+1)
  return lvl

# isTableKey check if the line is "table key", this is prone to 
# errors, not sure about edge cases and how boltdb_dump ohandles this, 
# report if issue noticed
def isTableKey(line:str) -> bool:
  return line.startswith("[") and line.endswith("]")

# getCursor returns the reference point in the DB which 
# corresponds to the lvl of indentation of the line
def getCursor(lvl:int) -> dict:
  while 1:
    if len(STACK) > lvl:
      STACK.pop()
    elif len(STACK) == lvl:
      s = STACK.pop()
      STACK.append(s)
      return s
    else:
      raise AssertionError(f"stack went wild: {STACK}; lvl: {lvl}")

ln = 0 # used for numbering lines, mostly for debug
for l in stdin:
  if STEP_DEBUG: 
    print(f"[+++] status for line {ln}\n{DB}")
  ln += 1
  if DEBUG: print(f"[+] processing line {ln}")
  line_lvl = findLvl(l, 1)
  if DEBUG: print(f"[+] line has indentation lvl of {line_lvl}")
  stripped = l.rstrip()[len(DELIMITER)*line_lvl-len(DELIMITER):]
  if DEBUG: print(f"[+] stripped like is: {stripped}")

  # this here is to guard regarding badly formatted database dumps
  if line_lvl==1:
    if not isTableKey(stripped):
      raise AssertionError(f"expected table key at line {ln}: {stripped}")

  # guarding some unexpected errors
  if LVL < 1 and line_lvl != 1 and isTableKey(stripped):
    raise AssertionError("file is not indented good or is invalid")

  # table key handling
  if isTableKey(stripped):
    if DEBUG: print("[+] found table key")
    cursor = getCursor(line_lvl)
    k = stripped[1:-1]
    cursor[k]={}
    STACK.append(cursor[k])
    LVL += 1
  # key value handling
  else:
    if not GETKEY:
      cursor = getCursor(line_lvl)
      k = stripped
      cursor[k]={}
      STACK.append(cursor[k])
      GETKEY=True
      KEYSTACK=k
      LVL += 1
    else:
      v = stripped
      try: 
        v_formatted = loads(v)
      except:
        if DEBUG: print(f"[+] could not convert to dictionary, line: {v}")
        v_formatted = v
      cursor = getCursor(line_lvl-1)
      cursor[KEYSTACK]=v_formatted
      STACK.append(cursor)
      GETKEY=False
      KEYSTACK=""
      LVL -= 1
      
print(dumps(DB))