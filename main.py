##########
#TODO:
#
##########
#DESCRIPTION:
# - screen max chars: 56x33
# - python /storage/emulated/0/BitMiller/Pradhana/Dropbox/bitmiller_hu/progs/python_for_termux/__public_projects/verebely_kviz_at250218-2/main.py
##########

import os, sys, shutil, random
from my.screen import *

# Global variables:
delimiter1 = "#"
delimiter2 = "$"
delimiter3 = ","
scr_x, scr_y = shutil.get_terminal_size()

class Riddle:
 def __init__(self, riddle_raw_line):
  global delimiter1, delimiter2
  riddle_raw_line = riddle_raw_line.split(delimiter1)
  #dprint(f"len(riddle_raw_line): {len(riddle_raw_line)}", debug)
  self.hardness = int(riddle_raw_line[0])
  self.question = riddle_raw_line[1]
  self.answers:list = riddle_raw_line[2].split(delimiter2)
  #self.solutions:list = list(map(int, riddle_raw_line[3].split(delimiter2))) # error if last line in file has no solutions' data ( .split() returns [''] string )
  self.solutions:list = riddle_raw_line[3].split(delimiter2)
  dprint(f"self.solutions: {self.solutions}", debug)
  empty_solution:bool = False
  if len(self.solutions) == 1:
   try:
    tmp = self.solutions[0]
   except ValueError:
    empty_solution = True
    self.solutions = []
  if not empty_solution:
   for i in range(len(self.solutions)):
    dprint(f"self.solutions[i].strip(): {(self.solutions[i].strip())}", debug)
    try:
     self.solutions[i] = int(self.solutions[i].strip())
    except ValueError:
     self.solutions.pop(i)
  dprint(f"Check: {self.solutions}", debug)

 def __str__(self):
  ret = f"Question: {self.question}"
  for i in range(len(self.answers)):
   ret+=f" | Answer {i+1}.: {self.answers[i]}"
  for i in range(len(self.solutions)):
   ret+=f" | Solution {i+1}.: {self.solutions[i]}"
  return ret

##########

class Gamer:
 def __init__(self, name, score=0):
  self.name = name
  self.score = score

##########

def validate_answer(ans, answers_num) -> int:
 global valid_answers, quitters, delimiter3
 valid_answers = []

 ans = ans.split(delimiter3)
 for i in range(len(ans)):
  ans[i] = ans[i].strip().lower()

 if len(ans) == 1:
  if ans[0] in quitters:
   return 0
  if ans[0] == "0":
   return 1

 for a in range(len(ans)):
  try: ans[a] = int(ans[a])
  except ValueError:
   valid_answers = []
   return -1
  if ans[a] in valid_answers or ans[a] < 1 or ans[a] > answers_num:
   valid_answers = []
   return -1
  else:
   valid_answers.append(ans[a])

 return 1

##########

def show_help(cl_sc = False):
 if cl_sc: clrscr()
 print("Súgó:")
 print(" Ha több helyes válasz is lehetséges, vesszővel válaszd el őket!")
 print(" Ha nincs helyes válasz, a nulla szám bevitelével jelezd!")
 print(" A több helyes válasz esetén nem megadott válaszok egyenként egy pont, rossz találatok két pont veszteséggel járnak.")
# print(" Súgó előcsalogatása: ?")
 print(" Válasz: \"q\" = játék abbafejezése")
 input("Nyomj [ENTER]-t a folytatáshoz!")

##########

quitters:list = [
"q", "quit", "exit", "halt", "die", "ki", "kilép", "kilépés", "vége", "ende", "konyec", "egzit",
]
max_rounds:int = 5
valid_answers:list = []
debug = False

if debug:
 riddles_filename = "riddles_for_debug.txt"
else:
 riddles_filename = "riddles.txt"

os.chdir(os.path.dirname(__file__))

# Populate rankings' database:
with open("scores_data/ranking.txt", "a+", encoding="UTF-8") as f:
 f.seek(0)
 raw_ranking = f.readlines()

# Populate riddles' database:
try:
 with open("riddle_data/"+riddles_filename, "r", encoding="UTF-8") as f:
  raw_data = f.readlines()
except FileNotFoundError:
 exit(f"Hiányzik a \"riddle_data/{riddles_filename}\" fájl. Ebben lennének a feladványok.")

