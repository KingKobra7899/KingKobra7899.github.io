import pandas as pd
import pandas as pd

class DraftSimulator:
    def __init__(self, path, num_teams, num_rounds):
        self.data = pd.read_csv(path)
        self.num_teams = num_teams
        self.teams = [[] for _ in range(num_teams)]
        for i in range(num_teams):
            self.teams[i] = []
        self.teamId = int(input("Which team am I drafting for? \n")) - 1
        self.num_rounds = num_rounds
        
        self.QB_slots = 1
        self.RB_slots = 2
        self.WR_slots = 3
        self.TE_slots = 1
        self.flex = 1
        self.bench = 6
        
        self.QB_drafted = 0
        self.RB_drafted = 0
        self.WR_drafted = 0
        self.TE_drafted = 0
        self.flex_drafted = 0

sim = DraftSimulator("big_board.csv", 10)