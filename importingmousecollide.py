# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 15:14:51 2025

@author: Solo
"""
import importlib

import pygame
import mouse_collide

#importlib.reload(mouse_collide)

pygame.init()
WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
collidescreen = pygame.Surface([WIDTH, HEIGHT])
fps = 60
timer = pygame.time.Clock()
font_EN1 = pygame.font.Font('freesansbold.ttf', 18)
font_CH1 = pygame.font.Font('TaipeiSansTCBeta-Regular.ttf', 18)
button1_enabled = True
new_press = True
mouse_collide.init(pygame.K_SPACE)

class Button:
    def __init__(self, text, x_pos, y_pos, enabled, valid_time = 0, width = 150, height = 25):#valid time 0: 1: 2:
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enabled = enabled
        self.valid_time = valid_time
        self.width = width
        self.height = height
        self.draw()
        
    def draw(self):
        button_text = font_CH1.render(self.text, True, 'black')
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (self.width, self.height))
        if self.enabled:
            if self.check_click():
                pygame.draw.rect(screen, 'dark gray', button_rect, 0, 5)
            else:
                pygame.draw.rect(screen, 'light gray', button_rect, 0, 5)
        else:
                pygame.draw.rect(screen, 'black', button_rect, 0, 5)

        pygame.draw.rect(screen, 'black', button_rect, 2, 5)
        screen.blit(button_text, (self.x_pos +3, self.y_pos + 3))
        
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (self.width, self.height))
        if left_click and button_rect.collidepoint(mouse_pos) and self.enabled:
            return True
        else:
            return False
    
    def check_valid(self):
        pass

test = 0
    
run = True
while run:
    screen.fill('white')
    timer.tick(fps)
    mouse_collide.update()
    
    my_button = Button('Click Me!', 10, 10, button1_enabled)
    my_button2 = Button('Click Me, Too!', 10, 40, True)
    my_button3 = Button('Click Me, Three!', 10, 70, True)
    
    if pygame.mouse.get_pressed()[0] and new_press:
        new_press = False
        if my_button3.check_click():
            if button1_enabled:
                button1_enabled = False
            else:
                button1_enabled = True
    
    if not pygame.mouse.get_pressed()[0] and not new_press:
        new_press = True
    
    if my_button2.check_click():
        button_text = font_CH1.render('Button 2 is being pressed!', True, 'black')
        screen.blit(button_text, (200, 200))
    
    for event in pygame.event.get():
        if  event.type == pygame.QUIT:
            run = False
    
    if test == 0:
        print("assigned")
        #mouse_collide.call_mouse_collide_rect((1, 1), 0, 250, 250, 250, 0)
        mouse_collide.call_mouse_collide_polygon((2, 1), [(0, 250), (250, 250), (250, 500), (0, 500)], pygame.K_SPACE)
        test = 1
    
    #print(mouse_collide.box_info((1, 1))[0:11])
    print(mouse_collide.box_info((2, 1), pygame.K_SPACE)[0:11])
    
#    mouse_collide.call_mouse_collide_rect((1, 0), 250, 250, 250, 250, 2)
#    collidebox_rect = pygame.rect.Rect((0, 250), (250, 250))
#    if mouse_collide.box_info((1, 1)) == 
#    pygame.draw.rect(screen, 'black', collidebox_rect, 0, 5)
#    print("old", mouse_collide.list_of_mouse_collide_box_old)
#    print("new", mouse_collide.list_of_mouse_collide_box_new)
    
#box_info = [0:CollideWhileLastDown?, 1:CollideWhileLastUp?, 2:FramesKeepColliding=-1, 
 #3:pos_LastMouseDown, 4:pos_LastMouseUp, 5:frames_LastMouseDown, 6:frames_LastMouseUp, 
 #7:pos_MouseNow, 8:cur_mouse_down?, 9:UpdatedThisFrame?(Manually), 10:ReverseAutoUpdate?, 11:object]



    pygame.display.flip()
pygame.quit()
    
    
    