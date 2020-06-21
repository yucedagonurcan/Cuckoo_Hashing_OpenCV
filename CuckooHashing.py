import cv2
import random
import argparse
import numpy as np
from utils import *
from Hash import HashCell, HashTable

dummy = lambda x : 0

MARGIN = 10
NUM_CELLS = 10
NUM_TABLES = 2
WINDOW_NAME = 'Cuckoo Hashing Visualization'
WIN_SIZE = [900, 1400, 3]

def CheckLoop(number_history):

    minrun = 3
    lendata = len(number_history)
    for runlen in range(minrun, lendata // 2):
        i = 0
        while i < lendata - runlen * 2:
            s1 = number_history[i:i + runlen]
            s2 = number_history[i + runlen:i + runlen * 2]
            if s1 == s2:
                
                print_red_bold(f"\t[ERROR] Loop detected...")
                return True
                i += runlen 
            else:
                i += 1
    return False
def CheckNumExistsInHashTables(hash_tables, number):
    results = []
    for has_tab in hash_tables:
        results.append(has_tab.CheckNumExists(number))
    return any(results)

def AddNumberToHashTables(hash_tables, number, exclude_hash_tables, number_history=[]):
    
    if CheckNumExistsInHashTables(hash_tables, number):
        print_red_bold(f"\t{number} is already exists...")
        return True
    
    number_history.append(number)
    if CheckLoop(number_history=number_history):
        print_red_bold("\t[INFO] Please press 'r' to reset the table.")
        return False
        
    print_yellow(f"\t[INFO] Number History: {number_history}")
    search_hash_tables = [ x for x in list(range(len(hash_tables))) if x not in exclude_hash_tables]
    if len(search_hash_tables) == 0:
        search_hash_tables = list(range(len(hash_tables) - 1))
        random.shuffle(search_hash_tables)
        exclude_hash_tables = []

    for current_try_hash_table in search_hash_tables:
        
        reinsert_number = hash_tables[current_try_hash_table].TryAddNumber(number, image, WINDOW_NAME)
        if reinsert_number is not None:
            exclude_hash_tables.append(current_try_hash_table)
            return AddNumberToHashTables(hash_tables, reinsert_number, exclude_hash_tables, number_history)
            
        else: 
            return True
            
def CreateHashTables(win_size, num_tables, num_cells, margin):
    hash_tables = []
    image = np.zeros(shape=win_size)
    info_text_font_scale = 0.7
    cv2.putText(image, "Press 'p' for PLAY", (15, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, info_text_font_scale, (255, 255, 255))
    cv2.putText(image, "Press 'r' for RESET", (15, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, info_text_font_scale, (255, 255, 255))

    width_of_each_table = round((win_size[1]*0.8)/num_tables)
    for i in range(num_tables):
        
        start_x_for_rects = int(win_size[1] * 0.1 + width_of_each_table * (i))
        end_x_for_rects =  int(start_x_for_rects + width_of_each_table)
        
        start_y_for_rects = int(win_size[0] * 0.1)
        end_y_for_rects = int(win_size[0] * 0.9)

        h1 = HashTable(start_point=(start_x_for_rects, start_y_for_rects), end_point=(end_x_for_rects, end_y_for_rects), num_cells=num_cells, name=f"h_{i}")
        h1.CalculateRectsPositions(margin=margin)
        image = h1.DrawTable(image=image)
        hash_tables.append(h1)
    return image, hash_tables

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--num_cells", type=int, help="Number of cells for each table.", default=10)
    parser.add_argument("--num_tables", type=int, help="Number of tables.", default=2)
    args = parser.parse_args()
    
    NUM_CELLS = args.num_cells
    NUM_TABLES = args.num_tables
    
    reset_needed = False
    print_yellow_bold(f"[ARGUMENT] Number of Cells: {NUM_CELLS}")
    print_yellow_bold(f"[ARGUMENT] Number of Tables: {NUM_TABLES}")

    cv2.namedWindow(WINDOW_NAME)  
    cv2.moveWindow(WINDOW_NAME, 0, 0)  
    cv2.createTrackbar("AddNumber", WINDOW_NAME, 1, 300, dummy)
    cv2.setTrackbarMin("AddNumber", WINDOW_NAME, 0)
    image, hash_tables = CreateHashTables(win_size=WIN_SIZE, num_tables=NUM_TABLES, num_cells=NUM_CELLS, margin=MARGIN)
    number_history = []
    while(True):

        add_number = cv2.getTrackbarPos("AddNumber", WINDOW_NAME)
        k = cv2.waitKey(1) & 0xFF
        number_history = []

        if k == ord('p') and not reset_needed:
            print_yellow_bold(f"Trying to add {add_number} into hash tables.")
            if not AddNumberToHashTables(hash_tables=hash_tables, number=add_number, exclude_hash_tables=[], number_history=number_history):
                reset_needed = True
            for table in hash_tables:
                table.DrawTable(image=image)
                
        elif k == ord('r'):
            reset_needed = False
            image, hash_tables = CreateHashTables(win_size=WIN_SIZE, num_tables=NUM_TABLES, num_cells=NUM_CELLS, margin=MARGIN)
        elif k == 27:
            break
        cv2.imshow(WINDOW_NAME,image)
    cv2.destroyAllWindows()