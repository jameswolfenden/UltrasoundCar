import matplotlib.pyplot as plt
import numpy as np
import csv
import asyncio
import websockets
import websocket



resultData = []



# fig, ax = plt.subplots()
# im = ax.pcolormesh(range(90, -91, -10), np.ones(2),  np.ones(19), cmap="Greys_r", vmax = 250, vmin = 0) #idk somehow make empty graph
# plt.colorbar(im)

# plt.ion()
# plt.show()
# plt.pause(1)


async def hello():
    async with websockets.connect("ws://192.168.4.1:8765") as websocket:
        #await websocket.send("Hello world!Hello world!  Hello world! Hello world! Hello world! Hello world! Hello world! Hello world! Hello world! Hello world! Hello world! ")
        resultsTotal = []
        resultsTemp = []
        while True:
            result = await websocket.recv()
            if result == "stop":
                break
            if result == "[":
                resultsTemp = []
            elif result == "]":
                resultsTotal.append(resultsTemp)
                dataArray = np.array(resultsTotal).astype("float")
                print(dataArray)
                # im = ax.pcolormesh(range(90, -91, -10), range(1,dataArray.shape[0]+1,1),  dataArray, cmap="Greys_r", vmax = 250, vmin = 0)
                # plt.draw()
                # plt.pause(0.1)
            else:
                resultsTemp.append(float(result))

asyncio.run(hello())






