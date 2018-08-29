import numpy as np
import cv2

# source: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret==True:
    	frame = cv2.flip(frame, 0)
    	
    	out.write(frame)
		
		cv2.imshow('frame', frame)
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else:
		break

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    #cv2.imshow('frame',frame)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
     #   break

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
