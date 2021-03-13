import random

class Maze:

    def gen(self, f):
        for line in f:
            for i in range(len(line)):
                line[i] = "wall"

        fs, ws = self.arr(f)
        cell = random.choice(fs)
        while not(len(f) - 5 > cell[0] > 4 and len(f[0]) - 5 > cell[1] > 4):
            cell = random.choice(fs)
        f[cell[0]][cell[1]] = "visited"

        while self.unvisited_cells(f) > 0:
            if len(f)-2 > cell[0] > 1 and len(f[0])-2 > cell[1] > 1:
                neighbor, side = self.choose_neighbor(cell, ["u","d","l","r"])
                if f[neighbor[0]][neighbor[1]] == "empty":
                    if side == "r": ws, f = self.remove_wall(cell[0], cell[1] + 1, ws, f)
                    if side == "l": ws, f = self.remove_wall(cell[0], cell[1] - 1, ws, f)
                    if side == "u": ws, f = self.remove_wall(cell[0] - 1, cell[1], ws, f)
                    if side == "d": ws, f = self.remove_wall(cell[0] + 1, cell[1], ws, f)
                    f[neighbor[0]][neighbor[1]] = "visited"
                    cell = neighbor
                else:
                    cell = random.choice(fs)
                    while f[cell[0]][cell[1]] != "visited":
                        cell = random.choice(fs)
            else:   
                sides = ["u","d","l","r"]
                if not cell[0] > 1: sides.remove("u")
                if not cell[0] < len(f)-2: sides.remove("d")
                if not cell[1] > 1: sides.remove("l")
                if not cell[1] < len(f[0])-2: sides.remove("r")

                neighbor, side = self.choose_neighbor(cell, sides)
                if f[neighbor[0]][neighbor[1]] == "empty":
                    if side == "r": ws, f = self.remove_wall(cell[0], cell[1] + 1, ws, f)
                    if side == "l": ws, f = self.remove_wall(cell[0], cell[1] - 1, ws, f)
                    if side == "u": ws, f = self.remove_wall(cell[0] - 1, cell[1], ws, f)
                    if side == "d": ws, f = self.remove_wall(cell[0] + 1, cell[1], ws, f)
                    f[neighbor[0]][neighbor[1]] = "visited"
                    cell = neighbor
                else:
                    cell = random.choice(fs)
                    while f[cell[0]][cell[1]] != "visited":
                        cell = random.choice(fs)

        for i in range(len(f)):
            for k in range(len(f[0])):
                if f[i][k] == "visited":
                    f[i][k] = 0
                if f[i][k] == "wall":
                    f[i][k] = 1

        return f

    def arr(self, f):
        fs, ws = [], []
        for i in range(1, len(f) - 1, 2):
            for k in range(1, len(f[0]) - 1, 2):
                f[i][k] = "empty"
                fs.append([i,k])
        for i in range(2, len(f) - 1, 2):
            for k in range(1, len(f[0]) - 1, 2):
                ws.append([i,k])
        for i in range(1, len(f) - 1, 2):
            for k in range(2, len(f[0]) - 1, 2):
                ws.append([i,k])
        return fs, ws

    def unvisited_cells(self, f):
        unvisited_cells = 0
        for i in range(1, len(f) - 1, 2):
            for k in range(1, len(f[0]) - 1, 2):
                if f[i][k] != "visited":
                    unvisited_cells += 1
        return unvisited_cells

    def choose_neighbor(self, cell, sides):
        side = random.choice(sides) 
        if side == "l": return [cell[0], cell[1] - 2], side
        if side == "r": return [cell[0], cell[1] + 2], side
        if side == "u": return [cell[0] - 2, cell[1]], side
        if side == "d": return [cell[0] + 2, cell[1]], side

    def remove_wall(self, a, b, ws, f):
        for i in range(len(ws)):
            if ws[i] == [a,b]:
                f[ws[i][0]][ws[i][1]] = "visited"
                del ws[i]
                return ws, f

    
            
