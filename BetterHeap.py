'''
BetterHeap v1.0

I made this to try to remedy several problems with the default python library heapq.
for example heapq doesnt allow you to have a queue of tuples, lists, custom data types, or really anything other than numbers.
ALSO HEAPQ CANT MAKE MAXHEAPS!!! (or at least if it can, I havent figured out how)
my implementation is unfinished, but currently it allows you to supply a key function to tell the heap how to interpret other data types.

-PaiShoFish49
'''
def _parent(index: int) -> int:
    return (index - 1) // 2

def _parentItem(heap: list, index: int):
    return heap[_parent(index)]

def _children(index: int) -> list[int, int]:
    return [index*2 + 1, index*2 + 2]

def _childrenItems(heap: list, index: int) -> list:
    childItems = []
    for i in _children(index):
        if i < len(heap):
            childItems.append(heap[i])

def _swap(heap: list, index1: int, index2: int):
    temp = heap[index1]
    heap[index1] = heap[index2]
    heap[index2] = temp

def _bubbleUp(heap: list, index: int, maxHeap: bool = False, key: function = lambda x: x):
    sign = -1 if maxHeap else 1

    while (index != 0) and (sign * key(heap[index]) < sign * key(_parentItem(heap, index))):
        _swap(heap, index, _parent(index))
        index = _parent(index)

def _bubbleDown(heap: list, index: int, maxHeap: bool = False, key: function = lambda x: x):
    sign = -1 if maxHeap else 1

    while _children(index)[0] < len(heap):
        children = _childrenItems(heap, index)
        if len(children) == 1:
            if sign * key(heap[index]) > sign * key(children[0]):
                _swap(heap, index, _children(index)[0])
                index = _children(index)[0]

            else:
                break

        elif len(children) == 2:
            if sign * key(children[0]) < sign * key(children[1]):
                switchInd = _children(index)[0]
            else:
                switchInd = _children(index)[1]

            if sign * key(heap[index]) > sign * key(heap[switchInd]):
                _swap(heap, index, switchInd)
                index = switchInd

            else:
                break

def heapify(inputList: list, maxHeap: bool = False, key: function = lambda x: x):
    for i in range(len(inputList)):
        _bubbleDown(inputList, len(inputList) - i - 1, maxHeap, key)

def heapified(inputList: list, maxHeap: bool = False, key: function = lambda x: x):
    copyList = inputList.copy()
    heapify(copyList, maxHeap, key)
    return copyList

def append(heap: list, item, maxHeap: bool = False, key: function = lambda x: x):
    heap.append(item)
    _bubbleUp(heap, len(heap) - 1, maxHeap, key)

def pop(heap: list, index: int = None, maxHeap: bool = False, key: function = lambda x: x):
    sign = -1 if maxHeap else 1

    if index is None:
        _swap(heap, 0, len(heap) - 1)
        returnValue = heap.pop()
        _bubbleDown(heap, 0, maxHeap, key)

    else:
        _swap(heap, index, len(heap) - 1)
        returnValue = heap.pop()
        if sign * key(heap[index]) > sign * key(returnValue):
            _bubbleDown(heap, index, maxHeap, key)
        else:
            _bubbleUp(heap, index, maxHeap, key)

    return returnValue
