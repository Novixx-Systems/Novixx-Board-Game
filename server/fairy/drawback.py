import random
import chess
from logger import log
WHITE, BLACK = 0, 1

# Convert algebraic notation like "g1" to 0-63 index
def square_to_index(square):
    col = ord(square[0].lower()) - ord('a')
    row = 8 - int(square[1])
    return row * 8 + col

# Convert 0-63 index to (row, col)
def to_row_col(pos):
    return divmod(pos, 8)

# Compute intermediate squares for a non-jumping knight
def intermediate_squares(start_idx, end_idx):
    start_row, start_col = to_row_col(start_idx)
    end_row, end_col = to_row_col(end_idx)

    dr = end_row - start_row
    dc = end_col - start_col

    squares = []

    # L shape: one direction moves 2, other moves 1
    if (abs(dr), abs(dc)) not in [(2,1), (1,2)]:
        return squares  # not an L move

    # Move along major axis first (the one with 2)
    if abs(dr) == 2:
        step_r = 1 if dr > 0 else -1
        squares.append((start_row + step_r) * 8 + start_col)  # first step
        squares.append((start_row + 2*step_r) * 8 + start_col)  # second step
        # minor axis
        step_c = 1 if dc > 0 else -1
        squares.append((start_row + 2*step_r) * 8 + (start_col + step_c))
    else:  # abs(dc) == 2
        step_c = 1 if dc > 0 else -1
        squares.append(start_row * 8 + (start_col + step_c))
        squares.append(start_row * 8 + (start_col + 2*step_c))
        # minor axis
        step_r = 1 if dr > 0 else -1
        squares.append((start_row + step_r) * 8 + (start_col + 2*step_c))

    return squares


