class Piece:
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol

    def can_move(self, start, end, board):
        raise NotImplementedError("Subclasses must implement this method.")

    def potential_attacks(self, position, board):
        raise NotImplementedError("Subclasses must implement this method.")


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'P')

    def can_move(self, start, end, board):
        direction = -1 if self.color == 'white' else 1
        start_row, start_col = start
        end_row, end_col = end

        if start_col == end_col:  # Forward movement
            if (start_row + direction == end_row and board[end_row][end_col] is None) or \
               (self.color == 'white' and start_row == 6 and end_row == 4 and board[4][start_col] is None) or \
               (self.color == 'black' and start_row == 1 and end_row == 3 and board[3][start_col] is None):
                return True
        elif abs(start_col - end_col) == 1 and start_row + direction == end_row:
            if board[end_row][end_col] and board[end_row][end_col].color != self.color:
                return True
        return False

    def potential_attacks(self, position, board):
        attacks = []
        direction = -1 if self.color == 'white' else 1
        row, col = position

        for delta_col in (-1, 1):
            attack_row, attack_col = row + direction, col + delta_col
            if 0 <= attack_row < 8 and 0 <= attack_col < 8:
                target = board[attack_row][attack_col]
                if target and target.color != self.color:
                    attacks.append((attack_row, attack_col))
        return attacks


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'R')

    def can_move(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end

        if start_row == end_row:  # Horizontal movement
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if board[start_row][col]:
                    return False
            return True

        if start_col == end_col:  # Vertical movement
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if board[row][start_col]:
                    return False
            return True
        return False

    def potential_attacks(self, position, board):
        return self._scan_directions(position, board, [(-1, 0), (1, 0), (0, -1), (0, 1)])

    def _scan_directions(self, position, board, directions):
        attacks = []
        row, col = position
        for dx, dy in directions:
            x, y = row + dx, col + dy
            while 0 <= x < 8 and 0 <= y < 8:
                if board[x][y]:
                    if board[x][y].color != self.color:
                        attacks.append((x, y))
                    break
                x += dx
                y += dy
        return attacks


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'N')

    def can_move(self, start, end, board):
        dx, dy = abs(start[0] - end[0]), abs(start[1] - end[1])
        return (dx, dy) in [(2, 1), (1, 2)]

    def potential_attacks(self, position, board):
        attacks = []
        row, col = position
        knight_moves = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]

        for dx, dy in knight_moves:
            x, y = row + dx, col + dy
            if 0 <= x < 8 and 0 <= y < 8:
                attacks.append((x, y))
        return attacks


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'B')

    def can_move(self, start, end, board):
        if abs(start[0] - end[0]) == abs(start[1] - end[1]):  # Diagonal movement
            dx = 1 if end[0] > start[0] else -1
            dy = 1 if end[1] > start[1] else -1
            x, y = start[0] + dx, start[1] + dy
            while x != end[0]:
                if board[x][y]:
                    return False
                x += dx
                y += dy
            return True
        return False

    def potential_attacks(self, position, board):
        return Rook(self.color)._scan_directions(position, board, [(-1, -1), (-1, 1), (1, -1), (1, 1)])


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'Q')

    def can_move(self, start, end, board):
        return Rook(self.color).can_move(start, end, board) or Bishop(self.color).can_move(start, end, board)

    def potential_attacks(self, position, board):
        return Rook(self.color).potential_attacks(position, board) + Bishop(self.color).potential_attacks(position, board)


class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'K')

    def can_move(self, start, end, board):
        return abs(start[0] - end[0]) <= 1 and abs(start[1] - end[1]) <= 1

    def potential_attacks(self, position, board):
        attacks = []
        row, col = position
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                x, y = row + dx, col + dy
                if 0 <= x < 8 and 0 <= y < 8:
                    attacks.append((x, y))
        return attacks


class Board:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_turn = 'white'

    def initialize_board(self):
        grid = [[None for _ in range(8)] for _ in range(8)]

        # Place black and white pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, PieceClass in enumerate(piece_order):
            grid[0][i] = PieceClass('black')
            grid[7][i] = PieceClass('white')
        for i in range(8):
            grid[1][i] = Pawn('black')
            grid[6][i] = Pawn('white')
        return grid

    def display(self):
        for row in self.board:
            print(" ".join([piece.symbol if piece else '.' for piece in row]))

    def move_piece(self, start, end):
        pass  # Implement logic similar to original but with some structural changes


# Example main function
def main():
    chess = Board()
    chess.display()


if __name__ == "__main__":
    main()