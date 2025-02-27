##########
#TODO:
# - User selectable game parameters
# - Option for more informative feedback on gained points
# - Localization
# - Fancier GUI
# - Scoring table and its output to file
##########
#DESCRIPTION:
# - screen max chars: 56x33
# - python /storage/emulated/0/BitMiller/Pradhana/Dropbox/bitmiller_hu/progs/python_for_termux/__public_projects/verebely_kviz_at250218-2/main.py
##########

import os, sys, shutil, random
from my.screen import *

# Global variables:
scr_x, scr_y = shutil.get_terminal_size()

class Riddle:
 def __init__(self, riddle_raw_line):
  global DELIMITER_1, DELIMITER_2
  riddle_raw_line = riddle_raw_line.split(DELIMITER_1)
  #dprint(f"len(riddle_raw_line): {len(riddle_raw_line)}")
  self.hardness = int(riddle_raw_line[0])
  self.question = riddle_raw_line[1]
  self.answers:list = riddle_raw_line[2].split(DELIMITER_2)
  #self.solutions:list = list(map(int, riddle_raw_line[3].split(DELIMITER_2))) # error if last line in file has no solutions' data ( .split() returns [''] string )
  self.solutions:list = riddle_raw_line[3].split(DELIMITER_2)
  dprint(f"self.solutions: {self.solutions}")
  empty_solution:bool = False
  if len(self.solutions) == 1:
   try:
    tmp = self.solutions[0]
   except ValueError:
    empty_solution = True
    self.solutions = []
  if not empty_solution:
   for i in range(len(self.solutions)):
    dprint(f"self.solutions[i].strip(): {(self.solutions[i].strip())}")
    try:
     self.solutions[i] = int(self.solutions[i].strip())
    except ValueError:
     self.solutions.pop(i)
  dprint(f"Check: {self.solutions}")

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

class Points:
 hit:int = 1
 missed:int = -1
 mishit:int = -2

##########

def validate_answer(ans, answers_num) -> int:
 global quitters, DELIMITER_3
 guesses = []

 ans = ans.split(DELIMITER_3)
 for i in range(len(ans)):
  ans[i] = ans[i].strip().lower()

 if len(ans) == 1:
  if ans[0] in quitters:
   return [0]
  if ans[0] == "0":
   return []

 for a in range(len(ans)):
  try: ans[a] = int(ans[a])
  except ValueError:
   return [-1]
  if ans[a] in guesses or ans[a] < 1 or ans[a] > answers_num:
   return [-1]
  else:
   guesses.append(ans[a])

 return guesses

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

if DEBUG: max_rounds = MAX_ROUNDS_DEBUG_MODE
else: max_rounds = MAX_ROUNDS_NORMAL_MODE

if DEBUG:
 riddles_filename = RIDDLES_FILENAME_DEBUG_MODE
else:
 riddles_filename = RIDDLES_FILENAME_NORMAL_MODE

valid_answers:list = []


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

clrscr()

print("Üdvözöllek! Játsszunk!")
show_help()
gamer = Gamer(input("A neved, lécci! : "))


# Game's main cycle:

round_num:int = 0
riddles_selected:list = []
game_is_on:bool = True

while game_is_on and round_num < max_rounds:
 round_num += 1

# Randomly select a riddle what haven't appeared yet in this game:
 #if True:
 if RANDOMIZE_QUESTIONS:
  new_riddle_ok:bool = False
  while not new_riddle_ok:
   new_riddle_index = random.randrange(0, len(riddles))
   if new_riddle_index not in riddles_selected:
    new_riddle_ok = True
 else:
  new_riddle_index = round_num - 1
 riddles_selected.append(new_riddle_index)
 if len(riddles_selected) >= len(riddles):
  game_is_on = False

# Generate answers' random sequence:
 #if True:
 if RANDOMIZE_ANSWERS:
  randomed_answers:list = []
  while len(randomed_answers) < len(riddles[new_riddle_index].answers):
   new_answer_ok = False
   while not new_answer_ok:
    new_answer_index = random.randrange(0, len(riddles[new_riddle_index].answers))
    if new_answer_index not in randomed_answers:
     new_answer_ok = True
   randomed_answers.append(new_answer_index)
 else:
  randomed_answers = list(range(0, len(riddles[new_riddle_index].answers)))

# Outputting the riddle:
 print(f"\n{round_num}. kérdés:")
 print(f"{riddles[new_riddle_index].question}")
 print(f"Nehézség: {riddles[new_riddle_index].hardness}")
 print(f"Választható válaszok:")
 for i in range(len(riddles[new_riddle_index].answers)):
  print(f"Kérdés {i+1}.: {riddles[new_riddle_index].answers[randomed_answers[i]]}")
 print("Válaszod: ", end="")

# Getting answers:
 guesses = [-1]

# Check for invalid input:
 while guesses == [-1]:
  guesses = validate_answer(input(), len(riddles[new_riddle_index].answers))
  if guesses == [-1]: print("Nomég1x: ", end="")

# Gamer quitted:
 if guesses == [0]: game_is_on = False

# We've got valid answers:
 else:
  question_score:int = 0
  tmp_sol = list(riddles[new_riddle_index].solutions)
  dprint(f"tmp_sol: {tmp_sol}")

  if guesses == [] and riddles[new_riddle_index].solutions == []:
   dprint("Helyes, hogy nincs helyes válasz!")
   question_score = 1
  else:
   dprint(f"Van némi válasz.")
   for i in range(len(guesses)):
    orig_sol_val = randomed_answers[guesses[i]-1]+1
    dprint(f"orig_sol_val|i: {orig_sol_val}|{i}")
    if orig_sol_val in tmp_sol:
     dprint("+1p!")
     question_score += Points.hit
     tmp_sol.pop(tmp_sol.index(orig_sol_val))
    else:
     question_score += Points.mishit
     dprint("-2p!")
   question_score += len(tmp_sol)*Points.missed
   dprint(f"Ennyi jó válasz maradt: len(tmp_sol): {len(tmp_sol)}")

# Multiple up the scores:
  question_score *= riddles[new_riddle_index].hardness
  gamer.score += question_score
  print(f"Ebben a körben {question_score} pontot sikerült gyűjteni.")
  print(f"Most összesen {gamer.score} pontod van.")

print(f"\nJó játék volt! Szevasz, {gamer.name}!")


