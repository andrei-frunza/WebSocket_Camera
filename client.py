#The client side takes a picture from a webcam and sends it to the server
#through WebSockets

import asyncio
import websockets
import cv2
import numpy as np

#The websocket connection and sending of the image
async def imageSend(data):
    try:
        async with websockets.connect("ws://localhost:8000") as ws:
            print("sending the image to the server...")
            await ws.send(data)
            print("Image was sent")
            print("Awaiting confirmation from the server...")
            result = await ws.recv()
            print("Server says: ",result)
    except:
        print("There was an error when attempting to connect to the server...")
        print("Please check server and try again")

#Defining the capture object for the camera
vid = cv2.VideoCapture(0)

#Use the video loop from https://www.geeksforgeeks.org/python-opencv-capture-video-from-camera/ 
#as a "view finder". Have the 'c' key "take the picture" and present it to the user. The user
#can then confirm if they want to send that picture to the server, or they can take the image 
#again.
while(True):
      
    ret, frame = vid.read()
    #Creating the Keybind Panel in the top left of the webcam image
    cv2.rectangle(frame,(0,0),(155,65),(255,255,255),cv2.FILLED)
    cv2.putText(frame,"Keybinds:",(0,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,cv2.FILLED)
    cv2.putText(frame,"C - capture image",(0,35),cv2.FONT_HERSHEY_SIMPLEX,0.5,cv2.FILLED)
    cv2.putText(frame,"Q - quit capture",(0,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,cv2.FILLED)
  
    cv2.imshow('frame', frame)
    
    #The 'c' button is set as the 'capture'
    #which will stop the recording on the current frame,
    #and ask if it should be sent to the server.
    if cv2.waitKey(1) & 0xFF == ord('c'):
        ret, clean_image = vid.read()
        #print the same question and prompt to the console just in case
        print("Would you like to send this image to the server? (y/n)")
        #The putText functions place text on the screen that ask the user if they would like to send
        #the current frame to the server
        cv2.rectangle(frame,(0,0),(155,65),(255,255,255),cv2.FILLED)
        cv2.putText(frame,"Send this image",(0,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,cv2.FILLED)
        cv2.putText(frame,"to the server?",(0,35),cv2.FONT_HERSHEY_SIMPLEX,0.5,cv2.FILLED)
        cv2.putText(frame,"(y/n)",(0,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,cv2.FILLED)
        while(True):
            cv2.imshow('frame', frame)
            #if yes, the frame will be sent to the server over the websocket connection and wait for 
            #confirmation from the server
            if cv2.waitKey(1) & 0xFF == ord('y'):
                #Encoding the image 
                img_encode = cv2.imencode('.jpg',clean_image)[1]
                #Converting the image into an array
                data_encode = np.array(img_encode)
                #calling the websocket connect and send funciton
                asyncio.run(imageSend(data_encode.tobytes()))
                break

            #If 'no' this infinite loop breaks, and the regular function of the first loop begins again
            if cv2.waitKey(1) & 0xFF == ord('n'):
                break
    #If the user hits the 'q' key during regular function of the 'view finder',
    #it exits and terminates the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the capture object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
