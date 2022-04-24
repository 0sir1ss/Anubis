class NQueens:
    """Generate all valid solutions for the n queens puzzle"""
    
    def __init__(self, size):
        # Store the puzzle (problem) size and the number of valid solutions
        self.__size = size
        self.__solutions = 0
        self.__solve()

    def __solve(self):
        """Solve the n queens puzzle and print the number of solutions"""
        positions = [-1] * self.__size
        self.__put_queen(positions, 0)
        print("Found", self.__solutions, "solutions.")

    def __put_queen(self, positions, target_row):
        """
        Try to place a queen on target_row by checking all N possible cases.
        If a valid place is found the function calls itself trying to place a queen
        on the next row until all N queens are placed on the NxN board.
        """
        # Base (stop) case - all N rows are occupied
        if target_row == self.__size:
            self.__show_full_board(positions)
            self.__solutions += 1
        else:
            # For all N columns positions try to place a queen
            for column in range(self.__size):
                # Reject all invalid positions
                if self.__check_place(positions, target_row, column):
                    positions[target_row] = column
                    self.__put_queen(positions, target_row + 1)


    def __check_place(self, positions, ocuppied_rows, column):
        """
        Check if a given position is under attack from any of
        the previously placed queens (check column and diagonal positions)
        """
        for i in range(ocuppied_rows):
            if positions[i] == column or positions[i] - i == column - ocuppied_rows or positions[i] + i == column + ocuppied_rows:
                return False
        return True

    def __show_full_board(self, positions):
        """Show the full NxN board"""
        for row in range(self.__size):
            line = ""
            for column in range(self.__size):
                if positions[row] == column:
                    line += "Q "
                else:
                    line += ". "
            print(line)
        print("\n")

    def __show_short_board(self, positions):
        """
        Show the queens positions on the board in compressed form,
        each number represent the occupied column position in the corresponding row.
        """
        line = ""
        for i in range(self.__size):
            line += str(positions[i]) + " "
        print(line)

def main():
    """Initialize and solve the n queens puzzle"""
    NQueens(8)

if __name__ == "__main__":
    # execute only if run as a script
    main()
