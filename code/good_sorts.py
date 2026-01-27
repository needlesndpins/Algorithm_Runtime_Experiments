"""
This file corresponds to the first graded lab of 2XC3.
Feel free to modify and/or add functions to this file.

In contains traditional implementations for:
1) Quick sort
2) Merge sort
3) Heap sort

Author: Vincent Maccio
"""
import random
import matplotlib.pyplot as plt
import timeit
import copy
import math
import sys
sys.setrecursionlimit(10000)

def create_random_list(length, max_value):
    return [random.randint(0, max_value) for _ in range(length)]

# I have created this function to make the sorting algorithm code read easier
def swap(L, i, j):
    L[i], L[j] = L[j], L[i]



# Creates a near sorted list by creating a random list, sorting it, then doing a random number of swaps
# Swaps = 0 -> List is sorted 
def create_near_sorted_list(length, max_value, swaps):
    L = create_random_list(length, max_value)
    L.sort()
    for _ in range(swaps):
        r1 = random.randint(0, length - 1)
        r2 = random.randint(0, length - 1)
        swap(L, r1, r2)
    return L



# ************ Quick Sort ************
def quicksort(L):
    copy = quicksort_copy(L)
    for i in range(len(L)):
        L[i] = copy[i]


def quicksort_copy(L):
    if len(L) < 2:
        return L
    pivot = L[0]
    left, right = [], []
    for num in L[1:]:
        if num < pivot:
            left.append(num)
        else:
            right.append(num)
    return quicksort_copy(left) + [pivot] + quicksort_copy(right)

# *************************************


# ************ Merge Sort *************

def mergesort(L):
    if len(L) <= 1:
        return
    mid = len(L) // 2
    left, right = L[:mid], L[mid:]

    mergesort(left)
    mergesort(right)
    temp = merge(left, right)

    for i in range(len(temp)):
        L[i] = temp[i]


def merge(left, right):
    L = []
    i = j = 0

    while i < len(left) or j < len(right):
        if i >= len(left):
            L.append(right[j])
            j += 1
        elif j >= len(right):
            L.append(left[i])
            i += 1
        else:
            if left[i] <= right[j]:
                L.append(left[i])
                i += 1
            else:
                L.append(right[j])
                j += 1
    return L

# *************************************

# ************* Heap Sort *************

def heapsort(L):
    heap = Heap(L)
    for _ in range(len(L)):
        heap.extract_max()

