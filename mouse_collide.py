
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 13:33:34 2025

@author: Solo

version info:
different keys enabled, but need to use mouse_collide.init().
revised the message printed so that they'll be understood more easily.
use dict to replace list.
"""
print(
      """
mouse_collide imported successfully!
    1.Use mouse_collide.init(*keys) in the begining, "*keys" include 'l', 'm', 'r' as left, middle, right mouse key, pygame constant like pygame.K_SPACE.
    2.Use "mouse_collide.update(AutoUpdate = 1)" right after the start of each frame!
    3."call_mouse_collide_rect(index, x_pos, y_pos, width, height, key_index = 'l', ReverseAutoUpdate = -1)"
    4."call_mouse_collide_polygon(index, points_pos, key_index = 'l', ReverseAutoUpdate = -1)"
    5.for point 2, 3, use them to assign a collide box, then use "box_info" to get their information.
    6.mouse_collide.box_info(index, key_index = 'l') = 
      [0:CollideWhileLastDown?, 1:CollideWhileLastUp?, 2:FramesKeepColliding=-1, 
      3:pos_LastMouseDown, 4:pos_LastMouseUp, 5:frames_LastMouseDown, 6:frames_LastMouseUp, 
      7:pos_MouseNow, 8:cur_mouse_down?, 9:UpdatedThisFrame?(Manually), 10:ReverseAutoUpdate?, 11:object]
    7.if AutoUpdate equals to 1 and not Reversed, information of collide box would be auto updated each frame once a box is called.
      Otherwise, collide box should be called each frame, or it would be deleted.
    8.del_box(index, key_index = 'l') when the box is no longer in use if AutoUpdate=1 and not reversed.
      """
      )
import pygame
import copy
import numpy

pos_MouseNow = (-10, -10)

def init(*keys):
    global dict_of_mouse_collide_box_old
    global dict_of_mouse_collide_box_new
    global pos_LastMouseDown, pos_LastMouseUp
    global new_mouse_down
    global cur_mouse_down
    global frames_LastMouseDown, frames_LastMouseUp
    new_keys = list(keys)
    new_keys.extend(['l', 'm', 'r']) #dict would overwrite them anyway
    dict_of_mouse_collide_box_old = {key: {} for key in new_keys}
    dict_of_mouse_collide_box_new = {key: {} for key in new_keys}
    pos_LastMouseDown = {key: (-10, -10) for key in new_keys}
    pos_LastMouseUp = {key: (-10, -10) for key in new_keys}
    new_mouse_down = {key: True for key in new_keys}
    cur_mouse_down = {key: False for key in new_keys}
    frames_LastMouseDown = {key: 0 for key in new_keys}
    frames_LastMouseUp = {key: 0 for key in new_keys}

#dict_of_mouse_collide_box_old[key_index]["key"] = [0:mouse_collide_rect(x_pos,
 #y_pos, width, height) / mouse_collide_polygon(index, points_pos), 1:CollideWhileLastDown?, 
 #2:CollideWhileLastUp?, 3:FramesKeepColliding=-1, 4:UpdatedThisFrame?(Manually), 5:ReverseAutoUpdate?]

def AutoUpdate_single_box(key_index, index):
    global dict_of_mouse_collide_box_old
    global dict_of_mouse_collide_box_new
    if dict_of_mouse_collide_box_old[key_index][index][0].type == "rect":
        call_mouse_collide_rect(index, dict_of_mouse_collide_box_old[key_index][index][0].x_pos, \
                               dict_of_mouse_collide_box_old[key_index][index][0].y_pos, \
                                   dict_of_mouse_collide_box_old[key_index][index][0].width, \
                                       dict_of_mouse_collide_box_old[key_index][index][0].height, \
                                           key_index, dict_of_mouse_collide_box_old[key_index][index][5])
    elif dict_of_mouse_collide_box_old[key_index][index][0].type == "polygon":
        call_mouse_collide_polygon(index, dict_of_mouse_collide_box_old[key_index][index][0].points_pos, \
                                           key_index, dict_of_mouse_collide_box_old[key_index][index][5])
    dict_of_mouse_collide_box_old[key_index][index][4] = 0

def update(AutoUpdate = 1): #(put at the top of main loop) (if not AutoUpdate, those not in used would be deleted)
    global dict_of_mouse_collide_box_old
    global dict_of_mouse_collide_box_new
    global pos_LastMouseDown, pos_LastMouseUp
    global new_mouse_down
    global frames_LastMouseDown, frames_LastMouseUp
    global pos_MouseNow, cur_mouse_down
    
    for key_index in list(dict_of_mouse_collide_box_old.keys()):
        for index in list(dict_of_mouse_collide_box_old[key_index].keys()):
            if AutoUpdate == dict_of_mouse_collide_box_old[key_index][index][5]: #Not AutoUpdate (0, 0) or (1, 1)
                if dict_of_mouse_collide_box_old[key_index][index][4] == 0:
                    del_box(index, key_index)

    
    frames_LastMouseDown = dict(map(lambda item: (item[0], item[1] + 1), frames_LastMouseDown.items()))
    frames_LastMouseUp = dict(map(lambda item: (item[0], item[1] + 1), frames_LastMouseUp.items()))
    pos_MouseNow = pygame.mouse.get_pos()
    
    dict_of_mouse_collide_box_old = copy.deepcopy(dict_of_mouse_collide_box_new) 
    #dict_of_mouse_collide_box_old = dict_of_mouse_collide_box_new.copy() 
    #(It would cause each element in old list and new list being combined together)
    cur_mouse_down['l'] = pygame.mouse.get_pressed()[0]
    cur_mouse_down['m'] = pygame.mouse.get_pressed()[1]
    cur_mouse_down['r'] = pygame.mouse.get_pressed()[2]
    pygame_key_pressed = pygame.key.get_pressed()
    for i in list(dict_of_mouse_collide_box_old.keys()):
        if type(i) == int:
            cur_mouse_down[i] = pygame_key_pressed[i]
        if cur_mouse_down[i] and new_mouse_down[i]:
            pos_LastMouseDown[i] = pos_MouseNow
            frames_LastMouseDown[i] = 0
            new_mouse_down[i] = False
        if not cur_mouse_down[i] and not new_mouse_down[i]:
            pos_LastMouseUp[i] = pos_MouseNow
            frames_LastMouseUp[i] = 0
            new_mouse_down[i] = True

    for key_index in list(dict_of_mouse_collide_box_old.keys()):
        for index in list(dict_of_mouse_collide_box_old[key_index].keys()):
            if AutoUpdate != dict_of_mouse_collide_box_old[key_index][index][5]: #AutoUpdate (0, 1) or (1, 0)
                AutoUpdate_single_box(key_index, index)
                
def call_mouse_collide_rect(index, x_pos, y_pos, width, height, key_index = 'l', ReverseAutoUpdate = -1):
    global dict_of_mouse_collide_box_old
    global dict_of_mouse_collide_box_new
    if not (key_index in dict_of_mouse_collide_box_old):
        print("mouse_collide.call_mouse_collide_rect: key_index not found! (key_index: \"" + str(key_index) + "\"), try adding it in mouse_collide.init()")
        return
    #handle new
    if index in dict_of_mouse_collide_box_old[key_index]:
        if dict_of_mouse_collide_box_old[key_index][index][4] == 1:
            print("mouse_collide.call_mouse_collide_rect: the box had already been assigned this frame! (key_index: \"" + str(key_index) + "\", index: \"" + str(index) + "\")")
        dict_of_mouse_collide_box_new[key_index][index][0] = mouse_collide_rect(index, x_pos, y_pos, width, height)
        if ReverseAutoUpdate == 0 or ReverseAutoUpdate == 1:
            dict_of_mouse_collide_box_new[key_index][index][5] = ReverseAutoUpdate
            
    else:
        if ReverseAutoUpdate != 1: #check valid: (and ReverseAutoUpdate != 0), but it is going to be set to 0 anyway.
            ReverseAutoUpdate = 0
        dict_of_mouse_collide_box_old[key_index][index] = [mouse_collide_rect(index, x_pos, y_pos, width, height), 0, 0, -1, 0, ReverseAutoUpdate]
        dict_of_mouse_collide_box_new[key_index][index] = [mouse_collide_rect(index, x_pos, y_pos, width, height), 0, 0, -1, 0, ReverseAutoUpdate]
        if len(dict_of_mouse_collide_box_old[key_index]) != len(dict_of_mouse_collide_box_new[key_index]):
            print("mouse_collide.call_mouse_collide_rect: old and new lenth of list not equal!")
    Update_single_box(index, key_index)
    
def call_mouse_collide_polygon(index, points_pos, key_index = 'l', ReverseAutoUpdate = -1):
    global dict_of_mouse_collide_box_old
    global dict_of_mouse_collide_box_new
    if not (key_index in dict_of_mouse_collide_box_old):
        print("mouse_collide.call_mouse_collide_polygon: key_index not found! (key_index: \"" + str(key_index) + "\"), try adding it in mouse_collide.init()")
        return
    #handle new
    if index in dict_of_mouse_collide_box_old[key_index]:
        if dict_of_mouse_collide_box_old[key_index][index][4] == 1:
            print("mouse_collide.call_mouse_collide_polygon: the box had already been assigned this frame! (key_index: \"" + str(key_index) + "\", index: \"" + str(index) + "\")")
        dict_of_mouse_collide_box_new[key_index][index][0] = mouse_collide_polygon(index, points_pos)
        if ReverseAutoUpdate == 0 or ReverseAutoUpdate == 1:
            dict_of_mouse_collide_box_new[key_index][index][5] = ReverseAutoUpdate
            
    else:
        if ReverseAutoUpdate != 1: #check valid: (and ReverseAutoUpdate != 0), but it is going to be set to 0 anyway.
            ReverseAutoUpdate = 0
        dict_of_mouse_collide_box_old[key_index][index] = [mouse_collide_polygon(index, points_pos), 0, 0, -1, 0, ReverseAutoUpdate]
        dict_of_mouse_collide_box_new[key_index][index] = [mouse_collide_polygon(index, points_pos), 0, 0, -1, 0, ReverseAutoUpdate]
        if len(dict_of_mouse_collide_box_old[key_index]) != len(dict_of_mouse_collide_box_new[key_index]):
            print("mouse_collide.call_mouse_collide_polygon: old and new lenth of list not equal!")
    Update_single_box(index, key_index)
    
def Update_single_box(index, key_index = 'l'):
    global dict_of_mouse_collide_box_old
    global dict_of_mouse_collide_box_new
    global frames_LastMouseDown, frames_LastMouseUp
    global pos_LastMouseDown, pos_LastMouseUp
    global pos_MouseNow
    #Collide While Last Down?
    if frames_LastMouseDown[key_index] == 0:
        if dict_of_mouse_collide_box_new[key_index][index][0].check_collide(pos_LastMouseDown[key_index]):
            dict_of_mouse_collide_box_new[key_index][index][1] = 1
        else:
            dict_of_mouse_collide_box_new[key_index][index][1] = 0
    #Collide While Last Up?
    elif frames_LastMouseUp[key_index] == 0:
        if dict_of_mouse_collide_box_new[key_index][index][0].check_collide(pos_LastMouseUp[key_index]):
            dict_of_mouse_collide_box_new[key_index][index][2] = 1
        else:
            dict_of_mouse_collide_box_new[key_index][index][2] = 0
    #How Many Frames It last touching mouse?
    if dict_of_mouse_collide_box_new[key_index][index][0].check_collide(pos_MouseNow):
        dict_of_mouse_collide_box_new[key_index][index][3] += 1
    else:
        dict_of_mouse_collide_box_new[key_index][index][3] = -1
    dict_of_mouse_collide_box_old[key_index][index][4] = 1
       
    
def del_box(index, key_index = 'l'):
    global dict_of_mouse_collide_box_old
    global dict_of_mouse_collide_box_new
    if not (key_index in dict_of_mouse_collide_box_old):
        print("mouse_collide.del_box: key_index not found! (key_index: \"" + str(key_index) + "\"), try adding it in mouse_collide.init()")
        return
    if index in dict_of_mouse_collide_box_old[key_index]:
        del dict_of_mouse_collide_box_old[key_index][index]
        del dict_of_mouse_collide_box_new[key_index][index]
    else:
        print("mouse_collide.del_box: box not found! (key_index: \"" + str(key_index) + "\", index: \"" + str(index) + "\")")

class mouse_collide_rect:   #每一幀都要呼叫，否則就要del重來
    def __init__(self, index, x_pos, y_pos, width, height):
        self.index = index
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.type = "rect"

    def check_collide(self, pos):
        self.pos = pos
        global dict_of_mouse_collide_box_old
        global dict_of_mouse_collide_box_new
        collidebox_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (self.width, self.height))
        if collidebox_rect.collidepoint(self.pos):
            return True
        else:
            return False
        
class mouse_collide_polygon:
    def __init__(self, index, points_pos): #"points_pos" should be carried in list or tuple
        self.index = index
        self.points_pos = points_pos
        self.type = "polygon"
        self.num_points = len(self.points_pos)

    def check_collide(self, pos):
        sign = 1
        x_pos_rel = [self.points_pos[i][0] - pos[0] for i in range(self.num_points)]
        y_pos_rel = [self.points_pos[i][1] - pos[1] for i in range(self.num_points)]
        for i in range(self.num_points):
            if y_pos_rel[i] == 0:
                if x_pos_rel[i] == 0:
                    return 2 #on point
                elif x_pos_rel[i] > 0:
                    if y_pos_rel[i-1] != 0:
                        sign *= numpy.sign(y_pos_rel[i-1])
                    if y_pos_rel[(i+1) % self.num_points] != 0:
                        sign *= numpy.sign(y_pos_rel[(i+1) % self.num_points])
            elif y_pos_rel[i-1] * y_pos_rel[i] < 0:
                m, n = abs(y_pos_rel[i-1]), abs(y_pos_rel[i])
                x_intersection = (x_pos_rel[i] * m + x_pos_rel[i-1] * n)/(m + n)
                if x_intersection == 0:
                    return 3 #on edge
                elif x_intersection > 0:
                    sign *= -1
        return int(sign == -1)

def box_info(index, key_index = 'l'):
    global dict_of_mouse_collide_box_old
    global dict_of_mouse_collide_box_new
    global pos_LastMouseDown, pos_LastMouseUp
    global frames_LastMouseDown, frames_LastMouseUp
    global pos_MouseNow, cur_mouse_down
    if not (key_index in dict_of_mouse_collide_box_old):
        print("mouse_collide.box_info: key_index not found! (key_index: \"" + str(key_index) + "\"), try adding it in mouse_collide.init()")
        return [0, 0, -1, (-10, -10), (-10, -10), 100, 100, (-10, -10), False, 0, 0, None]
    if not (index in dict_of_mouse_collide_box_old[key_index]):
        print("mouse_collide.box_info: box not found! (key_index: \"" + str(key_index) + "\", index: \"" + str(index) + "\")")
        return [0, 0, -1, (-10, -10), (-10, -10), 100, 100, (-10, -10), False, 0, 0, None]
    Info_list = dict_of_mouse_collide_box_new[key_index][index][1:4]
    Info_list.append(pos_LastMouseDown[key_index])
    Info_list.append(pos_LastMouseUp[key_index])
    Info_list.append(frames_LastMouseDown[key_index])
    Info_list.append(frames_LastMouseUp[key_index])
    Info_list.append(pos_MouseNow)
    Info_list.append(cur_mouse_down[key_index])
    Info_list.append(dict_of_mouse_collide_box_old[key_index][index][4])
    Info_list.append(dict_of_mouse_collide_box_new[key_index][index][5])
    Info_list.append(dict_of_mouse_collide_box_new[key_index][index][0])
    return(Info_list)
