class Maze:
    def __init__(self, filename):
        self.file = open(filename, "r") #open the file
        self.file = self.file.readlines() #read the file
        self.grid = []

        for line in self.file:
            row = []
            for tile in line.rstrip():
                row.append(int(tile))
            self.grid.append(row)
        
        self.start = []
        self.finish = []

        for row in range(0, len(self.grid)):
            for column in range(0, len(self.grid[row])):
                if self.grid[row][column] == 2:
                    self.start.append(row)
                    self.start.append(column)
                elif self.grid[row][column] == 0 and ((row == 0 or row == len(self.grid)-1) or (column == 0 or column == len(self.grid[row])-1)):
                    self.finish.append(row)
                    self.finish.append(column)
        
        self.robot = Robot(self, self.start) 
        
    def get_finish(self):
        return self.finish
    
    def get_grid(self):
        return self.grid

    def get_neighbourhood(self, pos):
        neighbourhood = []
        x = pos[0]
        y = pos[1]

        for i in range(x-1, x+2):
            row = []
            for j in range(y-1, y+2):
                row.append(self.grid[i][j])
            neighbourhood.append(row)
        return neighbourhood

    
class Robot:
    def __init__(self, maze, starting):
        self.curr_pos = starting
        self.last_pos = self.curr_pos
        self.maze = maze
        self.last_dir = "up" #start with standard direction up
        self.turns_left = 0 #counts the number of times the robot moves left (or right)

    def change_pos(self, pos):
        self.last_pos = self.curr_pos
        self.curr_pos = pos

    def get_pos(self):
        return self.curr_pos
    
    def walk_options(self):
        neighbourhood2 = self.maze.get_neighbourhood(self.curr_pos)
        row = self.curr_pos[0]
        col = self.curr_pos[1]

        walk_options = {
                        "up": [row - 1, col],
                        "down": [row + 1, col],
                        "left": [row, col -1],
                        "right": [row, col + 1]
        }
        
        if neighbourhood2[0][1] == 1:
            del walk_options["up"]
        if neighbourhood2[2][1] == 1:
            del walk_options["down"]
        if neighbourhood2[1][0] == 1:
            del walk_options["left"]
        if neighbourhood2[1][2] == 1:
            del walk_options["right"]
        return walk_options

    def change_last_dir(self):
        curr_row = self.curr_pos[0]
        curr_col = self.curr_pos[1]
        last_row = self.last_pos[0]
        last_col = self.last_pos[1]

        if (curr_row - last_row) == -1:
            self.last_dir = "up"
        elif (curr_row - last_row) == 1:
            self.last_dir = "down"
        elif (curr_col - last_col) == -1:
            self.last_dir = "left"
        elif (curr_col - last_col) == 1:
            self.last_dir = "right"
    
    def is_finished(self):
        finish = self.maze.get_finish()
        if finish == self.curr_pos:
            return True
        else:
            return False

    def take_one_step(self):
        if self.is_finished() == True: #if one robot is already finished and the other not, return the finsihlocation of the robot
            return self.maze.get_finish()
        # the robot tries to go right first, up second, then left and as last option backwards
        # Because we don't want that the robot will walk in circles we count the number it turns left (or right), right gives a count of -1, up 0, left 1 and backward +2
        #order the directions in this way, because now right has index 0, up 1, left 2 and down 3
        #the directions are orderd in this way, because now is the index -1 the number you plus self.turns_left with
        direction = ["right", "up", "left", "down"]
        index = direction.index(self.last_dir)
        #take this range bacause of the fact that turning right gave you a
        for i in range(-1,3):
            if direction[(index + i)%4] in self.walk_options() and ((i%2 == 1 and self.turns_left != 4*i) or i%2 == 0): #we don't want running in circles so we keep looking to self.turns_left when the robot turns left or right,
                #we don't need to check it if the robot is going forward
                self.change_pos(self.walk_options()[direction[(index + i)%4]]) #update current position
                self.change_last_dir() #update last direction
                self.turns_left += i #update turns_left
                return self.curr_pos

def main():
    maze1 = Maze("maze1.txt")
    maze2 = Maze("maze2.txt")
    robot1 = maze1.robot
    robot2 = maze2.robot
    path1 = []
    path2 = []

    i = 0
    while i<100 and (robot1.is_finished()==False or robot2.is_finished() == False):
        path1.append(robot1.take_one_step())
        path2.append(robot2.take_one_step())
        i += 1
    
    print(path1)
    print(path2)

main()
print(marieke is geweldig en britte kan het niet)