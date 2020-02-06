# -*- coding: ISO-8859-1 -*-

# Use Python 3

import sys, os, time, subprocess

from functions_lib import *
from makecutsSMT_Z3 import *


#VAR_SUPPR_SMR : on souhaite simplement supprimer dans les coupes les éléments qui ne sont pas cohérents :
#En effet une coupe est un ensemble d'evenements de bases qui, lorsqu'il défaillent, provoque la défaillance de r1 (TE)
#Or ici nos coupes sont composés de gates et du TE, qui doivent donc être supprimés
# inp : fichier smt2 du systeme => outp : fichier contenant les coupes avec uniquement les events

def var_suppr_SMT( inp, outp ):

    #On recup l'ensemble des coupes grâce au fichier makecutsSMT-Z3.py :
    CutSets = algorithm_SMT(inp,"CutSetsResult.txt")
    Taille=len(CutSets)
    
    iter = 1 #INDICATIF : savoir ou en est le prog

    for i in range(len(CutSets)):
        for j in range(len(CutSets[i])-1,-1,-1):  #on fait dans sens inverse car sinon lorsque del -> tous les element de la liste perdent un indice
            #print(type(CutSets[i][j]),CutSets[i][j],CutSets[i][j][0])
            if CutSets[i][j][0] != 'e' :  #on regarde ma premiere lettre [0] du str : si c'est pas e = event, on del
                #print("ancien :",CutSets[i])
                del CutSets[i][j]
                #print("je supprime :",CutSets[i][j-1])     #apres suppr : j-1
                #print("nouveau :",CutSets[i])
                
        print("Suppression des variables supp :",iter,"/",Taille," => ",round((iter*100)/Taille,2),"%")
        iter=iter+1
                
    #on reecrit les VRAIES coupes dans outp
    with open (outp, "w") as cutFile :
        # cutFile : file where we are going to solve system tie sets
            cutFile.write("Cut sets are : \n\n")
            for c in CutSets :
                cutFile.write(str(c)+'\n')
            cutFile.write("\n")
            
    return CutSets
    
   
def run( inp, outp ):
    # Time measurement
    start=time.time()

    # We call the algorithm to compute the minimal tie sets.
    CutWAV = var_suppr_SMT( inp, outp )
    #for m in minimalties :
        #print (m)
     
    # Time measure
    end=time.time()
    timeNeeded = end - start
    print ('-> Time needed for the computation:', timeNeeded)
    return timeNeeded

def main():
    if len(sys.argv) != 3 :
        print ("usage: maketies <input-file> <output-file>")
        sys.exit(2)
    inp = sys.argv[1]
    outp = sys.argv[2]
    run(inp, outp)

# if this is the main file, execute main
if __name__ == "__main__":
    main()
