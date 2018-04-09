#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 22:24:20 2017

@author: wangzheng
"""

import matplotlib.pyplot as plt
from chat_utils import *


class Chess:
    print('successful class chess')
    def __init__(self, color):
        self.color = color
        self.cid = ''
        self.step = [] 
        self.field = [
                    (0.5, 0.5), (0.5, 1.5), (0.5, 1.5), (0.5, 2.5), (0.5, 3.5), (0.5, 4.5), (0.5, 5.5),
                    (1.5, 0.5), (1.5, 1.5), (1.5, 1.5), (1.5, 2.5), (1.5, 3.5), (1.5, 4.5), (1.5, 5.5),
                    (2.5, 0.5), (2.5, 1.5), (2.5, 1.5), (2.5, 2.5), (2.5, 3.5), (2.5, 4.5), (2.5, 5.5),
                    (3.5, 0.5), (3.5, 1.5), (3.5, 1.5), (3.5, 2.5), (3.5, 3.5), (3.5, 4.5), (3.5, 5.5),
                    (4.5, 0.5), (4.5, 1.5), (4.5, 1.5), (4.5, 2.5), (4.5, 3.5), (4.5, 4.5), (4.5, 5.5),
                    (5.5, 0.5), (5.5, 1.5), (5.5, 1.5), (5.5, 2.5), (5.5, 3.5), (5.5, 4.5), (5.5, 5.5)]
                    
        self.field_dic = {t:0 for t in self.field}  
        self.invalid = {t:0 for t in self.field}
        
            
    def int_point(self, point):
        intx = int(point[0][0]) + 0.5
        inty = int(point[0][1]) + 0.5
        return [intx, inty]
    
       
    def make_color(self, x, y, field_dic, m, p):
        m_count = 0
        p_count = 0
        list_9 = [(x-1, y+1), (x, y+1), (x+1, y+1), (x-1, y), (x+1, y), (x-1, y-1), (x, y-1), (x+1, y-1)]
        real_list = []
       
        for i in list_9:
            if i in field_dic:
                real_list.append(i)
        
        for j in real_list:
            if field_dic[j] == m:
                m_count += 1
            elif field_dic[j] == p:
                p_count += 1
                
        if m_count >= p_count - 1:
            return m
        else:
            return p
    
    def game_over(self, m, p):
        empty_dic = {}
        m_count = 0
        p_count = 0
        for point in self.field_dic:
            if self.field_dic[point] == 0:
                empty_dic[point] = 0
                
        for point in empty_dic:
           if self.make_color(point[0], point[1], self.field_dic, m, p) == p:
               p_count += 1
           if self.make_color(point[0], point[1], self.field_dic, m, p) == m \
           and self.make_color(point[0], point[1], self.field_dic, p, m) == m:
               m_count += 1
               
        if m_count == len(empty_dic):
            for point in empty_dic:
                self.field_dic[point] = m
            return True
        elif p_count == len(empty_dic):
            for point in empty_dic:
                self.field_dic[point] = p
            return True
        else:
            print('not over', m_count, p_count)
            return False
        
    
    def winner(self):
        points = {self.color:0, self.pcolor:0}
        for c in self.field_dic.values():             
            if c == self.color:  
                points[self.color] += 1  
            else:
                points[self.pcolor] += 1
        if points[self.color] > points[self.pcolor]:
            return 'YOU WIN'
        else:
            return 'YOU LOSE :('
         
            
        
        
        
        
        
        
        
        
        