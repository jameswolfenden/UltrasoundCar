import matplotlib.pyplot as plt
import numpy as np
import csv
import asyncio
import websockets



resultData = []



#fig, ax = plt.subplots()
#plt.show()

def on_message(wsapp, message):
    print(message)
    if message == "stop":
        wsapp.close()
    newResults = float(message.split(','))
    resultData.append(newResults)
    dataArray = np.array(resultData).astype("float")
    #im = ax.pcolormesh(range(90, -91, -10), range(1,dataArray.shape[0]+1,1),  dataArray, cmap="Greys_r", vmax = 250, vmin = 0)
    #plt.colorbar(im)



async def hello():
    async with websockets.connect("ws://192.168.4.1:8765") as websocket:
        await websocket.send("Hello world!Hello world!  Hello world! Hello world! Hello world! Hello world! Hello world! Hello world! Hello world! Hello world! Hello world! ")
        result = await websocket.recv()
        print(result)

asyncio.run(hello())




#wsapp = websocket.WebSocketApp("ws://192.168.4.1:8765", on_message=on_message)
#wsapp.run_forever() 






