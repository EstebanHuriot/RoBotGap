""" 
This class stores the state of the live game monitoring system.

This state is kept between monitoring loop iterations to track wether a game is currently active.
"""

class MonitoringState:

    def __init__(self):
        self.in_game = False
        self.last_event_id = -1
        self.events = []
        

    def start_game(self):
        self.in_game = True
        
    
    def end_game(self):
        self.in_game = False

    def reset(self):
        self.in_game = False
        self.last_event_id = -1
        self.events.clear()