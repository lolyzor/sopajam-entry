'''
Created on Jan 16, 2012

@author: Abdu
'''
import pygame
import pygame.mixer
import random
import os
from HTMLParser import HTMLParser
import mechanize
import re
import thread

pygame.mixer.init(44100, -16, 2, 2048)
pygame.mixer.music.set_volume(0.3)
intro = pygame.mixer.Sound("sound/intro.ogg")
login = pygame.mixer.Sound("sound/login.ogg")
boom = pygame.mixer.Sound("sound/boom.wav")
introstatus,logins,musics = 0,0,0

allchar = map(chr,range(33,125))
bigletters = map(chr, range(65,90))
smallletters = map(chr, range(97,122))
numbers = map(chr,range(48,57))
specialchars = map(chr,range(33,47))+map(chr,range(58,64))+map(chr,range(91,95))+map(chr,range(123,126))

bg1 = pygame.image.load("Bg/1.jpg")
bg2 = pygame.image.load("Bg/2.jpg")
bg3 = pygame.image.load("Bg/3.jpg")
bg4 = pygame.image.load("Bg/4.jpg")
bg5 = pygame.image.load("Bg/5.jpg")
bg6 = pygame.image.load("Bg/6.jpg")
bg7 = pygame.image.load("Bg/7.png")
bg8 = pygame.image.load("Bg/8.png")
bg9 = pygame.image.load("Bg/9.png")
bg10 = pygame.image.load("Bg/10.png")
bg11 = pygame.image.load("Bg/11.png")
bg12 = pygame.image.load("Bg/12.png")
bg13 = pygame.image.load("Bg/13.png")
upload = pygame.image.load("Bg/upload.png")
bglist = [bg1,bg2,bg3,bg4,bg5,bg6,bg7,bg8,bg9,bg10,bg11,bg12,bg13]
introtext = ["You just hacked into SOPA/PIPA support","voting server, you deployed a","script which kills any packet going",
             "through, all you need to do is","to type name of the packet","and you destroy it, stopping the VOTES !"]
currentbg,waiting,waiting2,reached,waiting3,waiting4,waiting5, waiting6 = 0,0,0,0,0,0,0,0
mainmenu = True
game = True
text1 = ""
x1,y1,seconds = 0,0,0
packet,usertype = "",""
userscore,usermissed = 0,10
correctg,level,combo,combomusics,comboacts = 0,0,0,0,0
mousejocker,username = 3,""
players,scores = [],[]
fetchscoress,uoploaded = 0,0

def drawtext(msg,s,t):
    myfont = pygame.font.Font("Font/starcraft.ttf", s) 
    if t == 1:
        myfont = pygame.font.SysFont("Font/starcraft.ttf", s) #drawtext s20,t0, drawtext2 s25,t1, drawtext3 s15t1, drawtext4 s20t1    
    mytext = myfont.render(msg, True, (0,255,100))
    mytext = mytext.convert_alpha()
        
    return mytext

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
def uploadscore(username,userscore):
    global fetchscoress,uploaded
    if not uploaded:
        fetchscoress = 0
        br = mechanize.Browser()
        br.open("http://hspladder.appspot.com/")
        br.select_form(name="score")
        br["author"] = username
        br["score"] = str(userscore)
        res = br.submit()
        print "sucess!"
        uploaded = 1
        #html = res.get_data()
    
def fetchscores():
    global scores,players
    br = mechanize.Browser()
    br.open("http://hspladder.appspot.com/")
    html = br.response().readlines()
    #parse the shit out of it
    html = remove_html_tags(str(html))
    html = "".join(e for e in html if e.isalnum())
    html = html.replace("nbsp", " ")
    html = html.replace("ntttntttAuthorntttScorentttntttntttnttt", "")
    players = html.split("score")
    scores = []
    #exstract scores and delete digits from players
    for el in players:
        #return only digits from strings
        tmp = re.sub("\D", "", el)
        if tmp:
            scores.append(tmp)
        tmp = el.replace(tmp, '')
        tmp = tmp.strip()
        players[players.index(el)] = tmp
    #players and scores are ready
    
    
