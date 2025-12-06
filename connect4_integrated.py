#!/usr/bin/env python3
"""
Connect 4 Game - Human vs AI
Integrates BAML GetAIMove function with the original game code
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
# This must be called before importing baml_client to ensure API keys are available
load_dotenv()

# Import BAML client and types
# The 'b' client is the synchronous client for calling BAML functions
from baml_client import b
from baml_client.types import GameState, AIMove


# Initialize gameboard
gameboard = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ']
]


def fancy_gameboard(gameboard):
    """Display the gameboard in a fancy format"""
    print("\n" + "=" * 50)
    print("  Connect 4 Game - Human (x) vs AI (o)")
    print("=" * 50)
    print("\n   " + "   ".join(str(i+1) for i in range(7)))
    print("  " + "-" * (7 * 4 - 1))
    
    for row in gameboard:
        print("  |" + "|".join(f" {cell} " for cell in row) + "|")
    
    print("  " + "-" * (7 * 4 - 1))
    print("   " + "   ".join(str(i+1) for i in range(7)))
    print()


def checkwin(gameboard):
    """Check if there's a winner"""
    # Check horizontal wins
    for row in gameboard:
        for i in range(4):
            if row[i] == row[i+1] == row[i+2] == row[i+3] and row[i] != ' ':
                return row[i]
    
    # Check diagonal (down-right)
    for i in range(4):
        for j in range(3, 6):
            if (gameboard[j][i] == gameboard[j-1][i+1] == gameboard[j-2][i+2] == gameboard[j-3][i+3] 
                and gameboard[j][i] != ' '):
                return gameboard[j][i]
    
    # Check diagonal (down-left)
    for i in range(3, 7):
        for j in range(3, 6):
            if (gameboard[j][i] == gameboard[j-1][i-1] == gameboard[j-2][i-2] == gameboard[j-3][i-3] 
                and gameboard[j][i] != ' '):
                return gameboard[j][i]
    
    # Check vertical wins
    for i in range(7):
        for j in range(3):
            if (gameboard[j][i] == gameboard[j+1][i] == gameboard[j+2][i] == gameboard[j+3][i] 
                and gameboard[j][i] != ' '):
                return gameboard[j][i]
    
    return None


def convert_board_to_baml_format(gameboard):
    """Convert gameboard from ['x', 'o', ' '] to BAML format ['p1', 'a1', '  ']"""
    baml_board = []
    for row in gameboard:
        baml_row = []
        for cell in row:
            if cell == 'x':
                baml_row.append('p1')
            elif cell == 'o':
                baml_row.append('a1')
            else:  # cell == ' '
                baml_row.append('  ')
        baml_board.append(baml_row)
    return baml_board


def convert_board_from_baml_format(baml_board):
    """Convert BAML format board back to game format"""
    gameboard = []
    for row in baml_board:
        game_row = []
        for cell in row:
            if cell == 'p1':
                game_row.append('x')
            elif cell == 'a1':
                game_row.append('o')
            else:  # cell == '  '
                game_row.append(' ')
        gameboard.append(game_row)
    return gameboard


def makeamove(gameboard, player):
    """Make a move for human player"""
    validmove = False
    while not validmove:
        try:
            playercolumnmove = input(f"Player {player}, choose a column (1-7): ")
            if playercolumnmove.isdigit():
                playercolumnmove = int(playercolumnmove)
                if 1 <= playercolumnmove <= 7:
                    if gameboard[0][playercolumnmove - 1] == ' ':
                        validmove = True
                        break
            print("Invalid move! Please enter a number between 1-7 for an available column.")
        except KeyboardInterrupt:
            print("\n\nGame interrupted. Goodbye!")
            sys.exit(0)
    
    # Drop the piece
    for i in range(5, -1, -1):
        if gameboard[i][playercolumnmove - 1] == ' ':
            gameboard[i][playercolumnmove - 1] = player
            break


def make_ai_move(gameboard):
    """Make a move for AI using BAML GetAIMove function"""
    try:
        # Convert board to BAML format
        baml_board = convert_board_to_baml_format(gameboard)
        
        # Create game state for BAML using proper Pydantic model
        # Note: GameState uses camelCase field names (currentPlayer, not current_player)
        game_state = GameState(
            board=baml_board,
            currentPlayer="a1"  # AI is always "a1"
        )
        
        # Get AI move using BAML client
        # Use keyword argument to match function signature: GetAIMove(gameState: types.GameState)
        print("AI is thinking...")
        result = b.GetAIMove(gameState=game_state)
        
        # Result is an AIMove object with a column attribute (0-6)
        ai_column = result.column
        
        # Convert from 0-based (BAML) to 1-based (game) indexing
        playercolumnmove = ai_column + 1
        
        # Validate and apply the move
        if 1 <= playercolumnmove <= 7 and gameboard[0][playercolumnmove - 1] == ' ':
            # Drop the piece in the chosen column
            for i in range(5, -1, -1):
                if gameboard[i][playercolumnmove - 1] == ' ':
                    gameboard[i][playercolumnmove - 1] = 'o'
                    print(f"AI chooses column {playercolumnmove}")
                    return
        else:
            # Fallback: AI returned invalid column, find first available
            print(f"AI tried column {playercolumnmove} but it's invalid. Finding alternative...")
            for col in range(7):
                if gameboard[0][col] == ' ':
                    for i in range(5, -1, -1):
                        if gameboard[i][col] == ' ':
                            gameboard[i][col] = 'o'
                            print(f"AI chooses column {col + 1}")
                            return
    
    except Exception as e:
        print(f"Error getting AI move: {e}")
        import traceback
        traceback.print_exc()
        # Fallback: find first available column
        for col in range(7):
            if gameboard[0][col] == ' ':
                for i in range(5, -1, -1):
                    if gameboard[i][col] == ' ':
                        gameboard[i][col] = 'o'
                        print(f"AI chooses column {col + 1} (fallback)")
                        return


def startgame(gameboard):
    """Start the game loop - Human (x) vs AI (o)"""
    print("\n" + "=" * 50)
    print("  Welcome to Connect 4!")
    print("  You are 'x', AI is 'o'")
    print("=" * 50)
    
    win = False
    turn = 0
    
    while not win:
        # Human player's turn
        fancy_gameboard(gameboard)
        makeamove(gameboard, 'x')
        win = checkwin(gameboard)
        
        if win:
            fancy_gameboard(gameboard)
            print("🎉 You win!")
            break
        
        # Check for draw
        if all(gameboard[0][col] != ' ' for col in range(7)):
            fancy_gameboard(gameboard)
            print("🤝 It's a draw!")
            break
        
        # AI player's turn
        fancy_gameboard(gameboard)
        make_ai_move(gameboard)
        win = checkwin(gameboard)
        
        if win:
            fancy_gameboard(gameboard)
            print("🤖 AI wins!")
            break
        
        # Check for draw
        if all(gameboard[0][col] != ' ' for col in range(7)):
            fancy_gameboard(gameboard)
            print("🤝 It's a draw!")
            break
        
        turn += 1


if __name__ == "__main__":
    try:
        startgame(gameboard)
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

