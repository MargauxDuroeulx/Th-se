# -*- coding: utf-8 -*-

import re,sys

from peekablestream import PeekableStream

#NB_LIGNES : on a besoin du nombre de lignes pour la creation de la liste de tuples

def nb_lignes(inp):
    fd = open(inp, 'r')
    n = 0
    while fd.readline():
        n += 1
    fd.close()
    return n
    

#RECHERCHE_STRING : on recherche les strings a travers les tokens
#cela permet de rentrer l'ensemble des tuples dans la liste afin de travailler sur les indices i

def recherche_tuple(delim,cont):
    S1 = ""
    while cont.next != delim:   #on boucle tant qu'on arrive pas au delim = '"' = fin du string
        c = cont.move_next()
        if c is None:
            raise Exception("Un tuple n'a pas ete acheve avant la fin du programme")
        S1 = S1+c   #on ajoute le char a chaque iter
    cont.move_next()    #on passe juste le dernier '"'
    
    S2 = ""
    while c != delim:  #on boucle pour arriver sur le second string (debut = '"')
        c = cont.move_next()
    while cont.next != delim:   # meme methode que S1
        c = cont.move_next()
        if c is None:
            raise Exception("Un tuple n'a pas ete acheve avant la fin du programme")
        S2 = S2+c
    cont.move_next()
    
    return (S1,S2)

#RECUP_TAB: methode qui rentre dans une liste de tuples ("type","valeur")
#on commence par obtenir le string du texte complet du fichier
#on lit ensuite ce string et des qu'on rencontre "(" on rentre les 2 strings

def recup_liste(inp): #tuple = ("type","valeur")

    nbl = nb_lignes(inp)

    with open (inp, "r") as tokenFile:
        contenuStr = tokenFile.read()   #on obtient la chaine de char du fichier
        contenu = PeekableStream(contenuStr)    #on le transforme en objet pour pouvoir travailler plus facilement dessus
        listeTuples = []
        while contenu.next is not None: 
            i=0
            c = contenu.move_next()
            if c=='"':  #on recherche le premier string d'un tuple pour ajouter un tuple (S1,S2) dans la liste
                listeTuples.append(recherche_tuple(c,contenu))
                i=i+1
                
    return listeTuples


#COMBIINDICE: renvoie la liste des combinaisons d'indice
#Exemple : combiIndice(2,3,None,None) renvoie [[3, 2], [3, 1], [2, 1]]
#inspiré de Guillaume Duriaud : https://guigui.developpez.com/

def combiIndice(K,N,liste,res):
    if liste is None: liste=[]
    if res is None: res=[]
    if K==0:
        res.append(liste)
        return 
    if N==0: return
    l1=list(liste)
    l1.append(N)
    combiIndice(K-1, N-1, l1, res)
    combiIndice(K, N-1, liste, res)
    return res

#COMBILISTE: renvoie la liste de toutes les combinaison possibles de KooN
#il suffira ensuite de faire des (or (and de tous les elements de cette liste

def combiListe(K,N,listeElements):
    listeIndice = combiIndice(K,N,None,None)
    pointeur = 0
    while pointeur < len(listeIndice):
        for i in range(K):
            indice = listeIndice[pointeur][i]
            listeIndice[pointeur][i] = listeElements[indice-1]
        pointeur = pointeur+1
    return listeIndice
    
#FORMEKOON: ecrit sous un str la porte KooN

def formeKooN(K,N,listeElements):
    liste = combiListe(K,N,listeElements)
    S = " (or "
    for i in range(len(liste)):
        S = S+"(and"
        for j in range(K):
            S = S+" "+liste[i][j]
        S = S+") "
    S = S+")"
    return S
    

#DETER_ABC: determine les elements des assert
#ATTENTION : pour l'instant on suppose que les portes sont a comportement unique
#c-a-d composee que de && ou de ||, pas de melange des deux

def deter_ABC(liste,pointeur):
        while (liste[pointeur][0] != "redoute") and (liste[pointeur][0] != "gate"): # on veut le A qui est soit rX ou gX
            pointeur=pointeur+1
            
        A = liste[pointeur][1]
        pointeur=pointeur+1
        
        B = []
        C = ""
        
        while (liste[pointeur][0] != "event") and (liste[pointeur][0] != "gate") and (liste[pointeur][0] != "koonGate"): # on veut les B qui sont soit gX ou eX ou savoir si KooN
            pointeur=pointeur+1
        
        if (liste[pointeur][0] == "koonGate"):
            C = liste[pointeur][1]  #Ici C enregistre le K du KooN
            while (liste[pointeur][0] != ";"):
                if (liste[pointeur][0] == "negation"):  #si on tombe sur "!" : on va a l'element suivant et on retourne le not
                    pointeur=pointeur+1
                    B.append(" (not "+liste[pointeur][1]+")")
                elif (liste[pointeur][0] == "event") or (liste[pointeur][0] == "gate"):
                    B.append(liste[pointeur][1]) #ici on enregistre toutes les e/g dans la KooN
                pointeur=pointeur+1
            return A,B,C,pointeur
            
        
        while (liste[pointeur][0] != ";"):
            if (liste[pointeur][0] == "negation"):  #si on tombe sur "!" : on va a l'element suivant et on retourne le not
                pointeur=pointeur+1
                B.append(" (not "+liste[pointeur][1]+")")
            elif (liste[pointeur][0] == "event") or (liste[pointeur][0] == "gate"):
                B.append(" "+liste[pointeur][1]) #on met le " " avant car besoin lors de la reecriture
            elif (liste[pointeur][0] == "&&") or (liste[pointeur][0] == "||"):
                C = liste[pointeur][0]
            pointeur=pointeur+1
        
        return A,B,C,pointeur



