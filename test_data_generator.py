
# Command line string for developing on Android:Termux :
# python /storage/emulated/0/BitMiller/Pradhana/Dropbox/bitmiller_hu/progs/python_for_termux/__public_projects/verebely_kviz_at250218-2/test_data_generator.py


import os, random

# Total questions number:
#  questions_num * questions_hardness_level_num
questions_num = 5
questions_hardness_level_num = 5

# Separates different types of data (1st level separator):
#  question hardness | question | possible answers | good answers
delimiter1 = "#"

# Separates same type of data (2nd level separator):
#  possible answers, good answers
delimiter2 = "$"

# Number of list elements give the maximum number of possible answers. The higher the value the more frequent will be the answer quantity of index+1.
# answers_weight = [2, 1] will create twice as much questions with one possible answer than two.
# Btw: a question with one possible answer is a simple decidable question.
answers_weight = [1, 4, 7, 7]


os.chdir(os.path.dirname(__file__))

with open("riddle_data/_output.txt", "w", encoding="UTF-8") as f:
 for i in range(questions_hardness_level_num):
  for j in range(questions_num):
   q_str:str = f"{'' if i==0 and j==0 else '\n'}"
   q_str += str(i+1) + delimiter1 + "Kérdés " + str(i*questions_hardness_level_num+j+1) + delimiter1
   answers_hardness = random.randint(1, sum(answers_weight))
   l:int = 0
   for k in range(len(answers_weight)):
    l += answers_weight[k]
    if answers_hardness <= l:
     break

# Filling up answers and deciding which one will be good or bad:
   answers_num:int = k+1
   answers_nature:list = []
   for k in range(answers_num):
    if k != 0: q_str += delimiter2
    nature:bool = bool(random.randint(0, 1))
    answers_nature.append(nature)
    q_str += f"{'Jó' if nature else 'Rossz'} válasz ({k+1}.)"

# The list of the number of good answers will follow:
   q_str += delimiter1

# If we have no good answers:
   #if True not in answers_nature:
   # q_str += "0"

   #else:
   if True:
    quant:int = 0
    for k in range(answers_num):
     if answers_nature[k]:
      if quant != 0:
       q_str += delimiter2
      q_str += str(k+1)
      quant += 1

# Outputting the riddle:
   f.writelines(q_str)


