# File: combined_pieces.py

from player import Player
from piece import Piece



class King(Piece):
    def get_valid_piece_moves(self, game_state):
        _peaceful_moves = []
        _piece_takes = []
        moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for move in moves:
            new_row = self.get_row_number() + move[0]
            new_col = self.get_col_number() + move[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                evaluating_square = game_state.get_piece(new_row, new_col)
                if evaluating_square == Player.EMPTY:
                    _peaceful_moves.append((new_row, new_col))
                elif not evaluating_square.is_player(self.get_player()):
                    _piece_takes.append((new_row, new_col))
        
        # Castling moves
        if self.is_player(Player.PLAYER_1):
            if game_state.king_can_castle_left(Player.PLAYER_1):
                _peaceful_moves.append((0, 1))
            if game_state.king_can_castle_right(Player.PLAYER_1):
                _peaceful_moves.append((0, 5))
        else:
            if game_state.king_can_castle_left(Player.PLAYER_2):
                _peaceful_moves.append((7, 1))
            if game_state.king_can_castle_right(Player.PLAYER_2):
                _peaceful_moves.append((7, 5))
        
        return _peaceful_moves + _piece_takes
    
class Bishop(Piece):
    def get_valid_piece_moves(self, game_state):
        moves = []
        current_row, current_col = self.get_row_number(), self.get_col_number()
        
        def check_new_position(row_step, col_step):
            row, col = current_row + row_step, current_col + col_step
            while 0 <= row < 8 and 0 <= col < 8:
                piece = game_state.get_piece(row, col)
                if piece is Player.EMPTY:
                    moves.append((row, col))
                elif game_state.is_valid_piece(row, col) and not piece.is_player(self.get_player()):
                    moves.append((row, col))
                    break
                else:
                    break
                row += row_step
                col += col_step
        
        check_new_position(-1, -1)
        check_new_position(-1, 1)
        check_new_position(1, -1)
        check_new_position(1, 1)
        
        return moves
    
class Rook(Piece):
    # Initialize the piece
    def __init__(self, name, row_number, col_number, player):
        super().__init__(name, row_number, col_number, player)
        self.has_moved = False

    # Get moves
    def get_valid_piece_moves(self, game_state):
        _peaceful_moves = []
        _piece_takes = []

        def check_new_position(new_row, new_col):
            # when the square to the left is empty
            if game_state.get_piece(new_row, new_col) == Player.EMPTY:
                _peaceful_moves.append((new_row, new_col))
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(new_row, new_col) and \
                    not game_state.get_piece(new_row, new_col).is_player(self.get_player()):
                _piece_takes.append((new_row, new_col))
                self._breaking_point = True
            else:
                self._breaking_point = True

        _up = 1
        _down = 1
        _left = 1
        _right = 1

        # Left of the Rook
        self._breaking_point = False
        while self.get_col_number() - _left >= 0 and not self._breaking_point:
            check_new_position(self.get_row_number(), self.get_col_number() - _left)
            _left += 1

        # Right of the Rook
        self._breaking_point = False
        while self.get_col_number() + _right < 8 and not self._breaking_point:
            check_new_position(self.get_row_number(), self.get_col_number() + _right)
            _right += 1

        # Below the Rook
        self._breaking_point = False
        while self.get_row_number() + _down < 8 and not self._breaking_point:
            check_new_position(self.get_row_number() + _down, self.get_col_number())
            _down += 1

        # Above the Rook
        self._breaking_point = False
        while self.get_row_number() - _up >= 0 and not self._breaking_point:
            check_new_position(self.get_row_number() - _up, self.get_col_number())
            _up += 1

        return _peaceful_moves + _piece_takes

class Queen(Rook, Bishop):
    def get_valid_piece_moves(self, game_state):
        return (Rook.get_valid_piece_moves(Rook(self.get_name(), self.get_row_number(), self.get_col_number(), self.get_player()), game_state) +
                Bishop.get_valid_piece_moves(Bishop(self.get_name(), self.get_row_number(), self.get_col_number(), self.get_player()), game_state))

class Knight(Piece):
    def get_valid_piece_moves(self, game_state):
        _peaceful_moves = []
        _piece_takes = []
        moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for move in moves:
            new_row = self.get_row_number() + move[0]
            new_col = self.get_col_number() + move[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                evaluating_square = game_state.get_piece(new_row, new_col)
                if evaluating_square == Player.EMPTY:
                    _peaceful_moves.append((new_row, new_col))
                elif not evaluating_square.is_player(self.get_player()):
                    _piece_takes.append((new_row, new_col))
        
        return _peaceful_moves + _piece_takes