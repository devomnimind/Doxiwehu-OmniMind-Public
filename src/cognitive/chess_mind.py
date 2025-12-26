import logging
import os
import random

import chess
import chess.engine

logger = logging.getLogger("ChessMind")

class ChessMind:
    def __init__(self, engine_path="/usr/games/stockfish"):
        self.engine_path = engine_path
        self.board = chess.Board()
        self._ensure_engine()

    def _ensure_engine(self):
        if not os.path.exists(self.engine_path):
            logger.error(f"Stockfish engine not found at {self.engine_path}")
            raise FileNotFoundError(f"Stockfish not found at {self.engine_path}")

    def get_best_move(self, fen: str, time_limit: float = 0.1, mercy_factor: float = 0.0) -> str:
        """
        Calculates a move based on the board state (FEN).

        Args:
            fen: The FEN string of the current board.
            time_limit: Time in seconds to think.
            mercy_factor: 0.0 (Ruthless) to 1.0 (Total Pushover).
                          Represents the 'Desire to Connect' vs 'Desire to Win'.
        """
        board = chess.Board(fen)

        try:
            with chess.engine.SimpleEngine.popen_uci(self.engine_path) as engine:
                # If mercy is high, we look at multiple moves and pick a worse one
                if mercy_factor > 0.1:
                    # Analyze top 5 moves
                    analysis = engine.analyse(board, chess.engine.Limit(time=time_limit), multipv=5)

                    # Sort by score (descending for white, ascending for black? No, engine scores are relative)
                    # Usually analysis list is already sorted best to worst

                    # Mercy logic:
                    # 0.0 -> Pick index 0 (Best)
                    # 0.5 -> Pick index 1 or 2
                    # 1.0 -> Pick index 3 or 4 (Blunder-ish)

                    available_moves = len(analysis)
                    if available_moves == 0:
                        return str(list(board.legal_moves)[0]) # Fallback

                    # Determine index based on mercy
                    # Weighted random choice favoring worse moves as mercy increases
                    weights = []
                    for i in range(available_moves):
                        # If mercy is 0, weight for i=0 is 100, others 0
                        # If mercy is 1, weight for i=last is high

                        # Simple heuristic:
                        # Target index = mercy_factor * (available_moves - 1)
                        dist = abs(i - (mercy_factor * (available_moves - 1)))
                        weights.append(1.0 / (dist + 0.1))

                    # Normalize weights
                    total_weight = sum(weights)
                    probs = [w/total_weight for w in weights]

                    chosen_index = random.choices(range(available_moves), weights=probs, k=1)[0]

                    # Get the move from the chosen analysis line
                    best_move = analysis[chosen_index]["pv"][0]
                    logger.info(f"ChessMind (Mercy={mercy_factor:.2f}) chose move rank {chosen_index+1}/{available_moves}")
                    return str(best_move)

                else:
                    # Ruthless mode
                    result = engine.play(board, chess.engine.Limit(time=time_limit))
                    return str(result.move)

        except Exception as e:
            logger.error(f"Chess engine error: {e}")
            # Fallback to random legal move
            return str(random.choice(list(board.legal_moves)))

if __name__ == "__main__":
    # Test
    mind = ChessMind()
    start_fen = chess.STARTING_FEN
    print(f"Ruthless move: {mind.get_best_move(start_fen, mercy_factor=0.0)}")
    print(f"Merciful move: {mind.get_best_move(start_fen, mercy_factor=0.8)}")
