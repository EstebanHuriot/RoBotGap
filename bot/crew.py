""" 
CrewMember represents a player's identity. 
Crew manages the group and its members.
"""


class CrewMember:


    def __init__(self, pseudo:str, tagline:str, puuid=None):
        self.pseudo = pseudo
        self.tagline = tagline
        self.puuid = puuid
        self.full = f"{pseudo.strip()}#{tagline.strip()}".lower()


class Crew:


    def __init__(self):
        self.crewMembers = []

    def add(self, crewmember:CrewMember):
        y = crewmember.full

        x = [member.full for member in self.crewMembers]

        if y not in x:
            self.crewMembers.append(crewmember)
            print(f"Crew member added: {crewmember.pseudo}")
            return True

        else:
            print("Crew member already in")
            return False

    def remove(self, crewmember:CrewMember):
        
        for index, member in enumerate(self.crewMembers):
            if member.full == crewmember.full:
                self.crewMembers.pop(index)
                print(f"Ciao {member.pseudo}")
                return True

        print('Crew member not found')
        return False


    def reset(self):
        self.crewMembers.clear()
        print("Cleared crew")


    def show(self):
        return [member.pseudo for member in self.crewMembers]
    

    def find(self, crewmember:CrewMember):
        y = crewmember.full

        x = [member.full for member in self.crewMembers]

        if y in x:
            return f"{crewmember.pseudo} is in there"

        else:
            return f"{crewmember.pseudo} is not here"