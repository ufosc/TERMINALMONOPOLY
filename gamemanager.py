import screenspace as ss
class Game:
    def __init__(self, name: str, players: list, board: str, other_data):
        self.name = name
        self.id = None
        self.players = players # list of Client objects
        self.board = board
        self.other_data = other_data
        self.gamestate = ''
        self.MAXPLAYERS = 0

    def __str__(self):
        return f"[N:{self.name} | ID:{self.id} | P:{[player.name for player in self.players]}]"
    
    def __repr__(self):
        return self.__str__()
games = []

def add_game(g: Game) -> None:
    g.id = len(games)
    games.append(g)

def add_player_to_game(game_id: int, player) -> None:
    """
    Adds a player to a game.
    
    Parameters:
    game_id: int - The id of the game to add the player to.
    player: Client - The player to add to the game.
    
    Raises:
    ValueError - If the player is already in the game.
    
    Returns:
    None
    """
    if not player in games[game_id].players:
        games[game_id].players.append(player)
    else: raise ValueError('Player already in game.')

def remove_game(game_id: int) -> None:
    """
    Removes a game from the game manager by its ID.

    This function searches for a game with the given ID in the list of active games
    and removes it if found.

    Args:
        game_id (int): The unique identifier of the game to be removed.

    Returns:
        None
    """
    games.pop(game_id) # intentional choice to keep all other game ids the same

def is_game_full(game_id: int):
    """
    Checks whether a game has reached its maximum number of players.

    This function retrieves a game by its ID and determines if the number of 
    players has reached the game's defined limit.

    Args:
        game_id (int): The unique identifier of the game.

    Returns:
        bool: True if the game is full, False otherwise.
    """
    if None in games[game_id].players:
        return False
    return len(games[game_id].players) >= games[game_id].MAXPLAYERS

def game_exists(game_name: str) -> bool:
    """
    Checks if a game with the specified name exists in the game manager.

    This function iterates through the list of active games and determines
    if a game with the given name is currently available.

    Args:
        game_name (str): The name of the game to check.

    Returns:
        bool: True if the game exists, False otherwise.
    """
    for game in games:
        if game.name == game_name:
            return True
    return False

def player_in_game(game_name: str, player: str) -> bool:
    """
    Determines whether a specific player is currently in a game.

    This function searches for a game with the given name and checks if the player 
    is listed among its participants.

    Args:
        game_name (str): The name of the game.
        player_name (str): The name of the player to check.

    Returns:
        bool: True if the player is in the specified game, False otherwise.
    """
    for game in games:
        if game.name == game_name and player in [player.name for player in game.players]:
            return True
    return False

def get_game_by_id(game_id: int) -> Game:
    """
    Returns the game object with the given id.
    
    Parameters:
    game_id: int - The id of the game to return.

    Returns:
    Game - The game object with the given id.
    If the id is out of range, returns None.
    """
    try:
        return games[game_id]
    except IndexError:
        return None

def get_game_by_name(game_name: str) -> list:
    """
    Returns a list of game objects with the given name.
    Made into a function to support type hints.
    """
    return [game for game in games if game.name == game_name]

def display_games(id: int = -1, name:str = '', player_name: str= '', page:int = 0) -> str:
    """
    Returns a string of all games and their players.

    Parameters:
    id: int - Filter games by id (shows one game).
    name: str - Filter games by this name.
    player_name: str - Filter games by a specific player name.
    page: int - The page of games to display.

    Returns:
    str - The string of games to display.
    """
    ret_val = 'List of Games\n'
    ret_val += f'Page {page}\n'
    for game in games:
        if id != -1 and game.id != id:
            continue
        if name != '' and game.name != name:
            continue
        if player_name != '' and player_name not in [player.name for player in game.players]:
            continue
        game_info = f'{game.id}: {game.name}: {[player.name for player in game.players]}'
        while len(game_info) > ss.cols:
            ret_val += game_info[:ss.cols] + '\n'
            game_info = game_info[ss.cols:]
        ret_val += game_info.ljust(ss.cols) + '\n'

    ret_val += 'PAD ME PLEASE!' # need to pad juuust in case

    start_index = page * ss.rows * ss.cols
    end_index = start_index + ss.rows * ss.cols
    return ret_val[start_index:end_index]