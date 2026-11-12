#!/usr/bin/env python3
"""Cinzas da Torre — RPG de turnos ASCII, apenas com Python 3."""
import random
import sys
import textwrap

ART = {
    'Goblin': ['   /\\ /\\', '  ( o  o )', '   /|==|\\', '    /  \\'],
    'Esqueleto': ['    .----.', '    |o  o|', '    | == |', '   /| || |\\', '     /  \\'],
    'Lobo sombrio': [' /\\___/\\', '( >   < )___', ' \\  ^  /   \\__', '  || ||  || ||'],
    'Guardiao de ferro': ['   [======]', '   | O  O |', ' __|______|__', '|__|  []  |__|', '   |__||__|'],
    'Rei das Cinzas': ['    /\\ /\\ /\\', '   [=========]', '    | *   * |', '  __|   V   |__', ' /  |=======|  \\', '    /  ||  \\'],
}


def say(message):
    print(textwrap.fill(message, 72))


def choose(prompt, options):
    print('\n' + prompt)
    for i, option in enumerate(options, 1):
        print(f'  {i}. {option}')
    while True:
        answer = input('> ').strip().lower()
        if answer == 'q':
            raise KeyboardInterrupt
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return int(answer) - 1
        print('Digite o numero de uma opcao (ou Q para sair).')


class Hero:
    def __init__(self, name, job):
        self.name, self.job = name, job
        self.level, self.xp, self.gold = 1, 0, 20
        self.max_hp, self.max_mp, self.attack, self.armor = (
            (45, 12, 10, 3) if job == 'Guerreiro' else
            (30, 24, 7, 1) if job == 'Mago' else (36, 16, 9, 2))
        self.hp, self.mp = self.max_hp, self.max_mp
        self.potions = 3
        self.weapon = 0

    def status(self):
        print(f'\n{self.name} | {self.job} Nv.{self.level} | '
              f'PV {self.hp}/{self.max_hp} | PM {self.mp}/{self.max_mp}')
        print(f'XP {self.xp}/{self.level * 15} | Ouro {self.gold} | '
              f'Pocoes {self.potions} | Arma +{self.weapon}')

    def reward(self, xp, gold):
        self.xp += xp
        self.gold += gold
        say(f'Recebeu {xp} XP e {gold} moedas!')
        while self.xp >= self.level * 15:
            self.xp -= self.level * 15
            self.level += 1
            self.max_hp += 7
            self.max_mp += 4
            self.attack += 2
            self.armor += 1
            self.hp, self.mp = self.max_hp, self.max_mp
            say(f'NIVEL {self.level}! Seus atributos aumentaram e voce recuperou PV e PM.')


