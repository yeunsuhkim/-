#ball
global y, ydir
x = 300
y= 300
xdir = 7.5
ydir = 10
diam = 20

#pad
padX=0
padY=0
padWidth=200
padHeight=20

#life item
life=5
lifeappear=False
lifeappear=True
heartX=490
heartY=30    

#item
item_Data = dict()
itemappear=True
i=1

#target item
targetUse=False
make=0

#bigger item
biggerUse=False
startTime_bigger=False

#bomb item
bombUse=False

#savior item
saviorUse=False
saviorStacked=0

#Alarm
alarmMessage=False
alarm=""
alarmR=0
alarmG=0
startTime=False

#bricks
box_where = dict()
brick_generate=True
p=160
q=-1000
leng=50
t=0
brick=0
deadBrick=0
down_velocity=0.2

#combo
combo_time=0
combo_nowCheck=0
combo_plus=0
colliding=False
combo_lighting1=255
combo_lighting2=255
combo_lighting3=255
other_lighting1=255
other_lighting2=255
other_lighting3=255


#etc events
DEAD=False
score=0
Resume=False
START=True


#collision checking function

def collide(posX,posY,posL,posH):
    global combo_time,colliding
    if x+diam/2 >= posX and x+diam/2 <= posX + posL and y - diam/2 <= posY+posH and y-diam/2>=posY:
        combo_time=millis()
        colliding=True
        return True
    
    
#highscore checking&save function

def highscoreCheck():
    global score, highscore
    for g in range(0,2):
        if int(highscore[1-g])>score>=int(highscore[2-g]):
            highscore[2-g]=str(score) 
            fill(255,255,0)
            text("Your score is "+str(3-g)+" place!",360,620)
    if int(highscore[0])<score:
        highscore[0]=str(score)
        fill(255,0,0)
        text("You made a new HIGHSCORE!!",250,620)
    saveStrings("highscore.txt", highscore)   



def setup():
    global padY,padHeight, heart,alive,dead,box_where,s,pause,exiT,s2,mush,bomb,savior,aim,help,highscore
    
    pause=loadImage("pause.png")
    exiT=loadImage("exiT.png")
    help=loadImage("help.png")
    aim=loadImage("target.png")
    mush=loadImage("mushy.png")
    bomb=loadImage("bomb.png")
    savior=loadImage("timer.png")
    heart=loadImage("heart.png")

    size(1040,1000)
    padY = height - padHeight
    item_Data['0']={'x':400, 'y':20, 'item': aim} #make one target item for start
    
    imageMode(CORNER)
    rectMode(CORNER)
    s=millis()
    s2=millis()
    strokeWeight(5)
    strokeJoin(MITER)
    
    highscore = loadStrings("highscore.txt")
    
    noLoop()
    
'''if you want to see the highscore event, edit highscore.txt. 
ex) 3850 => 1000 
    2430 => 500 
    2000 => 10'''
    

    
