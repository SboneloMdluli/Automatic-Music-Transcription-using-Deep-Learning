import numpy as np
from predictor import pred,load_image
import glob, os

piano = {1 : 'A0',
         2 : 'A#0',
         3 : 'B0',
         4 : 'C1',
         5 : 'C#1',
         6 : 'D1',
         7 : 'D#1',
         8 : 'E1',
         9 : 'F1',
         10 : 'F#1',
         11 : 'G1',
         12 : 'G#1',
         13 : 'A1',
         14 : 'A#1',
         15 : 'B1',
         16 : 'C2',
         17 : 'C#2',
         18 : 'D2',
         19 : 'D#2',
         20 : 'E2',
         21 : 'F2',
         22 : 'F#2',
         23 : 'G2',
         24 : 'G#2',
         25 : 'A2',
         26 : 'A#2',
         27 : 'B2',
         28 : 'C3',
         29 : 'C#3',
         30 : 'D3',
         31 : 'D#3',
         32 : 'E3',
         33 : 'F3',
         34 : 'F#3',
         35 : 'G3',
         36 : 'G#3',
         37 : 'A3',
         38 : 'A#3',
         39 : 'B3',
         40 : 'C4',
         41 : 'C#4',
         42 : 'D4',
         43 : 'D#4',
         44 : 'E4',
         45 : 'F4',
         46 : 'F#4',
         47 : 'G4',
         48 : 'G#4',
         49 : 'A4',
         50 : 'A#4',
         51 : 'B4',
         52 : 'C5',
         53 : 'C#5',
         54 : 'D5',
         55 : 'D#5',
         56 : 'E5',
         57 : 'F5',
         58 : 'F#5',
         59 : 'G5',
         60 : 'G#5',
         61 : 'A5',
         62 : 'A#5',
         63 : 'B5',
         64 : 'C6',
         65 : 'C#6',
         66 : 'D6',
         67 : 'D#6',
         68 : 'E6',
         69 : 'F6',
         70 : 'F#6',
         71 : 'G6',
         72 : 'G#6',
         73 : 'A6',
         74 : 'A#6',
         75 : 'B6',
         76 : 'C7',
         77 : 'C#7',
         78 : 'D7',
         79 : 'D#7',
         80 : 'E7',
         81 : 'F7',
         82 : 'F#7',
         83 : 'G7',
         84 : 'G#7',
         85 : 'A7',
         86 : 'A#7',
         87 : 'B7',
         88 : 'C8'}

Drums = {35 : 'B0',
         36 : 'C1',
         37 : 'C#1',
         38 : 'D1',
         39 : 'Eb1',
         40 : 'E1',
         41 : 'F1',
         42 : 'F#1',
         43 : 'G1',
         44 : 'Ab1',
         45 : 'A1',
         46 : 'Bb1',
         47 : 'B1',
         48 : 'C2',
         49 : 'C#2',
         50 : 'D2',
         51 : 'Eb2',
         52 : 'E2',
         53 : 'F2',
         54 : 'F#2',
         55 : 'G2',
         56 : 'Ab2',
         57 : 'A2',
         58 : 'Bb2',
         59 : 'B2',
         60 : 'C3',
         61 : 'C#3 ',
         62 : 'D3',
         63 : 'Eb3',
         64 : 'E3',
         65 : 'F3',
         66 : 'F#3',
         67 : 'G3',
         68 : 'Ab3',
         69 : 'A3',
         70 : 'Bb3',
         71 : 'B3',
         72 : 'C4',
         73 : 'C#4',
         74 : 'D4',
         75 : 'Eb4',
         76 : 'E4',
         77 : 'F4',
         78 : 'F#4',
         79 : 'G4',
         80 : 'Ab4',
         81 : 'A4'}

# search for any image
notelist  = []

def getnotes(Y): #one hot encoding
    img = None
    
    for file in glob.glob("*.png"):
        img = file
    
    image = load_image(img)
    notes = {}
    inst = pred(image) # classification model
    insttype = None
    if inst > 0.5 :
        notes = piano
        insttype = 'Piano'
    else :
        notes = Drums
        insttype = 'Drums'
        
    print("notes: ", notes)
    print("insttype: ", insttype)
    print(Y.shape)
    Y = Y.transpose ( )
    prev = -1
    for y in Y :

        x = np.array ( y )
        cur = np.where ( x == 1 )[0]

        for m in cur :
            if prev !=  m :
                notelist.append(notes.get ( m+9 ))
            prev =  m
    return notelist,insttype