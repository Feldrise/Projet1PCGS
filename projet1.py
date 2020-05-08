import numpy as np
import time
import random
import math

AFFICHE_ANIMATION = True
TEMP_ANIMATION = 0.3 # Le temps est en secondes
TEMP_ENTRE_JOUEUR = 1 # Le temps est en secondes

plateau = np.zeros((6,7))   
joueur = 1

## Cette fonction est purement à but d'affichage
def clearScreen():
    for i in range(0, 10):
        print()

#############################################
## Cette partie concerne le début du TP et ## 
## les principales méchaniques du jeu.     ##
#############################################

## Cette fonction permet d'initialiser le plateau de jeu
def init():
    global plateau

    plateau = np.zeros((6,7))  

## Cette fonction n'est pas dans le TP
## 
## Elle permet de donner le symbole du pion qui doit être affiché :
##  - Une croix si c'est le joueur 1 ("X")
##  - Un rond si c'est le joueur 2 ("0")
##  - Un espace si c'est une case vide (" ")
def symboleCase(symbole):
    if (symbole == 1):
        return "X"
    if (symbole == 2):
        return "O"
    
    return " "

## Cette fonction permet d'afficher le plateau 
def affiche():
    # On doit commencer par afficher les numéro de colonnes
    clearScreen()
    print("|1|2|3|4|5|6|7|")

    for ligne in range(0, len(plateau)):
        ligneString = "|"
        for colonne in range(0, len(plateau[ligne])):
            ligneString += (symboleCase(plateau[ligne, colonne]) + "|")
        
        print(ligneString)

## Cette fonction choisi le premier joueur
def choisirPremierJoueur():
    global joueur

    joueur = random.randint(1,2)

## Cette fonction change le joueur qui joue
def joueurSuivant():
    global joueur

    if joueur == 1:
        joueur = 2
    else:
        joueur = 1

## Cette fonction indique si le coup est possible
def coupEstPossible(colonne):
    return colonne >= 0 and colonne < len(plateau[0]) and plateau[0, colonne] == 0

## Cette fonction place la pièce au bon endroit
## Pour des question pratique, la fonction nous renvoie le numéro de la ligne sur laquelle le pion est tombé
def lacherPiece(colonne):
    global plateau

    plateau[0, colonne] = joueur # Il faut que par défaut il soit en haut
    ligneDuPion = 0

    for ligne in range(0, len(plateau) - 1): # Le "-1" indique qu'on ne veut pas aller check sur la dernière ligne, car c'est justement la dernière ligne
        if plateau[ligne + 1, colonne] == 0:
            plateau[ligne, colonne] = 0
            plateau[ligne + 1, colonne] = joueur

            ligneDuPion = ligne + 1
        
            if AFFICHE_ANIMATION:
                time.sleep(TEMP_ANIMATION)
                affiche()

    return ligneDuPion

# N'oubliez pas qu'une bonne pratique est de tester le plus vite et régulièrement possible.
# Il ne faut pas attendre le projet pour commencer à chercher les bugs

# affiche()
# lacherPiece(2)

############################################################
## Cette partie concerne la détermination du coup gagnant ##
############################################################

## Cette fonction détermine si le coup est gagnant verticalement
def coupGagnantVertical(lignePion, colonnePion, joueur):
    ## NOTE : ici on ne prend pas la variable global joueur mais celle passée à la fonction

    # Cette fonction est relativement simple, on doit juste vérifier qu'il y 3 pions en dessous
    pionEntourant = 0
    for ligne in range(lignePion + 1, len(plateau)):
        if plateau[ligne, colonnePion] != joueur:
            break
        
        pionEntourant += 1

    return pionEntourant >= 3

## Cette fonction détermine si le coup est gagnant horizontalement
def coupGagnantHorizontal(lignePion, colonnePion, joueur):
    ## NOTE : ici on ne prend pas la variable global joueur mais celle passée à la fonction

    # Dans cette fonction, on compte le nombre de pion du joueur à droite, puis à gauche
    pionEntourant = 0

    for colonne in range(colonnePion + 1, len(plateau)): # D'abord à droite
        if plateau[lignePion, colonne] != joueur:
            break
        
        pionEntourant += 1

    for colonne in range(colonnePion - 1, 0, -1): # Puis à gauche
        if plateau[lignePion, colonne] != joueur:
            break
        
        pionEntourant += 1

    return pionEntourant >= 3

