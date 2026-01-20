"""
This file corresponds to the first graded lab of 2XC3.
Feel free to modify and/or add functions to this file.
"""
import random
import matplotlib.pyplot as plt
import timeit
import copy
import math

# Create a random list length "length" containing whole numbers between 0 and max_value inclusive
def create_random_list(length, max_value):
    return [random.randint(0, max_value) for _ in range(length)]


# Creates a near sorted list by creating a random list, sorting it, then doing a random number of swaps
def create_near_sorted_list(length, max_value, swaps):
    L = create_random_list(length, max_value)
    L.sort()
    for _ in range(swaps):
        r1 = random.randint(0, length - 1)
        r2 = random.randint(0, length - 1)
        swap(L, r1, r2)
    return L


# I have created this function to make the sorting algorithm code read easier
def swap(L, i, j):
    L[i], L[j] = L[j], L[i]


# ******************* Insertion sort code *******************

# This is the traditional implementation of Insertion Sort.
def insertion_sort(L):
    for i in range(1, len(L)):
        insert(L, i)


def insert(L, i):
    while i > 0:
        if L[i] < L[i-1]:
            swap(L, i-1, i)
            i -= 1
        else:
            return


# This is the optimization/improvement we saw in lecture
def insertion_sort2(L):
    for i in range(1, len(L)):
        insert2(L, i)


def insert2(L, i):
    value = L[i]
    while i > 0:
        if L[i - 1] > value:
            L[i] = L[i - 1]
            i -= 1
        else:
            L[i] = value
            return
    L[0] = value


# ******************* Bubble sort code *******************

# Traditional Bubble sort
def bubble_sort(L):
    for i in range(len(L)):
        for j in range(len(L) - 1):
            if L[j] > L[j+1]:
                swap(L, j, j+1)


# Updated Bubble Sort (Our code)
def bubble_sort2(L):
    for i in range(len(L)):
        swapped = False
        for j in range(len(L) - 1 - i):
            if L[j] > L[j+1]:
                swap(L, j, j+1)
                swapped = True
        if not swapped:
            break

# ******************* Selection sort code *******************

# Traditional Selection sort
def selection_sort(L):
    for i in range(len(L)):
        min_index = find_min_index(L, i)
        swap(L, i, min_index) #Swap L[i] and L[min_index]


def find_min_index(L, n):
    min_index = n
    for i in range(n+1, len(L)): #Check everything to right of position n
        if L[i] < L[min_index]:
            min_index = i
    return min_index

# Updated Selection Sort (Our code)

# Input: 
#  L - Array
#  j - Current index
#  k - Largest index filled (So check up to k-1)
def find_min_and_max_index(L,j,k):
    min_ind = j
    max_ind = j

    for i in range(j + 1, k): 
        if L[i] < L[min_ind]: 
            min_ind = i

        elif L[max_ind] < L[i]: 
            max_ind = i

    return (min_ind,max_ind)

# Improved Selection sort

# Find max element and min element and put in their respective positions 
# Keep track of the max and min index (Already put element there)
#   - Put max element at N-1, then the current possible max index is N-2
#   - Put min element at 0, then the current possible min index is 1
def selection_sort2(L): 
    if len(L) == 0: 
        return -1
    
    largest_filled = len(L) 
    i = 0

    # current index is less than the place where max element is
    while i < largest_filled - 1:

        min_index, max_index = find_min_and_max_index(L,i,largest_filled)

        swap(L,max_index,largest_filled - 1)

        # Min element was at end of available entries, so max element was swapped there
        # Thus the min element is now at the place where the max element was
        if min_index == largest_filled - 1: 
            min_index = max_index

        swap(L,i,min_index)

        largest_filled -= 1
        i += 1



# ******************* Experiment Code (Our Code) ********************


def experiment1():
    lengths = [100 * x for x in range(30)]
    max_value = 2 ** 30
    randomLists = [create_random_list(x,max_value) for x in lengths]
    n = len(lengths)
    bubbleData = []
    selectionData = []
    insertionData = []
    bubbleTotal = 0
    selectionTotal = 0
    insertionTotal = 0

    for i in range(n):
        L = randomLists[i]
        L1 = copy.deepcopy(L)
        L2 = copy.deepcopy(L)

        start = timeit.default_timer()
        bubble_sort(L)
        end = timeit.default_timer() - start
        bubbleTotal += end
        bubbleData.append(end)

        start = timeit.default_timer()
        selection_sort(L1)
        end = timeit.default_timer() - start
        selectionTotal += end
        selectionData.append(end)

        start = timeit.default_timer()
        insertion_sort(L2)
        end = timeit.default_timer() - start
        insertionTotal += end
        insertionData.append(end)




    plt.plot(lengths, bubbleData, color='blue', label = "Bubble sort")
    plt.plot(lengths, insertionData, color='red', label = "Insertion sort")
    plt.plot(lengths, selectionData, color='green', label = "Selection sort")

    plt.xlabel("List Length")
    plt.ylabel("Time (s)")
    plt.title("Runtime analysis")
    plt.legend()
    plt.show()

    return