def draw():
    global x,y, ydir, xdir, diam # ball
    global padX, padY, padWidth, padHeight # pad
    global life, i,lifeappear,heartX, heartY, s, s2, s3,biggerUse,saviorStacked,itemappear,item_Data,targetUse,bombUse, saviorUse,startTime_bigger #item event
    global alarm,alarmMessage,startTime,s4 # alarm events
    global p,q,leng,t,brick_generate,brick,last,combo_time,combo_nowCheck,combo_plus,colliding,deadBrick,down_velocity # brick
    global combo_lighting1,combo_lighting2,combo_lighting3,other_lighting1,other_lighting2,other_lighting3,alarmR,alarmG # coloring
    global score,Resume, DEAD,highscore,START # big events
    global pause,exiT,bomb,savior,mush,aim,heart,help # images

    stroke(0)
    background(0)
    fill(255)
    
    
    #Check left life
    
    if life<=0:
       DEAD=True
       
       
    #brick xyz generating event 
    
    while brick_generate:
           leng=random(50, 100)
           box_where[str(t)]={'x':p, 'y':q, 'lenth':leng, 'Show':True}
           p+=leng
           
           if box_where[str(t)]['x']+leng>960:
             if q<=50:
               if q==50:
                   last = t+1
               q+=50
               p=160
               box_where[str(t)]['lenth']-=box_where[str(t)]['x']+leng-960
               
               if box_where[str(t)]['lenth']<=30:
                   box_where[str(t-1)]['lenth']+=box_where[str(t)]['lenth']
                   del box_where[str(t)]
                   t-=1
                   
             else:
               q=0
               t-=1
               brick_generate=False
               
           t+=1  
  

    #brick drawing  
    
    for brick in box_where:
          if box_where[str(brick)]['Show']==True:
             fill(other_lighting1,other_lighting2,other_lighting3)
             rect(box_where[str(brick)]['x'],box_where[str(brick)]['y'],box_where[str(brick)]['lenth'],50)
             
             if collide(box_where[str(brick)]['x'],box_where[str(brick)]['y'],box_where[str(brick)]['lenth'],50):
                 
                 deadBrick+=1
                 
                 if box_where[str(brick)]['x']+diam/2<x<=box_where[str(brick)]['x']+box_where[str(brick)]['lenth']-diam/2: #ball collide brick from down or up
                    y+=2
                    ydir*=-1
                    
                 elif box_where[str(brick)]['y']+diam/2<y<box_where[str(brick)]['y']+50-diam/2: #ball collide brick from left or right
                    xdir*=-1
                
                 else: # ball collide at brick's one of four corners
                    bounce=int(random(3))
                    
                    if bounce==1:
                        xdir*=-1
                        
                    elif bounce==2:
                        ydir*=-1
                        
                    else:
                        xdir*=-1
                        ydir*=-1
                        
                 box_where[str(brick)]['Show']=False
                 score+=10
             
             if box_where[str(brick)]['y']+50>height:
                 
                 #if there is stacked savior item, even though brick touches the bottom, you live.
                 
                 if saviorStacked>0:
                     box_where[str(brick)]['Show']=False
                     deadBrick+=1
                     saviorStacked-=1
                     alarmR=255
                     alarmG=255
                     alarm="Savior item to the rescue! You live!"
                     startTime=True
                     alarmMessage=True
                 
                 else:
                    DEAD=True
             
             box_where[str(brick)]['y']+=down_velocity
     
             
    #combo checking                         
    
    combo_nowCheck=millis()
    
    if combo_plus>9:
        if 16>combo_plus>9:
            combo_lighting1=255
            other_lighting1=255
            combo_lighting2=255
            other_lighting2=255
            combo_lighting3=0
            other_lighting3=0
        
        if 30>combo_plus>15:
            combo_lighting1=255
            other_lighting1=255
            combo_lighting2=0
            other_lighting2=0
            combo_lighting3=0
            other_lighting3=0
            
        if combo_plus>29:
            combo_lighting1
            other_lighting1=random(255)
            combo_lighting2=random(255)
            other_lighting2=random(255)
            combo_lighting3=random(255)
            other_lighting3=random(255)
        
        noStroke()
        fill(10,50)
        rect(470,5,150,33)
        textSize(20)
        fill(combo_lighting1,combo_lighting2,combo_lighting3)
        text(combo_plus,480,30)
        text("COMBO!",530,30)
        
    if 0<combo_nowCheck-combo_time<600 and colliding:
        combo_plus+=1
        colliding=False
        
    elif combo_nowCheck-combo_time>600:
        if 16>combo_plus>9:
            score+=5*combo_plus  
              
        if 30>combo_plus>15:
            score+=10*combo_plus
            
        if combo_plus>29:
            score+=20*combo_plus
            
        other_lighting1=255
        other_lighting2=255
        other_lighting3=255
        combo_plus=0 
    
        
    #box outline 
    
    noStroke()
    fill(0)
    rect(0,0,160,height)
    rect(960,0,80,height)
    fill(200)
    rect(152,0,8,height)
    rect(961,0,8,height)
    
                                  
    #menu button
        
    imageMode(CORNER)
    image(pause,977,15,50,50)
    image(exiT,977,75,50,50)
    image(help,977,135,50,50)  
    
    #ball drawing
    
    fill(other_lighting1,other_lighting2,other_lighting3)
    ellipse(x,y,diam,diam)
    x=x+xdir
    y=y+ydir
    
    
    #pad drawing and movement
    
    padX=mouseX-padWidth/2
    
    if padX<160:
        padX=163
        
    elif padX>width-100-padWidth:
        padX=757
        
    rect(padX,padY,padWidth,padHeight)
    
    


    # ball bouncing  
      
    if x + diam/2 > width-100:
        xdir = xdir * -1
        x=width-100-diam/2
        
    if y + diam/2 >= height:
        ydir = ydir * -1
        y=height-diam/2
        y-=1
        life-=1
        
    if x - diam/2<160:
        xdir = xdir * -1
        x=160+diam/2
        
    if y - diam/2<0:
        ydir = ydir*-1
        y+=1
        
    if x > padX and x < padX + padWidth and y + diam/2 > padY :
        combo_plus=0   #combo stacked only when it's airborne
        ydir = ydir * -1
        y=height-padHeight-diam/2
        y-=2
       

    # highscore show & life count & score count
    
    textSize(20)
    fill(100)
    text("HIGHSCORE",16,650)
    text("-----------",10,670)
    textSize(27)
    text("[1]"+highscore[0],15,690)
    text("[2]"+highscore[1],15,720)
    text("[3]"+highscore[2],15,750)
    
    fill(255)
    textSize(20)
    text("LIFE :", 12, 35)
    text(life, 72, 35)
    
    fill(combo_lighting1,combo_lighting2,combo_lighting3)
    text("SCORE :", 12, 70)
    text(score, 92, 70)
    combo_lighting1=255
    combo_lighting2=255
    combo_lighting3=255
    
    
    
    # life item - event
    
    if lifeappear:
      image(heart, heartX,heartY, 50, 50)
      heartY+=down_velocity
      
      if collide(heartX, heartY, 50, 50):
         life+=1
         heartX=random(160,925)
         heartY=random(400)
         lifeappear=False
      
            
    # other item generating event 
        
    if itemappear:
        for l in range(1,2):
            item_Data[str(i)]={'x':random(160,920), 'y':random(500), 'item': aim}
            i+=1
            item_Data[str(i)]={'x':random(160,920), 'y':random(500), 'item': mush}
            i+=1
            
            bombMake=int(random(1,4))
            if bombMake==3:
                print("bombmade!")
                item_Data[str(i)]={'x':random(160,920), 'y':random(500), 'item': bomb}
                i+=1
                
            elif bombMake==2:
                item_Data[str(i)]={'x':random(160,920), 'y':random(500), 'item': savior}
                i+=1
                
        itemappear=False
        
        
    # Show items
    
    for make in item_Data:
        item_Data[str(make)]['y']+=down_velocity
        image(item_Data[str(make)]['item'], item_Data[str(make)]['x'],item_Data[str(make)]['y'], 50, 50)
        
        if collide(item_Data[str(make)]['x'], item_Data[str(make)]['y'], 50, 50):
            if item_Data[str(make)]['item']==aim:
                targetUse=True
                
            elif item_Data[str(make)]['item']==mush:
                startTime_bigger=True
                biggerUse=True
                
            elif item_Data[str(make)]['item']==bomb:
                startTime_bomb=True
                bombUse=True
                
            elif item_Data[str(make)]['item']==savior:
                startTime_savior=True
                saviorUse=True
                
            del item_Data[str(make)]
    
    
    # When target item is in use  
             
    if targetUse:
        imageMode(CENTER)
        X=mouseX
        
        if mouseX<160:
            X=185
            
        if mouseX>960:
            X=935
            
        image(aim,X,mouseY,60,60)
    
    
    #when bigger item is used
    
    if biggerUse:
        if startTime_bigger:
            s3=millis()
            if xdir<0:xdir=-8.5
            else:xdir=8.5
            if ydir<0:ydir=-11
            else:ydir=11
            startTime_bigger=False
            
        diam=40
        m2=millis()
        
        if m2>s3+9000:
            diam=20
            if xdir<0:xdir=-7.5
            else:xdir=7.5
            if ydir<0:ydir=-10
            else:ydir=10
            biggerUse=False
    
    
    #when bomb item is used
    
    if bombUse:
        if saviorStacked==0:
            down_velocity+=0.1
            alarm="Brick is getting down faster!"
            
        else:
            saviorStacked-=1
            alarm="Savior item saves you! Bomb eliminated!"
            
        alarmR=255
        alarmG=0
        startTime=True
        alarmMessage=True
        bombUse=False  
            
      
    #when savior item is used        
          
    if saviorUse:
        if down_velocity>=0.2:
            down_velocity-=0.1
            alarm="Brick is getting down slower!"
            
        else:
            saviorStacked+=1
            alarm="Since it's slowest velocity, savior item is stacked!"
            
        startTime=True
        alarmR=0
        alarmG=255
        alarmMessage=True
        saviorUse=False  
            
            
            
    #alarm event
            
    if alarmMessage:
        fill(alarmR,alarmG,0)
        textSize(20)
        if startTime:
            s4=millis()
            startTime=False
        m3=millis()       
        text(alarm,12,95,145,200)   
        if m3>s4+2000:
            alarmMessage=False
    
    
    
    #show stacked savior items  
           
    if saviorStacked>0:
        fill(0,255,0)
        textSize(12)
        text("Savior Saved: ",12,300)
        text(saviorStacked,130,300)      
          
          
    #generate again items
    
    m=millis()  
               
    if m>s+10000:
        s=m
        lifeappear=True
        
    if m>s2+13000:
        s2=m
        itemappear=True
        
     
    #start screen
    if START:
        fill(0)
        rect(0,0,width,height)
        fill(255)
        textSize(50)
        text("PRESS S TO START",300,height/2-10) 
           
    #resume event   
     
    if Resume:  
        loop()
        Resume=False
    
    
    #clear check
    
    if deadBrick==t+1:
        fill(0,200)
        rect(0,0,1040,height)
        textSize(45)
        fill(255)
        text("CLEAR!!",480,height/2-50)   
        text("Your score :", 385, height/2+10)
        text(score, 680, height/2+10)
        text("PRESS ESC TO EXIT", 380, height/2+70)
        highscoreCheck()
        noLoop()
    
    
    #Game over event
    
    if DEAD:
        fill(0,200)
        rect(0,0,1040,height)
        textSize(45)
        fill(255)
        text("GAME OVER",455,height/2-50)   
        text(" Your score :", 385, height/2+10)
        text(score, 680, height/2+10)
        text("PRESS ESC TO EXIT", 380, height/2+70)
        highscoreCheck()
        noLoop()
        
 


