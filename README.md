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