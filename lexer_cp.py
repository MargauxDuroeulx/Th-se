# -*- coding: utf-8 -*-

import re,sys

from peekablestream import PeekableStream


#RECHERCHE : on recherche le nom de l'objet en entier type e24 ou g6

def recherche(debut,cont):
    S = debut
    i = cont.next
    if re.match("[.0-9]", i): #Si ca continue que par des chiffres -> e,g,r
        while i is not None and re.match("[.0-9]", i) : #si c'est un element type r1,g35,e12
            S = S+cont.move_next()
            i = cont.next
    else:
        while i is not None and i not in " \n\t": #si c'est un element type variable, bool, rule
            S = S+cont.move_next()
            i = cont.next
    return S
    


#LEXER : separe le fichier entree par une liste de tokens (lexemes)

def lexer_cp(inp) :

    with open (inp, "r") as cpFile:

        contenuStr = cpFile.read() #on obtient la chaine de char du fichier
        contenu = PeekableStream(contenuStr)

        open("listeTokens.txt", "w").close() #on clear le fichier

        outputFile = open("listeTokens.txt", "w")#on va réecrire les tokens dans une sortie listeTokens
        
        while contenu.next is not None:
            c = contenu.move_next()
            if c in " \n\t":    #Si espace, passage ligne ou tabulation
                pass
            elif c in "();,":   #Si "();," -> type unique
                outputFile.write('("'+c+'","")\n')
            elif c in "=&|":    #Si "=&|" on sait qu'il y aurait le même juste dernier -> c+c
                outputFile.write('("'+c+c+'","")\n')
                c = contenu.move_next()
            elif c in "!":  #Si "!" => negation 
                outputFile.write('("negation", "'+c+'")\n')
            elif c in "+":  #Si "+" => interieur porte KooN
                outputFile.write('("'+c+'","")\n')
            elif re.match("[e]", c): #Si commence par e -> event
                S=recherche(c, contenu)
                outputFile.write('("event", "'+S+'")\n')
            elif re.match("[g]", c):    #Si commence par g -> gate
                S=recherche(c, contenu)
                outputFile.write('("gate", "'+S+'")\n')
            elif re.match("[r]", c):    #Si commence par r -> redoute ou rule
                S=recherche(c, contenu)
                if S=="rule":
                    outputFile.write('("declaration", "rule")\n')
                else:
                    outputFile.write('("redoute", "'+S+'")\n')
            elif re.match("[.0-9]", c):  #Si debut KooN -> on cherche le K correspondant (peut etre >9)
                S=recherche(c, contenu)
                outputFile.write('("koonGate", "'+S+'")\n')
            elif re.match("[a-z]", c):  #Si pas cas precedents -> string de declaration de bloc type variable ou rule
                S=recherche(c, contenu)
                outputFile.write('("declaration", "'+S+'")\n')
            else:
                outputFile.write("char inconnu :'"+c+"'.\n")
                
        outputFile.close()


def run(inp):
    lexer_cp(inp)
    print("Tokens ecrits dans le fichier listeTokens")
               
               
def main():
    if len(sys.argv) != 2 :
        print ("usage: lexer_cp <input-file> ")
        sys.exit(2)
    inp = sys.argv[1]
    run(inp)


# if this is the main file, execute main
if __name__ == "__main__":
    main()
