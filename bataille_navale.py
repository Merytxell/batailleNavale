#!/usr/bin/env python
#  -*- coding: utf-8 -*-

# la grille de jeu virtuelle est composée de 10 x 10 cases
# une case est identifiée par ses coordonnées, un tuple (no_ligne, no_colonne)
# un no_ligne ou no_colonne est compris dans le programme entre 1 et 10,
# mais pour le joueur une colonne sera identifiée par une lettre (de 'A' à 'J')

grid_size = 10

# détermination de la liste des lettres utilisées pour identifier les colonnes :
LETTERS = [chr(letter_code) for letter_code in range(ord('A'), ord('A') + grid_size)]

# différents états possibles pour une case de la grille de jeu
SEA, MISSED_SHOT, HIT_SHOT, SUNK_SHOT = 0, 1, 2, 3
# représentation du contenu de ces différents états possible pour une case
# (tableau indexé par chacun de ces états)
SQUARE_STATE_REPR = [' ', 'X', '#', '-']

# chaque navire est constitué d'un dictionnaire dont les clés sont les
# coordonnées de chaque case le composant, et les valeurs correspondantes
# l'état de la partie du navire correspondant à la case
# (True : intact ; False : touché)

# les navires suivants sont disposés de façon fixe dans la grille :
#      +---+---+---+---+---+---+---+---+---+---+
#      | A | B | C | D | E | F | G | H | I | J |
#      +---+---+---+---+---+---+---+---+---+---+
#      | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10|
# +----+---+---+---+---+---+---+---+---+---+---+
# |  1 |   |   |   |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  2 |   | o | o | o | o | o |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  3 |   |   |   |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  4 | o |   |   |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  5 | o |   | o |   |   |   |   | o | o | o |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  6 | o |   | o |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  7 | o |   | o |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  8 |   |   |   |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  9 |   |   |   |   | o | o |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# | 10 |   |   |   |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+



#ajout class bateau avec les états (touché ou coulé)
class Ship:
    def __init__(self,name,positions):
        self.name= name
        self.position={pos: True for pos in positions}

    def is_hit(self, shot_coord):
        if shot_coord in self.position:
            self.position[shot_coord]= False
            return True
        return False

    def is_sunk(self):
        return not any(self.position.values())

 #ajout grille avec bateau touché ou coulé
class Grid:
    def __init__(self):
        self.size = grid_size
        self.ships = []
        self.shoot = set()

    def add_ship(self,ship):
        self.ships.append(ship)

    def ship_shoot(self, coord):
        if coord in self.shoot:
            print("Vous avez déjà tiré ici.")
            return False

        self.shoot.add(coord)

        for ship in self.ships:
            if ship.is_hit(coord):
                print("Touché !")
                if ship.is_sunk():
                    print(f"{ship.name} est coulé !")
                    self.ships.remove(ship)
                return True

        print("Manqué !")
        return False

    def display_grid(self):
     """Affichage de la grille de jeu."""
     print("\n    " + "   ".join(LETTERS))
     print("  +" + "---+" * self.size)
     for line_no in range(1, self.size + 1):
         row = f"{line_no:2} |"
         for column_no in range(1, self.size + 1):
             coord = (line_no, column_no)
             if coord in self.shoot:
                 state = "X" if any(coord in ship.position and not ship.position[coord] for ship in self.ships) else "O"
             else:
                 state = " "
             row += f" {state} |"
         print(row)
         print("  +" + "---+" * self.size)


def ask_coord():
    while True:
    # ex. d'entrée attendue : 'A1'
        player_coord = input("Entrez les coordonnées de votre tir (ex. : 'A1', 'H8') : ")

        if len(player_coord) <= 2:
            letter, number = player_coord[0], player_coord[1:]
            if letter in LETTERS:
                try:
                    line_no = int(number)
                    column_no = LETTERS.index(letter) + 1
                    if 1 <= line_no <= grid_size:
                        return (line_no, column_no)
                except ValueError:
                    pass
        print("Coordonnée invalides, réessayez")



grid = Grid()
ships_list = [
    Ship("Porte-avions", [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6)]),
    Ship("Croiseur", [(4, 1), (5, 1), (6, 1), (7, 1)]),
    Ship("Destroyer", [(5, 3), (6, 3), (7, 3)]),
    Ship("Sous-marin", [(5, 8), (5, 9), (5, 10)]),
    Ship("Torpilleur", [(9, 5), (9, 6)])
]


for ship in ships_list:
    grid.add_ship(ship)

# Boucle de jeu
while grid.ships:
    grid.display_grid()
    coord = ask_coord()
    grid.ship_shoot(coord)

print("Félicitations ! Tous les navires ont été coulés.")







