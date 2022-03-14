from pickletools import uint8
from matplotlib import image
import numpy as np
import matplotlib.pyplot as plt
from pandas import wide_to_long


class Seam:
    width_ = 0
    height_ = 0
    
    def __init__(self, filename):
        temp = plt.imread(filename)
        self.width_ = temp.shape[1]
        self.height_ = temp.shape[0]
        self.image_ = np.zeros(temp.shape, dtype = np.uint8)
        for i in range(self.height_):
            for j in range(self.width_):
                self.image_[i][j] = temp[i][j]
        del temp
        self.array_ = self.image_.astype(np.int64)
        
        
    def GetVerticalSeam(self):
        values = self.GetValuesArray()
        arr = []
        min = values[0][0]
        min_id = 0
        for i in range(self.width_):
            if values[0][i] < min:
                min = values[0][i]
                min_id = i
        arr.append(min_id)
        for row in range(self.height_ - 1):
            mid = values[row + 1][min_id]
            left = mid + 1 if min_id == 0 else values[row + 1][min_id - 1]
            right = mid + 1 if min_id == self.width_ - 1 else values[row + 1][min_id + 1]
            min_id = self.BestRowCol(mid, left, right, min_id, min_id - 1, min_id + 1)
            arr.append(min_id)
        return arr
    
    def CarveVerticalSeam(self):
        arr = self.GetVerticalSeam()
        temp = np.zeros((self.height_, self.width_ - 1, 3), dtype = np.uint8)
        for row in range(self.height_):
            col_iter = 0
            for col in range(self.width_):
                if arr[row] != col:
                    temp[row][col_iter] = self.image_[row][col]
                    col_iter += 1
                
        del arr
        del self.array_
        del self.image_
        self.image_ = temp
        self.array_ = self.image_.astype(np.int64)
        self.width_ -= 1
                
          
    def DrawSeam(self):
        arr = self.GetVerticalSeam()
        temp = self.image_
        for i in range(self.height_):
            temp[i][arr[i]] = [255, 0, 0]
        self.image_ = temp
        
    
    def GetEnergy(self, x, y):
        left = y - 1
        right = y + 1
        top = x - 1
        down = x + 1
        if left == -1:
            left = self.width_ - 1
        if right == self.width_:
            right = 0
        if top == -1:
            top = self.height_ - 1
        if down == self.height_:
            down = 0
        to_return = 0
        to_return += (self.array_[x][left][0] - self.array_[x][right][0])**2
        to_return += (self.array_[x][left][1] - self.array_[x][right][1])**2
        to_return += (self.array_[x][left][2] - self.array_[x][right][2])**2
        to_return += (self.array_[top][y][0] - self.array_[down][y][0])**2
        to_return += (self.array_[top][y][1] - self.array_[down][y][1])**2
        to_return += (self.array_[top][y][2] - self.array_[down][y][2])**2
        return to_return
        
    def GetValuesArray(self):
        values = np.zeros((self.height_, self.width_))
        for i in range(self.width_):
            values[self.height_ - 1][i] = self.GetEnergy(self.height_ - 1, i)
        
        for row in range(self.height_ - 2, -1, -1):
            for col in range(self.width_):
                mid = values[row + 1][col]
                left = mid + 1 if col == 0 else values[row + 1][col - 1]
                right = mid + 1 if col == self.width_ - 1 else values[row + 1][col + 1]
                values[row][col] = self.GetEnergy(row, col) + self.GetMin(mid, left, right)
        return values
        
    def GetMin(self, a, b, c):
        min = a
        if b < min:
            min = b
        if c < min:
            min = c   
        return min
        
    def BestRowCol(self, mid, left_top, right_down, mid_id, lt_id, rd_id):
        min = self.GetMin(mid, left_top, right_down)
        if min == mid:
            return mid_id
        if min == left_top:
            return lt_id
        return rd_id