def drawmainmenu(sc):
    global waiting,currentbg,bglist,reached,waiting2,waiting3,mainmenu,waiting4,text1,x1,y1,seconds
    global packet,introstatus,seconds,logins,musics,waiting5,game
    if currentbg <= 12:
            sc.blit(bglist[currentbg],(0,0))
    waiting +=1
    waiting2 +=1
    waiting3 +=1
    if waiting > 3:
        currentbg+=1
        waiting = 0
    if currentbg>=6 and seconds <=12:
        currentbg = 0
    
    x,y = 25,42
    if waiting2 >=60:
        seconds +=2
        if not introstatus:
            intro.play()
            introstatus = True           
        if seconds > 8 and not logins:
            login.play()
            logins = True
        waiting2 = 0
        if seconds > 14:
            reached +=1
    for i in range(6):
        if i <= reached and seconds >= 13:
            text = drawtext(introtext[i],20,0)
            sc.blit(text,(x,y))
        y+=77
    if waiting3 == 900:
        mainmenu = False
        game = True
        seconds = 0
        
def drawgame(sc):
    global packet,introstatus,seconds,logins,usertype,userscore,musics,waiting5,usermissed,correctg,game
    global waiting4, text1,x1,y1,allchar,smallletters,bigletters,numbers,specialchars,level,combo,combomusic,combomusics
    global comboacts,mousejocker
    
    waiting4 +=1
    waiting5 +=1
    if waiting5 > 30:
        seconds += 1
        waiting5 = 0
    if combo == 5:
        waiting4+=2
    if waiting4 > 90:
        waiting4 = 0
        if not correctg and packet:
            if combo != 5:
                usermissed -=1
                combo = 0
            else:
                combo = 0
                comboacts = 0
                combomusics = 0
        if usermissed < 0:
            game = False              
        if correctg:
            correctg = 0            
        lenpacket = random.choice([i for i in range(1,6)])
        packet = ""
        for i in range(lenpacket):
            if combo == 5:
                packet = random.choice(smallletters+numbers+specialchars)
            else:
                if level == 0:
                    packet += random.choice(smallletters)
                if level == 1:
                    packet += random.choice(bigletters+smallletters)
                if level == 2:
                    packet += random.choice(bigletters+smallletters+numbers)
                if level == 3:
                    packet += random.choice(allchar)
                if level == 4:
                    packet += random.choice(specialchars)
        text1 = drawtext(packet,25,1)
        x1,y1 = random.randint(150,600),random.randint(0,400)
        usertype = "" 
                   
    sc.blit(text1,(x1,y1))
    text = drawtext("You typed:",15,0)
    sc.blit(text,(5,460))
    text = drawtext(usertype,25,1)
    sc.blit(text,(140,460))
    text = drawtext("Level:",15,10)
    sc.blit(text,(400,460))
    text = drawtext(str(level),15,10)
    sc.blit(text,(500,460))
    text = drawtext("Destroyed packets:",15,0)
    sc.blit(text,(5,440))
    text = drawtext(str(userscore),15,0)
    sc.blit(text,(240,440))
    text = drawtext("Remaining misses:",15,0)
    sc.blit(text, (400,440))
    text = drawtext(str(usermissed),15,0)
    sc.blit(text, (600,440))
    text = drawtext("Remaining mouse clicks:",15,0)
    sc.blit(text, (5,420))
    text = drawtext(str(mousejocker),15,0)
    sc.blit(text,(280,420))    
    
    if usertype == packet and (usertype or packet):
        if combo != 5:
            combo +=1
        userscore +=1
        if userscore == 10:
            level += 1
            mousejocker = 2
        if userscore == 20:
            level += 1
            mousejocker = 2
        if userscore == 30:
            level += 1
            mousejocker = 2
        if userscore == 40:
            level += 1
            mousejocker = 2
        usertype = ""
        correctg = 1
        boom.play()
        
    if combo == 5 and not comboacts:
        comboact.play()
        comboacts = 1
    if not musics and not combomusics:
        pygame.mixer.music.load("sound/music.ogg")
        pygame.mixer.music.play(-1)
        musics = 1
    
    if combo == 5 and not combomusics:        
        pygame.mixer.music.load("sound/combomusic.ogg")
        pygame.mixer.music.play(-1)
        combomusics = 1
        musics = 0
   
    if combo != 5 and combomusics:
        pygame.mixer.music.load("sound/music.ogg")
        pygame.mixer.music.play(-1)
        combomusics = 0
        musics = 0
        combo = 0
    
    
