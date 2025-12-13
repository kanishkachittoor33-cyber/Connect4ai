// Connect 4 Game State
class GameState {
  // 2D array representing the board (6 rows × 7 columns)
  // Each cell can be: "  " (empty, two spaces), "p1" (player 1), "p2" (player 2), "a1" (AI 1), or "a2" (AI 2)
  board string[][]
  // Indicates whose turn it is: "p1", "p2", "a1", or "a2"
  currentPlayer string
}

// AI Move Output
class AIMove {
  // Column number where AI should place its piece (0-6)
  column int @description("The column number where the AI should place its piece, must be between 0 and 6")
}

// Function to get AI's strategic move in Connect 4
function GetAIMove(gameState: GameState) -> AIMove {
  client AmazonNova2LiteOpenRouter
  prompt #"
    {{ _.role("user")}}

    You are playing Connect 4. The game is played on a 6-row by 7-column board.
    Players take turns dropping pieces into columns. Pieces fall to the lowest available space in the chosen column.
    The goal is to connect 4 pieces horizontally, vertically, or diagonally.

    Piece types:
    - "p1" = Player 1
    - "p2" = Player 2
    - "a1" = AI 1
    - "a2" = AI 2
    - "  " = Empty cell (two spaces)

    Current board state:
    {{ gameState.board }}

    Current player: {{ gameState.currentPlayer }}

    Your pieces on the board are marked as "{{ gameState.currentPlayer }}". All other pieces (p1, p2, a1, a2 that are not "{{ gameState.currentPlayer }}") are your opponents.

    Analyze the board and choose the best strategic move. Consider:
    1. Block opponents if they are about to win (have 3 in a row)
    2. Create your own winning opportunity if you have 3 in a row
    3. Prefer center columns (columns 2, 3, 4) as they offer more winning opportunities
    4. Block opponents from creating threats
    5. Build your own threats when possible

    Return the column number (0-6) where you should place your piece. The column must be a valid integer between 0 and 6 (inclusive).

    {{ ctx.output_format }}
  "#
}

// Test cases for GetAIMove function
test empty_board {
  functions [GetAIMove]
  args {
    gameState {
      board [
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "]
      ]
      currentPlayer "a1"
    }
  }
}
test horizontal_win_right {
  functions [GetAIMove]
  args {
    gameState {
      board [
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "p1", "p1", "  ", "  "],
        ["  ", "  ", "p1", "a1", "a1", "a1", "  "]
      ]
      currentPlayer "a1"
    }
  }
  @@assert( {{ this.column ==  6 }})
}
test horizontal_win_left {
  functions [GetAIMove]
  args {
    gameState {
      board [
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "p1", "p1", "a1", "  "],
        ["  ", "  ", "  ", "a1", "a1", "a1", "p1"]
      ]
      currentPlayer "a1"
    }
  }
  @@assert( {{ this.column ==  2 }})
}
test horizontal_win_vertical {
  functions [GetAIMove]
  args {
    gameState {
      board [
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "a1", "p1", "  ", "  ", "  "],
        ["  ", "  ", "a1", "p1", "  ", "  ", "  "],
        ["  ", "  ", "a1", "p1", "p1", "  ", "  "],
        ["  ", "  ", "p1", "a1", "a1", "a1", "p1"]
      ]
      currentPlayer "p1"
    }
  }
  @@assert( {{ this.column ==  3 }})
}
test diagonally_win_right {
  functions [GetAIMove]
  args {
    gameState {
      board [
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "p1", "a1", "  "],
        ["  ", "  ", "  ", "p1", "p1", "p1", "  "],
        ["  ", "  ", "p1", "a1", "a1", "a1", "p1"]
      ]
      currentPlayer "p1"
    }
  }
  @@assert( {{ this.column ==  5 }})
}
test diagonally_win_left {
  functions [GetAIMove]
  args {
    gameState {
      board [
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["a1", "a1", "  ", "  ", "  ", "  ", "  "],
        ["p1", "p1", "a1", "p1", "p1", "  ", "  "],
        ["a1", "p1", "p1", "a1", "a1", "a1", "p1"]
      ]
      currentPlayer "a1"
    }
  }
  @@assert( {{ this.column ==  0}})
}

test blocking_move {
  functions [GetAIMove]
  args {
    gameState {
      board [
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "p1", "p1", "  ", "  "],
        ["  ", "  ", "p1", "a1", "a1", "a1", "  "]
      ]
      currentPlayer "p1"
    }
  }
  @@assert( {{ this.column ==  6 }})
}

