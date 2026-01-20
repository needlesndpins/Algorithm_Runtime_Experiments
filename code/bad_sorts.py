"""
This file corresponds to the first graded lab of 2XC3.
Feel free to modify and/or add functions to this file.
"""
import random
import matplotlib.pyplot as plt
import timeit
import copy

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
        swap(L, i, min_index)


def find_min_index(L, n):
    min_index = n
    for i in range(n+1, len(L)):
        if L[i] < L[min_index]:
            min_index = i
    return min_index

# Updated Selection Sort (Our code)


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

        start = timeit.default_timer()
        bubble_sort(L)
        end = timeit.default_timer() - start
        bubbleTotal += end
        bubbleData.append(end)

        start = timeit.default_timer()
        insertion_sort(L)
        end = timeit.default_timer() - start
        insertionTotal += end
        insertionData.append(end)

        start = timeit.default_timer()
        selection_sort(L)
        end = timeit.default_timer() - start
        selectionTotal += end
        selectionData.append(end)




    plt.plot(lengths, bubbleData, color='blue')
    plt.title('Bubble sort')
    plt.xlabel("List Length")
    plt.ylabel("Time in seconds")
    plt.show()

    plt.plot(lengths, insertionData, color='red')
    plt.title('Insertion sort')
    plt.xlabel("List Length")
    plt.ylabel("Time in seconds")
    plt.show()

    plt.plot(lengths, selectionData, color='green')
    plt.title('Selection sort')
    plt.xlabel("List Length")
    plt.ylabel("Time in seconds")
    plt.show()

    return


def experiment2():
    lengths = [100 * x for x in range(30)]
    max_value = 2 ** 30
    randomLists = [create_random_list(x,max_value) for x in lengths]
    n = len(lengths)

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

    plt.plot(lengths, tradBubbleData, color='blue', label='Traditional Bubble Sort Avg time = ' + str(tradBubbleTotal/n))
    plt.plot(lengths, updBubbleData, color='red', label='Updated Bubble Sort Avg time = ' + str(updBubbleTotal/n))
    plt.xlabel("List Length")
    plt.ylabel("Time in seconds")
    plt.legend()
    plt.show()

    return


#Running the experiments
experiment2()