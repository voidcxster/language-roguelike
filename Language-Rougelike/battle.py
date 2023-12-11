#in here put like battle funcs
import random
from termcolor import cprint
import os

def choose(*choices):  # make a func to select somethingerrorMessage, printColor = "white", 
  while True:
    print("\n\tType the corresponding number.")
    print(
      *[("\t" if index == 1 else "") + f"{index}. {item}" 
        for index, item in enumerate(choices, 1)], 
      sep = ", "
    )

    selection = input("\n\tMake your selection : ")
    for index, choice in enumerate(choices, 1):
      if selection == str(index):
        return choice
    else:  # user's choice did not match any of the options
      print("\nPlease enter a valid option!")

class Question:
  def __init__(self):
    # do not leave empty lines in the files, we need every line to hold a question
    #also, the numbers at the start need to be removed in the final product
    questions = open(r'questions.txt','r')
    answers = open(r'answers.txt','r')
    n = questions.readlines()
    self.query = n[k := random.randint(0,len(n)-1)]
    questions.close()
    self.answer = answers.readlines()[k].strip('\n')
    answers.close()



# takes a player and an enemy and returns a bool
#True if player wins, false otherwise

def startBattle(player, enemy):
  """Returns True if player wins, otherwise returns False"""
  #Shows what enemy appeared
  if enemy.name[0] in ['a', 'e', 'i', 'o', 'u']:
    cprint(f"\nAn {enemy.name} has appeared!", "light_red")
  else:
    cprint(f"\nA {enemy.name} has appeared!", "light_red")
  input("\nPress ENTER to continue\n\n")
  #Turn Order, if true its the player's turn, else false
  #(speed determines who goes first)
  if player.spd == enemy.spd:
    # gives a random individual the first turn
    yourTurn = random.choice([True,False])
  elif player.spd > enemy.spd:
    #The player goes first
    yourTurn = True
  else:
    #The enemy goes first
    yourTurn = False

  if yourTurn:
    cprint(f"\nYour SPD stat of {player.spd} lets you make the first move!", "light_red")
  else:
    cprint(f"\nThe {enemy.name}'s SPD stat of {enemy.spd} lets them make the first move!", "light_red")
  while player.hp > 0 and enemy.hp > 0: # makes sure neither the player or enemy is dead
    #take turns
    cprint(f"\nYou have {player.hp}/{player.maxhp} HP", "green")
    cprint(f"The enemy has {enemy.hp}/{enemy.maxhp} HP", "red")
    if yourTurn:
      choice = choose(' Attack ',' Shout "E!" at enemy ',)
      if choice == ' Attack ': #choose attack
        cprint("\nYou plan your attack!", "light_red")
        cprint("To hit the enemy, answer this question\n", "light_red")
        # attacks the enemy if you answer the question correctly
        # the part i am the least excited to debug -x
        question = Question()
        cprint(question.query + '\n', "green")
        if input('Your answer: ').strip().lower() == question.answer.lower().strip():
          cprint(f"\nCorrect! Your attack succesfully hits the {enemy.name}!", "light_green")
          attackDamage = random.randint(1,4) * player.atk
          cprint(f'You deal {attackDamage} damage to the {enemy.name}!', "light_red")
          input('\nPress ENTER to continue')
          enemy.hp -= attackDamage
        else: #dum idot you didnt get it right \j
          cprint(f"\nIncorrect! Your attack fails! \nThe correct answer was '{question.answer.strip(' ')}'", "red")
          input('\nPress ENTER to continue')
      elif choice == ' Shout "E!" at enemy ': #basically a pass turn no idea what its for
        cprint(f'\nYou shout "E!". The enemy {enemy.name} seems a bit disgruntled\nbut doesn\'t say anything', "blue")
        input('\nPress ENTER to continue')
        # enemy.spd -= 1 #most effective move, might have to nerf
    else: # has the enemy attack you
      attackDamage = random.randint(-1, 3) * enemy.atk
      if attackDamage <= 0: # if the attack fails
        cprint(f'\n{enemy.name} tries to attack but misses!', "light_green")
        input('\nPress ENTER to continue!')
      else: # if it hits
        cprint(f'\n{enemy.name} attacks you for {attackDamage} damage!', "red")
        input('\nPress ENTER to continue!')
        player.hp -= attackDamage

    #win lose case
    if player.hp <= 0: #you lose
      cprint("\nYou were defeated!!!", "red")
      input('\nPress ENTER to continue')
      os.system("clear")
      return False
    elif enemy.hp <= 0: #you win
      cprint("\nYou WIN!!!", "light_green")
      input('\nPress ENTER to continue!')
      os.system("clear")
      return True
    # swaps the turn order
    else: yourTurn = not yourTurn