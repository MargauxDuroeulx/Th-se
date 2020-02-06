# -*- coding: utf-8 -*-

import re,sys

from peekablestream import PeekableStream
from lexer_cp import *
from parser_smt2 import *

def LexAndPars(inp,outp):

    #On appelle le lexer pour créer le listeTokens.txt
    lexer_cp(inp)

    #On appelle le parser sur le fichier listeTokens.txt
    #amelioration : ne pas creer de fichier listeTokens
    parser_smt2("listeTokens.txt",outp)




def run(inp,outp):
    LexAndPars(inp,outp)
    print("Fichier converti de .cp vers .smt2")
                        
def main():
    if len(sys.argv) != 3 :
        print ("usage: LexAndPars <input-file> <output-file>")
        sys.exit(2)
    inp = sys.argv[1]
    outp = sys.argv[2]
    run(inp, outp)

# if this is the main file, execute main
if __name__ == "__main__":
    main()