class Heap:
    length = 0
    data = []

    def __init__(self, L):
        self.data = L
        self.length = len(L)
        self.build_heap()

    def build_heap(self):
        for i in range(self.length // 2 - 1, -1, -1):
            self.heapify(i)

    def heapify(self, i):
        largest_known = i
        if self.left(i) < self.length and self.data[self.left(i)] > self.data[i]:
            largest_known = self.left(i)
        if self.right(i) < self.length and self.data[self.right(i)] > self.data[largest_known]:
            largest_known = self.right(i)
        if largest_known != i:
            self.data[i], self.data[largest_known] = self.data[largest_known], self.data[i]
            self.heapify(largest_known)

    def insert(self, value):
        if len(self.data) == self.length:
            self.data.append(value)
        else:
            self.data[self.length] = value
        self.length += 1
        self.bubble_up(self.length - 1)

    def insert_values(self, L):
        for num in L:
            self.insert(num)

    def bubble_up(self, i):
        while i > 0 and self.data[i] > self.data[self.parent(i)]:
            self.data[i], self.data[self.parent(i)] = self.data[self.parent(i)], self.data[i]
            i = self.parent(i)

    def extract_max(self):
        self.data[0], self.data[self.length - 1] = self.data[self.length - 1], self.data[0]
        max_value = self.data[self.length - 1]
        self.length -= 1
        self.heapify(0)
        return max_value

    def left(self, i):
        return 2 * (i + 1) - 1

    def right(self, i):
        return 2 * (i + 1)

    def parent(self, i):
        return (i + 1) // 2 - 1

    def __str__(self):
        height = math.ceil(math.log(self.length + 1, 2))
        whitespace = 2 ** height
        s = ""
        for i in range(height):
            for j in range(2 ** i - 1, min(2 ** (i + 1) - 1, self.length)):
                s += " " * whitespace
                s += str(self.data[j]) + " "
            s += "\n"
            whitespace = whitespace // 2
        return s

# *************************************
    
def experiment4():
    lengths = [2 ** x for x in range(20)]
    max_value = 2 ** 30
    randomLists = [create_random_list(x,max_value) for x in lengths]
    n = len(lengths)
    heapData = []
    mergeData = []
    quickData = []
    heapTotal = 0
    mergeTotal = 0
    quickTotal = 0

    for i in range(n):
        L = randomLists[i]
        L1 = copy.deepcopy(L)
        L2 = copy.deepcopy(L)

        start = timeit.default_timer()
        heapsort(L)
        end = timeit.default_timer() - start
        heapTotal += end
        heapData.append(end)

        start = timeit.default_timer()
        mergesort(L1)
        end = timeit.default_timer() - start
        mergeTotal += end
        mergeData.append(end)

        start = timeit.default_timer()
        quicksort(L2)
        end = timeit.default_timer() - start
        quickTotal += end
        quickData.append(end)




    plt.plot(lengths, heapData, color='blue', label = "Heap sort")
    plt.plot(lengths, mergeData, color='red', label = "Merge sort")
    plt.plot(lengths, quickData, color='green', label = "Quick sort")

    plt.xlabel("List Length")
    plt.ylabel("Time (s)")
    plt.title("Runtime analysis")
    plt.legend()
    plt.show()

    return




# Quicksort is O(n^2) for sorted and reverse sorted lists 
# It will be beat by mergesort and heapsort 
# How "non-sorted" does the array have to be until Quicksort starts to win again? 
#  * Start at sorted array, and gradually become less sorted until you have a completely random array
#  * Plot this 
def experiment5():

    length = 5000
    max_value = 2 ** 30
    # max_swaps = int(length*math.log(length) / 2)
    max_swaps = 400
    num_swaps = []
    nearSortedLists = []
    for x in range(0,max_swaps,16): 
        nearSortedLists.append(create_near_sorted_list(length,max_value,x))
        num_swaps.append(x)

    print(len(nearSortedLists))


    #n = max_swaps
    n = len(nearSortedLists)
    heapData = []
    mergeData = []
    quickData = []
    heapTotal = 0
    mergeTotal = 0
    quickTotal = 0

    for i in range(n):
        print(i)
        L = nearSortedLists[i]
        L1 = copy.deepcopy(L)
        L2 = copy.deepcopy(L)

        start = timeit.default_timer()
        heapsort(L)
        end = timeit.default_timer() - start
        heapTotal += end
        heapData.append(end)

        start = timeit.default_timer()
        mergesort(L1)
        end = timeit.default_timer() - start
        mergeTotal += end
        mergeData.append(end)

        start = timeit.default_timer()
        quicksort(L2)
        end = timeit.default_timer() - start
        quickTotal += end
        quickData.append(end)





    # Need to accurately capture number of swaps per iteration, this doesn't do that
    plt.plot(num_swaps, heapData, color='blue', label = "Heapsort Avg time = " + str(round(heapTotal/n, 4)))
    plt.plot(num_swaps, mergeData, color='red', label = "Mergesort Avg time = " + str(round(mergeTotal/n, 4)))
    plt.plot(num_swaps, quickData, color='green', label = "Quicksort Avg time = " + str(round(quickTotal/n, 4)))
    
    plt.xlabel("Swaps")
    plt.ylabel("Time (s)")
    plt.title("Runtime analysis")
    plt.legend()
    plt.show()

    return


experiment5()
# comment