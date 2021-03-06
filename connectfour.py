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