def mouseClicked():
    
    global x,y,targetUse
    
    if 977<mouseX and mouseX<1027 and 15<mouseY and mouseY<65:
            noLoop()   
            fill(0,200)
            rect(163,0,800,height)
            textSize(45)
            fill(255)
            text("PAUSED, PRESS S TO RESUME",255,height/2-10)     
                
    elif 977<mouseX and mouseX<1027 and 75<mouseY and mouseY<125:
            exit()
            
    elif 977<mouseX and mouseX<1027 and 135<mouseY and mouseY<185:
            noLoop()   
            fill(0,200)
            rect(0,0,width,height)
            textSize(25)
            textLeading(30)
            fill(255)
            f=220
            text(" "*53+"[GAME HELP]\n\n\nThis is a brick-breaking game.\nPlayer have to break moving bricks before it reaches the bottom line.",10,f,1000,200)
            f=f+140
            text("\nCombo System - Over 10 blocks have to be broken while airborne. 5 more points are given for each combo level. Standard for each level is 10, 15, 30.",10,f,1000,200)            
            f=f+60
            text("\nItems - Heart : Life item. You get one more life 'for your ball'.",10,f,1000,100) 
            f=f+40
            text("\n      - Target : Item that allows you to move your ball to the place you want.",10,f,1000,100)
            f=f+50
            text("\n      - Mushroom : Item that make your ball bigger..and faster!",10,f,1000,100)
            f=f+50 
            text("\n      - Bomb : Bang! Make your brick move down faster.",10,f,1000,100) 
            f=f+50
            text("\n- Savior : Your savior. If stacked, it gives one more chance to you even if brick has touched the bottom. Else, it slows down bricks.",50,f,950,100)  
            f=f+120
            text("\n"+" "*42+"PAUSED, PRESS S TO RESUME",10,f,1000,100)        
            
    if targetUse:
        if 160<mouseX<960:
            x=mouseX
            y=mouseY
            imageMode(CORNER)
            targetUse=False
            
        
def keyPressed():
    redraw()
    global Resume,START
    if key=='s':   
        START=False
        Resume=True 

        
    
        
        
        
        
    
        
