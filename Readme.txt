8 puzzle is a sliding puzzle that consists of a frame of randomly ordered, numbered square tiles with one missing tile. The object of the puzzle is to place the tiles in the right order by using sliding moves to utilize the empty space.
The program solves such puzzle using A* algorithm. Moreover, it can be 3X3, 4X4 and so forth.
To use this program you should call 'solve_puzzle(initial_state)' function. initial_state should look like: 
                                [[1, 2, 3],
                                 [4, 6, 8],
                                 [7, 5, 0]]
The function returns set of letters that show you how to "move" the missing tile. ('U' means up, 'R' means right and so forth)
