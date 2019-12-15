#/usr/bin/python3


# solve game from winning ways for your mathematical plays

#Win is a dict with the repr of the position as the index and the winning move as the value
win={}

# lose is a set of losing positions with the repr of the position as the index (set member)
lose=set()

# kill is the number of pieces that can be taken from the selected heap
kill=[1,2]

# Debug flag for showing internal process
dbg = False


# heap array is a list of the number of heaps of different sizes
# big-endian
# i.e. [2,0,1] is 2 heaps of 3 and 1 heap of one
#   legal moves: (heap,killsize,subheap size)
#   (1,1,0) -> [2,0,0]
#   (3,1,1) -> [1,0,2]
#   (3,2,0) -> [1] (actually [0,0,1] but we take off leading zeroes)

def SingleHeapArray(size):
    # Single heap, rest are empty
    return [1] + [0]*(size-1)
    
def StartWithNonempty(heapArray):
    while heapArray:
        if heapArray[0] != 0 :
            return
        del(heapArray[0])

def TestHeapAray(heapArray):
    StartWithNonempty(heapArray)
    rp=repr(heapArray)
    if dbg:
        print("Eval "+rp)

    # Position already known?
    if rp in win:
        if dbg:
            print("Fast win "+rp)
        return "W"
    if rp in lose:
        if dbg:
            print("Fast lose "+rp)
        return "L"

    # Try all legal moves
    heaparrayLength = len(heapArray)
    for i,h in enumerate(heapArray): # loop through heaps
        
        if h==0:
            # no heaps of this size
            continue
            
        heapSize = heaparrayLength-i
        for k in kill: 
            #loop through kill sizes
            
            if k > heapSize:
                # heap size too small for this kill size
                continue
                
            for subheap1 in range(heapSize-k+1): 
                #loop through splits
                subheap2=heapSize-k-subheap1
                
                if subheap2 > subheap1: 
                    #redundant by symmetry
                    continue
                    
                # apply the move to a copy of heapArray
                modHeapArray = heapArray.copy()
                modHeapArray[i] -= 1
                if subheap1 > 0:
                    modHeapArray[heaparrayLength-subheap1] += 1
                if subheap2 > 0:
                    modHeapArray[heaparrayLength-subheap2] += 1

                # Test the modified position
                if TestHeapAray(modHeapArray) == "L":
                    # made other guy a loser
                    win[rp] = (heapSize,k,subheap1)
                    if dbg:
                        print("Slow win "+rp)
                    return "W"
    # no good moves -- I'm a loser
    lose.add(rp)
    if dbg:
        print("Slow lose "+rp)
    return "L"

def HeapArrayMove( ha, mov ):
    ham = ha.copy()
    hal = len(ha)
    h1 = mov[2]
    h2 = mov[0] - mov[1] - h1
    ham[hal-mov[0]] -= 1
    if h1 > 0 :
        ham[hal-h1] += 1
    if h2 > 0 :
        ham[hal-h2] += 1
    return ham

def List2HeapArray( lisst ):
    ha = []
    for l in lisst:
        while len(ha) < l:
            ha.insert(0,0)
        ha[len(ha)-l] += 1
    return ha

def HAstring2HeapArray(ha_string):
    if ha_string=='[]':
        return []
    return list(map(int,ha_string[1:-1].split(",")))

def HeapArray2List(ha):
    l=[]
    for i,h in enumerate(ha):
        if h == 0:
            continue
        elif h == 1:
            l.append(len(ha)-i)
        else:
            l.append(str(len(ha)-i)+'*'+str(h))
    return l
    

def CommandLine():
    cl = argparse.ArgumentParser(description="Solve Kayles game from Winning Ways for Your Mathematical Plays\n{c} Paul H Alfille 2019")
    cl.add_argument("S",help="Size[s] of initial large heap",type=int,nargs="*",default=[25])
    cl.add_argument("-L","--lose",help="Show losing positions found",action="store_true")
    cl.add_argument("-W","--win",help="Show winning positions with correct move triplet (heapsize,killsize,biggest split_heapsize)",action="store_true")
    cl.add_argument("-D","--debug",help="Debug -- show progress through analysis",action="store_true")
    cl.add_argument("-R","--reverse",help="Reverse rule -- no moves is a WIN",action="store_true")
    cl.add_argument("-H","--heaps",help="Initial Heap Distribution",nargs="*",default=[])
    
    return cl.parse_args()

def ShowWins():
    print("Winning positions:")
    for w in sorted(list(win)):
        ha = HAstring2HeapArray(w)
        print("{}\t->\t{}\t->\t{}".format(HeapArray2List(ha),win[w],HeapArray2List(HeapArrayMove(ha,win[w]))))

def ShowLosses():
    print("Losing positions:")
    for l in sorted(list(lose)):
        print(HeapArray2List(HAstring2HeapArray(l)))

def main(args):

    args = CommandLine()
    dbg = args.debug
    
    # salt the problem
    if args.reverse:
        win[repr([])]="Finished"
    else:
        lose.add(repr([]))
        
    if args.heaps:
        print(args.heaps)
        heaps = []
        for h in args.heaps:
            heaps.append(int(h))
        value = TestHeapAray(List2HeapArray(heaps))

        if args.lose:
            ShowLosses()
        
        if args.win:
            ShowWins()

        print("Kayles with initial heap of {} is a {}".format(heaps,value))
        return
        
    for S in args.S:
        if S < 1:
            print("Starting heap size must be a positive number, of course")
            return
            
        value = TestHeapAray(SingleHeapArray(S))

        if args.lose:
            ShowLosses()
        
        if args.win:
            ShowWins()

        print("Kayles with initial heap size of {} is a {}".format(S,value))
        return


if __name__ == "__main__":
    import sys
    import argparse
    import re
    # execute only if run as a script
    sys.exit(main(sys.argv))
