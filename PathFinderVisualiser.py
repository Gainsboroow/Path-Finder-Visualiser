"""
Made by Gainsboroow 
Github : https://github.com/Gainsboroow
"""

from tkinter import *
from tkinter.messagebox import *

from time import sleep
from random import *

import sys
sys.setrecursionlimit(10**6)


#____Initialisation de la window_____
hauteur, largeur = 600, 1000
caseSize = 40

window = Tk()
window.title("Shortest path visualizer")
window.geometry(str(largeur)+"x"+str(hauteur)+"+0+0")

canvas = Canvas(background = "black")
canvas.place(x=0,y=0, width = largeur, height = hauteur)

nbRow, nbCol = hauteur // caseSize, largeur // caseSize

points, passageEnCours = [ () ] *2

minCaseSize, maxCaseSize = 6, 200

nbMaxRow, nbMaxCol = hauteur // minCaseSize, largeur // minCaseSize

grid = [ [ None for a in range(nbMaxCol+1) ] for i in range(nbMaxRow+1)]
gridDistance = [ [ -1 for a in range(nbMaxCol+1) ] for i in range(nbMaxRow+1) ]

#____________________________________

affichageChemin = []

couleurObstacle = "white"
ancienneCouleurCible = "white"
couleurCible = "red"

coordCible = (nbRow // 2, nbCol // 3)
coordArrivee = (nbRow // 2, 2 * nbCol // 3)



deplacement = [ (0, 1), (1,0), (0,-1), (-1,0) ]

#____________________________________

def createRectangle(lin, col, color = "white"):
    global grid
    return canvas.create_rectangle(col*caseSize, lin*caseSize, (col+1)*caseSize, (lin+1)*caseSize, \
                                   fill = color, outline = "grey")


for i in range(nbMaxRow):
    for a in range(nbMaxCol):
        grid[i][a] = createRectangle(i, a)

def init(*param):
    global points, passageEnCours, grid, coordCible, coordArrivee, gridDistance, nbRow, nbCol, affichageChemin
    points = []


    for i in affichageChemin:
        canvas.delete(i)

    affichageChemin = []

    passageEnCours = False

    nbRow, nbCol = hauteur // caseSize, largeur // caseSize

    gridDistance = [ [ -1 for a in range(nbMaxCol+1) ] for i in range(nbMaxRow+1) ]

    coordCible = (nbRow // 2, nbCol // 3)
    coordArrivee = (nbRow // 2, 2 * nbCol // 3)

    for i in range(nbMaxRow):
        for a in range(nbMaxCol): 
            """
            if randint(0,5):
                canvas.itemconfig(grid[i][a], fill = "white" )
            else:
                canvas.itemconfig(grid[i][a], fill = "firebrick" )
            """
            canvas.itemconfig(grid[i][a], fill = "white" )
            canvas.coords(grid[i][a], a*caseSize, i*caseSize, (a+1)*caseSize, (i+1)*caseSize)

    canvas.itemconfig(grid[nbRow//2][nbCol//3], fill = couleurCible)
    canvas.itemconfig(grid[nbRow//2][2*nbCol//3], fill = couleurCible)


init()

def inGrid(lin, col):
    global nbRow, nbCol
    return 0 <= lin < nbRow and 0 <= col < nbCol

def mouse_wheel(event):
    global caseSize

    #canvas.yview_scroll(-1*(event.delta//120), "units")

    if event.delta == -120 and minCaseSize < int(caseSize // 1.5): #Scroll vers le bas
        caseSize = int( caseSize // 1.5 )
    elif event.delta == 120 and maxCaseSize > int(caseSize * 1.5): #Scroll vers le haut
        caseSize = int( caseSize * 1.5 )
    else: return

    init()


def obstacle(event):
    global grid, gridDistance, couleurObstacle
    lin, col = event.y // caseSize, event.x // caseSize

    if not( inGrid(lin, col) ) :
        return

    caseCouleur = canvas.itemcget( grid[lin][col] , 'fill')

    if caseCouleur == couleurObstacle == "white":
        canvas.itemconfig(grid[lin][col], fill = "firebrick")
        gridDistance[lin][col] = float("inf")

    elif caseCouleur == couleurObstacle == "firebrick":
        canvas.itemconfig(grid[lin][col], fill = "white")
        gridDistance[lin][col] = -1


def _obstacle(event):
    global couleurObstacle
    lin, col = event.y // caseSize, event.x // caseSize

    if not( inGrid(lin, col) ) :
        return

    couleurObstacle = canvas.itemcget( grid[lin][col] , 'fill')


def bfs(linDep, colDep):
    global passageEnCours, grid, gridDistance, points, coordArrivee
    
    passageEnCours = True
    
    couleurCase = canvas.itemcget( grid[linDep][colDep] , 'fill')
    if not( inGrid(linDep, colDep) ) or (couleurCase != "white" and couleurCase != couleurCible):
        return
    
    points = []
    for dlin, dcol in deplacement:
        if inGrid(linDep+dlin, colDep+dcol) and canvas.itemcget( grid[linDep + dlin][colDep + dcol] , 'fill') == "white":
            points.append( (linDep+dlin, colDep+dcol) )
            gridDistance[linDep+dlin][colDep+dcol] = 1

    while points:
        if not passageEnCours: return

        lin, col = points.pop(0)
        canvas.itemconfig(grid[lin][col], fill = "light green")
        
        for a,b in deplacement:
            if not(inGrid(lin+a, col+b)): 
                continue

            nLin, nCol = lin+a, col+b
            couleurCase = canvas.itemcget( grid[nLin][nCol] , 'fill')

            if couleurCase == "white":
                points.append( (nLin, nCol) )
                canvas.itemconfig(grid[nLin][nCol], fill = "chartreuse")
                distanceCase = gridDistance[lin][col] + 1
                gridDistance[nLin][nCol] = distanceCase

            elif couleurCase == couleurCible and (nLin,nCol) != (linDep, colDep):
                passageEnCours = False
                distanceCase = gridDistance[lin][col] + 1
                gridDistance[nLin][nCol] = distanceCase

        if visualisation.get():
            if caseSize < 10:
                if not( distanceCase % (valeurScale.get()//10 + 1) ):
                    canvas.update()
            else:
                attente = ( 100 - valeurScale.get() ) 
                for i in range(attente**3):
                    pass
                canvas.update()
        

def dfs(lin, col, distance):
    global passageEnCours, grid, gridDistance, coordCible, coordArrivee

    if not(passageEnCours) or not( inGrid(lin, col) ) or 0 <= gridDistance[lin][col] <= distance or gridDistance[lin][col] == float("inf"):
        return


    gridDistance[lin][col] = distance

    couleurCase = canvas.itemcget( grid[lin][col] , 'fill')

    if couleurCase == couleurCible and (lin,col) == coordArrivee:
        return 

    if visualisation.get():
        if distance != 0:
            canvas.itemconfig(grid[lin][col], fill = "gainsboro" )
        if distance % 2 == 1:
            canvas.update()

    for a,b in deplacement:
        dfs(lin+a, col+b, distance+1)
    
    if visualisation.get():
        canvas.itemconfig(grid[lin][col], fill = "white" )


def recherche(*param):
    global passageEnCours, coordCible, gridDistance, coordArrivee
    passageEnCours = True

    typeDeRecherche = algoRechercheChemin.get()

    if typeDeRecherche == "BFS":
        gridDistance[coordCible[0]][coordCible[1]] = 0
        bfs(*coordCible)

    elif typeDeRecherche == "DFS":
        dfs(*coordCible, 0)

    else: return    

    passageEnCours = True
    remonterChemin()
    passageEnCours = False
    canvas.itemconfig(grid[coordCible[0]][coordCible[1]], fill = couleurCible )
    
    lin, col = coordArrivee
    distanceTrouvee = gridDistance[lin][col]
    if distanceTrouvee != -1:
        showinfo('Plus court chemin', 'Distance ' + str(gridDistance[lin][col]) + '\nAppuyez sur F4 pour effectuer une remise à 0')
    else:
        showerror('Plus court chemin', 'Pas de chemin trouvé')


def remonterChemin():
    global couleurCible, coordArrivee, coordCible, gridDistance, affichageChemin

    lin, col = coordArrivee

    affichageChemin = []

    while (lin, col) != coordCible:
        if not(passageEnCours): return 
            
        minimum = float("inf")
        nLin, nCol = (0,0)
        for dLin, dCol in deplacement:
            if inGrid(lin+dLin, col+dCol) and 0 <= gridDistance[lin+dLin][col+dCol] < minimum:
                nLin, nCol = lin+dLin, col+dCol 
                minimum = gridDistance[lin+dLin][col+dCol]

        if minimum == float("inf"):
            return

        #canvas.itemconfig(grid[lin][col], fill = "magenta")
        
        affichageChemin.append( canvas.create_line( (col+0.5)*caseSize, (lin+0.5)*caseSize, (nCol+0.5)*caseSize, (nLin+0.5)*caseSize, width = 3, fill = "magenta" ) )
        lin, col = nLin, nCol        



def afficherScale():
    if visualisation.get() == 1:
        scale.place(x=largeur-110, y = 0)
    else:
        scale.place(x=largeur-110, y = -1000)


def checkCible(event):
    global couleurCible, coordCible, coordArrivee

    lin, col = event.y // caseSize, event.x // caseSize

    if not(inGrid(lin, col)) or canvas.itemcget(grid[lin][col], 'fill') != couleurCible:
        return
    
    if coordCible != (lin,col):
        coordCible, coordArrivee = (lin, col), coordCible


def moveCible(event):
    global couleurCible, coordCible, ancienneCouleurCible

    lin, col = event.y // caseSize, event.x // caseSize

    if not(inGrid(lin, col)) or ( abs(coordCible[0]-lin) + abs(coordCible[1]-col) > 3):
        return
    
    precLin, precCol = coordCible
    canvas.itemconfig(grid[precLin][precCol], fill = ancienneCouleurCible)
    
    ancienneCouleurCible = canvas.itemcget(grid[lin][col], 'fill')
    canvas.itemconfig(grid[lin][col], fill = couleurCible)

    coordCible = (lin,col)

def fonctionDiagonale():
    global deplacement
    if etatDiagonale.get():
        deplacement = [ (0, 1), (1,0), (0,-1), (-1,0), (-1,-1), (-1,1), (1,-1), (1,1) ]
    else:
        deplacement =  [ (0, 1), (1,0), (0,-1), (-1,0) ]

#_______________ WIDGETS __________________________

algoRechercheChemin = StringVar() 
algoRechercheChemin.set(0)
boutonBfs = Radiobutton(window, text="BFS", variable = algoRechercheChemin, value="BFS", relief=RAISED)
boutonDfs = Radiobutton(window, text="DFS", variable = algoRechercheChemin, value="DFS", relief=RAISED)

boutonBfs.place(x=0,y=0, width = 50, height = 25)
boutonDfs.place(x=0, y=25, width = 50, height = 25)

etatDiagonale = IntVar()
boutonDiag = Checkbutton(window, command = fonctionDiagonale, variable = etatDiagonale, text="Autoriser les diagonales", relief=RAISED)
boutonDiag.place(x=0, y=50, width = 155, height = 25)

visualisation = IntVar()
boutonVisualiser = Checkbutton(window, command = afficherScale, variable = visualisation, text="Visualiser le parcours", relief=RAISED)
boutonVisualiser.place(x=0, y = 75, width = 140, height = 25)

valeurScale = IntVar()
scale = Scale(window, variable = valeurScale, label='Vitesse (%)', sliderlength = 20)



menubar = Menu(window)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Lancer la recherche     F5", command=recherche)
menu1.add_command(label="Remise à 0                    F4", command=init)
menu1.add_separator()
menu1.add_command(label="Quitter", command=window.quit)
menubar.add_cascade(label="Executer", menu=menu1)

window.config(menu=menubar)


#______________ BIND _____________________________

window.focus_set()

window.bind("<B3-Motion>", obstacle )
window.bind('<ButtonPress-3>', _obstacle)

window.bind("<ButtonPress-1>", checkCible)
window.bind("<B1-Motion>", moveCible)

window.bind("<F5>", recherche)
window.bind("<F4>", init)

window.bind("<MouseWheel>", mouse_wheel)


window.mainloop()
