from queue import PriorityQueue
import copy
import math


class Puzzle8:
    def __init__(self, initial_state):
        self.n = len(initial_state)
        self.state = initial_state
        self.goal_state = [[i + j * self.n + 1 for i in range(self.n)] for j in range(self.n)]
        self.goal_state[-1][-1] = 0

    @staticmethod
    def find_number(state, number):
        for i, row in enumerate(state):
            if number in row:
                for j, item in enumerate(row):
                    if item == number:
                        return i, j

    @staticmethod
    def check_on_resolvability(state):
        n = len(state)
        items = [state[i][j] for i in range(n) for j in range(n)]
        inversions = 0
        for i, itemi in enumerate(items):
            for j, itemj in enumerate(items[i + 1:]):
                if itemi != 0 and itemj != 0:
                    if itemi > itemj:
                        inversions += 1
        row = Puzzle8.find_number(state, 0)[0]
        return not (n % 2 == 1 and inversions % 2 == 1) or (n % 2 == 0 and (inversions + row) % 2 == 0)

    @staticmethod
    def move(old_state, destination):
        new_state = copy.deepcopy(old_state)
        row, column = Puzzle8.find_number(new_state, 0)
        if destination == 'U':
            new_state[row][column], new_state[row - 1][column] = new_state[row - 1][column], new_state[row][column]
        elif destination == 'D':
            new_state[row][column], new_state[row + 1][column] = new_state[row + 1][column], new_state[row][column]
        elif destination == 'R':
            new_state[row][column], new_state[row][column + 1] = new_state[row][column + 1], new_state[row][column]
        elif destination == 'L':
            new_state[row][column], new_state[row][column - 1] = new_state[row][column - 1], new_state[row][column]
        return new_state

    @staticmethod
    def neighbors(state):
        row, column = Puzzle8.find_number(state, 0)
        n = len(state)
        res = [(row - 1, column, 'U'), (row + 1, column, 'D'), (row, column - 1, 'L'), (row, column + 1, 'R')]
        result = []
        for row, column, letter in res:
            if 0 <= row < n and 0 <= column < n:
                result.append((row, column, letter))
        return result

    @staticmethod
    def manhattan(state, goal_state):
        result = 0
        for i, row in enumerate(goal_state):
            for j, item in enumerate(row):
                if item != 0:
                    if item != state[i][j]:
                        r, c = Puzzle8.find_number(state, item)
                        result += abs(r - i) + abs(c - j)
        return result


def a_star_search(state, goal_state):
    q = PriorityQueue()
    n = len(state)
    came_from = dict()
    cost_so_far = dict()
    s = (''.join(str(state[i][j]) for i in range(n) for j in range(n)))
    came_from[s] = None
    cost_so_far[s] = 0
    turn = 0
    cur_state = state
    while cur_state != goal_state:
        for neighbor in Puzzle8.neighbors(cur_state):
            row, column, dest = neighbor
            next_state = Puzzle8.move(cur_state, dest)
            s = (''.join(str(next_state[i][j]) for i in range(n) for j in range(n)))
            new_cost = Puzzle8.manhattan(next_state, goal_state) + turn
            if s not in cost_so_far or new_cost < cost_so_far[s]:
                came_from[s] = cur_state
                cost_so_far[s] = new_cost
                q.put((new_cost, next_state))
        tmp, cur_state = q.get()
        turn += 1
    return came_from


def show_way(path: dict, goal_state):
    def find_number(s: str, number):
        row = int(s.find(number) / n)
        column = int(s.find(number) % n)
        return row, column

    res = []
    n = int(math.sqrt(len(goal_state)))
    row1, column1 = find_number(goal_state, '0')
    state = goal_state
    while True:
        if path[state] is not None:
            state = (''.join(str(path[state][i][j]) for i in range(n) for j in range(n)))
            row2, column2 = find_number(state, '0')
            if row1 != row2:
                if row2 < row1:
                    res.append('D')
                else:
                    res.append('U')
            else:
                if column2 < column1:
                    res.append('R')
                else:
                    res.append('L')
            row1, column1 = row2, column2
        else:
            break
    res.reverse()
    return res


def solve_puzzle(p):
    size = len(p)
    goal = [[i + j * size + 1 for i in range(size)] for j in range(size)]
    goal[-1][-1] = 0
    if Puzzle8.check_on_resolvability(p):
        m = a_star_search(p, goal)
        goal = (''.join(str(goal[i][j]) for i in range(size) for j in range(size)))
        ress = (show_way(m, goal))
        return ress
    else:
        return 'this puzzle can not be solved'


very_initial_state = [[1, 2, 3],
                      [0, 4, 5],
                      [7, 8, 6]]
print(solve_puzzle(very_initial_state))
