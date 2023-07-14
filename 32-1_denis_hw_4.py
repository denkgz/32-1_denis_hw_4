from enum import Enum
from random import choice, randint


class SuperAbility(Enum):
    NONE = 0
    CRITICAL_DAMAGE = 1
    BOOST = 2
    HEAL = 3
    BLOCK_DAMAGE_AND_REVERT = 4
    STUN = 5
    REVIVAL = 6
    TAKEHEALTH = 7
    BOMB = 8
    REAPER = 9


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.__health} damage: {self.__damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = SuperAbility.NONE

    @property
    def defence(self):
        return self.__defence


    def choose_defence(self, heroes):
        hero = choice(heroes)
        self.__defence = hero.ability

    def attack(self, heroes):
        for hero in heroes:
            if hero.health > 0:
                if hero.ability == SuperAbility.BLOCK_DAMAGE_AND_REVERT:
                    hero.blocked_damage = int(self.damage / 5)
                    hero.health -= int(self.damage - hero.blocked_damage)
                else:
                    hero.health -= self.damage

    def __str__(self):
        return 'BOSS ' + super().__str__() + f' defence: {self.__defence.name}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        if isinstance(ability, SuperAbility):
            self.__ability = ability
        else:
            raise ValueError('Wrong data type for ability')

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss):
        if self.health > 0 and boss.health > 0:
            boss.health -= self.damage

    def apply_super_power(self, boss, heroes):
        pass

    def __str__(self):
        return super().__str__() + f' ability: {self.__ability.name}'


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.CRITICAL_DAMAGE)

    def apply_super_power(self, boss, heroes):
        coeefccient = randint(2, 7)
        boss.health -= self.damage * coeefccient
        print(f'Warrior {self.name} hit critically {self.damage * coeefccient}')

times1 = 0
class Thor(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.STUN)

    def apply_super_power(self, boss, heroes):
        global times1
        chance = choice([True,False])
        if chance and times1 < 1:
            times1 += 1
            boss.damage = 0
            print('БОСС ОГЛУШЕН')
        else:
            boss.damage = 50

class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.BOOST)

    def apply_super_power(self, boss, heroes):
        boost_damage = randint(0,3)
        for hero in heroes:
            if hero.ability == SuperAbility.REVIVAL:
                continue
            hero.damage += boost_damage
        print(f'Magic {self.name} в этом раунде увеличил урон на {boost_damage} ')

class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.BLOCK_DAMAGE_AND_REVERT)
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss, heroes):
        boss.health -= self.blocked_damage
        print(f'Berserk {self.name} reverted {self.blocked_damage}')


class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, SuperAbility.HEAL)
        self.__heal_points = heal_points

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0 and hero != self:
                hero.health += self.__heal_points
        print(f'Medic {self.name} вылечил всех на {self.__heal_points}')

time = 0
class Witcher(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.REVIVAL)

    def apply_super_power(self, boss, heroes):
        global  time
        for hero in heroes:
            if time < 1:
                if hero.health <= 0:
                    time += 1
                    hero.health = self.health
                    self.health = 0
                    print(f'Witcher {self.name} отдал свою жизнь {hero.name}')

class Hacker(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.TAKEHEALTH)

    def apply_super_power(self, boss, heroes):
        hero = choice(heroes)
        rand_health = randint(5, 20)
        if round_number % 2:
            if hero != self:
                hero.health += rand_health
                print(f'Hacker забрал у боса здоровья {rand_health} и восстановил его {hero.name}')

time2 = 0
class Bomber(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.BOMB)

    def apply_super_power(self, boss, heroes):
        global time2
        bomb = 100
        if time2 < 1 and self.health <= 0:
            time2 += 1
            boss.health -= bomb
            print(f'Bomber {self.name} взорвался и нанес {bomb} урона. ')

time5 = 0
time6 = 0

class Reaper(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.REAPER)

    def apply_super_power(self, boss, heroes):
        global time5,time6
        health_hero = 300
        if self.health < health_hero * 0.3 and time5 < 1:
            time5 += 1
            self.damage = self.damage * 2
            print(f'Reaper {self.name} усилился в 2 раза')
        if self.health < health_hero * 0.15 and time6 < 1:
            time6 += 1
            self.damage = self.damage * 3
            print(f'Reaper {self.name} усилился в 3 раза')


round_number = 0
def show_stats(boss, heroes):
    print(f'\nROUND {round_number} ----------')
    print(boss)
    for hero in heroes:
        print(hero)


def is_game_over(boss, heroes):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True

    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
    return all_heroes_dead


def play_round(boss, heroes):
    global round_number,time,time2
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if boss.defence != hero.ability:
            hero.attack(boss)
            if hero.health > 0 and boss.health > 0 or hero.ability == SuperAbility.BOMB and time2 < 1:
                hero.apply_super_power(boss, heroes)
    show_stats(boss, heroes)


def start_game():
    boss = Boss('Doom', 2000, 50)

    reaper1 = Reaper('Evil',300,5)
    bomber1 = Bomber('Dinamit',250,5)
    hacker1 = Hacker('itcpec',300,5)
    witcher = Witcher('Damen',300,0)
    thor = Thor('Donar',300,0)
    warrior = Warrior('Superman', 270, 10)
    doc = Medic('Aibolit', 250, 5, 15)
    magic = Magic('Hendolf', 280, 15)
    berserk = Berserk('Garol', 260, 10)
    assistant = Medic('Haus', 300, 5, 5)
    heroes_list = [warrior, doc, magic, berserk, assistant,witcher,thor,hacker1,bomber1,reaper1]

    show_stats(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)
    return heroes_list

start_game()

