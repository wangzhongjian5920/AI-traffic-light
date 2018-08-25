"""
COMP9417 Reinforement learning -- traffic light simulation

Black rectangle: Road
White rectangle: Cars
Gray area: Ground
"""

import numpy as numpy
import tkinter as tk
import time
import random as rnd

UNIT = 6		# pixels
MAP_H = 100		# Map height
MAP_W = 100		# Map width
WHOLE_PERIOD = 1000
class Map(tk.Tk, object):

    def __init__(self):
        super(Map, self).__init__()
        self.action_space = ['y', 'n']
        self.n_action = len(self.action_space)
        self.list1 = []
        self.list2 = []
        self.list3 = []
        self.list4 = []
        self.list1_L = []
        self.list1_R = []
        self.list2_L = []
        self.list2_R = []
        self.list3_L = []
        self.list3_R = []
        self.list4_L = []
        self.list4_R = []
        self.time = 0
        self.delay = 0
        self.yellow_time = 0
        self.title('Map')
        self.geometry('{0}x{1}'.format(MAP_H * UNIT, MAP_W * UNIT))
        self._build_map()

    def _build_map(self):
        self.canvas = tk.Canvas(self, bg='grey',
                           height=MAP_H * UNIT,
                           width=MAP_W * UNIT)

        # create grid
        for c in range(0, MAP_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAP_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAP_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAP_H * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)


        # creare the road
        self.road1 = self.canvas.create_rectangle(
            0, (MAP_H/2-3)*UNIT, MAP_H*UNIT, (MAP_H/2+3)*UNIT, fill='black')
        self.road2 = self.canvas.create_rectangle(
            (MAP_W/2-3)*UNIT, 0, (MAP_W/2+3)*UNIT, MAP_W*UNIT, fill='black')

        # create the traffic light
        self.light1 = self.canvas.create_rectangle(
            (MAP_H/2-3)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2-4)*UNIT,(MAP_W/2)*UNIT, fill='green',tags='g'
            )
        self.light2 = self.canvas.create_rectangle(
            (MAP_H/2)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2-4)*UNIT, fill='red', tags='r'
            )
        self.light3 = self.canvas.create_rectangle(
            (MAP_H/2+4)*UNIT,(MAP_H/2)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2+3)*UNIT, fill='red', tags='r'
            )
        self.light4 = self.canvas.create_rectangle(
            (MAP_H/2)*UNIT,(MAP_H/2+4)*UNIT,(MAP_W/2-3)*UNIT,(MAP_W/2+3)*UNIT, fill='red', tags='r'
            )

        self.canvas.pack()


    def switch_light(self, action):
        t1 = self.canvas.gettags(self.light1)
        t2 = self.canvas.gettags(self.light2)

        # Finding the closest car
        distance1_stg = 9
        distance1_l = 9
        distance1_r = 9
        distance2_stg = 9
        distance2_l = 9
        distance2_r = 9
        distance3_stg = 9
        distance3_l = 9
        distance3_r = 9
        distance4_stg = 9
        distance4_l = 9
        distance4_r = 9

        # the clostest distance of road 1 straight
        p1 = self.canvas.coords(self.light1)
        for car_index1 in range(len(self.list1)):
            p = self.canvas.coords(self.list1[car_index1])
            if p1[0]-8*UNIT <= p[0] and p[0] <= p1[0]:
                distance1_stg = (p1[0] - p[0])/UNIT
                break
        # the clostest distance of road 1 left
        for car_index1l in range(len(self.list1_L)):
            p = self.canvas.coords(self.list1_L[car_index1l])
            if p1[0]-8*UNIT <= p[0] and p[0] <= p1[0]:
                distance1_l = (p1[0] - p[0])/UNIT
                break
        # the clostest distance of road 1 left
        for car_index1r in range(len(self.list1_R)):
            p = self.canvas.coords(self.list1_R[car_index1r])
            if p1[0]-8*UNIT <= p[0] and p[0] <= p1[0]:
                distance1_r = (p1[0] - p[0])/UNIT
                break
        distance1 = min(distance1_stg, distance1_l, distance1_r)

        # the clostest distance of road 2 straight
        p2 = self.canvas.coords(self.light2)
        for car_index2 in range(len(self.list2)):
            p = self.canvas.coords(self.list2[car_index2])
            if p2[1]-8*UNIT <= p[1] and p[1] <= p2[1]:
                distance2_stg = (p2[1] - p[1])/UNIT
                break
        # the clostest distance of road 2 left
        for car_index2l in range(len(self.list2_L)):
            p = self.canvas.coords(self.list2_L[car_index2l])
            if p2[1]-8*UNIT <= p[1] and p[1] <= p2[1]:
                distance2_l = (p2[1] - p[1])/UNIT
                break 
        # the clostest distance of road 2 right
        for car_index2r in range(len(self.list2_R)):
            p = self.canvas.coords(self.list2_R[car_index2r])
            if p2[1]-8*UNIT <= p[1] and p[1] <= p2[1]:
                distance2_r = (p2[1] - p[1])/UNIT
                break
        distance2 = min(distance2_stg, distance2_l, distance2_r)        

        # the clostest distance of road 3 straight
        p3 = self.canvas.coords(self.light3)
        for car_index3 in range(len(self.list3)):
            p = self.canvas.coords(self.list3[car_index3])
            if p3[0]+8*UNIT >= p[0] and p[0] >= p3[0]:
                distance3_stg = (p[0] - p3[0])/UNIT
                break
        # the clostest distance of road 3 left
        for car_index3l in range(len(self.list3_L)):
            p = self.canvas.coords(self.list3_L[car_index3l])
            if p3[0]+8*UNIT >= p[0] and p[0] >= p3[0]:
                distance3_l = (p[0] - p3[0])/UNIT
                break
        # the clostest distance of road 3 right
        for car_index3r in range(len(self.list3_R)):
            p = self.canvas.coords(self.list3_R[car_index3r])
            if p3[0]+8*UNIT >= p[0] and p[0] >= p3[0]:
                distance3_r = (p[0] - p3[0])/UNIT
                break   
        distance3 = min(distance3_stg, distance3_l, distance3_r)       

        # the clostest distance of road 4 straight
        p4 = self.canvas.coords(self.light4)
        for car_index4 in range(len(self.list4)):
            p = self.canvas.coords(self.list4[car_index4])
            if p4[1]+8*UNIT >= p[1] and p[1] >= p4[1]:
                distance4_stg = (p[1] - p4[1])/UNIT
                break
        # the clostest distance of road 4 left
        for car_index4l in range(len(self.list4_L)):
            p = self.canvas.coords(self.list4_L[car_index4l])
            if p4[1]+8*UNIT >= p[1] and p[1] >= p4[1]:
                distance4_l = (p[1] - p4[1])/UNIT
                break
        # the clostest distance of road 4 right
        for car_index4r in range(len(self.list4_R)):
            p = self.canvas.coords(self.list4_R[car_index4r])
            if p4[1]+8*UNIT >= p[1] and p[1] >= p4[1]:
                distance4_r = (p[1] - p4[1])/UNIT
                break   
        distance4 = min(distance4_stg, distance4_l, distance4_r)       

        # print(distance1,distance2,distance3,distance4)

        # reward: per car waiting is -1, no car waiting is 0
        # reward += road1 and road3(row)
        reward = 0
        t1 = self.canvas.gettags(self.light1)
        if t1[0] == 'r':
            # reward: road1 straight
            if distance1_stg == 0:
                reward -= 1
                while car_index1 + 1 < len(self.list1):
                    p1 = self.canvas.coords(self.list1[car_index1])
                    p2 = self.canvas.coords(self.list1[car_index1+1])
                    if p1[0] - p2[0] == UNIT:
                        reward -= 1
                    else:
                        break
                    car_index1 += 1
            # reward: road1 left
            if distance1_l == 0:
                reward -= 1
                while car_index1l + 1 < len(self.list1_L):
                    p1 = self.canvas.coords(self.list1_L[car_index1l])
                    p2 = self.canvas.coords(self.list1_L[car_index1l+1])
                    if p1[0] - p2[0] == UNIT:
                        reward -= 1
                    else:
                        break
                    car_index1l += 1
            # reward: road1 right
            if distance1_r == 0:
                reward -= 1
                while car_index1r + 1 < len(self.list1_R):
                    p1 = self.canvas.coords(self.list1_R[car_index1r])
                    p2 = self.canvas.coords(self.list1_R[car_index1r+1])
                    if p1[0] - p2[0] == UNIT:
                        reward -= 1
                    else:
                        break
                    car_index1r += 1

        t3 = self.canvas.gettags(self.light3)

        if t3[0] == 'r':
            # rewaid: road3 straight
            if distance3_stg == 0:
                reward -= 1
                while car_index3 + 1 < len(self.list3):
                    p1 = self.canvas.coords(self.list3[car_index3])
                    p2 = self.canvas.coords(self.list3[car_index3+1])
                    if p2[0] - p1[0] == UNIT:
                        reward -= 1
                    else:
                        break
                    car_index3 += 1
            # rewaid: road3 left
            if distance3_l == 0:
                reward -= 1
                while car_index3l + 1 < len(self.list3_L):
                    p1 = self.canvas.coords(self.list3_L[car_index3l])
                    p2 = self.canvas.coords(self.list3_L[car_index3l+1])
                    if p2[0] - p1[0] == UNIT:
                        reward -= 1
                    else:
                        break
                    car_index3l += 1
                        # rewaid: road3 left
            if distance3_r == 0:
                reward -= 1
                while car_index3r + 1 < len(self.list3_R):
                    p1 = self.canvas.coords(self.list3_R[car_index3r])
                    p2 = self.canvas.coords(self.list3_R[car_index3r+1])
                    if p2[0] - p1[0] == UNIT:
                        reward -= 1
                    else:
                        break
                    car_index3r += 1

        # reward += road2 and road4(column)
        t2 = self.canvas.gettags(self.light2)
        if t2[0] == 'r':
            # road 2 straight
            if distance2_stg == 0:
                reward -= 1
                while car_index2 + 1 < len(self.list2):
                    p1 = self.canvas.coords(self.list2[car_index2])
                    p2 = self.canvas.coords(self.list2[car_index2+1])
                    if p1[1] - p2[1] == UNIT:
                        reward -= 1
                    else:
                        break
                    car_index2 += 1
            # road 2 left
            if distance2_l == 0:
                reward -= 1
                while car_index2l + 1 < len(self.list2_L):
                    p1 = self.canvas.coords(self.list2_L[car_index2l])
                    p2 = self.canvas.coords(self.list2_L[car_index2l+1])
                    if p1[1] - p2[1] == UNIT:
                        reward -= 1
                    else:
                        break
                    car_index2l += 1
            # road 2 right
            if distance2_r == 0:
                reward -= 1
                while car_index2r + 1 < len(self.list2_R):
                    p1 = self.canvas.coords(self.list2_R[car_index2r])
                    p2 = self.canvas.coords(self.list2_R[car_index2r+1])
                    if p1[1] - p2[1] == UNIT:
                        reward -= 1
                    else:
                        break
                    car_index2r += 1            

        t4 = self.canvas.gettags(self.light4)
        if t4[0] == 'r': 
            # road4 straight
            if distance4_stg == 0:
                reward -= 1
                while car_index4 + 1 < len(self.list4):
                    p1 = self.canvas.coords(self.list4[car_index4])
                    p2 = self.canvas.coords(self.list4[car_index4+1])
                    if p2[1] - p1[1] == UNIT:
                        reward -= 1
                    else:
                        break
                    car_index4 += 1
            # road4 left
            if distance4_l == 0:
                reward -= 1
                while car_index4l + 1 < len(self.list4_L):
                    p1 = self.canvas.coords(self.list4_L[car_index4l])
                    p2 = self.canvas.coords(self.list4_L[car_index4l+1])
                    if p2[1] - p1[1] == UNIT:
                        reward -= 1
                    else:
                        break
                    car_index4l += 1

           # road4 right
            if distance4_r == 0:
                reward -= 1
                while car_index4r + 1 < len(self.list4_R):
                    p1 = self.canvas.coords(self.list4_R[car_index4r])
                    p2 = self.canvas.coords(self.list4_R[car_index4r+1])
                    if p2[1] - p1[1] == UNIT:
                        reward -= 1
                    else:
                        break
                    car_index4r += 1
        # print(reward)
        t1 = self.canvas.gettags(self.light1)
        t2 = self.canvas.gettags(self.light2)
        t3 = self.canvas.gettags(self.light3)
        t4 = self.canvas.gettags(self.light4)
        # check the time of yellow light: if the time is 3 then change the light to be red
        if self.yellow_time == 3:
            if t1[0] == 'y':
                self.delay = 0
                self.light1 = self.canvas.create_rectangle(
                    (MAP_H/2-3)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2-4)*UNIT,(MAP_W/2)*UNIT, fill='red',tags='r'
                    )
                self.light2 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2-4)*UNIT, fill='green',tags='g'
                    )
                self.light3 = self.canvas.create_rectangle(
                    (MAP_H/2+4)*UNIT,(MAP_H/2)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2+3)*UNIT, fill='red',tags='r'
                    )
                self.light4 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2+4)*UNIT,(MAP_W/2-3)*UNIT,(MAP_W/2+3)*UNIT, fill='red',tags='r'
                    )
            elif t2[0] == 'y':
                self.delay = 0
                self.light1 = self.canvas.create_rectangle(
                    (MAP_H/2-3)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2-4)*UNIT,(MAP_W/2)*UNIT, fill='red',tags='r'
                    )
                self.light2 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2-4)*UNIT, fill='red',tags='r'
                    )
                self.light3 = self.canvas.create_rectangle(
                    (MAP_H/2+4)*UNIT,(MAP_H/2)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2+3)*UNIT, fill='green',tags='g'
                    )
                self.light4 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2+4)*UNIT,(MAP_W/2-3)*UNIT,(MAP_W/2+3)*UNIT, fill='red',tags='r'
                    )
            elif t3[0] == 'y':
                self.delay = 0
                self.light1 = self.canvas.create_rectangle(
                    (MAP_H/2-3)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2-4)*UNIT,(MAP_W/2)*UNIT, fill='red',tags='r'
                    )
                self.light2 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2-4)*UNIT, fill='red',tags='r'
                    )
                self.light3 = self.canvas.create_rectangle(
                    (MAP_H/2+4)*UNIT,(MAP_H/2)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2+3)*UNIT, fill='red',tags='r'
                    )
                self.light4 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2+4)*UNIT,(MAP_W/2-3)*UNIT,(MAP_W/2+3)*UNIT, fill='green',tags='g'
                    )
            elif t4[0] == 'y':
                self.delay = 0
                self.light1 = self.canvas.create_rectangle(
                    (MAP_H/2-3)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2-4)*UNIT,(MAP_W/2)*UNIT, fill='green',tags='g'
                    )
                self.light2 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2-4)*UNIT, fill='red',tags='r'
                    )
                self.light3 = self.canvas.create_rectangle(
                    (MAP_H/2+4)*UNIT,(MAP_H/2)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2+3)*UNIT, fill='red',tags='r'
                    )
                self.light4 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2+4)*UNIT,(MAP_W/2-3)*UNIT,(MAP_W/2+3)*UNIT, fill='red',tags='r'
                    )

        if action == 'y':
            # light delay:
            self.yellow_time = 0
            self.delay = 0
            if t1[0] == 'g':
                self.light1 = self.canvas.create_rectangle(
                    (MAP_H/2-3)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2-4)*UNIT,(MAP_W/2)*UNIT, fill='yellow',tags='y'
                    )
                self.light2 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2-4)*UNIT, fill='red',tags='r'
                    )
                self.light3 = self.canvas.create_rectangle(
                    (MAP_H/2+4)*UNIT,(MAP_H/2)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2+3)*UNIT, fill='red',tags='r'
                    )
                self.light4 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2+4)*UNIT,(MAP_W/2-3)*UNIT,(MAP_W/2+3)*UNIT, fill='red',tags='r'
                    )
            elif t2[0] == 'g':
                self.light1 = self.canvas.create_rectangle(
                    (MAP_H/2-3)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2-4)*UNIT,(MAP_W/2)*UNIT, fill='red', tags='r'
                    )
                self.light2 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2-4)*UNIT, fill='yellow', tags='y'
                    )
                self.light3 = self.canvas.create_rectangle(
                    (MAP_H/2+4)*UNIT,(MAP_H/2)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2+3)*UNIT, fill='red',tags='r'
                    )
                self.light4 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2+4)*UNIT,(MAP_W/2-3)*UNIT,(MAP_W/2+3)*UNIT, fill='red',tags='r'
                    )
            elif t3[0] == 'g':
                self.light1 = self.canvas.create_rectangle(
                    (MAP_H/2-3)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2-4)*UNIT,(MAP_W/2)*UNIT, fill='red', tags='r'
                    )
                self.light2 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2-4)*UNIT, fill='red', tags='r'
                    )
                self.light3 = self.canvas.create_rectangle(
                    (MAP_H/2+4)*UNIT,(MAP_H/2)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2+3)*UNIT, fill='yellow', tags='y'
                    )
                self.light4 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2+4)*UNIT,(MAP_W/2-3)*UNIT,(MAP_W/2+3)*UNIT, fill='red',tags='r'
                    )
            elif t4[0] == 'g':
                self.light1 = self.canvas.create_rectangle(
                    (MAP_H/2-3)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2-4)*UNIT,(MAP_W/2)*UNIT, fill='red', tags='r'
                    )
                self.light2 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2-4)*UNIT, fill='red', tags='r'
                    )
                self.light3 = self.canvas.create_rectangle(
                    (MAP_H/2+4)*UNIT,(MAP_H/2)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2+3)*UNIT, fill='red', tags='r'
                    )
                self.light4 = self.canvas.create_rectangle(
                    (MAP_H/2)*UNIT,(MAP_H/2+4)*UNIT,(MAP_W/2-3)*UNIT,(MAP_W/2+3)*UNIT, fill='yellow', tags='y'
                    )


        # sign = 1: road1 (-->right) is green light and others are red
        if t1[0] == 'g':          
            sign = 1
        # sign = 2: road1 (-->right) is yellow light and others are red
        elif t1[0] == 'y':
            sign = 2
        # sign = 3: road2 (-->down) is green light and others are red
        elif t2[0] == 'g':
            sign = 3
        # sign = 4: road2 (-->down) is yellow light and others are red
        elif t2[0] == 'y':
            sign = 4
        # sign = 5: road3 (-->left) is green light and others are red 
        elif t3[0] == 'g':
            sign = 5
        # sign = 6: road3 (-->left) is yellow light and others are red 
        elif t3[0] == 'y':
            sign = 6
        # sign = 7: road4 (-->up) is green light and others are red 
        elif t4[0] == 'g':
            sign = 7
        # sign = 8: road4 (-->up) is yellow light and others are red 
        elif t4[0] == 'y':
            sign = 8


        
        # time step:
        if self.time == WHOLE_PERIOD:
            done = True
        else:
            done = False 

        # light delay time. NEED to be change to 6       
        if self.delay>6:
            d = 6
        else:
            d = self.delay

        return [int(distance1),int(distance2),int(distance3),int(distance4),sign,d], reward, done
            # , self.time, self.delay

    # car goes straight
    def cars_append1(self):
        cars1 = self.canvas.create_rectangle(
            0, (MAP_H/2-2)*UNIT,UNIT,(MAP_H/2-1)*UNIT, fill='white', tags='w'
            )
        self.list1.append(cars1)

    def cars_append2(self):
        cars2 = self.canvas.create_rectangle(
            (MAP_W/2+1)*UNIT, 0, (MAP_W/2+2)*UNIT, UNIT, fill='white', tags='w'
            )
        self.list2.append(cars2)

    def cars_append3(self):
        cars3 = self.canvas.create_rectangle(
            (MAP_W)*UNIT, (MAP_H/2+1)*UNIT,(MAP_W-1)*UNIT,(MAP_H/2+2)*UNIT, fill='white', tags='w'
            )
        self.list3.append(cars3)

    def cars_append4(self):
        cars4 = self.canvas.create_rectangle(
            (MAP_W/2-2)*UNIT, (MAP_H)*UNIT,(MAP_W/2-1)*UNIT,(MAP_H-1)*UNIT, fill='white', tags='w'
            )
        self.list4.append(cars4)
    # left and right
    def cars_append1_L(self):
        cars1_L = self.canvas.create_rectangle(
            0, (MAP_H/2-3)*UNIT,UNIT,(MAP_H/2-2)*UNIT, fill='white', tags='w'
            )
        self.list1_L.append(cars1_L)

    def cars_append1_R(self):
        cars1_R = self.canvas.create_rectangle(
            0, (MAP_H/2-1)*UNIT,UNIT,(MAP_H/2)*UNIT, fill='white', tags='w'
            )
        self.list1_R.append(cars1_R)

    def cars_append2_L(self):
        cars2_L = self.canvas.create_rectangle(
            (MAP_W/2+2)*UNIT, 0, (MAP_W/2+3)*UNIT, UNIT, fill='white', tags='w'
            )
        self.list2_L.append(cars2_L)

    def cars_append2_R(self):
        cars2_R = self.canvas.create_rectangle(
            (MAP_W/2)*UNIT, 0, (MAP_W/2+1)*UNIT, UNIT, fill='white', tags='w'
            )
        self.list2_R.append(cars2_R)

    def cars_append3_L(self):
        cars3_L = self.canvas.create_rectangle(
            (MAP_W)*UNIT, (MAP_H/2+2)*UNIT,(MAP_W-1)*UNIT,(MAP_H/2+3)*UNIT, fill='white', tags='w'
            )
        self.list3_L.append(cars3_L)

    def cars_append3_R(self):
        cars3_R = self.canvas.create_rectangle(
            (MAP_W)*UNIT, (MAP_H/2)*UNIT,(MAP_W-1)*UNIT,(MAP_H/2+1)*UNIT, fill='white', tags='w'
            )
        self.list3_R.append(cars3_R)

    def cars_append4_L(self):
        cars4_L = self.canvas.create_rectangle(
            (MAP_W/2-3)*UNIT, (MAP_H)*UNIT,(MAP_W/2-2)*UNIT,(MAP_H-1)*UNIT, fill='white', tags='w'
            )
        self.list4_L.append(cars4_L)

    def cars_append4_R(self):
        cars4_R = self.canvas.create_rectangle(
            (MAP_W/2-1)*UNIT, (MAP_H)*UNIT,(MAP_W/2)*UNIT,(MAP_H-1)*UNIT, fill='white', tags='w'
            )
        self.list4_R.append(cars4_R)



    def render(self):
        self.time += 1
        self.delay += 1
        self.yellow_time += 1
        # move cars which in road 1
        for car_index1 in range(len(self.list1)):
            p = self.canvas.coords(self.list1[car_index1])
            t1 = self.canvas.gettags(self.light1)
            if (p[0] == self.canvas.coords(self.light1)[0]) and (t1[0] == 'r'):
                continue
            elif (len(self.list1) >= 2) and (car_index1 != 0):
                p_pre = self.canvas.coords(self.list1[car_index1-1])
                if p_pre[0] != p[0] + UNIT:
                    self.canvas.move(self.list1[car_index1],UNIT,0)
            else:
                # print(car_index1,len(self.list1))
                self.canvas.move(self.list1[car_index1],UNIT,0)
        # delete the car which is out of bound
        if len(self.list1) > 0:
            p = self.canvas.coords(self.list1[0])
            if p[0] > MAP_W*UNIT:
                self.list1 = self.list1[1:]

        # move cars which in road 2
        for car_index2 in range(len(self.list2)):
            p = self.canvas.coords(self.list2[car_index2])
            t2 = self.canvas.gettags(self.light2)
            if (p[1] == self.canvas.coords(self.light2)[1]) and (t2[0] == 'r'):
                continue
            elif (len(self.list2) >= 2) and (car_index2 != 0):
                p_pre = self.canvas.coords(self.list2[car_index2-1])
                if p_pre[1] != p[1] + UNIT:
                    self.canvas.move(self.list2[car_index2],0,UNIT)
            else:
                self.canvas.move(self.list2[car_index2],0,UNIT)
                    # delete the car which is out of bound
        if len(self.list2) > 0:
            p = self.canvas.coords(self.list2[0])
            if p[1] > MAP_H*UNIT:
                self.list2 = self.list2[1:]

        # move cars which in road 3
        for car_index3 in range(len(self.list3)):
            p = self.canvas.coords(self.list3[car_index3])
            t3 = self.canvas.gettags(self.light3)
            if (p[0] == self.canvas.coords(self.light3)[0]) and (t3[0] == 'r'):
                continue
            elif (len(self.list3) >= 2) and (car_index3 != 0):
                p_pre = self.canvas.coords(self.list3[car_index3-1])
                if p_pre[0] != p[0] - UNIT:
                    self.canvas.move(self.list3[car_index3],-UNIT,0)
            else:
                self.canvas.move(self.list3[car_index3],-UNIT,0)
                    # delete the car which is out of bound
        if len(self.list3) > 0:
            p = self.canvas.coords(self.list3[0])
            if p[0] < 0:
                self.list3 = self.list3[1:]

        # move cars which in road 4
        for car_index4 in range(len(self.list4)):
            p = self.canvas.coords(self.list4[car_index4])
            t4 = self.canvas.gettags(self.light4)
            if (p[1] == self.canvas.coords(self.light4)[1]) and (t4[0] == 'r'):
                continue
            elif (len(self.list4) >= 2) and (car_index4 != 0):
                p_pre = self.canvas.coords(self.list4[car_index4-1])
                if p_pre[1] != p[1] - UNIT:
                    self.canvas.move(self.list4[car_index4],0,-UNIT)
            else:
                self.canvas.move(self.list4[car_index4],0,-UNIT)
                    # delete the car which is out of bound
        if len(self.list4) > 0:
            p = self.canvas.coords(self.list4[0])
            if p[1] < 0:
                self.list4 = self.list4[1:]

        # move cars which in road 1 -- turn left
        t1 = self.canvas.gettags(self.light1)
        pl = self.canvas.coords(self.light1)
        for car_index1l in range(len(self.list1_L)):
            # print(car_index1l)
            p = self.canvas.coords(self.list1_L[car_index1l])
            if (p[0] == self.canvas.coords(self.light1)[0]) and (t1[0] == 'r'):
                continue
            elif p[0] - pl[0] >= 2 * UNIT:
                
                self.canvas.move(self.list1_L[car_index1l],0,-UNIT)
            elif (len(self.list1_L) >= 2) and (car_index1l != 0):
                p_pre = self.canvas.coords(self.list1_L[car_index1l-1])
                if p_pre[0] != p[0] + UNIT or p_pre[1] != p[1]:
                    self.canvas.move(self.list1_L[car_index1l],UNIT,0)
            else:
                # print(car_index1,len(self.list1))
                self.canvas.move(self.list1_L[car_index1l],UNIT,0)
        # delete the car which is out of bound
        if len(self.list1_L) > 0:
            p = self.canvas.coords(self.list1_L[0])
            if p[1] < 0:
                self.list1_L = self.list1_L[1:]

        # move cars which in road 1 -- turn right
        t1 = self.canvas.gettags(self.light1)
        pl = self.canvas.coords(self.light1)
        for car_index1r in range(len(self.list1_R)):
            p = self.canvas.coords(self.list1_R[car_index1r])
            if (p[0] == self.canvas.coords(self.light1)[0]) and (t1[0] == 'r'):
                continue
            elif p[0] - pl[0] >= 5 * UNIT:                
                self.canvas.move(self.list1_R[car_index1r],0,UNIT)
            elif (len(self.list1_R) >= 2) and (car_index1r != 0):
                p_pre = self.canvas.coords(self.list1_R[car_index1r-1])
                if p_pre[0] != p[0] + UNIT or p_pre[1] != p[1]:
                    self.canvas.move(self.list1_R[car_index1r],UNIT,0)
            else:
                self.canvas.move(self.list1_R[car_index1r],UNIT,0)
        # delete the car which is out of bound
        if len(self.list1_R) > 0:
            p = self.canvas.coords(self.list1_R[0])
            if p[1] > MAP_H*UNIT:
                self.list1_R = self.list1_R[1:]

        # move cars which in road 2 -- turn left
        t2 = self.canvas.gettags(self.light2)
        pl = self.canvas.coords(self.light2)
        for car_index2l in range(len(self.list2_L)):
            # print(car_index2l)
            p = self.canvas.coords(self.list2_L[car_index2l])
            if (p[1] == self.canvas.coords(self.light2)[1]) and (t2[0] == 'r'):
                continue
            elif p[1] - pl[1] >= 2 * UNIT:
                self.canvas.move(self.list2_L[car_index2l],UNIT,0)
            elif (len(self.list2_L) >= 2) and (car_index2l != 0):
                p_pre = self.canvas.coords(self.list2_L[car_index2l-1])
                if p_pre[1] != p[1] + UNIT or p_pre[0] != p[0]:
                    self.canvas.move(self.list2_L[car_index2l],0,UNIT)
            else:
                # print(car_index1,len(self.list1))
                self.canvas.move(self.list2_L[car_index2l],0,UNIT)
        # delete the car which is out of bound
        if len(self.list2_L) > 0:
            p = self.canvas.coords(self.list2_L[0])
            if p[0] > MAP_W*UNIT:
                self.list2_L = self.list2_L[1:]

        # move cars which in road 2 -- turn right
        t2 = self.canvas.gettags(self.light2)
        pl = self.canvas.coords(self.light2)
        for car_index2r in range(len(self.list2_R)):
            # print(car_index2r)
            p = self.canvas.coords(self.list2_R[car_index2r])
            if (p[1] == self.canvas.coords(self.light2)[1]) and (t2[0] == 'r'):
                continue
            elif p[1] - pl[1] >= 5 * UNIT:     
                self.canvas.move(self.list2_R[car_index2r],-UNIT,0)
            elif (len(self.list2_R) >= 2) and (car_index2r != 0):
                p_pre = self.canvas.coords(self.list2_R[car_index2r-1])
                if p_pre[1] != p[1] + UNIT or p_pre[0] != p[0]:
                    self.canvas.move(self.list2_R[car_index2r],0,UNIT)
            else:
                # print(car_index1,len(self.list1))
                self.canvas.move(self.list2_R[car_index2r],0,UNIT)
        # delete the car which is out of bound
        if len(self.list2_R) > 0:
            p = self.canvas.coords(self.list2_R[0])
            if p[0] < 0:
                self.list2_R = self.list2_R[1:]


        # move cars which in road 3 -- turn left
        t3 = self.canvas.gettags(self.light3)
        pl = self.canvas.coords(self.light3)
        for car_index3l in range(len(self.list3_L)):
            # print(car_index1l)
            p = self.canvas.coords(self.list3_L[car_index3l])
            if (p[0] == self.canvas.coords(self.light3)[0]) and (t3[0] == 'r'):

                continue
            elif pl[0] - p[0] >= 2 * UNIT:
                self.canvas.move(self.list3_L[car_index3l],0,UNIT)
            elif (len(self.list3_L) >= 2) and (car_index3l != 0):
                p_pre = self.canvas.coords(self.list3_L[car_index3l-1])
                if p_pre[0] != p[0] - UNIT or p_pre[1] != p[1]:

                    self.canvas.move(self.list3_L[car_index3l],-UNIT,0)
            else:
                # print(car_index1,len(self.list1))

                self.canvas.move(self.list3_L[car_index3l],-UNIT,0)
        # delete the car which is out of bound
        if len(self.list3_L) > 0:
            p = self.canvas.coords(self.list3_L[0])
            if p[1] > MAP_H*UNIT:
                self.list3_L = self.list3_L[1:]


       # move cars which in road 3 -- turn left
        t3 = self.canvas.gettags(self.light3)
        pl = self.canvas.coords(self.light3)
        for car_index3r in range(len(self.list3_R)):
            # print(car_index1l)
            p = self.canvas.coords(self.list3_R[car_index3r])
            if (p[0] == self.canvas.coords(self.light3)[0]) and (t3[0] == 'r'):

                continue
            elif pl[0] - p[0] >= 5 * UNIT:
                self.canvas.move(self.list3_R[car_index3r],0,-UNIT)
            elif (len(self.list3_R) >= 2) and (car_index3r != 0):
                p_pre = self.canvas.coords(self.list3_R[car_index3r-1])
                if p_pre[0] != p[0] - UNIT or p_pre[1] != p[1]:

                    self.canvas.move(self.list3_R[car_index3r],-UNIT,0)
            else:
                # print(car_index1,len(self.list1))

                self.canvas.move(self.list3_R[car_index3r],-UNIT,0)
        # delete the car which is out of bound
        if len(self.list3_R) > 0:
            p = self.canvas.coords(self.list3_R[0])
            if p[1] < 0:
                self.list3_R = self.list3_R[1:]


        # move cars which in road 4 -- turn left
        t4 = self.canvas.gettags(self.light4)
        pl = self.canvas.coords(self.light4)
        for car_index4l in range(len(self.list4_L)):
            # print(car_index2l)
            p = self.canvas.coords(self.list4_L[car_index4l])
            if (p[1] == self.canvas.coords(self.light4)[1]) and (t4[0] == 'r'):
                continue
            elif pl[1] - p[1] >= 2 * UNIT:
                self.canvas.move(self.list4_L[car_index4l],-UNIT,0)
            elif (len(self.list4_L) >= 2) and (car_index4l != 0):
                p_pre = self.canvas.coords(self.list4_L[car_index4l-1])
                if p_pre[1] != p[1] - UNIT or p_pre[0] != p[0]:
                    self.canvas.move(self.list4_L[car_index4l],0,-UNIT)
            else:
                # print(car_index1,len(self.list1))
                self.canvas.move(self.list4_L[car_index4l],0,-UNIT)
        # delete the car which is out of bound
        if len(self.list4_L) > 0:
            p = self.canvas.coords(self.list4_L[0])
            if p[0] < 0:
                self.list4_L = self.list4_L[1:]

        # move cars which in road 4 -- turn right
        t4 = self.canvas.gettags(self.light4)
        pl = self.canvas.coords(self.light4)
        for car_index4r in range(len(self.list4_R)):
            # print(car_index2r)
            p = self.canvas.coords(self.list4_R[car_index4r])
            if (p[1] == self.canvas.coords(self.light4)[1]) and (t4[0] == 'r'):
                continue
            elif pl[1] - p[1] >= 5 * UNIT:     
                self.canvas.move(self.list4_R[car_index4r],UNIT,0)
            elif (len(self.list4_R) >= 2) and (car_index4r != 0):
                p_pre = self.canvas.coords(self.list4_R[car_index4r-1])
                if p_pre[1] != p[1] - UNIT or p_pre[0] != p[0]:
                    self.canvas.move(self.list4_R[car_index4r],0,-UNIT)
            else:
                # print(car_index1,len(self.list1))
                self.canvas.move(self.list4_R[car_index4r],0,-UNIT)
        # delete the car which is out of bound
        if len(self.list4_R) > 0:
            p = self.canvas.coords(self.list4_R[0])
            if p[0] > MAP_W*UNIT:
                self.list4_R = self.list4_R[1:]


        self.update()


    def reset(self):
        self.update()
        self.canvas.delete(self.road1)
        self.canvas.delete(self.road2)
        # reset the roads
        self.road1 = self.canvas.create_rectangle(
            0, (MAP_H/2-3)*UNIT, MAP_H*UNIT, (MAP_H/2+3)*UNIT, fill='black')
        self.road2 = self.canvas.create_rectangle(
            (MAP_W/2-3)*UNIT, 0, (MAP_W/2+3)*UNIT, MAP_W*UNIT, fill='black')

        # reset the traffic light
        self.light1 = self.canvas.create_rectangle(
            (MAP_H/2-3)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2-4)*UNIT,(MAP_W/2)*UNIT, fill='green',tags='g'
            )
        self.light2 = self.canvas.create_rectangle(
            (MAP_H/2)*UNIT,(MAP_H/2-3)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2-4)*UNIT, fill='red', tags='r'
            )
        self.light3 = self.canvas.create_rectangle(
            (MAP_H/2+4)*UNIT,(MAP_H/2)*UNIT,(MAP_W/2+3)*UNIT,(MAP_W/2+3)*UNIT, fill='red', tags='r'
            )
        self.light4 = self.canvas.create_rectangle(
            (MAP_H/2)*UNIT,(MAP_H/2+4)*UNIT,(MAP_W/2-3)*UNIT,(MAP_W/2+3)*UNIT, fill='red', tags='r'
            )

        # reset the car list
        self.list1 = []
        self.list2 = []
        self.list3 = []
        self.list4 = []
        self.list1_L = []
        self.list1_R = []
        self.list2_L = []
        self.list2_R = []
        self.list3_L = []
        self.list3_R = []
        self.list4_L = []
        self.list4_R = []

        return [9,9,9,9,2,0]

