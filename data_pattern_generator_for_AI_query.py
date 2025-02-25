
# Command line string for developing on Android:Termux :
# python /storage/emulated/0/BitMiller/Pradhana/Dropbox/bitmiller_hu/progs/python_for_termux/__public_projects/verebely_kviz_at250218-2/data_pattern_generator_for_AI_query.py

"""
- @250224-1-2240
> https://chatgpt.com/c/67bce6d6-e0cc-800a-bceb-d273b111c595

Egy kis kvízjátékot fejlesztek Python-ban. Szükségem van hozzá feladványokra. Adok egy adathalmazt, és kérlek, annak a mintájára állíts nekem elő adatokat (kérdéseket, válaszokat)!
Egy sor így néz ki:
1#Kérdés 5#Rossz$Rossz$Jó#3
Az adatfajták # jellel vannak elválasztva. Sorrendben:
kérdés nehézsége # kérdés # válaszok # helyes válaszok sorszáma
A válaszok és helyes válaszok $ jellel vannak elválasztva.
Ha nincs jó válasz, akkor a helyes válaszok helyén "0" áll.
Íme a minta, cseréld le az elemeit értelmes dolgokra:

1#Kérdés 1#Rossz$Jó$Rossz$Jó#2$4
1#Kérdés 2#Jó$Jó$Jó#1$2$3
1#Kérdés 3#Jó$Rossz#1
1#Kérdés 4#Jó$Jó$Jó#1$2$3
1#Kérdés 5#Rossz$Rossz$Jó#3
2#Kérdés 6#Jó$Jó$Rossz$Rossz#1$2
2#Kérdés 7#Rossz$Rossz#0
2#Kérdés 8#Rossz$Rossz$Jó#3
2#Kérdés 9#Rossz$Rossz$Jó$Rossz#3
2#Kérdés 10#Jó#1
3#Kérdés 11#Rossz#0
3#Kérdés 12#Rossz$Rossz$Rossz#0
3#Kérdés 13#Jó$Jó#1$2
3#Kérdés 14#Jó$Rossz#1
3#Kérdés 15#Rossz$Jó$Rossz$Jó#2$4
4#Kérdés 16#Rossz$Rossz$Rossz#0
4#Kérdés 17#Rossz$Rossz$Jó$Jó#3$4
4#Kérdés 18#Rossz$Rossz$Rossz$Jó#4
4#Kérdés 19#Jó$Jó$Rossz$Rossz#1$2
4#Kérdés 20#Jó$Rossz$Rossz$Jó#1$4
5#Kérdés 21#Jó$Rossz$Rossz#1
5#Kérdés 22#Jó$Jó$Rossz#1$2
5#Kérdés 23#Rossz$Jó$Rossz#2
5#Kérdés 24#Rossz$Jó$Jó$Jó#2$3$4
5#Kérdés 25#Jó$Jó$Jó#1$2$3


"""


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

with open("riddle_data/_query.txt", "w", encoding="UTF-8") as f:
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
    q_str += f"{'Jó' if nature else 'Rossz'}"

# The list of the number of good answers will follow:
   q_str += delimiter1

# If we have no good answers:
   if True not in answers_nature:
    q_str += "0"

   else:
    quant:int = 0
    for k in range(answers_num):
     if answers_nature[k]:
      if quant != 0:
       q_str += delimiter2
      q_str += str(k+1)
      quant += 1

# Outputting the riddle:
   f.writelines(q_str)


