import random


class Game:
    def __init__(self, lobbyQueue, gameID):
        self.__lobbyQueue = lobbyQueue
        self.__gameID = gameID
        self.__playerList = []
        self.__captainsList = []

        # adds players to the game lobby. Will cap at 10 to a game, but allows for smaller lobbies to exist.
        for player in lobbyQueue:
            self.__playerList.append(player)
            if len(self.__playerList) > 9:
                break

        self.__captainsList = self.pickCaptains()

    def getID(self):
        return self.__gameID

    def getPlayerList(self):
        return self.__playerList

    def returnCaptains(self):
        return self.__captainsList

    # returns two random players from the game lobby
    def pickCaptains(self):
        captainList = []
        try:
            indexList = random.sample(range(0, len(self.__playerList)), 2)
            for i in indexList:
                captainList.append(self.__playerList[i])
        except ValueError:
            print('Not enough players to gen captains')

        return captainList