riddles:list = []

for r in raw_data:
 riddles.append(Riddle(r))

score:int = 0
riddles_selected:list = []
game_is_on:bool = True

clrscr()

print("Üdvözöllek! Játsszunk!")
show_help()
gamer = Gamer(input("A neved, lécci! : "))


# Game's main cycle:

round_num:int = 0

while game_is_on and round_num < max_rounds:
 round_num += 1

# Randomly select a riddle what haven't appeared yet in this game:
 new_riddle_ok:bool = False
 while not new_riddle_ok:
  new_riddle_index = random.randrange(0, len(riddles))
  if new_riddle_index not in riddles_selected:
   new_riddle_ok = True
 riddles_selected.append(new_riddle_index)
 if len(riddles_selected) >= len(riddles):
  game_is_on = False

# Generate answers' random sequence:
 randomed_answers:list = []
 while len(randomed_answers) < len(riddles[new_riddle_index].answers):
  new_answer_ok = False
  while not new_answer_ok:
   new_answer_index = random.randrange(0, len(riddles[new_riddle_index].answers))
   if new_answer_index not in randomed_answers:
    new_answer_ok = True
  randomed_answers.append(new_answer_index)

# Outputting the riddle:
 print(f"\n{round_num}. kérdés:")
 print(f"{riddles[new_riddle_index].question}")
 print(f"Nehézség: {riddles[new_riddle_index].hardness}")
 print(f"Választható válaszok:")
 for i in range(len(riddles[new_riddle_index].answers)):
  print(f"Kérdés {i+1}.: {riddles[new_riddle_index].answers[randomed_answers[i]]}")
 print("Válaszod: ", end="")

# Getting answers:
 res:int = -1

# Check for invalid input:
 while res == -1:
  res = validate_answer(input(), len(riddles[new_riddle_index].answers))
  if res == -1: print("Nomég1x: ", end="")


# We've got valid answers:
 if res == 1:
  question_score:int = 0
  dprint(f"valid_answers: {valid_answers}", debug)
# Check if the guesses are correct:
  if len(valid_answers) == 0:
   if len(riddles[new_riddle_index].solutions) == 0:
    question_score = 1
   else:
    question_score = -len(riddles[new_riddle_index].solutions)
  else:
   #dprint("Non-empty answer.", debug)
   for i in range(len(valid_answers)):
    #dprint(f"for loop i: {i}", debug)
    #dprint(f"riddles[new_riddle_index].solutions: {riddles[new_riddle_index].solutions}", debug)
    if randomed_answers[valid_answers[i]-1]+1 in riddles[new_riddle_index].solutions:
     question_score += 1
     dprint(f"Found solution:{valid_answers[i]} at i:{i}", debug)
     #dprint(f"i: {i}", debug)
     dprint(f"randomed_answers[valid_answers[i]-1]+1: {randomed_answers[valid_answers[i]-1]+1}", debug)

# Check if there are incorrect/blind guesses.
# The rest of valid answers are incorrect:
   dprint(f"question_score: {question_score}", debug)
   dprint(f"len(valid_answers): {len(valid_answers)}", debug)
   dprint(f"len(riddles[new_riddle_index].solutions): {len(riddles[new_riddle_index].solutions)}", debug)
   dprint(f"(len(valid_answers)-question_score)*2: {(len(valid_answers)-question_score)*2}", debug)
   if question_score < len(riddles[new_riddle_index].solutions) and question_score < len(valid_answers) or len(valid_answers) > len(riddles[new_riddle_index].solutions):
    question_score -= (len(valid_answers)-question_score)*2
    dprint(f"question_score: {question_score}", debug)
   elif len(valid_answers) < len(riddles[new_riddle_index].solutions):
    question_score -= len(riddles[new_riddle_index].solutions)-len(valid_answers)
# Multiple up the scores:
  question_score *= riddles[new_riddle_index].hardness
  gamer.score += question_score

  print(f"Ebben a körben {question_score} pontot sikerült gyűjteni.")
  print(f"Most összesen {gamer.score} pontod van.")

# res == 0, Gamer quitted:
 else: game_is_on = False

print(f"\nJó játék volt! Szevasz, {gamer.name}!")


