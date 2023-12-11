#Libaries
from termcolor import colored, cprint
import sys
import pygame
import os
import random
import time
import gameloop
import battle

#KISS

#Classes


#Battle
class Enemy:

  def __init__(self, name: str, atk: int, spd: int, hp: int, maxhp: int):
    self.name = name
    self.atk = atk
    self.spd = spd
    self.hp = hp
    self.maxhp = maxhp

  def displayStats(self):
    print(f"""Name: {self.name}
    ATK: {self.atk}
    SPD: {self.spd}
    HP: {self.hp}/{self.maxhp}
    """)


class Player:

  def __init__(self, name: str, atk: int, spd: int, hp: int, maxhp: int,
               score: int, xp: int, level:int, items: list):
    self.name = name.title().strip()
    self.atk = atk
    self.spd = spd
    self.hp = hp
    self.maxhp = maxhp
    self.score = score
    self.xp = xp
    self.items = items
    self.level = level

  def displayStats(self):
    print(f"""
    ATK : {self.atk}
    SPD : {self.spd}
    HP  : {self.hp}/{self.maxhp}
    SCORE : {self.score}
    XP : {self.xp}
    Name : {self.name}\n""")


#Item class will contain what items do such as buffs
class Item:

  def __init__(self,
               name: str,
               buffType: str,
               buffAmount: int,
               buffDuration: int = -1):
    #buffDuration <= -1 if the item is permanent
    self.name = name
    self.buffType = buffType
    self.buffAmount = buffAmount
    self.buffDuration = buffDuration

  #will return a list starting with Type then Amount then Duration
  def returnItemStats(self):
    return [self.buffType, self.buffAmount, self.buffDuration]

  def __str__(self):
    return self.name




#Functions
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


#Game Setup
def startRun():
  cprint("\tAn old wizard approaches you...", "light_blue")
  time.sleep(1)
  cprint("Old Wizard : What's your name youngin'?\n", "light_cyan")
  name = ""
  noName = True
  while noName:  # loop until valid name given
    name = input("\tEnter Name : ")
    if name.strip() != "":
      noName = False
    else:
      cprint("\nOld Wizard : Don't be shy youngin'! What's your name?\n",
             "light_cyan")
  #                     atk spd hp mhp scr xp items
  player = Player(name, 10, 4, 100, 100, 0, 0, 1, [])
  time.sleep(.25)
  cprint(f"\n\n\nOld Wizard : Ah what a wonderful name, {player.name}!",
         "light_cyan")
  cprint("Old Wizard : Well, let's get started then! Choose your first item!",
         "light_cyan")
  starterItems = [
      Item("Wooden Sword", "ATK", 3),
      Item("Bow and Arrow", "SPD", 2),
      Item(f"Magic {player.name} Book", "XP", 2)
  ]
  selectedItem = choose(*starterItems)
  player.items.append(selectedItem) # player chooses starter item
  player = addItem(player, selectedItem)
  print(f"\n\tYou got the {selectedItem}!\n")
  
  cprint(
      "Old Wizard : Now that you have selected your item, I have to send you down the Murder Hole™!",
      "light_cyan")
  cprint(
      "Old Wizard : Before you enter however, you will need this magic book so I can speak with you while you're exploring.",
      "light_cyan")
  cprint("Old Wizard : Remember, your task will be to escape. Good luck!\n",
         "light_cyan")
  cprint(
      "\t The Old Wizard kicked you into the inconspicous hole behind you.\n",
      "light_blue")
  input("Press Enter to continue\n\n")
  os.system("clear")
  return player

#Treasure
def treasure(player:Player, *items):
  cprint("\tYou come across a few items", "light_blue")
  cprint("Old Wizard: Remember, you may only choose one.", "light_cyan")
  selectedItem = choose(*items)
  player.items.append(selectedItem) # player chooses starter item
  print(f"\n\tYou got the {selectedItem}!\n")
  player = addItem(player, selectedItem)
  return player

def addItem(player:Player, item:Item):
  stat = item.buffAmount
  if (item.buffDuration < 0):
    match item.buffType:
      case "ATK":
        player.atk += stat
      case "SPD":
        player.spd += stat
      case "HP":
        player.maxhp += stat
        player.hp += stat
      case "XP":
        player.xp += stat
      case "SCORE":
        player.score += stat
      case _:
        input("WHAT")
  elif (item.buffDuration > 0):
    match type:
      case "HP":
        player.hp += stat
  return player
#Battle


def levelUp(player: Player, isBoss: bool):
  if not isBoss:
    player.atk += random.randint(3, 8)
    player.spd += random.randint(1, 4)
    player.hp += random.randint(8, 23)
    player.score += 1
  elif isBoss:
    player.atk += random.randint(8, 13)
    player.spd += random.randint(4, 8)
    player.hp += random.randint(23, 31)
    player.score += 5
  cprint("You leveled up!\nThese are your new stats!\n", "magenta")
  player.displayStats()
  input("Press Enter to continue\n")
  return player


#Game Start
while True:  
  os.system("clear")
  cprint(
      """ Welcome to Sprodigy™! The greatest Spanish language game
  You will learn awesome Spanish!
  """, "light_blue")
  input("Press Enter to continue\n\n")
  os.system("clear")
  player = startRun()
  while True:
    newEnemyHP = player.maxhp + random.randint(5, 20) - 30
    newEnemy = Enemy(
      "Goblin", 
      random.randint(player.atk - 5, player.atk), 
      random.randint(player.spd - 4, player.spd + 2), 
      newEnemyHP, 
      newEnemyHP
    )
    cprint("\tNOTE : Do NOT include ACCENTS or PUNCTUATION in your answers", "yellow")
    if (battle.startBattle(player, newEnemy)):
      player.score += 1
      player.xp += random.randint(10, 15)
      if (player.xp > 50):
        player.xp -= 50
        player.level += 1
        player = levelUp(player, False)
      cprint(f"Old Wizard : Since you're new to this, {player.name}, I'll heal you son!", "light_cyan")
      player.hp = player.maxhp
      chestItems = [
          Item("Power potion", "ATK", random.randint(1, 12)),
          Item("Speed potion", "SPD", random.randint(1,6)),
          Item("Health potion", "HP", random.randint(10,20)),
          Item("Score booster", "SCORE", random.randint(1, 5))
      ]
      treasure(player, *chestItems)
      while True:
        cprint('\nWould you like to look at stats or continue down the path?', "light_blue")
        if choose(' Stats ', ' Continue ') == ' Stats ':
            player.displayStats()
            input("Press ENTER to continue")
        else:
          break
      os.system("clear")
      cprint("You continue down the path\n", "light_blue")
    else:
      os.system("clear")
      cprint(f"""
        You died!
        Your score was : {player.score}.
        Your level was : {player.level}.
      """, "red")
      input("Press ENTER to continue")
      print("Start new Game?")
      choice = choose(' Yes ', ' No ')
      if (choice == ' No '):
        print('Thanks for playing!')
        sys.exit()
      else:
        break