def flash():
    # time = 0
    for i in range(10):
        env.reset()
    r1 = rnd
    r2 = rnd
    r1.seed(1)
    r2.seed(2)
    while True:
        env.render()
        # delay += 1
        # rnd.seed(1)
        time.sleep(0.1)
        if env.time%(r1.randint(0,10)+5) == 0:
            choose_road = r2.randint(1,13)
            if choose_road == 1:
                env.cars_append1()
            if choose_road == 2:
                env.cars_append1_L()
            if choose_road == 3:
                env.cars_append1_R()
            if choose_road == 4:
                env.cars_append2()
            if choose_road == 5:
                env.cars_append2_L()
            if choose_road == 6:
                env.cars_append2_R()
            if choose_road == 7:
                env.cars_append3()
            if choose_road == 8:
                env.cars_append3_L()
            if choose_road == 9:
                env.cars_append3_R()
            if choose_road == 10:
                env.cars_append4()
            if choose_road == 11:
                env.cars_append4_L()
            if choose_road == 12:
                env.cars_append4_R()
        # if env.time%(rnd.randint(0,10)+5) == 1:
        #     env.cars_append3()
        # if env.time%(rnd.randint(0,10)+5) == 0:
        #     env.cars_append4()
        if env.time%50 == 0:
             env.switch_light('y')
        else:
            env.switch_light('n')
                # delay = 0
            # print(env.time)



if __name__ == '__main__':
    env = Map()
    flash()
    env.mainloop()

 