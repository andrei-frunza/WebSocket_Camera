import asyncio
import websockets
import numpy as np
import cv2

#Defining how the server will handle receiving the data
async def server(websocket):
    async for message in websocket:
        print("received data from the client")

        try:
            #decoding the data we recived from the client
            im = np.frombuffer(message, np.uint8)
            image = cv2.imdecode(im,cv2.IMREAD_COLOR)
            #saving the image in the folder
            print("saving image as 'result.jpg'")
            cv2.imwrite("result.jpg",image)
            #creating a cv2 frame and showing the image just received
            cv2.namedWindow("frame")
            cv2.imshow("frame",image)
            await websocket.send("Image transfer succesful!")
            #waiting for the user to enter any key to kill the image window
            print("press any key to close image window")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except:
            print("Message is not an image, or formatted incorrectly")
            await websocket.send("Image transfer was NOT successful")
            
    

#serving the server on localhost port 8000 and looping it forever
async def main():
    print("Starting WebSocket Server...")
    async with websockets.serve(server,"localhost",8000):
        print("Server started!")
        await asyncio.Future()

asyncio.run(main())