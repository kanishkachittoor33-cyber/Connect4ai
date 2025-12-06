#!/usr/bin/env python3
"""
Connect 4 Game with AI Support
Supports PvP (Player vs Player), AVA (AI vs AI), and PVA (Player vs AI) modes
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from baml_client import b
from baml_client.types import GameState, AIMove


class Connect4Game:
    ROWS = 6
    COLS = 7
    
    def __init__(self, mode="pvp"):
        """
        Initialize the game
        mode: "pvp" (Player vs Player), "ava" (AI vs AI), or "pva" (Player vs AI)
        """
        self.mode = mode.lower()
        self.board = [["  " for _ in range(self.COLS)] for _ in range(self.ROWS)]
        
        # Determine players based on mode
        if self.mode == "pvp":
            self.players = ["p1", "p2"]
        elif self.mode == "ava":
            self.players = ["a1", "a2"]
        elif self.mode == "pva":
            self.players = ["p1", "a1"]
        else:
            raise ValueError(f"Invalid mode: {mode}. Must be 'pvp', 'ava', or 'pva'")
        
        self.current_player_index = 0
        self.game_over = False
        self.winner = None
    
    def get_current_player(self):
        """Get the current player identifier"""
        return self.players[self.current_player_index]
    
    def is_ai_turn(self):
        """Check if current player is an AI"""
        return self.get_current_player().startswith("a")
    
    def print_board(self):
        """Print the game board"""
        print("\n" + "=" * 50)
        print("  Connect 4 Game")
        print("=" * 50)
        print("\n   " + "   ".join(str(i) for i in range(self.COLS)))
        print("  " + "-" * (self.COLS * 4 - 1))
        
        for row in self.board:
            print("  |" + "|".join(f" {cell} " for cell in row) + "|")
        
        print("  " + "-" * (self.COLS * 4 - 1))
        print("   " + "   ".join(str(i) for i in range(self.COLS)))
        print()
    
    def is_valid_column(self, col):
        """Check if column is valid and not full"""
        return 0 <= col < self.COLS and self.board[0][col] == "  "
    
    def drop_piece(self, col, player):
        """Drop a piece in the specified column"""
        if not self.is_valid_column(col):
            return False
        
        # Find the lowest available row in the column
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == "  ":
                self.board[row][col] = player
                return True
        return False
    
    def check_winner(self):
        """Check if there's a winner"""
        directions = [
            (0, 1),   # horizontal
            (1, 0),   # vertical
            (1, 1),   # diagonal down-right
            (1, -1)   # diagonal down-left
        ]
        
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.board[row][col] == "  ":
                    continue
                
                player = self.board[row][col]
                
                for dr, dc in directions:
                    count = 1
                    for i in range(1, 4):
                        r, c = row + dr * i, col + dc * i
                        if (0 <= r < self.ROWS and 0 <= c < self.COLS and 
                            self.board[r][c] == player):
                            count += 1
                        else:
                            break
                    
                    if count >= 4:
                        return player
        
        return None
    
    def is_board_full(self):
        """Check if the board is full"""
        return all(self.board[0][col] != "  " for col in range(self.COLS))
    
    def get_player_input(self):
        """Get column input from human player"""
        while True:
            try:
                col = int(input(f"Player {self.get_current_player()}, enter column (0-6): "))
                if self.is_valid_column(col):
                    return col
                else:
                    print("Invalid column! Column is either out of range or full. Try again.")
            except ValueError:
                print("Please enter a valid number (0-6).")
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Goodbye!")
                sys.exit(0)
    
    def get_ai_move(self):
        """Get AI move using BAML GetAIMove function"""
        try:
            game_state = GameState(
                board=self.board,
                currentPlayer=self.get_current_player()
            )
            result = b.GetAIMove(game_state)
            return result.column
        except Exception as e:
            print(f"Error getting AI move: {e}")
            # Fallback: return center column if AI fails
            return 3
    
    def play_turn(self):
        """Play a single turn"""
        current_player = self.get_current_player()
        self.print_board()
        
        if self.is_ai_turn():
            print(f"AI {current_player} is thinking...")
            col = self.get_ai_move()
            print(f"AI {current_player} chooses column {col}")
        else:
            col = self.get_player_input()
        
        if not self.drop_piece(col, current_player):
            print("Invalid move! Try again.")
            return
        
        # Check for winner
        winner = self.check_winner()
        if winner:
            self.game_over = True
            self.winner = winner
            self.print_board()
            if winner.startswith("a"):
                print(f"\n🎉 AI {winner} wins!")
            else:
                print(f"\n🎉 Player {winner} wins!")
            return
        
        # Check for draw
        if self.is_board_full():
            self.game_over = True
            self.print_board()
            print("\n🤝 It's a draw!")
            return
        
        # Switch to next player
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def play(self):
        """Main game loop"""
        print(f"\n{'='*50}")
        print(f"  Starting Connect 4 - Mode: {self.mode.upper()}")
        print(f"{'='*50}\n")
        
        while not self.game_over:
            self.play_turn()
        
        print("\nThanks for playing!")


def choose_game_mode():
    """Let user choose the game mode"""
    print("\n" + "="*50)
    print("  Welcome to Connect 4!")
    print("="*50)
    print("\nChoose game mode:")
    print("  1. PvP - Player vs Player")
    print("  2. AVA - AI vs AI")
    print("  3. PVA - Player vs AI")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-3): ").strip()
            if choice == "1":
                return "pvp"
            elif choice == "2":
                return "ava"
            elif choice == "3":
                return "pva"
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)


def main():
    """Main entry point"""
    try:
        mode = choose_game_mode()
        game = Connect4Game(mode=mode)
        game.play()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

