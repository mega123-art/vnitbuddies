# Define constants
GRID_SIZE = 6
MAX_CAGES = 10

# Define the Cage structure
class Cage:
    def __init__(self, target, operation, cells):
        self.target = target  # Target value for the cage
        self.operation = operation  # Logical operation: 'A' (AND), 'O' (OR), 'X' (XOR)
        self.cells = cells  # List of cells (as tuples of row, column) in the cage

# Function to apply logical operations
def apply_logic(operation, values):
    if operation == 'A':  # AND operation
        result = 1
        for value in values:
            result &= value
        return result
    elif operation == 'O':  # OR operation
        result = 0
        for value in values:
            result |= value
        return result
    elif operation == 'X':  # XOR operation
        result = 0
        for value in values:
            result ^= value
        return result
    else:
        return -1  # Invalid operation

# Function to check if the grid satisfies all cage constraints
def is_grid_valid(grid, cages):
    for cage in cages:
        values = []
        for (row, col) in cage.cells:
            if grid[row][col] == -1:
                return True  # If any cell is empty, the grid is still potentially valid
            values.append(grid[row][col])
        if apply_logic(cage.operation, values) != cage.target:
            return False  # Cage constraint is not satisfied
    return True  # All cage constraints are satisfied

# Backtracking solver function
def solve_grid(grid, cages, row=0, col=0):
    # Base case: If we've reached the end of the grid, check if it's valid
    if row == GRID_SIZE:
        return is_grid_valid(grid, cages)
    
    # Calculate the next cell to move to
    next_row, next_col = (row, col + 1) if col < GRID_SIZE - 1 else (row + 1, 0)
    
    # If the current cell is already filled, move to the next cell
    if grid[row][col] != -1:
        return solve_grid(grid, cages, next_row, next_col)
    
    # Try placing 0 and 1 in the current cell
    for value in [0, 1]:
        grid[row][col] = value
        if is_grid_valid(grid, cages) and solve_grid(grid, cages, next_row, next_col):
            return True  # Solution found
        grid[row][col] = -1  # Backtrack
    
    return False  # No solution found

# Main function
def main():
    # Initialize the grid with empty cells (-1)
    grid = [[-1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # Input the grid
    print("Enter the 6x6 grid (-1 for empty cells):")
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            grid[row][col] = int(input(f"Enter value for cell ({row}, {col}): "))
    
    # Input the number of cages
    cage_count = int(input("Enter the number of cages: "))
    cages = []
    
    # Input details for each cage
    for i in range(cage_count):
        target = int(input(f"Enter target value for cage {i + 1}: "))
        operation = input(f"Enter operation for cage {i + 1} (A for AND, O for OR, X for XOR): ").upper()
        cell_count = int(input(f"Enter the number of cells in cage {i + 1}: "))
        cells = []
        for j in range(cell_count):
            row = int(input(f"Enter row for cell {j + 1} in cage {i + 1}: "))
            col = int(input(f"Enter column for cell {j + 1} in cage {i + 1}: "))
            cells.append((row, col))
        cages.append(Cage(target, operation, cells))
    
    # Solve the grid
    if solve_grid(grid, cages):
        print("Solved Grid:")
        for row in grid:
            print(" ".join(map(str, row)))
    else:
        print("NO SOLUTION")

# Run the program
if __name__ == "__main__":
    main()
