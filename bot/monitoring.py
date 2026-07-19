""" 
This class is an attempt to resolve a potential global values issue
"""

class MonitoringState:

    def __self__(self):
        self.in_game = False
        self.last_event_id = -1
        

    def start_game(self):
        self.in_game =True
        