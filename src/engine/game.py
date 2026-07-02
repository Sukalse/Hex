import json

class Tile:
    def __init__(self, color: bool):
        self.color = color

class Game:
    def __init__(self) -> None:
        self.grid: dict[tuple[int, int], Tile | None] = {}

        self.add_tile(0,0,True)

    def add_tile(self, x: int, y: int, color: bool):
        self.grid[(x, y)] = Tile(color)

    def get_tile(self, x: int, y: int) -> Tile | None:
        return self.grid.get((x, y), None)
    
    def get_grid(self) -> dict[tuple[int, int], Tile | None]:
        return self.grid
    
    def export_grid(self) -> str:
        # export the grid as a JSON string
        export_dict = {}
        for (x, y), tile in self.grid.items():
            if tile is not None:
                export_dict[f"{x},{y}"] = tile.color
        return json.dumps(export_dict)

    def apply_moves(self, color: bool, last_move1: tuple[int, int], last_move2: tuple[int, int]) -> bool | None:
        self.add_tile(last_move1[0], last_move1[1], color)
        self.add_tile(last_move2[0], last_move2[1], color)
        
        directions = [
            (1, 0),  # Horizontal
            (0, 1),  # Top-left to bottom-right diagonal
            (1, 1)  # Top-right to bottom-left diagonal
        ]
        for direction in directions:
            for tile in [last_move1, last_move2]:
                count = 1
                for step in range(1, 6):
                    next_tile = (tile[0] + direction[0] * step, tile[1] + direction[1] * step)
                    if self.get_tile(next_tile[0], next_tile[1]) and self.get_tile(next_tile[0], next_tile[1]).color == color:
                        count += 1
                    else:
                        break
                for step in range(1, 6):
                    prev_tile = (tile[0] - direction[0] * step, tile[1] - direction[1] * step)
                    if self.get_tile(prev_tile[0], prev_tile[1]) and self.get_tile(prev_tile[0], prev_tile[1]).color == color:
                        count += 1
                    else:
                        break
                if count >= 6:
                    return color
        return None
