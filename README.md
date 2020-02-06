# These
Evaluation de la fiabilité des systèmes modélisés par arbres de défaillances grâce aux techniques de satisfiabilité

Les fichiers de ce répertoire permettent d'analyser des systèmes cohérents, non réparables et dont le comportement est 
binaire (marche ou panne), avec pour hypothèse que les défaillances des composants ne peuvent pas se produire simultanément.

L'objectif est de générer les liens minimaux (TS) dans le cas d'un système modélisé par un arbre de défaillance statique, 
ou les séquences de liens minimales (MTSS) dans le cas d'un système modélisé par un arbre de défaillance dynamique.

###

1. Analyse de la fonction de structure à partir d'un arbre de défaillances statique

Les fichiers suivants permettent de générer les liens minimaux d'un système statique.
   - maketiesDNF.py
   - maketiesCNF.py
   - maketiesFromCuts.py

Les fichiers suivants ont été développés par Romain Masson lors de son stage de master.
   - lexer_cp.py
   - parser_smt2.py
   - varsupprSMT_Z3.py
   - peekablestream.py
   - LexAndPars.py
   - mincutsSMT_Z3.py

Les fichiers suivants contiennent la fonction de structure d'arbres de défaillances statiques et ont été converti 
en fichiers smt2 par les fichiers de Romain Masson.
   - test.cp
   - chinese.cp
   - baobab2.cp

2. Analyse de la fonction de structure à partir d'un arbre de défaillances dynamique

Les fichiers suivants permettent de générer les séquences de lien d'un système dynamique, puis de déterminer les 
séquences de lien minimales. 
   - makecutsSMT_Z3.py
   - mincutsSMT_Z3.py
