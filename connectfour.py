class ConnectGame:

    def __init__(self, rows, columns, p1, p2):
        self.array = [[0 for i in range(columns)] for j in range(rows)]
        self.rows = rows
        self.columns = columns
        self.players = [p1, p2]
        self.x = 0
        self.y = 0
        self.turn = 0
        self.tops = [0] * columns
        self.leftovers = 0
        self.new = False
        self.messages = [[], [], [], []]
        self.won = False
        self.issmall = False
        # [[rowchannelid], [rowids], [reactorchannelid reactorid], [infochannelid, infoid]]


    def sendstart(self):
        pass

    def formatrow(self, rowsleft):
        message = str(self.array)[2:-2]
        message = message.replace(" ", "").replace(",", "").split("][")
        #print(message)
        if rowsleft >= 3:
            upperrow = rowsleft-1
            lowerrow = upperrow-2
        else:
            upperrow = rowsleft-1
            lowerrow = 0
        themessage = " "
        for bruh in range(upperrow-lowerrow+1):
            if self.issmall:
                themessage = "| "+message[lowerrow+bruh]+"|"+themessage
            else:
                themessage = message[lowerrow+bruh]+themessage
            if not bruh == upperrow-lowerrow:
                themessage = "\n" + themessage
        themessage = themessage.replace("0", "🔳 ").replace("1", "🔴 ").replace("2", "🔵 ").replace("3", "❔ ")

        return themessage

    def checkforwin(self):
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]  # -> <- | | / / \ \
        distances = [0, 0, 0, 0]  # - | / \
        for direction in directions:
            try:
                for distance in range(3):
                    newy = self.y+(distance+1)*direction[1]
                    newx = self.x+(distance+1)*direction[0]
                    if newx >= 0 and newy >= 0:
                        if self.array[newy][newx] == self.turn+1:
                            distances[round(directions.index(direction)/2-.1)] += 1
                        else:
                            break
                    else:
                        break
            except IndexError:
                # print(f"indexerror at direction {direction}")
                pass
            if 3 in distances:
                print(distances)
                return True
        print(distances)
        return False

    def jsonify(self):
        return [self.rows, self.columns, self.players, self.x, self.y, self.turn, self.tops, self.leftovers, self.new, self.messages, self.array, self.won, self.issmall]
