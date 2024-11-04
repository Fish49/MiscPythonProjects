# MiscPythonProjects
I have a lot of cool python projects, most of them are just one or two files, so i dont want to make a new repo for each one.

## Current Included Projects:
- ### Renderer
  - simple raytracing engine
  - can only handle one bounce, has no anti-aliasing, only one light source, and many other limitations
  - can import ASCII stl files
  - more of a learning expirience than anything useful
- ### initbfarray
  - for initializing arrays in brainfuck
  - for each number, it uses the shortest brainfuck syntax to achieve that number from zero, sometimes using multiplication or underflow (ex. 255 is just "-")
- ### BetterHeap
  - to solve the many issues with pythons default heap: heapq
  - it is a hasstle to make max heaps in heapq, but in BetterHeap, its as simple as passing true as the maxHeap argument
  - you cant have custom data types in python heapqs, but BetterHeap provides a key that lets you define a custom function for organizing items
  - has heapToString function which gives you an intuitive string representation of your heap
- ### CountableRationals
  - provides functions to convert rationals to integers and vice versa
  - pattern goes as follows: there are multiple sections, each of which adds a new fraction (1/section number) and increments each previous fraction
  - ```
    ex. 0, 1, 2, 1/2, 3, 3/2, 1/3, 4, 5/2, 2/3 rationals
        0, 1, 2, 3,   4, 5,   6,   7, 8,   9 mappings
           \ 1 / \    2     / \      3       / sections
- ### Apollonius
  - program for solving the apollonius problems