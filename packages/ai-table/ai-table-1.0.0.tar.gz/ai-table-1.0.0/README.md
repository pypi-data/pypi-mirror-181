## AI-TABLE
"ai-table" is a new Shape Matching technology.

### Installation
```
pip install ai-table
```
### About "ai-table"
Shape recognition is an intrinsic property of the human intellect. Kids aged 2-2.5 years old can recognize shapes even if they differ in size, position, orientation, or are severely deformed. 

![demo image](https://boriskravtsov.com/images/shapes.png)

To simulate such recognition capability, we introduce the MATCHSHAPES library and its only one function match(), which calculates the similarity of two compared shapes:

                                    similarity = match(shape_1, shape_1)

Here the shape is a grayscale contour image whose maximum dimension is not more than 100 pixels. 
In general, compared shapes may differ in size. The similarity value ranges from 0 to 1.0 (complete identity). 
The calculation time is about 7-9 seconds(!)

Our website demonstrates the effectiveness of the MATCHSHAPES technology on a large amount of data.


### How to use:
```Python
import cv2 as cv
import time
import matchshapes as ms

shape_1 = cv.imread(path_1, cv.IMREAD_GRAYSCALE)
shape_2 = cv.imread(path_2, cv.IMREAD_GRAYSCALE)

print(f'\nWait...')

timer_start = time.time()

similarity = ms.match(shape_1, shape_2)

seconds = time.time() - timer_start

if similarity < 0:
    print(f'\nERROR: Incorrect shape format')
else:
    print(f'\nSimilarity = {round(similarity, 5)}\n\nTime = {round(seconds, 1)} sec')
```
