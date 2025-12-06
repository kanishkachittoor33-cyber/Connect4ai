# Connect 4 Game with AI

A Python implementation of Connect 4 with AI support using BAML (BoundaryML).

## Features

- **PvP Mode**: Player vs Player - Two human players take turns
- **AVA Mode**: AI vs AI - Watch two AIs play against each other
- **PVA Mode**: Player vs AI - Play against an AI opponent

## Prerequisites

1. Python 3.7 or higher
2. Install required packages:
   ```bash
   pip install baml-py==0.214.0 python-dotenv
   ```
3. Required API key for Grok (used in the BAML function): `OPENROUTER_API_KEY`

## Setup

1. Make sure you have the BAML client generated:
   ```bash
   baml-cli generate
   ```

2. Create a `.env` file in the project root with your API key:
   ```bash
   echo "OPENROUTER_API_KEY=your-api-key-here" > .env
   ```
   
   Or manually create a `.env` file with:
   ```
   OPENROUTER_API_KEY=your-api-key-here
   ```

3. Run the game:
   ```bash
   python connect4_game.py
   ```
   
   **Note**: The game will automatically load environment variables from the `.env` file using `python-dotenv`.

## How to Play

1. When you start the game, choose your game mode:
   - Enter `1` for PvP (Player vs Player)
   - Enter `2` for AVA (AI vs AI)
   - Enter `3` for PVA (Player vs AI)

2. For human players:
   - Enter a column number (0-6) when prompted
   - Pieces fall to the lowest available space in that column

3. For AI players:
   - The AI will automatically choose a strategic move
   - The AI uses the `GetAIMove` BAML function for decision-making

4. Win condition:
   - Connect 4 pieces horizontally, vertically, or diagonally
   - The game ends when someone wins or the board is full (draw)

## Game Board

The board is displayed as:
- Empty cells: `  ` (two spaces)
- Player 1: `p1`
- Player 2: `p2`
- AI 1: `a1`
- AI 2: `a2`

## Example Game Flow

```
Choose game mode:
  1. PvP - Player vs Player
  2. AVA - AI vs AI
  3. PVA - Player vs AI

Enter your choice (1-3): 3

==================================================
  Starting Connect 4 - Mode: PVA
==================================================

  0   1   2   3   4   5   6
  ---------------------------
  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |
  ---------------------------
  0   1   2   3   4   5   6

Player p1, enter column (0-6): 3
...
```

## Troubleshooting

- **Import errors**: Make sure you've run `baml-cli generate` to generate the BAML client
- **API errors**: Check that your `OPENROUTER_API_KEY` environment variable is set correctly
- **Invalid moves**: The game will prompt you again if you enter an invalid column

## Notes

- The AI uses strategic thinking to block opponents, create winning opportunities, and prefer center columns
- The game validates all moves and prevents invalid column selections
- The board is 6 rows × 7 columns (standard Connect 4 size)

