# this program is about creating a simple RPG game using OOP - it is a dumbed down version of Runescape


class Player:
    def __init__(self, name, health, magic, defense):
        # stats
        self.name = name
        self.health = health * 100
        self.magic = magic
        self.defense = defense
        #inventory
        self.inventory = []
        # equipment
        self.weapons = []
        self.armoursets = []
        self.amulets = []
        self.rings = []
        self.boots = []
        self.gloves = []
        self.shields = []
        self.activeweapon = None
        self.activearmourset = None
        self.activeamulet = None
        self.activering = None
        self.activeboots = None
        self.activegloves = None
        self.activeshield = None
        self.abilitydamage = magic*40
        self.armourrate = 0
        self.adrenaline = 100
    def attack(self, target,ability):
        target.health -= ability.damage/100 * self.abilitydamage
        self.adrenaline += ability.adren_cost
        if target.health <= 0:
            self.gain_item(target)
    def defend(self,target):
        self.health -= target.damage * (1- (self.armourrate+self.defense)/200)
        if self.health <= 0:
            print(f"{self.name} has died")
    def gain_item(self,target):
            itemdrop = target.drop_item()
            print(f"{target.name} dropped {itemdrop.name}")
            if itemdrop.type == "weapon":
                self.weapons.append(itemdrop)
            elif itemdrop.type == "armourset":
                self.armoursets.append(itemdrop)
            elif itemdrop.type == "amulet":
                self.amulets.append(itemdrop)
            elif itemdrop.type == "ring":
                self.rings.append(itemdrop)
            elif itemdrop.type == "boots":
                self.boots.append(itemdrop)
            elif itemdrop.type == "gloves":
                self.gloves.append(itemdrop)
            elif itemdrop.type == "shield":
                self.shields.append(itemdrop)
            else:
                self.inventory.append(target.itemdrop)
    def equip_item(self,item):
        if item.type == "weapon":
            self.activeweapon = item
            self.abilitydamage += item.damage
        elif item.type == "armourset":
            self.activearmourset = item
            self.armourrate += item.armourrate
        elif item.type == "amulet":
            self.activeamulet = item
        elif item.type == "ring":
            self.activering = item
        elif item.type == "boots":
            self.activeboots = item
        elif item.type == "gloves":
            self.activegloves = item
        elif item.type == "shield":
            self.activeshield = item
    def __str__(self):
        return f"{self.name} has {self.health} health, {self.magic} magic, and {self.defense} defense"

class Enemy:
    def __init__(self, name, health, attack, defense, droptable):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.droptable = droptable
        self.damage = attack*100
    def __str__(self):
        return f"{self.name} has {self.health} health, {self.attack} attack, and {self.defense} defense"
    def drop_item(self):
        import random
        return random.choice(self.droptable)
class Item:
    def __init__(self, name,type, magiclevel, defenselevel):
        self.name = name
        self.type = type
        self.magiclevel = magiclevel
        self.defenselevel = defenselevel
     
    def __str__(self):
        return f"{self.name} has {self.magiclevel} magic level and {self.defenselevel} defense level"

class Ability:
    def __init__(self, name, damage, adren_cost):
        self.name = name
        self.damage = damage
        self.adren_cost = adren_cost
    
    def __str__(self):
        return f"{self.name} has {self.damage} damage and costs {self.adren_cost} adrenaline"

# Boss encounter with a giant rat.
giant_rat = Enemy("Giant Rat", 1000, 100, 50, [Item("bone_staff", "weapon", 30, 0), Item("rathide_armour", "armourset", 0, 20), Item("rat_ring", "ring", 0, 0)])

abilityrotation = [Ability("Fireball", 100, 10), Ability("Ice Shard", 120, 10), Ability("Lightning Bolt", 150, 10),Ability("Wild Magic",250,-25),Ability("Asphyxiate",300,-25)]
animaworker = Player("AnimaWorker", 99, 120, 99)

for abilty in abilityrotation:
    animaworker.attack(giant_rat, abilty)
    animaworker.defend(giant_rat)
    print(f"{giant_rat.name} has {giant_rat.health} health left")
    if giant_rat.health <= 0:
        print(f"{giant_rat.name} has been defeated")
        break   

print(animaworker.health)
