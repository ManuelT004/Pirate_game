from game import location
import game.config as config
from game.display import announce
from game.events import *
from game.items import Item
from game import event
from game.combat import Monster
import game.combat as combat
import random
from game.display import menu



class Mysterious_Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "Mysterious Island"
        self.symbol = '?'
        self.visitable = True
        self.starting_location = Beachwithship(self)
        self.locations = {}

        self.puppet = False

        self.locations["beach"] = self.starting_location
        self.locations["Forest"] = Forest(self)
        self.locations["cave"] = Cave(self)
        self.locations["ritualsite"] = Ritual(self)
        self.locations["demonicstatue"] = Statue(self)
        self.locations["ritualcircle"] = Ritual_circle(self)
        self.locations["insidestatue"] = inside_statue(self)



    def enter (self, ship):
        print ("arrived at an island with a mysterious aura")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Beachwithship(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 100
        self.events.append(DyingNPC())

    def enter (self):
        announce (
            "You step onto an island with a ghastly aura.\n" + 
            "The sand sinks beneath your feet, but lack all comfort from the ususal sandy beaches.\n" +
            "Although you blame the long journey, you could almost swear the island itself was a slight shade of crimsion with things shifting in the shadows\n" +
            "There was one thing that you were certin of after many years in battles, The air reeked of blood and the smell grew stronger deeper into the island"
        )

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False

        elif (verb == "north"):
            announce ("The dangers of this island draw u in and you venture to the north")
            config.the_player.next_loc = self.main_location.locations["ritualsite"]

        elif (verb == "east"):
            announce ("The island strikes your curiosity, but you arent ready to dive into the thick of it, So u scout around")
            config.the_player.next_loc = self.main_location.locations['forest']

        elif (verb == 'west'):
            announce ('The island strikes your curiosity, but you arent ready to dive into the thick of it, So u scout around')
            config.the_player.next_loc = self.main_location.locations['cave']


class DyingNPC (event.Event):
    def __init__(self):
        self.name = "Dying NPC"

    def process(self, world):
        result = {}
        announce (
            'You see a  man running towards the crew, he seems injured\n' +
        'He collaspses infront of you, you can now notice he is covered in blood\n' +
        'He begins to crawl towards you, using the very last of his life force\n' +
        'He pulls him self towards your legs\n' +
        'You kneel down to hear a dying mans last words\n'
        'With his final breathe he says "run"'
        )
        result["newevents"] = []
        result["message"] = ""
        return result

class Ritual(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Ritual Site"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['enter'] = self

    def enter (self):
        announce('you stumble upon the origin of the smell.\n' +
                 'There is a circle on the ground surrounded by strange markings and symbols.\n' +
                 'Although you cannot make out the markings or symbols there is one thing that is abundantly clear, every inch of this area is covered in blood.\n' +
                 'Layers upon layers of old dried blood and fresh crismon ooze')

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations['statue']

        elif (verb == 'east' ):
            config.the_player.next_loc = self.main_location.locations['forest']

        elif (verb == 'west'):
            config.the_player.next_loc = self.main_location.locations['cave']

        elif (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations['beach']

        elif (verb == 'enter'):
            config.the_player.go = True
            config.the_player.next_loc = self.main_location.locations['ritualcircle']

class Ritual_circle(location.SubLocation): 
     def __init__ (self, m):
        super().__init__(m)
        self.name = "Ritual Circle"
        self.verbs['exit'] = self
        self.verbs['leave'] = self
        self.verbs['sacrafice'] = self

        self.puppet = True

        self.event_chance = 100
        self.events.append(Dagger_Event())

     def enter (self):
         announce ('standing in the middle of the circle you feel an intense pressure')

     def process_verb (self, verb, cmd_list, nouns):
        if (verb == "exit" or verb == "leave"):
            config.the_player.next_loc = self.main_location.locations["ritualsite"]
            config.the_player.go = True

        elif (verb == 'sacrafice'):
            if self.puppet == True:
               announce ('The puppet walks up and grabs the knife out your hands and ends himself, seemingly completeing his purpose')
               self.main_location.location['insidestatue'].door_open = True
            else:
                sacrafice = input ('who will you sacrafice')
                combat.Combat([sacrafice]).combat()
                announce ('they collapse')
                self.main_location.locations['insidestatue'].door_open = True


class Dagger_Event (event.Event):
    def __init__(self):
        self.name = 'Dagger Encounter'

    def process(self, world):
        result = {}
        announce ('you walk into the middle of the circle and realize there is something in the middle\n' +
                  'You get closer to examine the object\n' +
                  'It is a blade of some sort and for some inexplicable reason, you want it' +
                  'You pick it up'
                  )
        result["newevents"] = []
        result["message"] = ""
        config.the_player.add_to_inventory([Ritual_Dagger()])
        announce ('you add the dagger to your inventory')
        return result
    
class Ritual_Dagger (Item):
    def __init__(self):
        super().__init__('Ritual Dagger', 5)
        self.damage = (1,99)
        self.skill = ('dagger') 
        self.verb = ('stab')
        self.verb2 = ('stabs')

class Cave(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Cave"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['enter'] = self

    def enter (self):
        announce('there is a dark cave, there might be important items inside')

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations['statue']

        elif (verb == 'east'):
            config.the_player.next_loc = self.main_location.locations['ritual']

        elif (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations['beach']

        elif (verb == 'west'):
            announce ('The island ends on this western Cave')

        elif (verb == 'enter'):
            config.the_player.next_loc = self.main_location.locations['inside cave']

class inside_cave(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "inside cave"
        self.verbs['exit'] = self
        self.verbs['leave'] = self 

    def enter (self):
        announce('There seems to be some kind of puppet, shaped vaguely like a human, but you can feel it inbuded with a simple form of life.'
                + 'At your movement the puppet stands and begins to follow you.' 
                + 'he seems ready to follow, but nor able to do much else')
        self.puppet = True
        
    def process_verb(self, verb, cmd_list, nouns):

         if (verb == "exit" or verb == "leave"):
            config.the_player.next_loc = self.main_location.locations["cave"]
    

class Forest(location.SubLocation): #code in a village that is devoid of life,  a rest area for the crew
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Forest"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['rest'] = self #code this in

    def enter (self):
        announce('You step into this steep forest with what seems to be some sort of camp deeper in, might be a place to "rest"')

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations['statue']
        
        elif (verb == 'east'):
            announce ('The island ends at this eastern forest')

        elif (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations['beach']

        elif (verb == 'west'):
            config.the_player.next_loc = self.main_location.locations['ritual']

        
        

class Statue(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "statue"
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['listen'] = self
        self.door_open = False

    def enter (self):
        announce('You stand at the feet of a massive statue devoted to a diety u are unaware of, you hear faint whispers perhaps if u "listen" you will hear better')

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'north'):
            announce ('the island ends at this northern statue, but you dont wanna get any closer then u need to already')

        elif (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations['ritual']

        elif (verb == 'east'):
            config.the_player.next_loc = self.main_location.locations['forest']

        elif (verb == 'west'):
            config.the_player.next_loc = self.main_location.locations['cave']

        elif (verb == 'enter') and (self.door_open == True):
            config.the_player.next_loc = self.main_location.locations['insidestatue']


        elif (verb == 'listen'):
            announce ('you hear a faint whisper as if the voice is in your head itself.\n' +
                      'though u were actively staring at the statue watching its motionless position.\n' +
                      'you knew deep in your souls the whipsers came from its motionless mouth.\n' +
                      '"BLOOD FOR GIFTS, BLOOD FOR REWARDS, BLOOD FOR POWER".\n' +
                      'the words send shivers down your soul')

class inside_statue(location.SubLocation): #set up an encounter with an enemy that drops a special sword if won 
     def __init__ (self, m):
        super().__init__(m)
        self.name = "inside statue"
        self.verbs['exit'] = self
        self.verbs['leave'] = self
        self.door_open = False

        self.event_chance = 100
        self.events.append(WarriorBossEvent())

     def enter (self):
         announce ('The air is dark and musty and u can feel that a presence awaits you deeper in the room')
      
     def process_verb (self, verb, cmd_list, nouns):
        if (verb == "exit" or verb == "leave"):
            config.the_player.next_loc = self.main_location.locations["statue"]
            config.the_player.go = True

class WarriorBossEvent(event.Event):
    def __init__(self):
        self.name = 'Warrior Boss'

    def process (self, world):
        result = {}
        warrior = Warrior_Boss()
        announce("A Man rises from his throne, clearly more dead then alive, He takes a battle stance"
                 +'in death his mind is gone, but his remains still crave battle'
                 +'he rushes at you, Prepare for Battle')
        combat.Combat([warrior]).combat()
        announce("He takes a Knee, and pushes off the ground to the crew, but he begins to disintergrate"
                 + 'his final moments he uses his sword to take one final swing at your head'
                 + 'he dissapears before he could land the hit')
    
        result["newevents"] = []
       
        result["message"] = ""

        announce("you pick up the warriors weapon.")
        config.the_player.add_to_inventory([GreatSword()])
        
        return result

class Warrior_Boss(Monster):
    
    
    def __init__ (self):
        attacks = {}
        attacks["cleave"] = ["cleaves",random.randrange(70,80), (20,30)]
        attacks["slash"] = ["slashes",random.randrange(60,80), (5,10)]
        attacks['poke'] = ['stabs',random.randrange(60,80), (1,10)]
        super().__init__("Warrior", random.randint(50,100), attacks, 100 + random.randint(0, 10)) 

class GreatSword(Item):

    def __init__(self):
        super().__init__("Greatsword", 100) 
        self.damage = (40,60) 
        self.skill = "swords"
        self.verb = "slam"
        self.verb2 = "slams"