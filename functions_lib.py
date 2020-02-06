# Library: functions to support maketiesCNF.py, maketiesDNF.py, and maketiesCut.py
# Use Python 3

import sys, time
from pyeda.inter import *
#http://pyeda.readthedocs.io/en/latest/bdd.html#constructing-bdds
#file:///Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pyeda/parsing/boolexpr.py

# Function : rewrite {'e1', 'e3'} like  1 3 0.
def rewriteCuts ( M ) :
    i = 2
    while i < len( M ) :
        new=[]
        j=0
        model=M[i].split()
        new.append(model[j][3:-2])
        j=1
        if len(model) > 1 :
            while j < len(model) :
                new.append(model[j][2:-2])
                j=j+1
        new.append(0)
        i=i+1
        # Write a CNF file with the minimal cuts
        with open("MCSS.cnf", "a") as cnfFile :
            cnfFile.write(' '.join(map(str, new)))
            cnfFile.write('\n')
    return new

# Function clear_inp : to get a readable input file
def extract_var( modelLines, j ) :
    return modelLines[j][14:-9]

# Function clear_inp : to get a readable input file
def extract_val( modelLines , j ) :
    val = modelLines[j+1][4:-2] %14
    return val

# Function clear_inp : to get a readable input file
def clear_inp( inp ) :
    # Input : input file with structure function inside
    # Output : readable structure function
    with open (inp, "r") as inputFile:
        modelLines = inputFile.readlines()
    i=1
    f=[]
    while i < int(len(modelLines)) :
        model = modelLines[i].split()
        line = [int(z) for z in model]
        #print("line:", line)
        f.append(line)
        #print("f:", f)
        i = i+1
    return f

# Function : We want to get the number of components from the input file.
def get_nb_comp( st_function ) :
    # Input : structure function
    # Output : number of components in the system
    alpha=1   #by default we consider that there is one component.
    for element in st_function:
        for subelement in element:
            if subelement > alpha: #is this number bigger than the current maximum?
                alpha = subelement
    return alpha

# Function definition is here : transform [-1,3] into [0,0,1]
def transform( tmp, components_nb ) :
# Input : a set like [-1,3]
# Output : a set like [0,0,1] where 0 means the component is negative or absent
    # The function aims at converting a tie expressed like [-1,3] into another
    # form [0,0,1] which only contains {0,1} and which describes each
    # component.The list should contain as many elements as the system
    # contains components.
    x=[]
    j=1
    for i in range (components_nb) :
        x.append(0)
    for i in range (1, components_nb +1) :
        if ( j <= len(tmp) )  :
            if (tmp[j-1]== i) :
                x[i-1]=1
                j=j+1
            elif ( ( tmp[j-1]== -i ) | ( tmp[j-1]== 0 ) ) :
                j=j+1
    return x

# Function definition is here : transform [0,0,1] into [3]
def transform_back( tmp ) :
# Input : a set like [0,0,1]
# Output : a set like [-1,3]
    # The function aims at transforming back a tie into a form where only
    # the functionning components are expressed.
    x=[]
    for i in range (len(tmp)) :
        if tmp[i] == 1 : #if components here, then we add it to the result.
            x.append(i+1)
    #print("Tmp:", tmp, "Result of the back transformation :", x)
    return x

# Function definition is here : test_smaller
def test_smaller( x, y ) :
# Input : two sets x, y.
# Output : 1 if x is smaller than y ; 0 if x is bigger than y or if they are not comparable.
# The function aims at testing if a tie is or isn't smaller than another tie. 
#"This tells us if x is smaller than y."
    if len(x)==len(y):
        i=0
        while i < len(x) : # we go throught both tuples with i :
            if ((y[i]==-1) & (x[i]>-1) | (y[i]==0) & (x[i]==1)) :
                return 0
            else :
                i=i+1
    else :
        print ('error')
    return 1 # if none of the x elements were equal or bigger than y elements, then x is smaller than y

# Function : does a list contain an element which is a subset of a tie t?
def contains_smaller( ties, tie ) :
    # Input : a list of ties, and a tie to compare to it
    # Output : false if minimal, true otherwise
    for t in ties :
        if t.issubset(tie) :
            return True
    return False

# Function sons : to know each node directly smaller than the node x
def sons( x, components_nb ):
    # Input : a set
    # Output : the direct descendants (sons) of the set
    s=[]
    i=0
    for i in range(0, components_nb):
        if x[i]==1:
            y=[]
            for l in x:
                y.append(l)
            y[i]=0
            s.append(y)
    return s

# Functions descendants : to know each node bigger than the node x
def descendants( x, components_nb ):
    # Input : a set
    # Output : the descendants of the set
    S=[]
    R=[]
    for s in sons(x, components_nb):
        S.append(s)
        R.append(s)
    while S != []:
        for s in S:
            for g in sons(s, components_nb):
                if not g in R:
                    R.append(g)
                    S.append(g)
            S.remove(s)
    return R

# Function fathers : to know each node directly bigger than the node x
def fathers( x, components_nb ):
    # Input : a set
    # Output : the direct ancestors (fathers) of the set
    f=[]
    i=0
    for i in range(0, components_nb):
        if x[i]==0:
            y=[]
            for l in x:
                y.append(l)
            y[i]=1
            f.append(y)
    return f