## Cette fonction détermine si le coup est gagnant sur la diagonal qui monte à droite
def coupGagnantDiagonalDroite(lignePion, colonnePion, joueur):
    ## NOTE : ici on ne prend pas la variable global joueur mais celle passée à la fonction

    # Dans cette fonction, on compte le nombre de pion du joueur à droite+haut, puis à gauche+bas
    pionEntourant = 0

    colonne = colonnePion
    for ligne in range(lignePion - 1, 0, -1): ## D'abord on regarde en haut à droite
        colonne += 1

        # NOTE : On ne veut pas dépasser le nombre de colonne du plateau
        if (colonne > len(plateau[ligne]) - 1 or plateau[ligne, colonne] != joueur):
            break
        
        pionEntourant += 1

    colonne = colonnePion
    for ligne in range(lignePion + 1, len(plateau)): ## Ensuite on regarde en bas à gauche
        colonne -= 1

        if (colonne < 0 or plateau[ligne, colonne] != joueur):
            break
        
        pionEntourant += 1

    return pionEntourant >= 3

## Cette fonction détermine si le coup est gagnant sur la diagonal qui monte à gauche
def coupGagnantDiagonalGauche(lignePion, colonnePion, joueur):
    ## NOTE : ici on ne prend pas la variable global joueur mais celle passée à la fonction

    # Dans cette fonction, on compte le nombre de pion du joueur à droite+bas, puis à gauche+haut
    pionEntourant = 0

    colonne = colonnePion
    for ligne in range(lignePion + 1, len(plateau)): ## D'abord on regarde en bas à droite
        colonne += 1

        # NOTE : On ne veut pas dépasser le nombre de colonne du plateau
        if (colonne > len(plateau[ligne]) - 1 or plateau[ligne, colonne] != joueur):
            break
        
        pionEntourant += 1

    colonne = colonnePion
    for ligne in range(lignePion - 1, 0, -1): ## Ensuite on regarde en haut à gauche
        colonne -= 1

        if (colonne < 0 or plateau[ligne, colonne] != joueur):
            break
        
        pionEntourant += 1

    return pionEntourant >= 3

## Retourne si un coup est gagnant
def coupGagnant(lignePion, colonnePion, joueur):
    return coupGagnantVertical(lignePion, colonnePion, joueur) or coupGagnantHorizontal(lignePion, colonnePion, joueur) or coupGagnantDiagonalDroite(lignePion, colonnePion, joueur) or coupGagnantDiagonalGauche(lignePion, colonnePion, joueur)


####################################################################
## Cette partie concerne l'IA. Décendez pour la partie concernant ##
## la boucle de jeu.                                              ##
####################################################################

def jouerOrdiV1():
    colonneJoue = random.randint(0,6)

    while coupEstPossible(colonneJoue) == False:
        colonneJoue = random.randint(0,6)

    return colonneJoue

############################################
## Cette partie concerne la boucle du jeu ##
############################################

## Cette fonction détermine si il reste encore des coups possible (donc que
## la première ligne n'est pas remplie)
def jeuEncorePossible():
    for colonne in range(0, len(plateau[0])):
        if plateau[0, colonne] == 0:
            return True

    return False

## Cette fonction n'est pas explicite dans le TP. C'est une sous partie de la boucle 
## du jeu qui conciste à jouer une partie
def jouerPartie():
    partieFini = False

    while partieFini == False:
        affiche()

        colonneJoue = 0
        ligneJoue = 0

        if joueur == 1:
            print("Votre tour :")
            colonneJoue = int(input("Choisis une colonne entre 1 et 7 : ")) - 1

            while coupEstPossible(colonneJoue) == False:
                colonneJoue = int(input("Erreur de saisie. Choisis une colonne entre 1 et 7 : ")) - 1
            
            ligneJoue = lacherPiece(colonneJoue)
        elif joueur == 2:
            print("Tour de l'ordinateur :")
            time.sleep(TEMP_ENTRE_JOUEUR)
            colonneJoue = jouerOrdiV1()
            
            ligneJoue = lacherPiece(colonneJoue)

        if coupGagnant(ligneJoue, colonneJoue, joueur):
            print()
            print("==========")
            if joueur == 1:
                print(" VAINQUEUR : vous")
            else:
                print(" VAINQUEUR : l'ordinateur")
            print("==========")
            print()

            partieFini = True
        elif jeuEncorePossible() == False:
            print()
            print("==========")
            print(" FIN DU JEU. Il n'y a pas de vainqueur...")
            print("==========")
            print()
        else:
            joueurSuivant()


# Et oui, j'ai tenté de jouer une simple partie avant de jouer le jeu.
# Tester le plus souvent possible ! 
# jouerPartie()

## Cette fonction est la boulce du jeu
def boucleJeu():
    jeuFini = False

    while jeuFini == False:
        init()
        choisirPremierJoueur()
        jouerPartie()

        jeuFini = input("Voulez vous rejouer ? (o/N)") != "o"

    print()
    print("Merci d'avoir joué !")
    print("2020 (c) Feldrise | https://feldrise.com")

boucleJeu()