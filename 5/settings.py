

class Settings:
    COUNTDOWN_STATUS='countdown'
    ASK_STATUS='ask'
    GAME_STATUS='game'
    SHOW_WINNER_STATUS = 'show_winner_status'

    def __init__(self, debug=False) -> None:
        self.bg_color = (74, 240, 154)

        self.status=""    
        self.debug = debug
        self.button_color = (2, 163, 88)