def battle(hero, name, stage, rng):
    boss = name == 'Rei das Cinzas'
    max_hp = 24 + stage * 7 + (22 if boss else 0)
    hp = max_hp
    power = 6 + stage * 2
    turn = 1
    skill = {'Guerreiro': 'Golpe esmagador', 'Mago': 'Bola de fogo',
             'Ladino': 'Ataque venenoso'}[hero.job]
    poison = 0
    say(f'Um {name} bloqueia seu caminho!')
    while hp > 0 and hero.hp > 0:
        print('\n' + '=' * 48)
        print('\n'.join(ART[name]))
        print(f'\n{name} | PV {max(0, hp)}/{max_hp} | Turno {turn}')
        charged = turn % 3 == 0
        if charged:
            print('!! O inimigo prepara um ataque poderoso. !!')
        hero.status()
        action = choose('Sua acao:', ['Atacar', f'{skill} (5 PM)',
                                     'Defender e recuperar 3 PM',
                                     'Usar pocao (+22 PV)'])
        defending = False
        if action == 0:
            damage = rng.randint(hero.attack - 2, hero.attack + 3) + hero.weapon * 3
            critical = rng.random() < (0.25 if hero.job == 'Ladino' else 0.1)
            if critical:
                damage *= 2
            hp -= damage
            say(f'{"CRITICO! " if critical else ""}Voce causou {damage} de dano.')
        elif action == 1:
            if hero.mp < 5:
                say('PM insuficiente. Escolha outra acao.')
                continue
            hero.mp -= 5
            damage = hero.attack + hero.weapon * 3 + rng.randint(7, 12)
            if hero.job == 'Mago':
                damage += 5
            if hero.job == 'Ladino':
                poison = 3
            hp -= damage
            say(f'{skill}: {damage} de dano!')
        elif action == 2:
            defending = True
            hero.mp = min(hero.max_mp, hero.mp + 3)
            say('Voce assume uma postura defensiva e recupera energia.')
        else:
            if not hero.potions:
                say('Suas pocoes acabaram. Escolha outra acao.')
                continue
            if hero.hp == hero.max_hp:
                say('Sua vida ja esta cheia. Escolha outra acao.')
                continue
            hero.potions -= 1
            healed = min(22, hero.max_hp - hero.hp)
            hero.hp += healed
            say(f'Voce recuperou {healed} PV.')
        if poison and hp > 0:
            hp -= 4
            poison -= 1
            say('O veneno causou 4 de dano.')
        if hp <= 0:
            break
        damage = max(1, power + rng.randint(-2, 2) - hero.armor)
        if charged:
            damage *= 2
        if defending:
            damage = max(1, damage // 3)
        hero.hp = max(0, hero.hp - damage)
        say(f'{name} atacou e causou {damage} de dano.')
        turn += 1
    if hero.hp <= 0:
        return False
    say(f'Voce derrotou {name}!')
    hero.reward(12 + stage * 4, 15 + stage * 5)
    return True


def camp(hero):
    print('\n       /\\       ACAMPAMENTO\n      /__\\      Uma fogueira ilumina a trilha.\n      /||\\\n     ======')
    while True:
        hero.status()
        cost = 25 + hero.weapon * 20
        action = choose('O que deseja fazer?', ['Seguir viagem', 'Descansar (10 ouro; restaura PV e PM)',
                                              'Comprar pocao (8 ouro)', f'Melhorar arma ({cost} ouro)'])
        if action == 0:
            return
        price = (0, 10, 8, cost)[action]
        if hero.gold < price:
            say('Ouro insuficiente.')
            continue
        hero.gold -= price
        if action == 1:
            hero.hp, hero.mp = hero.max_hp, hero.max_mp
            say('Uma noite tranquila devolve suas forcas.')
        elif action == 2:
            hero.potions += 1
            say('Pocao guardada na mochila.')
        else:
            hero.weapon += 1
            say('Sua arma agora causa mais 3 de dano por melhoria!')


def main():
    print(r'''
   /\                       /\
  /__\    CINZAS DA TORRE   /__\
  |[]|_____________________|[]|
  |  |  UM RPG DE TURNOS    |  |
  |__|_____________________|__|
''')
    say('O Rei das Cinzas roubou a luz do vale. Atravesse cinco regioes, '
        'fortaleca seu heroi e recupere a chama. Digite Q em qualquer menu para sair.')
    name = input('\nNome do heroi: ').strip()[:24] or 'Viajante'
    jobs = ['Guerreiro', 'Mago', 'Ladino']
    job = choose('Escolha sua classe:', ['Guerreiro: mais vida e armadura',
                                       'Mago: magia mais forte e mais PM',
                                       'Ladino: mais criticos e veneno'])
    hero = Hero(name, jobs[job])
    rng = random.Random()
    encounters = [('Bosque dos Sussurros', 'Goblin'),
                  ('Cripta Esquecida', 'Esqueleto'),
                  ('Trilha da Lua Morta', 'Lobo sombrio'),
                  ('Portoes da Torre', 'Guardiao de ferro'),
                  ('Trono das Cinzas', 'Rei das Cinzas')]
    for stage, (place, enemy) in enumerate(encounters, 1):
        print(f'\n[{stage}/5] {place.upper()}')
        if stage > 1:
            event = choose('Voce encontra uma fonte antiga:',
                           ['Beber: recuperar 10 PV', 'Meditar: recuperar 6 PM'])
            if event == 0:
                hero.hp = min(hero.max_hp, hero.hp + 10)
            else:
                hero.mp = min(hero.max_mp, hero.mp + 6)
        if not battle(hero, enemy, stage, rng):
            print('\n   +--------------------------+\n   |       FIM DE JOGO        |\n   +--------------------------+')
            say('A chama ainda espera por um heroi. Execute o jogo para tentar novamente.')
            return
        if stage < 5:
            camp(hero)
    print('\n       \\ | /\n      -- * --\n       / | \\\n\n          VITORIA!')
    say(f'{hero.name} recuperou a chama! O vale volta a florescer e sua historia '
        'sera contada por muitas geracoes.')
    hero.status()


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\nAte a proxima aventura!')
        sys.exit(0)
