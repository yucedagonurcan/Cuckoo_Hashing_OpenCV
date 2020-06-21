import cv2
import time
import warnings
import numpy as np
from utils import *
from random import randint
warnings.filterwarnings("ignore")

class HashTable():
    
    def __init__(self, start_point, end_point, num_cells, name):
        self.start_point = start_point
        self.end_point = end_point
        self.num_cells = num_cells
        self.random_num = randint(4, 1000)
        self.name = name
        self.occupancy = 0.0
        
    def CalculateRectsPositions(self, margin=10):
        start_x, start_y = self.start_point
        end_x, end_y = self.end_point
        
        rects_height = end_y - start_y
        rects_width = end_x - start_x
        
        height_for_each_block = round(rects_height/self.num_cells)
        width_for_each_table = round(rects_width)
        
        y_s = np.linspace(start_y, end_y-height_for_each_block, dtype=int, num=self.num_cells).reshape(-1, 1)
        x_s = np.array([round(start_x)]*y_s.size).reshape(-1, 1)

        rects_pos = np.concatenate([x_s, y_s, x_s + width_for_each_table - margin, y_s + height_for_each_block - margin], axis=1)
        self.cells = [HashCell(start_point=tuple(rect[:2]), end_point=tuple(rect[2:])) for rect in rects_pos] 
    def CalculateOccupancy(self):
        taken=0
        for cell in self.cells:
            if not cell.is_empty:
                taken+=1
        self.occupancy = round((taken/self.num_cells)*100, 2)
    def DrawTable(self, image):
        occupancy_font_scale = 1
        self.CalculateOccupancy()
        for cur_rect in self.cells:    
            image = cv2.rectangle(image, cur_rect.start_point, cur_rect.end_point, cur_rect.color,  cur_rect.thickness)
            width_rect, height_rect = np.array(cur_rect.end_point - np.array(cur_rect.start_point))
            font_scale = np.min((width_rect, height_rect))/70

            image = cv2.putText(image, str(cur_rect.number),
                                (int(cur_rect.start_point[0] + width_rect*0.45),
                                int(cur_rect.end_point[1] - height_rect*0.3) ), cv2.FONT_HERSHEY_SIMPLEX, font_scale, cur_rect.text_color)
            
        image = cv2.rectangle(image, (int(self.start_point[0] + width_rect*0.20), self.end_point[1] ),
                                    (int(self.end_point[0] - width_rect*0.20), self.end_point[1] + 45), (21, 55, 55),  -1)

        occupancy_width = int(self.end_point[0] - width_rect*0.20) - int(self.start_point[0] + width_rect*0.20)
        occupancy_height = self.end_point[1] + 45 - self.end_point[1]

        occupancy_font_scale = np.min((occupancy_width, occupancy_height))/110

        width_of_table = (self.end_point[0] - self.start_point[0])
        image = cv2.putText(image, str(self.occupancy) + '%',
                            (int(self.start_point[0] + width_of_table*0.30), int(self.end_point[1] + 25)),
                            cv2.FONT_HERSHEY_SIMPLEX, occupancy_font_scale, (0, 0, 0))
        return image
    def HashFunc(self, x):
        
        return (np.abs(hash(str(x))) * ((self.random_num)**2)) %self.num_cells 
    
    def CheckNumExists(self, number):
        return self.cells[self.HashFunc(number)].number == number 
        
    def TryAddNumber(self, number, image, winname):
        
        print_yellow_bold(f"\t-> {number} is trying to added to {self.name}: ")
        index_to_place = self.HashFunc(number)
        # self.cells[index_to_place].color = (255, 255, 255)
        
        reinsert_number = None
        
        i = 0
        while (True):
            
            self.cells[index_to_place].color =  (0, 20, 25)
            self.cells[index_to_place].text_color =  (0, 0, 0)

            cv2.imshow(winname, self.DrawTable(image))
            k = cv2.waitKey(33) & 0xFF
            if k == ord('p'):    
                break;
            i += 1
        if self.cells[index_to_place].is_empty:
            print_green_bold(f"\t\t[SUCCESS] {index_to_place} is empty, so {number} will be added.")
            self.cells[index_to_place].color = (55, 0, 0)
            self.cells[index_to_place].text_color = (255, 255, 255)

            self.cells[index_to_place].SetNumber(number = number)
        else:
            print_red_bold(f"\t\t[FAIL] {index_to_place} is NOT empty, so we are re-inserting {self.cells[index_to_place].number} to add {number} in {self.name} hash table")
            self.cells[index_to_place].color = (55, 0, 0)
            self.cells[index_to_place].text_color = (255, 255, 255)

            reinsert_number = self.cells[index_to_place].number
            self.cells[index_to_place].SetNumber(number = number)
            
        return reinsert_number
                
class HashCell():
    
    def __init__(self, start_point, end_point, color=(55, 0, 0), text_color=(255, 255, 255), thickness=-1):
        self.start_point = start_point
        self.end_point = end_point
        self.color = color
        self.text_color = text_color
        self.thickness = thickness
        self.is_empty = True
        self.number = ""
        
        
    def SetNumber(self, number=""):
        self.number = number
        self.is_empty = False
