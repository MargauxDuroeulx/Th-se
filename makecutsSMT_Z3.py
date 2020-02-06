# -*- coding: ISO-8859-1 -*-

# Algorithm: compute cut sets with sequences (MTSS) from a structure function in smt2.
# Use Python 3

import sys, os, time, subprocess
from functions_lib import *

#ELEM: extrait l'element uniquement

def elem(s,j):
    Sout = ''
    if j == 14:   #pour les lignes comprenant nom variable e24/g35 ...
        while s[j] != ' ':
                Sout = Sout+s[j]
                j = j+1
        return Sout
    elif j == 4:    #pour les lignes comprenant assignation : true/false
        while s[j] != ')':
                Sout = Sout+s[j]
                j = j+1
        return Sout
    else : 
        print("erreur sur valeur de j dans elem(s,j)")


#EXTRACT: extrait les nom de variables et leur assignation du modele donnÃ© par Z3
# on a en ENTREE modelLines : ['sat\n', '(model \n', '  (define-fun e5 () Bool\n',
# '    false)\n', '  (define-fun e4 () Bool\n', '    true)\n',...., ')\n']
# sortie : liste de tuple [ ("e1","true") , ("e2","false") , ("e3","true") ,...] 

def extract(model):
    nbLignes = len(model)
    listeAssign = []
    i=2 # on passe direct ligne 2 (passe sat et model)
    while i < nbLignes-1 : # on s'arrete avant derniere ligne puisque c'est ')\n'
        nomVar = elem(model[i],14) #pour nom variable
        i = i+1
        assign = elem(model[i],4)
        i = i+1
        tuple=(nomVar,assign)
        listeAssign.append(tuple)
    return listeAssign


#SAVECUT : dans l'optique d'une coupe 01011, on ne garde que les elemet defaillants
# ici on considere que lorsque r1=true=1, r1 a défailli, donc true <=> defaille
# ainsi pour sauvegarder les coupes, on ne garde que les éléments qui sont true 
#inp = listeAssign / outp = liste des éléments à true

def saveCut(listeA) :
    cut = []
    for i in range(len(listeA)):
        if listeA[i][1] == 'true':
            cut.append(listeA[i][0])
    return cut


#FORMESTR: forme la ligne a reinjecter dans le fichier a partir de listeAssign
#retourne la ligne a reinjecter

def formeStr(listeA):
    nbIter=len(listeA)
    i=0
    Sout = '(assert (not (and' #si c'etait liens : Sout = '(assert (not (and'
    while i < nbIter :
        nomVar = listeA[i][0]
        if listeA[i][1] == 'false' :
            Sout = Sout #+' (not '+nomVar+')'  ON NE RAJOUTE PAS LES NOTS POUR 
        elif listeA[i][1] == 'true':
            Sout = Sout+' '+nomVar
        else :
            print("erreur sur false/true dans def formeStr")
        i = i+1
    Sout = Sout+') ))\n'+';;\n' #si c'etait liens : Sout = Sout+') ))\n'+';;\n' 
    return Sout
    
    
#NBCHAR: nous donne nombre char dans le fichier 
#-> besoin pour reecrire les str reinjecte juste avant check-sat et get-model
#FINALEMENT PAS UTILE -> on garde quand meme si besoin plus tard

def nbChar(inp):
    with open(inp, 'r') as inpFile :
        Chars = inpFile.read()
        print(Chars)
        n = len(Chars)
        return n
    
# The program expects two arguments, namely the input and output file names.
# inp : fichier smt2 du système => outp : fichier contenant l'ensemble des "coupes" ( avec event(e), gates(g), top event(r) )

def algorithm_SMT( inp, outp ):
    # Run Z3 a first time on the input
    subprocess.getoutput('z3 ' + inp + '> z3.out') #'>' pour creer fichier
    with open ("z3.out", "r") as modelFile :
        modelLines = modelFile.readlines()
        
        #print('\n',"modelLines :",modelLines,'\n')
        #print('\n',"listeAssign :",extract(modelLines),'\n')
        #print('\n',"formeStr :",formeStr(extract(modelLines)),'\n')
        
    CutSets = []

    ### SAT
    while modelLines[0] == 'sat\n' :
       
        #On extrait l'
        listeAssign = extract(modelLines)
        
        #On sauvegarde la coupe actuelle et on l'ajoute à l'ensemble CutSets
        cut = saveCut(listeAssign)
        #print(cut)
        CutSets.append(cut)
        
        #On forme le String = formule booleene de la coupe que l'on va devoir ajouter au fichier d'entrée
        newStr = formeStr(listeAssign)
        
        # open input smt2 file for appending clause
        with open(inp, "r") as smt2File :   #on ouvre en lecture une 1ere fois
            # on récupère le contenu de smt2File et on supprime les 2 derniere lignes pour injecter le lien
            smt2File_str = ''.join(smt2File.readlines()[:-2])
        with open(inp, "w") as smt2File :   #on ouvre en ecriture pour pouvoir injecter
            # on injecte le lien et on reecrit les deux lignes qu'on a suppr
            smt2File.write(smt2File_str+newStr+"(check-sat)\n(get-model)")
            
        # Run Z3 again on the input and the additional clause
        subprocess.getoutput('z3 ' + inp + '> z3.out') #'>' pour creer fichier
        with open ("z3.out", "r") as modelFile :
            modelLines = modelFile.readlines()
            
        print("Nombre de coupes 'relatives' trouvées : ",len(CutSets))
        
        
    ### UNSAT
    if modelLines[0] =='unsat\n' or modelLines[0] =='unsat' :
        with open (outp, "w") as cutFile :
        # cutFile : file where we are going to solve system tie sets
            cutFile.write("Cut sets are : \n\n")
            for c in CutSets :
                cutFile.write(str(c)+'\n')
            cutFile.write("\n")

        
    ### TROUBLE
    else :
        print ("There is an error with the output.\n") # should never happen

    return CutSets

def run( inp, outp ):
    # Time measurement
    start=time.time()

    # We call the algorithm to compute the cut sets.
    CutSets = algorithm_SMT(inp, outp)
    print ('->', len(CutSets) , 'cut sets found')
    #for m in CutSets :
        #print (m)

    # Send the TSS to algorithm_DNF to get the MTSS.
    #Mincut = algorithm_DNF(comp_nb, CutSets)
    #print ('->', Mincut)

    # Time measure
    end=time.time()
    timeNeeded = end - start
    print ('-> Time needed for the computation:', timeNeeded)
    
    return timeNeeded

def main():
    if len(sys.argv) != 3 :
        print ("usage: makecuts <input-file> <output-file>")
        sys.exit(2)
    inp = sys.argv[1]
    outp = sys.argv[2]
    run(inp, outp)

# if this is the main file, execute main
if __name__ == "__main__":
    main()


