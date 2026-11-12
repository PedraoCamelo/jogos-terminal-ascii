# Jogos de terminal ASCII

Duas aventuras em Python 3, com gráficos ASCII e sem dependências externas.

## Jogar

```bash
git clone https://github.com/PedraoCamelo/jogos-terminal-ascii.git
cd jogos-terminal-ascii
python3 masmorra.py
# ou
python3 rpg_turnos.py
```

No Windows, você também pode usar `py` no lugar de `python3`. Execute em um terminal interativo.

## A Masmorra dos Cristais

Explore uma masmorra, colete cinco cristais e alcance a saída antes que sua vida acabe.

| Símbolo | Significado |
| --- | --- |
| `@` | Seu personagem |
| `#` | Parede |
| `*` | Cristal |
| `+` | Poção: recupera até 4 de vida |
| `M` | Monstro |
| `E` | Saída |

Use **WASD** para mover, **R** para reiniciar e **Q** para sair, sem pressionar Enter. Entrar na casa de um monstro o derrota e custa 2 de vida. A cada dois passos válidos, os monstros se movem; se entrarem na sua casa, causam 1 de dano.

```bash
python3 masmorra.py --seed 42  # repetir a distribuição dos objetos
python3 masmorra.py --preview  # exibir o mapa sem jogar
```

## Cinzas da Torre

Um RPG de batalhas por turnos: atravesse cinco regiões e derrote o Rei das Cinzas para devolver a luz ao vale.

- **Guerreiro:** mais vida e armadura; golpe esmagador.
- **Mago:** mais energia e magia poderosa; bola de fogo.
- **Ladino:** maior chance de crítico; ataque venenoso.

Digite o número da ação e pressione **Enter**. Ataque, use habilidades, defenda para recuperar energia ou beba poções. Ataques poderosos são anunciados antes da sua ação. Entre as batalhas, descanse, compre poções e melhore sua arma no acampamento. Ganhe experiência para subir de nível. Digite **Q** em qualquer menu para sair.

Os jogos rodam localmente no terminal; não precisam de servidor ou conta online. Não há salvamento: cada execução inicia uma nova aventura.
