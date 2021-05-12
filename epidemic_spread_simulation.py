import pygame
import random
import matplotlib.pyplot as plt
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

#Array for storing dictionary with people ingo
peps=[]

#First Patient Definition Dictionary
patient0 ={
        'pepx' : random.randint(0,windx),#Initial X-Position
        'pepy' : random.randint(0,windy),#Initial Y-Position
        'affected' : True,#True for Affected People
        'mask' : bool(random.randint(0,1)) #Mask On? F it Mask off.
    }
peps.append(patient0)

#Number of sample - Healthy People
nsamp = 500
fps = 30 #fps - Speed
#Statistics for graph - Displayed when window is closed
inf = 1
time = 0
plotx = []
ploty =[]

#Generate Random Healthy People
for i in range(0,nsamp):
    
    pepdict = {
        'pepx' : random.randint(0,windx),
        'pepy' : random.randint(0,windy),
        'affected' : False, # False for unaffected people
        'mask' : bool(random.randint(0,1))
    }
    peps.append(pepdict)
    

#This Function Moves People Randomly. Checks Covid Condition and assigns affected as per chances    
def movePepsRandom():
    global peps
    global inf
    #Loop through peps array
    for j in range(0,len(peps)):
        changex = ((2*random.random())-1)*4 #Random Change in X Position (Equation used (2x-1)*c. Generates value from -c to +c)
        changey = ((2*random.random())-1)*4
       
        px = peps[j]['pepx']
        py = peps[j]['pepy']
        pmask = peps[j]['mask']
        
        if(peps[j]['affected']):
            #Draw Red Circle for affected people
            pygame.draw.circle(displayWin,red,(px,py),2,0)
            
            for l in range(0,len(peps)):
                chance = 0#Initialize Chance of Being Affected
                hmask =peps[l]['mask']
                
                if(not peps[l]['affected']):
                    distance=100#Initialize Distance
                    
                    #Calculate Distance between unaffected person and affected Person
                    
                    #Use Circular Collider For Better Accuracy
                    #distance = (((peps[l]['pepx']-px)**2)+((peps[l]['pepy']-py))**2)**0.5
                    
                    #Use Square Collider for Better Performance
                    #Set Estimated Distance -- Not exact -- Based on collision with the square collider
                    if(abs(peps[l]['pepx']-px)<10 and abs(peps[l]['pepy']-py)<10):
                        distance =9
                    if(distance!=10 and abs(peps[l]['pepx']-px)<20 and abs(peps[l]['pepy']-py)<20):
                        distance =13
                   
                    #Set Chances based on covid conditions
                    #Chances Condition based on https://www.westsideseattle.com/sites/default/files/images/%5Bdomain-url%5D/%5Bnode-yyyy%5D/%5Bnode-mm%5D/face_mask_graphic.jpg
                    if(distance<=10):
                           if(pmask == False and hmask == False):
                               chance =95
                              
                           if(pmask==False and hmask==True):
                               chance=80
                           elif(pmask==True and hmask ==False):
                               chance =60
                           elif(pmask ==True and hmask == True):
                               chance =40
                    elif(distance<20 and distance>10):
                        chance = 20
                    else:
                        chance = 0
                    
                    #Luck
                    luck = random.randint(0,100)
                    if(luck<chance):
                        peps[l]['affected'] = True
                        inf = inf + 1
        else:
            #Draw Green Dot for healthy people
            pygame.draw.circle(displayWin,green,(px,py),2,0)
        #Change position of people if they donot overflow the screen size
        if((px+changex)<windx and (px+changex)>0 and (py+changey)<windy and (py+changey)>0  ):
            peps[j]['pepx'] = px +  changex
            peps[j]['pepy'] = py +  changey
           
            
        
while windowOpen:
    
    displayWin.fill(black)#CleanScreen - Fill black
    movePepsRandom()
    
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            windowOpen = False;
    time =time+(1/fps)     
    plotx.append(time)
    ploty.append(inf)
    pygame.display.update();
    clock.tick(fps)#FPS - Change this for speed 
    
pygame.quit()
#Display Final Plot
plt.plot(plotx,ploty)
plt.show()
    
    



    

    