def experiment2():
    lengths = [100 * x for x in range(30)]
    max_value = 2 ** 30
    randomLists = [create_random_list(x,max_value) for x in lengths]
    n = len(lengths)
    selectionData = []
    selectionImprovedData = []
    selectionTotal = 0
    selectionImprovedTotal = 0

    for i in range(n):
        L = randomLists[i]
        L1 = copy.deepcopy(L)
        L2 = copy.deepcopy(L)

        start = timeit.default_timer()
        selection_sort(L1)
        end = timeit.default_timer() - start
        selectionTotal += end
        selectionData.append(end)

        start = timeit.default_timer()
        selection_sort2(L2)
        end = timeit.default_timer() - start
        selectionImprovedTotal += end
        selectionImprovedData.append(end)




    plt.plot(lengths, selectionData, color='blue', label = "Selection sort " + str(round(selectionTotal/n,4)))
    plt.plot(lengths, selectionImprovedData, color='red', label = "Improved Selection sort " + str(round(selectionImprovedTotal/n,4)) )

    plt.xlabel("List Length")
    plt.ylabel("Time (s)")
    plt.title("Runtime analysis")
    plt.legend()
    plt.show()


    tradBubbleData = []
    updBubbleData = []
    tradBubbleTotal = 0
    updBubbleTotal = 0

    for i in range(n):
        L = randomLists[i]
        L1 = copy.deepcopy(L)
        L2 = copy.deepcopy(L)

        start = timeit.default_timer()
        bubble_sort(L1)
        end = timeit.default_timer() - start
        tradBubbleTotal += end
        tradBubbleData.append(end)

        start = timeit.default_timer()
        bubble_sort2(L2)
        end = timeit.default_timer() - start
        updBubbleTotal += end
        updBubbleData.append(end)

    plt.plot(lengths, tradBubbleData, color='blue', label='Traditional Bubble Sort Avg time = ' + str(round((tradBubbleTotal/n),4)))
    plt.plot(lengths, updBubbleData, color='red', label='Updated Bubble Sort Avg time = ' + str(round((updBubbleTotal/n),4)))
    plt.xlabel("List Length")
    plt.ylabel("Time in seconds")
    plt.legend()
    plt.show()

    return


def experiment3():
    length = 1250
    max_value = 2 ** 10
    max_swaps = 500   # int(length*math.log(length) / 2)
    nearSortedLists = [create_near_sorted_list(length,max_value,x) for x in range(max_swaps)]
    n = max_swaps
    bubbleData = []
    selectionData = []
    insertionData = []
    bubbleTotal = 0
    selectionTotal = 0
    insertionTotal = 0

    for i in range(n):
        L = nearSortedLists[i]
        L1 = copy.deepcopy(L)
        L2 = copy.deepcopy(L)

        start = timeit.default_timer()
        bubble_sort2(L)
        end = timeit.default_timer() - start
        bubbleTotal += end
        bubbleData.append(end)

        start = timeit.default_timer()
        selection_sort2(L1)
        end = timeit.default_timer() - start
        selectionTotal += end
        selectionData.append(end)

        start = timeit.default_timer()
        insertion_sort2(L2)
        end = timeit.default_timer() - start
        insertionTotal += end
        insertionData.append(end)




    plt.plot(range(max_swaps), bubbleData, color='blue', label = "Updated Bubble sort Avg time = " + str(round(bubbleTotal/n, 4)))
    plt.plot(range(max_swaps), insertionData, color='red', label = "Updated Insertion sort Avg time = " + str(round(insertionTotal/n, 4)))
    plt.plot(range(max_swaps), selectionData, color='green', label = "Updated Selection sort Avg time = " + str(round(selectionTotal/n, 4)))

    plt.xlabel("Swaps")
    plt.ylabel("Time (s)")
    plt.title("Runtime analysis")
    plt.legend()
    plt.show()

    return


#Running the experiments
experiment3()