def check_drawback(oldfen: str, newfen: str, move: str, drawback: str) -> bool:
    from fairy.fairy_board import FairyBoard
    """
    Checks if the move is against the drawback.
    """
    if drawback == "vegan":
        # can't capture knights
        # if move is capture and there is 1 less knight on the board, return False
        oldpieces = oldfen.split()[0].lower()
        newpieces = newfen.split()[0].lower()
        board = FairyBoard("chess", oldfen)
        if board.piece_at(move[0:2], True) == "K":
            return True
        else:
            if oldpieces.count("n") > newpieces.count("n"):
                return False
        return True

    if drawback == "atheist":
        # can't move bishops
        color = oldfen.split()[1]
        if color == "w":
            bishop_piece = "B"
        else:
            bishop_piece = "b"
        board = FairyBoard("chess", oldfen)
        bishop_positions = [i for i in range(64) if board.piece_at(i, False) == bishop_piece]
        new_board = FairyBoard("chess", newfen)
        new_bishop_positions = [i for i in range(64) if new_board.piece_at(i, False) == bishop_piece]

        return bishop_positions == new_bishop_positions

    if drawback == "kinglife":
        # king is stuck on first rank
        FIRST_RANK = 0
        color = oldfen.split()[1]
        if color == "w":
            FIRST_RANK = 7
        firstrank = newfen.split()[0].split("/")[FIRST_RANK].lower()
        if "k" in firstrank:
            return True
        return False

    if drawback == "queenhate":
        # no queen promotion
        oldpieces = oldfen.split()[0].lower()
        newpieces = newfen.split()[0].lower()
        if oldpieces.count("q") < newpieces.count("q"):
            return False
        return True

    if drawback == "rooklife":
        # must move both rooks before queen
        # check color
        color = WHITE if oldfen.split()[1] == "w" else BLACK
        # get first rank
        FIRST_RANK = 0
        if color == WHITE:
            FIRST_RANK = 7
        firstrank = oldfen.split()[0].split("/")[FIRST_RANK].lower()
        if firstrank.startswith("r") or firstrank.endswith("r"):
            # if queen moved, return False
            board = FairyBoard("chess", oldfen)
            queen_positions = [i for i in range(64) if board.piece_at(i, True) == "Q"]
            new_board = FairyBoard("chess", newfen)
            new_queen_positions = [i for i in range(64) if new_board.piece_at(i, True) == "Q"]
            log.debug("queen_positions: %s, new_queen_positions: %s", queen_positions, new_queen_positions)
            if len(queen_positions) > len(new_queen_positions):
                return True
            return queen_positions == new_queen_positions
        return True

    if drawback == "mustcapture":
        # must capture a piece if possible
        board = FairyBoard("chess", oldfen)
        moves = board.legal_moves()
        if len(moves) == 0:
            return True
        else:
            if board.can_capture():
                # make sure we captured a piece
                oldpieces = oldfen.split()[0]
                newpieces = newfen.split()[0]
                # check p, P, n, N, b, B, r, R, q, Q
                if oldpieces.count("p") > newpieces.count("p") or oldpieces.count("P") > newpieces.count("P") or oldpieces.count("n") > newpieces.count("n") or oldpieces.count("N") > newpieces.count("N") or oldpieces.count("b") > newpieces.count("b") or oldpieces.count("B") > newpieces.count("B") or oldpieces.count("r") > newpieces.count("r") or oldpieces.count("R") > newpieces.count("R") or oldpieces.count("q") > newpieces.count("q") or oldpieces.count("Q") > newpieces.count("Q"):
                    return True # captured a piece
                return False # didn't capture a piece
            else:
                return True

    if drawback == "centerban":
        # can't move to the center
        if move.startswith("e4") or move.startswith("e5") or move.startswith("d4") or move.startswith("d5") or move.endswith("e4") or move.endswith("e5") or move.endswith("d4") or move.endswith("d5"):
            return False
        return True

    if drawback == "limitedrooks":
        # rooks can only move one square
        board = FairyBoard("chess", oldfen)
        from_square = move[:2]
        to_square = move[2:4]
        if board.piece_at(from_square, True) == "R":
            # check distance between from_square and to_square (must be eithher -1, 1, 8 or -8 (orthogonal))
            if board.square_to_index(from_square) - board.square_to_index(to_square) not in [-1, 1, 8, -8]:
                return False
        return True

    if drawback == "neutralking":
        # king can't capture
        board = FairyBoard("chess", oldfen)
        from_square = move[:2]
        to_square = move[2:4]
        if board.piece_at(from_square, True) == "K":
            if board.piece_at(to_square, True).isalpha():
                return False
        return True

    if drawback == "antijump":
        # knights can't jump
        board = FairyBoard("chess", oldfen)
        from_square = move[:2]
        to_square = move[2:4]

        if board.piece_at(from_square, True) != "N":
            return True  # Not a knight, ignore

        start_idx = square_to_index(from_square)
        end_idx = square_to_index(to_square)

        # Check L shape
        if sorted([abs(to_row_col(start_idx)[0]-to_row_col(end_idx)[0]), 
                abs(to_row_col(start_idx)[1]-to_row_col(end_idx)[1])]) != [1,2]:
            return False  # not a valid L shape

        # Check intermediate squares
        for sq_idx in intermediate_squares(start_idx, end_idx)[:-1]:  # exclude final destination
            row, col = to_row_col(sq_idx)
            algebraic = chr(col + ord('a')) + str(8 - row)
            if board.piece_at(algebraic, True).isalpha():
                return False  # piece in the way

    if drawback == "c5mover":
        # if any piece can go to c5, must move to c5
        board = FairyBoard("chess", oldfen)
        moves = board.legal_moves(None)
        legal_c5_move = False
        for moveP in moves:
            if moveP.endswith("c5"):
                if move.endswith("c5"):
                    return True
                legal_c5_move = True

        return not legal_c5_move # if no piece can go to c5, returns True because else stalemate
    if drawback == "evenpawn":
        board = FairyBoard("chess", oldfen)

        moveclock = int(oldfen.split()[5]) # full move clock
        legal_moves = board.legal_moves(None)
        num_legal_pawn_moves = 0
        for moveP in legal_moves:
            if board.piece_at(moveP[0:2], True) == "P":
                num_legal_pawn_moves += 1
        
        if moveclock % 2 == 0 and num_legal_pawn_moves > 0:
            return board.piece_at(move[0:2], True) == "P"


        return True

    if drawback == "halfpawn":
        # lose when having 4 or less pawns
        board = FairyBoard("chess", oldfen)
        color = oldfen.split()[1]
        if color == "w":
            pawn_piece = "P"
        else:
            pawn_piece = "p"
        pawn_positions = [i for i in range(64) if board.piece_at(i, False) == pawn_piece]
        if len(pawn_positions) <= 4:
            return "LOSS"
        return True

    if drawback == "knightmare":
        # win when checking the opponent with a knight, lose when the opponent checks you with a knight
        board = FairyBoard("chess", oldfen)
        checkboard = chess.Board(oldfen)
        attacks = checkboard.attackers(not checkboard.turn, checkboard.king(checkboard.turn))
        if attacks:
            for square in attacks:
                piece = checkboard.piece_at(square)
                if piece.symbol().lower() == "n":
                    return "LOSS"

        from_square = move[:2]
        to_square = move[2:4]
        
        if board.piece_at(from_square, True) == "N":
            checkboard.push_uci(move)
            attacks = checkboard.attackers(not checkboard.turn, checkboard.king(checkboard.turn))
            if attacks:
                for square in attacks:
                    piece = checkboard.piece_at(square)
                    if piece.symbol().lower() == "n":
                        return "WIN"
        return True

    if drawback == "kingofthehill":
        # lose if opponent's king is on the center
        board = FairyBoard("chess", oldfen)
        mycolor = oldfen.split()[1]
        if mycolor == "w":
            opponent_color = "b"
        else:
            opponent_color = "w"
        king_name = "K" if opponent_color == "w" else "k"
        king_positions = [i for i in range(64) if board.piece_at(i, False) == king_name]
        if len(king_positions) > 0:
            if king_positions[0] in [board.square_to_index("a4"), board.square_to_index("b4"),
                                    board.square_to_index("c4"), board.square_to_index("d4"), 
                                    board.square_to_index("e4"), board.square_to_index("f4"), 
                                    board.square_to_index("g4"), board.square_to_index("h4"),

                                    board.square_to_index("a5"), board.square_to_index("b5"),
                                    board.square_to_index("c5"), board.square_to_index("d5"), 
                                    board.square_to_index("e5"), board.square_to_index("f5"), 
                                    board.square_to_index("g5"), board.square_to_index("h5")]:
                return "LOSS"
        return True

    if drawback == "unluckydice":
        # every time we get out of check, 1 in 6 chance it's a LOSS
        board = FairyBoard("chess", oldfen)
        mycolor = oldfen.split()[1]
        if mycolor == "w":
            opponent_color = "b"
        else:
            opponent_color = "w"
        if board.is_checked():
            if random.randint(0, 5) == 0:
                return "LOSS"
            else:
                return True
        return True
    
    if drawback == "minorhate":
        # can't move minor (Knight, Bishop) pieces every 2 moves
        board = FairyBoard("chess", oldfen)

        moveclock = int(oldfen.split()[5]) # full move clock
        legal_moves = board.legal_moves(None)
        num_legal_pawn_moves = 0
        for moveP in legal_moves:
            if board.piece_at(moveP[0:2], True) != "B" and board.piece_at(moveP[0:2], True) != "N": 
                num_legal_pawn_moves += 1
        
        if moveclock % 2 == 0 and num_legal_pawn_moves > 0:
            return board.piece_at(move[0:2], True) != "B" and board.piece_at(move[0:2], True) != "N"

    if drawback == "catastrophe":
        # you lose when you lose your queen(s)
        board = FairyBoard("chess", oldfen)
        mycolor = oldfen.split()[1]
        queenchar = "q" if mycolor == "b" else "Q"
        queen_positions = [i for i in range(64) if board.piece_at(i, False) == queenchar]
        if len(queen_positions) == 0:
            return "LOSS"

        return True

    if drawback == "rooklove":
        # can only promote to rooks and queen moves 1 square othogonally
        if move[-1] in ['q', 'b', 'n']:
            return False

        board = FairyBoard("chess", oldfen)
        start_square = move[0:2]
        end_square = move[2:4]

        piece = board.piece_at(start_square, True)
        if piece == 'Q':
            # check distance between from_square and end_square (must be eithher -1, 1, 8 or -8 (orthogonal))
            if board.square_to_index(from_square) - board.square_to_index(end_square) not in [-1, 1, 8, -8]:
                return False

        return True

    if drawback == "pawnshield":
        # can't move pieces to a square protected by an opponent's pawn
        board = FairyBoard("chess", oldfen)
        mycolor = oldfen.split()[1]
        opponent_color = "b" if mycolor == "w" else "w"
        to_square = move[2:4]
        to_idx = board.square_to_index(to_square)
        to_row, to_col = to_row_col(to_idx)

        # check if opponent pawn attacks this square
        if opponent_color == "w":
            # white pawns attack diagonally up
            attacking_squares = []
            if to_col > 0:
                attacking_squares.append((to_row + 1) * 8 + (to_col - 1))
            if to_col < 7:
                attacking_squares.append((to_row + 1) * 8 + (to_col + 1))
        else:
            # black pawns attack diagonally down
            attacking_squares = []
            if to_col > 0:
                attacking_squares.append((to_row - 1) * 8 + (to_col - 1))
            if to_col < 7:
                attacking_squares.append((to_row - 1) * 8 + (to_col + 1))

        for sq_idx in attacking_squares:
            row, col = to_row_col(sq_idx)
            if 0 <= row < 8 and 0 <= col < 8:
                algebraic = chr(col + ord('a')) + str(8 - row)
                if board.piece_at(algebraic, True) == ('P' if opponent_color == 'w' else 'p'):
                    return False  # square is protected by opponent pawn
        
        return True

    return True

DRAWBACK_DESCRIPTION = {
    "vegan": "pieces can't capture knights (except the king)",
    "atheist": "can't move bishops",
    "kinglife": "king is stuck on first rank",
    "queenhate": "no queen promotion",
    "rooklife": "must move both rooks before queen",
    "mustcapture": "must capture a piece if possible",
    "centerban": "can't move to the center",
    "limitedrooks": "rooks can only move one square",
    "neutralking": "king can't capture",
    "antijump": "knights can't jump",
    "c5mover": "if any piece can go to c5, must move to c5",
    "evenpawn": "must move pawn if possible if move number is even (first move is odd)",
    "halfpawn": "lose when having 4 or less pawns",
    "knightmare": "win when checking the opponent with a knight, lose when the opponent does it to you",
    "kingofthehill": "lose if opponent's king is on the center",
    "unluckydice": "every time you get out of check, 1 in 6 chance you lose",
    "minorhate": "can't move minor pieces (Knight, Bishop) if move number is even (first move is odd)",
    "catastrophe": "you lose when you lose your queen(s)",
    "rooklove": "can only promote to rooks and queen moves 1 square up, down, left and right",
    "pawnshield": "can't move pieces to a square protected by an opponent's pawn",
}