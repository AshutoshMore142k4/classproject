import pygame
import math
import heapq
from enum import Enum
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
ROWS, COLS = 40, 30
CELL_SIZE = WIDTH // ROWS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class NodeType(Enum):
    EMPTY = 0
    BARRIER = 1
    START = 2
    END = 3
    OPEN = 4
    CLOSED = 5
    PATH = 6

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * CELL_SIZE
        self.y = col * CELL_SIZE
        self.type = NodeType.EMPTY
        self.neighbors = []
        
        # A* specific attributes
        self.g_score = float('inf')
        self.f_score = float('inf')
        self.parent = None
        
    def get_color(self):
        color_map = {
            NodeType.EMPTY: WHITE,
            NodeType.BARRIER: BLACK,
            NodeType.START: GREEN,
            NodeType.END: RED,
            NodeType.OPEN: YELLOW,
            NodeType.CLOSED: TURQUOISE,
            NodeType.PATH: PURPLE
        }
        return color_map[self.type]
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.get_color(), 
                        (self.x, self.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GREY, 
                        (self.x, self.y, CELL_SIZE, CELL_SIZE), 1)
    
    def add_neighbors(self, grid):
        self.neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-directional
        
        for dr, dc in directions:
            new_row, new_col = self.row + dr, self.col + dc
            if (0 <= new_row < ROWS and 0 <= new_col < COLS and 
                grid[new_row][new_col].type != NodeType.BARRIER):
                self.neighbors.append(grid[new_row][new_col])

def heuristic(node1, node2):
    """Manhattan distance heuristic"""
    return abs(node1.row - node2.row) + abs(node1.col - node2.col)

def reconstruct_path(end_node):
    """Reconstruct the path from start to end"""
    path = []
    current = end_node
    while current.parent:
        path.append(current)
        current = current.parent
    return path[::-1]

def a_star(grid, start, end, screen, clock):
    """A* pathfinding algorithm with visualization"""
    
    # Initialize
    open_set = []
    open_set_hash = {start}
    
    start.g_score = 0
    start.f_score = heuristic(start, end)
    heapq.heappush(open_set, (start.f_score, id(start), start))
    
    while open_set:
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)
        
        if current == end:
            # Reconstruct and highlight path
            path = reconstruct_path(end)
            for node in path:
                if node.type not in [NodeType.START, NodeType.END]:
                    node.type = NodeType.PATH
            return True
        
        current.type = NodeType.CLOSED
        
        for neighbor in current.neighbors:
            tentative_g_score = current.g_score + 1
            
            if tentative_g_score < neighbor.g_score:
                neighbor.parent = current
                neighbor.g_score = tentative_g_score
                neighbor.f_score = tentative_g_score + heuristic(neighbor, end)
                
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (neighbor.f_score, id(neighbor), neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor.type not in [NodeType.START, NodeType.END]:
                        neighbor.type = NodeType.OPEN
        
        # Visualization update
        draw_grid(screen, grid)
        pygame.display.update()
        clock.tick(60)  # Control animation speed
    
    return False

def create_grid():
    """Create the initial grid"""
    grid = []
    for row in range(ROWS):
        grid.append([])
        for col in range(COLS):
            node = Node(row, col)
            grid[row].append(node)
    return grid

def draw_grid(screen, grid):
    """Draw the entire grid"""
    screen.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(screen)

def get_clicked_pos(pos):
    """Get grid position from mouse click"""
    x, y = pos
    row = x // CELL_SIZE
    col = y // CELL_SIZE
    return row, col

def generate_maze(grid):
    """Generate a random maze pattern"""
    for row in range(ROWS):
        for col in range(COLS):
            if random.random() < 0.3:  # 30% chance of barrier
                grid[row][col].type = NodeType.BARRIER
            else:
                grid[row][col].type = NodeType.EMPTY

def reset_pathfinding(grid):
    """Reset pathfinding visualization but keep barriers"""
    for row in grid:
        for node in row:
            if node.type in [NodeType.OPEN, NodeType.CLOSED, NodeType.PATH]:
                node.type = NodeType.EMPTY
            node.g_score = float('inf')
            node.f_score = float('inf')
            node.parent = None

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A* Pathfinding Visualizer")
    clock = pygame.time.Clock()
    
    grid = create_grid()
    start = None
    end = None
    
    running = True
    
    print("Controls:")
    print("Left Click: Place barriers")
    print("Right Click: Remove barriers")
    print("S: Set start point")
    print("E: Set end point")
    print("SPACE: Run A* algorithm")
    print("C: Clear grid")
    print("M: Generate random maze")
    print("R: Reset pathfinding (keep barriers)")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Mouse controls
            if pygame.mouse.get_pressed()[0]:  # Left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                if 0 <= row < ROWS and 0 <= col < COLS:
                    node = grid[row][col]
                    if node.type not in [NodeType.START, NodeType.END]:
                        node.type = NodeType.BARRIER
            
            elif pygame.mouse.get_pressed()[2]:  # Right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                if 0 <= row < ROWS and 0 <= col < COLS:
                    node = grid[row][col]
                    if node.type != NodeType.START and node.type != NodeType.END:
                        node.type = NodeType.EMPTY
            
            # Keyboard controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Set start
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos)
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        if start:
                            start.type = NodeType.EMPTY
                        start = grid[row][col]
                        start.type = NodeType.START
                
                elif event.key == pygame.K_e:  # Set end
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos)
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        if end:
                            end.type = NodeType.EMPTY
                        end = grid[row][col]
                        end.type = NodeType.END
                
                elif event.key == pygame.K_SPACE:  # Run A*
                    if start and end:
                        reset_pathfinding(grid)
                        # Add neighbors for all nodes
                        for row in grid:
                            for node in row:
                                node.add_neighbors(grid)
                        
                        result = a_star(grid, start, end, screen, clock)
                        if not result:
                            print("No path found!")
                
                elif event.key == pygame.K_c:  # Clear grid
                    grid = create_grid()
                    start = None
                    end = None
                
                elif event.key == pygame.K_m:  # Generate maze
                    grid = create_grid()
                    generate_maze(grid)
                    start = None
                    end = None
                
                elif event.key == pygame.K_r:  # Reset pathfinding
                    reset_pathfinding(grid)
        
        draw_grid(screen, grid)
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
