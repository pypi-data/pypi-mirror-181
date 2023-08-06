import cv2
import matplotlib.pyplot as plt
import numpy as np




squaresX = 5
squaresY = 7
squareLength = 60
markerLength = 30
dictionaryId = '6x6_250'
margins = squareLength - markerLength
borderBits = 1

imageSize = [squaresY, squaresX] * squareLength + 2 * margins

dictionary = {'Predefined', dictionaryId};
board = {squaresX, squaresY, squareLength, markerLength, dictionary}

boardImage = cv2.drawCharucoBoard(board, fliplr(imageSize), 'MarginSize',margins, 'BorderBits',borderBits)
imshow(boardImage), title('CharucoBoard')

plt.imshow(boardImage)
plt.show()