# Functions ancestors : to know each node bigger than the node x
def ancestors( x, components_nb ):
# Input : a set
# Output : the ancestors of the set
    F=[]
    R=[]
    for f in fathers(x, components_nb):
        F.append(f)
        R.append(f)
    while F != []:
        for f in F:
            for g in fathers(f, components_nb):
                if not g in R:
                    R.append(g)
                    F.append(g)
            F.remove(f)
    return R

# Function : convert a cube (list) to a tie (set), dropping negative literals
def make_tie( cube ) :
# Input : 
# Output : 
    return set([l for l in cube if l > 0])

# Function definition is here : transform [-1,3] into [0,0,1]
def transform_and_keep_positive( tmp, components_nb ) :
# Input : a list like [-1,3]
# Output : a like like [0,0,1]
# The function aims at converting a tie expressed like [-1,3] into another form [0,0,1] which only contains {0,1} and which describes each component.
# The list should contain as many elements as the system contains components.
    x=[]
    j=1
    for i in range (0, components_nb) :
        x.append(0)
    for i in range (1, components_nb +1) :
        if ( j <= len(tmp) )  :
            if (tmp[j-1]== i) :
                x[i-1]=1
                j=j+1
            elif ( tmp[j-1]== 0 ) | ( tmp[j-1]== -i ) :
                x[i-1]=0
                j=j+1
    return x

# We want to get the contrary of a set : transform [0,0,1] into [1,1,0].
def get_contrary( set, number ) :
    # Input :  a set and the number of components of the system
    # Output : the opposite of the set, i.e. [0,0,1] for [1,1,0]
    newset = []
    for element in set :
        i = 0
        s = []
        while i < number :
            if element[i] == 1 :
                s.append(0)
            else :
                s.append(1)
            i = i+1
        newset.append(s)
    return newset

# Function : transform [-1,3] into [0,0,1]
def transform_neg_in_pos( tmp, components_nb ) :
# Input : 
# Output : 
    # The function aims at converting a tie expressed like [-1,3] into another form [0,0,1] which only contains {0,1} and which describes each component. The list should contain as many elements as the system contains components.
    x=[]
    j=1
    for i in range (0, components_nb) :
        x.append(0)
    for i in range (1, components_nb +1) :
        if ( j <= len(tmp) )  :
            if (tmp[j-1]== i) :
                x[i-1]=1
                j=j+1
            elif ( tmp[j-1]== 0 ) :
                #x[i-1]=0
                j=j+1
            elif ( tmp[j-1]== -i ) :
                x[i-1]=1
                j=j+1
    return x

# Function : reorder the elements of the tie sets.
def reorder( f, components_nb ) :
# Input : a set of sets [[1,4,3],[5,2]]
# Output : a set of reordered sets [[1,3,4],[2,5]]
    # We can use the function of Python3 -sorted-
    G=[]
    for tieset in f :
        #print ('f:', f)
        g=[]
        g=sorted(tieset)
        #print ('g:', g)
        G.append(g)
    return G

# Function parse : to get the structure function from the input file
def parse( inp, number ) :
# Input : 
# Output : 
    # We want to read the input file and to write the structure function f
    # from the input file.
    with open (inp, "r") as inputFile:
        modelLines = inputFile.readlines()
        l = int(len(modelLines))
    return modelLines

# Function parse : to get the structure function from the input file
def parseInput( inp, number ) :
# Input : 
# Output : 
    # We want to read the input file and to write the structure function f
    # from the input file.
    with open (inp, "r") as inputFile:
        modelLines = inputFile.readlines()
        l = int(len(modelLines))
    return (modelLines, l)
# We want to get the minimal cut sets from the structure function.
# Input : structure function
# Output : 
def parse_cut( function, number ) :
    set = []
    for element in function :
        i = 0
        cut = []
        while i < number :
            if element[i] == 1 :
                cut.append(0)
            else :
                cut.append(1)
            i = i+1
        set.append(cut)
    return set

# Function parse : to get the structure function from the input file
def parse_and_split( inp, number ) :
# Input : 
# Output : 
    # We want to get the structure function from the input file.
    with open (inp, "r") as modelFile :
        modelLines = modelFile.readlines()
    f=[]
    new=[]
    for m in modelLines :
        n=m.split()
        if not n[0] == 'p' :
            for i in n:
                if not i == '0' :
                    new.append(int(i))
            f.append( new )
            new=[]
    return f

def newtie_c ( model ):
    tie = set([int(l) for l in model if int(l) > 0])
    return tie

def newtie_nc ( model ):
    tie = set([int(l) for l in model if int(l) != 0])
    return tie

# Write a boolean expression from a set.
# Input : 
# Output : 
def write_expr_from_set( s ):
    l = len(s)
    #print("l:", l, "\n")
    expression = "(" + str(s[0])
    i=1
    while i < l:
        #print(s[i], type(s[i]))
        element = str(s[i])
        new = expression + "|" + element
        expression = new
        i=i+1
    new = expression + ")"
    expression = new
    boolexpr = expr(expression)
    return boolexpr

# Write a boolean expression from the boolean expressions of clauses. From many clauses to a CNF.
# Input : 
# Output : 
def expr_of_clauses( variables, s ):
    l = len(s)
    expression = "(" + str(s[0])
    i=1
    while i < l:
        element = str(s[i])
        new = expression + "&" + element
        expression = new
        i=i+1
    finishExpression = expression + ")"
    boolexpr = expr(finishExpression)
    return boolexpr

