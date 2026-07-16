""" 
Responsabilité du Crew

Le Crew devrait savoir :

quels joueurs il contient ;
comment ajouter ou retirer un joueur ;
comment vérifier si un joueur appartient au crew ;
comment retrouver les membres présents dans allPlayers.


"""


class CrewMember:

    def __init__(self, pseudo, tagline, puuid=None):
        self.pseudo = pseudo
        self.tagline = tagline
        self.puuid = puuid


class Crew:

    def __init__(self):
        self.crewMembers = []

    def add(self, crewmember:CrewMember):
        self.crewMembers.append(crewmember)