#TRANSFO_C : besoin de transfo "&&" en "and" et "||" en "or"

def transfo_C(C):
    if C == "&&":
        C = "and"
    elif C == "||":
        C = "or"
    return C
    
    
    
#TSEITIN: transpose les relations portes avec la transfo de tseitin 

def tseitin(A,B,C):

    tseiStr1 = "(assert (or (not "+A+")"
    if C == "&&":   # si c'est un and, on a besoin de le preciser
        tseiStr1 = tseiStr1+" (and"
        for Bj in B:       
            tseiStr1 = tseiStr1+Bj
        tseiStr1 = tseiStr1+")))\n" # on referme 2 parenthese
    elif C == "||":
        for Bj in B:       # si c'est un ou, ou(ou)= ou donc pas besoin
            tseiStr1 = tseiStr1+Bj
        tseiStr1 = tseiStr1+"))\n"
    elif C == "":
        for Bj in B:       # si c'est juste un event type (g14==e65
            tseiStr1 = tseiStr1+Bj
        tseiStr1 = tseiStr1+"))\n"
    else: # C = K de la porte KooN
        N = len(B)   # nombre N d'elements e/g dans la porte KooN
        K = int(C)  # on convertit le string C en int K
        StrKooN = formeKooN(K,N,B)
        tseiStr1 = tseiStr1+StrKooN
        tseiStr1 = tseiStr1+"))\n"
        
    
    tseiStr2 = "(assert (or (not "
    
    if re.match("[.0-9]", C): # SI ON A KOON
        N = len(B)   # nombre N d'elements e/g dans la porte KooN
        K = int(C)  # on convertit le string C en int K
        StrKooN = formeKooN(K,N,B)
        tseiStr2 = tseiStr2+StrKooN
        tseiStr2 = tseiStr2+") " # on referme le KooN
        tseiStr2 = tseiStr2+A+"))\n"
        return (tseiStr1,tseiStr2)
        
    if C == "&&":   # si c'est un and, on a besoin de le preciser
        tseiStr2 = tseiStr2+"(and"
    elif C == "||":
        tseiStr2 = tseiStr2+"(or"
        
    for Bj in B:       
        tseiStr2 = tseiStr2+Bj
        
    if C == "":
        tseiStr2 = tseiStr2+") " 
    else:
        tseiStr2 = tseiStr2+")) "
        
    tseiStr2 = tseiStr2+A+"))\n"
    
    
    
    return (tseiStr1,tseiStr2)
    
 
    
    
#PARSER: on utilise les tokens pour trasnformer en format smt2 utilisable par Z3
#on rentre le output dans l'invite de commande -> cree le fichier

def parser_smt2(inp,outp):

    nbl = nb_lignes(inp) #on a besoin du nb de ligne pour ne pas etre out of range a la fin des verifs

    listeTuples = recup_liste(inp) #plus facile de travailler sur liste de tuples que directement sur des chars

    open(outp, "w").close() #on reset le fichier si on avait ecrit dessus

    with open(outp, "w") as outputFile: #on cree un fichier de sorti du nom choisi

        outputFile.write(";Tokens convertis en format smt2:\n;;\n(set-logic QF_UFLIA)\n")
       
        ptr = 0 #pointeur
        
        while (listeTuples[ptr][0] != "event") and (listeTuples[ptr][0] != "gate") and (listeTuples[ptr][0] != "redoute"): # on veut arriver au debut des declaration variables
            ptr = ptr+1
        
        while listeTuples[ptr][1] != "rule": # on veut traverser toutes les variables jusqu'au debut des rules
            if (listeTuples[ptr][0] == "event") or (listeTuples[ptr][0] == "gate") or (listeTuples[ptr][0] == "redoute"):
                outputFile.write("(declare-fun "+listeTuples[ptr][1]+" () Bool)\n") # des qu'on tombe sur event ou gate ou r1, on declare sa variable
            ptr = ptr+1
            
        outputFile.write(";;\n") # on demarre les regles
        
        
        
        #Format A == B[] avec A la gate et B = (B[1] && B[2] && ...) et C=&& ou C=||
        
        # ce bloc correspond a l'assert du top event -> 1er assert, pas de tseitin ici
        # (A,B,C,ptr) = deter_ABC(listeTuples,ptr)
        # outputFile.write("(assert ("+transfo_C(C))
        # for Bj in B:
            # outputFile.write(Bj)
        # outputFile.write("))\n;;\n")
        
        
        
        while (ptr+1 < nbl-1):
            (A,B,C,ptr) = deter_ABC(listeTuples,ptr)
            (tseiStr1,tseiStr2) = tseitin(A,B,C)    #on definit les 2 assert equivalent a la definition de la gate
            outputFile.write(tseiStr1+tseiStr2+";;\n")
            #print(A,B,C) #test si ca marche
            ptr=ptr+1 # quand on arrive au ";", on debute la ligne suivante pour etre coherent avec la verif is not None de ce while
        
        outputFile.write("(assert r1)\n;;\n")
        
        outputFile.write("(check-sat)\n(get-model)")
    
        


def run(inp,outp):
    parser_smt2(inp,outp)
    print("Tokens convertis en format smt2")
                        
def main():
    if len(sys.argv) != 3 :
        print ("usage: parser_smt2 <input-file> <output-file>")
        sys.exit(2)
    inp = sys.argv[1]
    outp = sys.argv[2]
    run(inp, outp)

# if this is the main file, execute main
if __name__ == "__main__":
    main()