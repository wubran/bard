class ConnectGame:

    def __init__(self, rows, columns):
        self.array = [[0 for i in range(rows)] for j in range(columns)]
        self.whos_turn = "idk lol"

    def formatrow(self, rowsleft):
        message = str(self.array)[2:-2]
        message = message.replace(" ", "").replace(",", "").split("][")
        if rowsleft >= 3:
            upperrow = rowsleft-1
            lowerrow = upperrow-2
        else:
            upperrow = rowsleft-1
            lowerrow = 0
        themessage = ""
        for bruh in range(upperrow-lowerrow+1):
            themessage = message[lowerrow+bruh]+themessage
            if not bruh == upperrow-lowerrow:
                themessage = "\n" + themessage
        themessage = themessage.replace("0", "🔳 ").replace("1", "🔴 ").replace("2", "🔵 ").replace("3", "❔ ")
        return themessage

    def checkforwin(self, x, y, turn):  # turn is either 1 or 2 for checking pieces (its your piece)
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]  # -> <- | | / / \ \
        distances = [0, 0, 0, 0]  # - | / \
        for direction in directions:
            try:
                for distance in range(3):
                    if self.array[y+(distance+1)*direction[1]][x+(distance+1)*direction[0]] == turn:
                        distances[round(directions.index(direction)/2-.1)] += 1
                    else:
                        break
            except IndexError:
                print(f"indexerror at direction {direction}")
            if 3 in distances:
                return True
        print(distances)
        return False