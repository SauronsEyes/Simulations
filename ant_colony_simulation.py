import pygame
import random
#---------------| Controls |---------------
#------|  => Key : Increase Speed   |------
#------|  <= Key : Decrease Speed   |------
#------|  Mouse Click: Add Food Src |------
#------------------------------------------

#Pygame Initialization
windx = 800
windy = 600
pygame.init()
displayWin = pygame.display.set_mode((windx,windy))
clock = pygame.time.Clock()
windowOpen = True;

#Color Definition for Pygame
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
blue= (0,0,255)

#initial ant base position
antbasex = 400
antbasey = 300

#ants array of dictionary with antInfo
ants=[]

#Array of Food Position
foodx =[100,700]
foody =[100,500]

#Array with index of ants who found food
foodfound =[]

#Speed /  FPS
speed = 30

#No. of Ants in Simulation
nants = 100

#Generate Ants
for i in range(0,nants):
    antInfo = {
            'aposx' : antbasex,#Ant X-Position
            'aposy' : antbasey,#Ant Y-Position
            'foodFound' : False,#Has the Ant found food?
            'oldPosx' : [],#Array for storing old x-position to remember old path so that ant can return home and goto food
            'oldPosy' : [],#Array for storing old y-position
            'randx' : (2*random.random() -1), #Random X-Direction Change 
            'randy' : (2*random.random() -1), #Randomize Y-Direction Change 
            'dchangeTime' : random.randint(30,90), #Ant Changes Direction in x-seconds
            'dchange' : 0, #Time Spent after changing direction
            'backTrack' : 0, #Index of Old Position - Used after ant finds food and returns home
            'btrackChange' : -1 #Change in Index - (-1) means ant is returning home +1 means ant is going for food
            
            
        }
    ants.append(antInfo)
    
while windowOpen:
    #Clear Screen
    displayWin.fill(black)
    
    #Loop through all ants
    for i in range(0,len(ants)):
         tempx = ants[i]['aposx']
         tempy = ants[i]['aposy'] 
         col = red
         if(not ants[i]['foodFound']):
             #Check Distance of all ant with all food source
             for g in range(0,len(foodx)):
                 timeDir = ants[i]['dchange']
                 ants[i]['dchange'] = timeDir + 1 #add 1 to time spent by ant after changing direction
                 fdistance = (((tempx-foodx[g])**2)+((tempy-foody[g])**2))**0.5 #Distance Formula
                 #if food is at 50 distance from ant the ant starts moving towards food
                 if(fdistance<50):
                     #Check difference in distance
                     ffarx = foodx[g] - tempx 
                     ffary = foodx[g] - tempy
                     #move ant towards food
                     if(ffarx>0):
                         ants[i]['randx'] = random.random()
                     if(ffarx<0):
                         ants[i]['randx'] = -random.random()
                     if(ffary>0):
                         ants[i]['randy'] = random.random()
                     if(ffary<0):
                         ants[i]['randy'] = -random.random()
                #If distance is less than 20 food is found
                 if(fdistance<20):
                     ants[i]['foodFound'] =  True #Set Food Found for ant to true
                     foodfound.append(i) #Append it to foodfound for futher computation
                     ants[i]['backTrack'] = len(ants[i]['oldPosx'])-1 #Hard to explain - sets backTrack to the last index so that the ant start moving from the last xy-position to initial xy-position
                 
            #Change Direction of ants after dchangeTime sec
             if(timeDir >= ants[i]['dchangeTime']):
                 ants[i]['randx'] = (2*random.random() -1)
                 ants[i]['randy'] = (2*random.random() -1)
                 ants[i]['dchange'] = 0 #Initialize dchange
             
         
         
         #Conditions if ant has found food 
         if(ants[i]['foodFound']):
            #This is for moving ants who have found food from food to home and vice versa
             btrack = ants[i]['backTrack']
             #Uncomment for food trail path after finding food
             #for l in range(0,len(ants[i]['oldPosx'])):
                  #pygame.draw.circle(displayWin, white, (ants[i]['oldPosx'][l],ants[i]['oldPosy'][l]), 1)
             if(btrack == 0):
                 ants[i]['btrackChange'] = 1 #moving towards food
             elif(btrack == (len(ants[i]['oldPosx'])-1)):
                 ants[i]['btrackChange'] = -1 #moving towards home
                 
             ants[i]['aposx'] = ants[i]['oldPosx'][btrack]
             ants[i]['aposy'] = ants[i]['oldPosy'][btrack]
             ants[i]['backTrack'] = btrack + ants[i]['btrackChange']
             col =green
                 
         else:
             #condition If ant has not found food
             
             #This checks distance of ant from other ants who have found food and borrows information about if other ants are nearby
             for m in range(0,len(foodfound)):
                 #Position of ant who has found food
                 oax = ants[foodfound[m]]['aposx'] 
                 oay = ants[foodfound[m]]['aposy']
                 #Distance of this ant from that other ant who has found food source
                 adistance = (((tempx-oax)**2)+((tempy-oay)**2))**0.5
                 if(adistance<5):
                         
                         ants[i]['foodFound']= True #Set Food Found for this ant to true
                         #Borrows trail Path from ant who has found food
                         ants[i]['oldPosx']= ants[foodfound[m]]['oldPosx'] 
                         ants[i]['oldPosy']= ants[foodfound[m]]['oldPosy']
                         #Move ant towards food
                         ants[i]['backTrack']= ants[foodfound[m]]['backTrack']
                         ants[i]['btrackChange'] = 1
                         
            #This changes direction of ant if it is moving out of bounds
            
             tempxcalc = tempx + ants[i]['randx']
             tempycalc = tempy + ants[i]['randy']
             #Check if it is moving out of bound in x-axis - change direction if so
             if(tempxcalc<0):
                  ants[i]['randx'] = random.random()
             elif(tempxcalc>windx):
                  ants[i]['randx'] = -random.random()  
             #Check if it is moving out of bounds in y-axis
             if(tempycalc<0):
                  ants[i]['randy'] = random.random()
             elif(tempycalc>windy):
                  ants[i]['randy'] = -random.random()
            #Move Ant
             ants[i]['aposx'] = tempxcalc 
             ants[i]['aposy'] = tempycalc
             #Append Current Position to array to create a path
             ants[i]['oldPosx'].append(tempx)
             ants[i]['oldPosy'].append(tempy)
         #Draw Ant
         pygame.draw.circle(displayWin, col, (tempx,tempy), 1)
    #Draw Base
    pygame.draw.circle(displayWin, blue, (antbasex,antbasey), 15) 
    #Draw All food source
    for f in range(0,len(foodx)):
        pygame.draw.circle(displayWin, green, (foodx[f],foody[f]), 10) 
    for event in pygame.event.get():
        #Add food on mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            foodx.append(event.pos[0])
            foody.append(event.pos[1])
        if(event.type == pygame.QUIT):
            windowOpen = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed =speed-10 #decrease speed on pressing left key
                
            if event.key == pygame.K_RIGHT:
                speed =speed +10 #increase speed on pressing right key
            print(speed)
            
            
    
    pygame.display.update();
    clock.tick(speed)

pygame.quit()