def drawoutro(sc):
    global waiting6,music2,game,userscore,usermissed,username,upload,players,scores,fetchscoress
    waiting6+=1
    msg = "You destroyed "+str(userscore)+" packet(s)"
    text = drawtext(msg,15,0)
    sc.blit(text,(50,100))
    msg3 = "We have to stop SOPA/PIPA act right now !"
    text = drawtext(msg3,20,1)
    sc.blit(text,(50,(150)))    
    msg2 = "Help the internet, check "
    msg4 = "americancensorship . org for more info"
    text = drawtext(msg2,20,1)
    sc.blit(text,(50,200))
    text = drawtext(msg4,20,1)
    sc.blit(text,(50,220))
    text = drawtext("press R to replay after uploading the score",20,1)
    sc.blit(text,(50,300)) 
    text = drawtext("Enter your name:", 20,1)
    sc.blit(text,(50,320))
    text = drawtext(username, 20,1)
    sc.blit(text, (170,320))
    sc.blit(upload,(70,360))
    pygame.draw.line(sc,(0,255,100),(350,0),(350,480),2)
    if waiting6 == 1:
        pygame.mixer.music.load("sound/music3.ogg")
        pygame.mixer.music.play(-1)                        

    if not fetchscoress:
        thread.start_new_thread(fetchscores,())
        fetchscoress = 1
    if fetchscoress:
        if not players:
            text = drawtext("Loading Top ten scores",20,1)
        if players:
            text = drawtext("Top ten scores",20,1)
        sc.blit(text, (400,100))
        x,y = 400,150
        for a,b in zip(players,scores):
            text = drawtext(a+" : "+b,20,1)
            sc.blit(text,(x,y))
            y+=20
    
    

    
    
def drawmenu(sc):
    global waiting,currentbg,bglist,reached,waiting2,waiting3,mainmenu,waiting4,text1,x1,y1
    global packet,introstatus,seconds,logins,usertype,userscore,musics,waiting5,usermissed,correctg,game
    global waiting6
    if mainmenu:
        drawmainmenu(sc)
    elif game:        
        drawgame(sc)
    else:
        drawoutro(sc)
    
def run():
    global text1,usertype,userscore,game,level,usermissed,mousejocker,x1,y1,waiting4,usertype,packet,correctg
    global username,players,scores,fetchscoress,uploaded
    
    pygame.init()   
    screen=pygame.display.set_mode((640,480))    
    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))
    screen.blit(background, (0,0))
    clock = pygame.time.Clock()
    mainloop = True
    FPS = 30
    text1 = drawtext("",20,0)
    while mainloop:
        clock.tick(FPS)     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if not game and uploaded:
                        game = True
                        userscore,level,usermissed = 0,0,10
                        pygame.mixer.music.load("sound/music.ogg")
                        pygame.mixer.music.play(-1)
                        fetchscoress,players,scores = 0,[],[]
                        uploaded = 0
                        
                if str(event.unicode):
                    if game:
                        usertype += str(event.unicode)
                    if not mainmenu and not game:
                        username += str(event.unicode)
                        
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC           
                if event.key == pygame.K_RETURN:
                        print 1
                if event.key == pygame.K_BACKSPACE:
                    if game:
                        usertype = usertype[:-2]
                    if not game and not mainmenu:
                        username = username[:-2]
                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                print x,y,x1,y1
                if game:
                    if x in range(x1-100,x1+100) and y in range(y1-100,y1+100):
                        if mousejocker > 0:
                            usertype = packet
                            waiting4,correctg = 90,1
                            mousejocker -=1
                if not mainmenu and not game:
                    if x in range(70,230) and y in range(300, 450):
                        if fetchscoress:
                            print "uploadin scores!@",username,userscore
                            uploadscore(username,userscore)
                   
                                   
        
        pygame.display.set_caption("SOPA/PIPA jam")
        screen.blit(background, (0,0))
        drawmenu(screen)
                
        pygame.display.flip()         
        
    
     
run()