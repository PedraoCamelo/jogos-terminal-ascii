#!/usr/bin/env python3
"""Uma pequena aventura ASCII. Requer apenas Python 3."""
import argparse
import os
import random
import sys

MAP = (
    '#################################',
    '#@....#.......#.................#',
    '#.##..#.###...#..#####..######..#',
    '#.....#...#.....#...............#',
    '###.#####.#.#####..####.#####...#',
    '#.........#........#........#...#',
    '#.#######.######...#.####...#...#',
    '#.......#..........#....#.......#',
    '#.###...#.######.#####.#.#####..#',
    '#...#..........#.......#........#',
    '#...########...#.#####.#####....#',
    '#..............#...............E#',
    '#################################',
)


class Game:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.floor = {(x, y) for y, row in enumerate(MAP)
                      for x, char in enumerate(row) if char != '#'}
        self.player = (1, 1)
        self.exit = (31, 11)
        # Distribua objetos somente em casas acessiveis.
        reachable, pending = {self.player}, [self.player]
        while pending:
            for cell in self.neighbors(pending.pop()):
                if cell not in reachable:
                    reachable.add(cell)
                    pending.append(cell)
        candidates = sorted(reachable - {self.player, self.exit})
        self.rng.shuffle(candidates)
        self.gems = set(candidates[:5])
        self.potions = set(candidates[5:8])
        self.monsters = set(candidates[8:14])
        self.hp = 10
        self.collected = 0
        self.turn = 0
        self.won = False
        self.message = 'Encontre os 5 cristais e alcance a porta E.'

    def neighbors(self, cell):
        x, y = cell
        return [(x + dx, y + dy) for dx, dy in
                ((0, -1), (0, 1), (-1, 0), (1, 0))
                if (x + dx, y + dy) in self.floor]

    def step(self, key):
        directions = {'w': (0, -1), 's': (0, 1),
                      'a': (-1, 0), 'd': (1, 0)}
        if key not in directions or self.hp <= 0 or self.won:
            return
        dx, dy = directions[key]
        target = (self.player[0] + dx, self.player[1] + dy)
        if target not in self.floor:
            self.message = 'Uma parede bloqueia o caminho.'
            return
        self.turn += 1
        self.message = 'Voce avanca pela masmorra...'
        if target in self.monsters:
            self.monsters.remove(target)
            self.hp -= 2
            self.message = 'Voce derrotou um monstro, mas perdeu 2 de vida!'
        self.player = target
        if target in self.gems:
            self.gems.remove(target)
            self.collected += 1
            self.message = 'Cristal encontrado! A porta sente sua presenca.'
        if target in self.potions:
            self.potions.remove(target)
            self.hp = min(10, self.hp + 4)
            self.message = 'Pocao encontrada: +4 de vida (maximo 10).'
        if self.hp <= 0:
            self.message = 'A masmorra venceu desta vez. Aperte R para tentar novamente.'
            return
        if target == self.exit:
            if self.collected == 5:
                self.won = True
                self.message = 'VITORIA! Voce escapou com todos os cristais!'
                return
            self.message = 'A porta exige os 5 cristais para abrir.'
        # Monstros se movem a cada dois passos; o jogador pode planejar desvios.
        if self.turn % 2 == 0:
            moved = set()
            for monster in sorted(self.monsters):
                choices = [p for p in self.neighbors(monster)
                           if p not in self.monsters and p not in moved
                           and p not in self.gems and p not in self.potions
                           and p != self.exit]
                destination = self.rng.choice(choices) if choices else monster
                if destination == self.player:
                    self.hp -= 1
                    self.message = 'Um monstro atacou voce! -1 de vida.'
                    destination = monster
                moved.add(destination)
            self.monsters = moved
        if self.hp <= 0:
            self.message = 'FIM DE JOGO. Aperte R para tentar novamente.'

    def render(self):
        lines = ['+---------------------------------+',
                 '|      A MASMORRA DOS CRISTAIS     |',
                 '+---------------------------------+',
                 f' Vida: {max(0, self.hp):2}/10   Cristais: {self.collected}/5   Passos: {self.turn}', '']
        for y, row in enumerate(MAP):
            line = ''
            for x, char in enumerate(row):
                p = (x, y)
                line += ('@' if p == self.player else
                         'M' if p in self.monsters else
                         '*' if p in self.gems else
                         '+' if p in self.potions else
                         'E' if p == self.exit else
                         '#' if char == '#' else ' ')
            lines.append(line)
        lines += ['', ' @ voce   * cristal   + pocao   M monstro   E saida',
                  ' WASD mover | R reiniciar | Q sair', '', self.message]
        return '\n'.join(lines)


def read_key():
    if os.name == 'nt':
        import msvcrt
        return msvcrt.getwch().lower()
    import termios
    import tty
    fd = sys.stdin.fileno()
    previous = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1).lower()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, previous)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, help='Repete a distribuicao dos objetos.')
    parser.add_argument('--preview', action='store_true', help='Exibe o mapa e sai.')
    args = parser.parse_args()
    game = Game(args.seed)
    if args.preview:
        print(game.render())
        return
    if not sys.stdin.isatty():
        parser.exit(1, 'Abra em um terminal interativo ou use --preview.\n')
    try:
        sys.stdout.write('\033[?25l')
        while True:
            print('\033[2J\033[H' + game.render(), end='', flush=True)
            key = read_key()
            if key in ('q', '\x03', '\x04'):
                break
            if key == 'r':
                game = Game(args.seed)
            else:
                game.step(key)
    except KeyboardInterrupt:
        pass
    finally:
        print('\033[?25h\nObrigado por jogar!', flush=True)


if __name__ == '__main__':
    main()
