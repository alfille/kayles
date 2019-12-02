#/usr/bin/python3


# solve game from winning ways for your mathematical plays

win=set()
lose=set()
kill=[1,2]

# heap array is a list of heaps of different sizes
# big-endian 

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
    # print("Eval "+rp)

    # Position already known?
    if rp in win:
        print("Fast win "+rp)
        return "W"
    if rp in lose:
        print("Fast lose "+rp)
        return "L"

    # Try all legal moves
    heaparrayLength = len(heapArray)
    for i in range(heaparrayLength): # loop through heaps
        
        if heapArray[i]==0:
            # no heaps of this size
            continue
            
        heap = heaparrayLength-i
        for k in kill: 
            #loop through kill sizes
            
            if k > heap:
                # heap size too small for this kill size
                continue
                
            for subheap1 in range(heap-k+1): 
                #loop through splits
                subheap2=heap-k-subheap1
                
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
                    win.add(rp)
                    print("Slow win "+rp)
                    return "W"
    # no good moves -- I'm a loser
    lose.add(rp)
    print("Slow lose "+rp)
    return "L"


def main():
    # salt the problem
    lose.add(repr([]))
    
    
    TestHeapAray(SingleHeapArray(25))
    print("win")
    print(sorted(list(win)))
    print("lose")
    print(sorted(list(lose)))
    
if __name__ == "__main__":
    # execute only if run as a script
    main()
