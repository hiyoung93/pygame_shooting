import pygame
import sys
import random
from time import sleep

padWidth = 480  # 게임 화면의 가로
padHeight = 640 # 게임 화면의 세로
rockImage = ['그림1.png','그림2.png','그림3.png','그림4.png','그림5.png',\
             '그림6.png','그림7.png','그림8.png','그림9.png','그림10.png']
# 운석을 맞춘 개수 계산
def writeScore(count):
    global gamePad
    font = pygame.font.Font('THE_Oegyeinseolmyeongseo.ttf',20)
    text = font.render('없앤 인형의 갯수' + str(count), True, (255,255,255)) #255는 RGB
    gamePad.blit(text,(0,0))
# 운석을 맞춘 개수 계산
def writePassed(count):
    global gamePad
    font = pygame.font.Font('THE_Oegyeinseolmyeongseo.ttf',20)
    text = font.render('지구 파괴하려는 인형수' + str(count), True, (255,0,0)) #255는 RGB
    gamePad.blit(text,(270,0))
# 게임 메세지 출력
def writeMessage(text):
    global gamePad, gameoverSound
    textfont = pygame.font.Font('THE_Oegyeinseolmyeongseo.ttf',80)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    sleep(10)  # 이초 쉬고 다시 실행해줘
    runGame()

# 전투기가 운석과 충돌했을때 메세지 출력
def crash():
    global gamePad
    writeMessage('상처난 고양이')

# 게임오버 메세지 보이기
def gameOver():
    global gamePad
    writeMessage('GAME OVER!')

# 게임에 등장하는 객체를 드로잉
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x,y))   # 해당하는 오브젝트를 x,y 위치로부터 그려라

def initGame():
    global gamePad, clock, background, fighter, missile, explosion
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('지구를지켜라!')                              # 게임이름
    background = pygame.image.load('PyShooting/background.png')             # 게임그림
    fighter = pygame.image.load('PyShooting/cat.png')                       # 전투기 그림
    missile = pygame.image.load('PyShooting/missile.png')                   # 미사일 그림
    explosion = pygame.image.load('PyShooting/explosion.png')
    clock = pygame.time.Clock()

def runGame():
    global gamePad, Clock, background, fighter, missile, explosion
    # 전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]
    # 초기 위치
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    # 무기좌표
    missileXY = []

    # 운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size # 운석크기
    rockWidth = rockSize[0]
    rockHight = rockSize[1]
    # 운석 초기 위치 설정
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    # 전투기 미사일에 돌이 맞았을 경우 True
    isShot = False
    shotCount = 0
    rockPassed = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:      # 게임프로그램 종료
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:  # 전투기 왼쪽으로 이동
                    fighterX -= 5

                elif event.key == pygame.K_RIGHT: # 전투기 오른쪽으로 이동
                    fighterX += 5

                elif event.key == pygame.K_SPACE: # 미사일 발사
                    missileX = x + fighterWidth/2
                    # 미사일이 전투기 가운데서 나갈수 있게 x좌표 잡기
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])


            if event.type in [pygame.KEYUP]: # 방향키를 떼면 전투기 멈춤
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0

        drawObject(background, 0, 0)        # 배경화면 그리기. (화면이 꽉찻기에 필요없음)
        # 누르는 키에 따라 전투기 위치 재조정
        x += fighterX
        if x < 0 :
            x = 0
        elif x > padWidth - fighterWidth: # 전투기의 width값에서
            x = padWidth - fighterWidth   # pad에서 width값을 뺀 나머지 값은 X위치로; 더 이상 오른쪽으로 못나가게

        # 전투기가 운석과 충돌했는지 체크
        if y < rockY + rockHight:
            if(rockX > x and rockX < x + fighterWidth) or  \
            (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                crash()

        drawObject(fighter, x, y)   # 전투기를 게임 화면의 (x,y)좌표에 그리기

        # 미사일 발사 화면에 그리기
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY): #미사일 요소에 대한 반복
                bxy[1] -= 10 # 총알의 y좌표 -10(위로 이동)
                missileXY[i][1] = bxy[1]

                # 미사일이 운석을 맞추었을 경우
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy) # 미사일이 운석 범위에 들어가면 미사일지우기
                        isShot = True
                        shotCount += 1


                if bxy[1] <= 0: # 미사일이 화면 밖을 벗어나면
                    try:
                        missileXY.remove(bxy) # 미사일 제거
                    except :
                        pass
        if len(missileXY) != 0: # 다시한번 그려주
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        # 운석 맞춘 점수 표시
        writeScore(shotCount)

        rockY += rockSpeed # 운석 아래로 움직임

        # 운석이 지구로 떨어진경우
        if rockY > padHeight:
            # 새로운 운석(랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size # 운석크기
            rockWidth = rockSize[0]
            rockHight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed +=1
        # 3개이상 놓치면 게임오버
        if rockPassed == 3:
            gameOver()
        # 놓친 운석 수 표시
        writePassed(rockPassed)
        # 운석을 맞춘경우
        if isShot:
            # 운석폭발
            drawObject(explosion, rockX, rockY) # 운석폭팔 그리기

            # 새로운 운석(랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHight = rockSize[1]
            rockX = random.randrange(0, padWidth-rockWidth)
            rockY = 0
            isShot = False

            #운석 맞추면 속도 증가
            rockSpeed += 0.2
            if rockSpeed >= 10: #10보다 높으면 게임 불가능하기에
                rockSpeed = 10


        drawObject(rock, rockX, rockY)  #운석 그리기

        pygame.display.update() # 게임화면을 다시 그림

        clock.tick(60)      # 게임 화면의 초단 프레읾수를 60으로 설정

    pygame.quit()           # pygame 종료

initGame()
runGame()
