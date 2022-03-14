from src.seamcarving import Seam
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def main():
    print("Program started")
    s = Seam("./images/test2.jpg")
    s.DrawSeam()
    for i in range(50):
        print("carving...", i)
        s.CarveVerticalSeam()
    
    im = Image.fromarray(s.image_)
    im.save('testtgb.png')  
    
    
    
    
if __name__ == "__main__":
    main()