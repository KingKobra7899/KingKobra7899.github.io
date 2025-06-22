import pandas as pd


class DraftSimulator:
    def __init__(self, path, num_teams, num_rounds):
        self.data = pd.read_csv(path)
        self.original_data = self.data.copy()

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
        self.bench_drafted = 0
        
        self.current_pick = 1
        self.current_round = 1

    def getAvailablePlayers(self):
        return self.data["player_display_name"].to_list()

    def getTeamPicking(self):
        return (self.current_pick - 1) % self.num_teams if ((self.current_pick - 1) // self.num_teams) % 2 == 0 else self.num_teams - 1 - ((self.current_pick - 1) % self.num_teams)

    def makePick(self, pick):
        team_making_pick = self.getTeamPicking()

        player_in_tracked_data = False
        player_data_row = self.data[self.data["player_display_name"] == pick]

        if not player_data_row.empty:
            player_in_tracked_data = True
            player_pos = player_data_row["position_group"].iloc[0]
            
            self.data = self.data[self.data["player_display_name"] != pick]

            if team_making_pick == self.teamId:
                if player_pos == "QB":
                    if self.QB_drafted < self.QB_slots:
                        self.QB_drafted += 1
                    else:
                        self.bench_drafted += 1
                elif player_pos == "RB":
                    if self.RB_drafted < self.RB_slots:
                        self.RB_drafted += 1
                    elif self.flex_drafted < self.flex:
                        self.flex_drafted += 1
                    else:
                        self.bench_drafted += 1
                elif player_pos == "WR":
                    if self.WR_drafted < self.WR_slots:
                        self.WR_drafted += 1
                    elif self.flex_drafted < self.flex:
                        self.flex_drafted += 1
                    else:
                        self.bench_drafted += 1
                elif player_pos == "TE":
                    if self.TE_drafted < self.TE_slots:
                        self.TE_drafted += 1
                    elif self.flex_drafted < self.flex:
                        self.flex_drafted += 1
                    else:
                        self.bench_drafted += 1

        self.teams[team_making_pick].append(pick)

        self.current_pick += 1
        if (self.current_pick - 1) % self.num_teams == 0 and self.current_pick > 1:
            self.current_round += 1

    def choosePlayer(self):
        sorted_players = self.data.sort_values(by="draft_value", ascending=False)
        
        current_id = 0
        while True:
            if current_id >= len(sorted_players):
                return None
            
            top_player = sorted_players.iloc[current_id]
            top_pos = top_player["position_group"]
            
            if top_pos == "TE":
                if(self.TE_drafted == 0):
                    return top_player["player_display_name"]
                else:
                    if(self.RB_drafted >= self.TE_drafted and self.WR_drafted >= self.TE_drafted and self.QB_drafted >= self.TE_drafted):
                        return top_player["player_display_name"]
                    else:
                        current_id+=1
            elif top_pos == "RB":
                if(self.RB_drafted == 0):
                    return top_player["player_display_name"]
                else:
                    if(self.TE_drafted >= self.RB_drafted and self.WR_drafted >= self.RB_drafted and self.QB_drafted >= self.RB_drafted):
                        return top_player["player_display_name"]
                    else:
                        current_id+=1
            elif top_pos == "WR":
                if(self.WR_drafted == 0):
                    return top_player["player_display_name"]
                else:
                    if(self.TE_drafted >= self.WR_drafted and self.RB_drafted >= self.WR_drafted and self.QB_drafted >= self.WR_drafted):
                        return top_player["player_display_name"]
                    else:
                        current_id+=1
            elif top_pos == "QB":
                if(self.QB_drafted == 0):
                    return top_player["player_display_name"]
                else:
                    if(self.TE_drafted >= self.QB_drafted and self.RB_drafted >= self.QB_drafted and self.WR_drafted >= self.QB_drafted):
                        return top_player["player_display_name"]
                    else:
                        current_id+=1
            else:
                current_id += 1

    def draft(self):
        while self.current_round <= self.num_rounds:
            current_team = self.getTeamPicking()
            print(f"\n--- Round {self.current_round}, Pick {self.current_pick} (Team {current_team + 1}) ---")

            if current_team == self.teamId:
                recommended_player = self.choosePlayer()
                recommendation_text = f"I recommend drafting {recommended_player}." if recommended_player else "I have no specific recommendation from the remaining offensive players."
                choice = input(f"{recommendation_text} Please choose your pick: ")
                self.makePick(choice)
            else:
                choice = input(f"please type Team {current_team + 1}'s pick: ")
                self.makePick(choice)
        
        print(f"\nThis is your team: \n")
        self.print_my_team()

    def print_my_team(self):
        print("Your Roster:")
        my_roster_names = self.teams[self.teamId]

        qbs = []
        rbs = []
        wrs = []
        tes = []
        flex_candidates = []
        bench_and_untracked = []

        assigned_to_primary_slot = set()

        for player_name in my_roster_names:
            player_info = self.original_data[self.original_data["player_display_name"] == player_name]

            if not player_info.empty:
                pos = player_info["position_group"].iloc[0]

                if pos == "QB" and len(qbs) < self.QB_slots:
                    qbs.append(player_name)
                    assigned_to_primary_slot.add(player_name)
                elif pos == "RB" and len(rbs) < self.RB_slots:
                    rbs.append(player_name)
                    assigned_to_primary_slot.add(player_name)
                elif pos == "WR" and len(wrs) < self.WR_slots:
                    wrs.append(player_name)
                    assigned_to_primary_slot.add(player_name)
                elif pos == "TE" and len(tes) < self.TE_slots:
                    tes.append(player_name)
                    assigned_to_primary_slot.add(player_name)
                else:
                    flex_candidates.append((player_name, pos))
            else:
                bench_and_untracked.append(player_name + " (Untracked/Non-Offensive)")
                assigned_to_primary_slot.add(player_name)

        flex_player_name = None
        if self.flex > 0:
            for name, pos in flex_candidates:
                if name not in assigned_to_primary_slot and pos in ["RB", "WR", "TE"]:
                    flex_player_name = name
                    assigned_to_primary_slot.add(name)
                    break

        for player_name in my_roster_names:
            if player_name not in assigned_to_primary_slot:
                bench_and_untracked.append(player_name)

        print(f"QB: {', '.join(qbs) if qbs else 'None'}")
        print(f"RB: {', '.join(rbs) if rbs else 'None'}")
        print(f"WR: {', '.join(wrs) if wrs else 'None'}")
        print(f"TE: {', '.join(tes) if tes else 'None'}")
        print(f"FLEX: {flex_player_name if flex_player_name else 'None'}")
        print(f"BENCH ({len(bench_and_untracked)} players): {', '.join(bench_and_untracked) if bench_and_untracked else 'None'}")
        

        

        



        
            


        
    

sim = DraftSimulator("big_board.csv", 14)