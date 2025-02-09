#include <stdio.h>

#define SIZE 6
#define MAX_CAGES 10

typedef struct {
    int target;
    char operation;
    int cells[SIZE][2];
    int cell_count;
} Cage;

int grid[SIZE][SIZE];
Cage cages[MAX_CAGES];
int cage_count;

// Function to apply logic operations
int apply_logic(char op, int values[], int count) {
    int result;
    if (op == 'A') {
        result = 1;
        for (int i = 0; i < count; i++) {
            result &= values[i];
        }
    } else if (op == 'O') {
        result = 0;
        for (int i = 0; i < count; i++) {
            result |= values[i];
        }
    } else if (op == 'X') {
        result = 0;
        for (int i = 0; i < count; i++) {
            result ^= values[i];
        }
    } else {
        return -1; 
    }
    return result;
}

// Function to check if the grid follows constraints
int is_valid_grid() {
    for (int c = 0; c < cage_count; c++) {
        int values[SIZE], count = 0;
        for (int i = 0; i < cages[c].cell_count; i++) {
            int r = cages[c].cells[i][0], col = cages[c].cells[i][1];
            if (grid[r][col] == -1) {
                return 1;
            }
            values[count++] = grid[r][col];
        }
        if (apply_logic(cages[c].operation, values, count) != cages[c].target) {
            return 0;
        }
    }
    return 1;
}

// Function to solve the grid using backtracking
int solve_grid(int r, int c) {
    if (r == SIZE) {
        return is_valid_grid();
    }
    
    int next_r, next_c;
    if (c == SIZE - 1) {
        next_r = r + 1;
        next_c = 0;
    } else {
        next_r = r;
        next_c = c + 1;
    }
    
    if (grid[r][c] != -1) {
        return solve_grid(next_r, next_c);
    }
    
    for (int val = 0; val <= 1; val++) {
        grid[r][c] = val;
        if (is_valid_grid() && solve_grid(next_r, next_c)) {
            return 1;
        }
        grid[r][c] = -1;
    }
    return 0;
}

int main() {
    printf("Enter the 6x6 grid (-1 for empty cells):\n");
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            scanf("%d", &grid[i][j]);
        }
    }
    
    printf("Enter number of cages: ");
    scanf("%d", &cage_count);
    
    for (int i = 0; i < cage_count; i++) {
        printf("Enter target, operation (A/O/X), and cell count: ");
        scanf("%d %c %d", &cages[i].target, &cages[i].operation, &cages[i].cell_count);
        for (int j = 0; j < cages[i].cell_count; j++) {
            printf("Enter cell (row col): ");
            scanf("%d %d", &cages[i].cells[j][0], &cages[i].cells[j][1]);
        }
    }
    
    if (solve_grid(0, 0)) {
        printf("Solved Grid:\n");
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                printf("%d ", grid[i][j]);
            }
            printf("\n");
        }
    } else {
        printf("NO SOLUTION\n");
    }
    return 0;
}

