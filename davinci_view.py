import pygame
import sys
import random as rn
import pygame.freetype as freetype


#매 턴마다 달라지는 것 : 플레이어의 카드 수, 공개된 카드 수, 카드더미 수
#
pygame.init()

blackCardArr = [ i for i in range(12)]
whiteCardArr = [ i for i in range(12)]

#스크린 사이즈, 배경 이미지, 폰트
screen = pygame.display.set_mode((1200, 720)) #스크린 사이즈
background = pygame.image.load('월넛.jpg') # 배경 이미지
font = pygame.font.SysFont("consolas", 30)
textFont = pygame.font.SysFont("consolas", 100)
userText = ''

inputRect   = pygame.Rect(450, 600, 300, 100)
inputColor  = pygame.Color('white')

#플레이어별 좌표값 (새 카드 추가 시 새로운 카드의 x좌표 : +card_width)
player1_x = 100
player1_y = 140
player2_x = 100
player2_y = 420

#카드 크기, 색깔
card_width = 80    #카드 너비
card_height = 128   #카드 높이
color_black = pygame.image.load('blackCard.png') #카드 색 : 블랙
color_white = pygame.image.load('whiteCard.png')   #카드 색 : 화이트

class Card:
    def __init__(self, argColor, argValue):
        self.color      = argColor
        self.value      = argValue
        self.open       = False
        self.opened     = False
        if argColor==color_black:
            self.colorNum = 0
        else:
            self.colorNum = 1

    def printCard(self, argX, argY):
        self.x = argX
        self.y = argY
        # 만약 공개여부가 true라면 숫자를 빨간색으로, 아니라면 카드와 같은 색으로 표시
        if self.open == True:
            textColor = (255, 0, 0)
        else:  # 미공개면 카드색과 같이 설정
            if self.color == color_black:
                textColor = (92, 92, 92)
            else:
                textColor = (239, 239, 239)
        if self.opened == True and self.open == False:
            if self.color == color_black:
                textColor = (255, 255, 255)
            else:
                textColor = (0, 0, 0)

        num = font.render(str(self.value), True, textColor)
        rect = screen.blit(self.color, (argX, argY))
        screen.blit(num, (argX + 28, argY + 48))  # 현 카드의 넘버 출력

        return rect

#플레이어당 카드배열, 개수
# 카드배열 : 색상, 숫자, 공개여부
Player1arr = []
Player2arr = []

#플레이어 초기 카드 분배 검2흰2
for i in range(2):
    randomInt = rn.randrange(0, len(blackCardArr))
    newCard = Card(color_black, blackCardArr[randomInt])
    Player1arr.append(newCard)
    blackCardArr.remove(newCard.value)

    randomInt = rn.randrange(0, len(whiteCardArr))
    newCard = Card(color_white, whiteCardArr[randomInt])
    Player1arr.append(newCard)
    whiteCardArr.remove(newCard.value)

    randomInt = rn.randrange(0, len(blackCardArr))
    newCard = Card(color_black, blackCardArr[randomInt])
    Player2arr.append(newCard)
    blackCardArr.remove(newCard.value)

    randomInt = rn.randrange(0, len(whiteCardArr))
    newCard = Card(color_white, whiteCardArr[randomInt])
    Player2arr.append(newCard)
    whiteCardArr.remove(newCard.value)

#카드 더미 사이즈, 색깔
heap_size = 80  #정방형
heap_black_x = 1000 #블랙카드 더미 위치
heap_black_y = 260
heap_white_x = 1000 #화이트카드 더미 위치
heap_white_y = 360
heap_black = (0, 0, 0)  #블랙더미 색
heap_white = (255, 255, 255)    #화이트더미 색

#카드더미 출력 함수 (남은 블랙 수, 남은 화이트 수)
def printHeap(argNumOfBlack, argNumOfWhite) :
    numOfHeap_black = font.render(argNumOfBlack , True, heap_white)
    numOfHeap_white = font.render(argNumOfWhite , True, heap_black)
    blackRect = pygame.draw.rect(screen, heap_black, [heap_black_x, heap_black_y, heap_size, heap_size])
    screen.blit(numOfHeap_black, (heap_black_x + 32, heap_black_y + 28)) #검은카드 더미 수 출력
    whiteRect = pygame.draw.rect(screen, heap_white, [heap_white_x, heap_white_y, heap_size, heap_size])
    screen.blit(numOfHeap_white, (heap_white_x + 32, heap_white_y + 28)) #하얀카드 더미 수 출력

    return [blackRect, whiteRect]

# 상대방 카드 중 어떤 카드를 클릭했는지 표시
def whatIsClicked (x, y) :
    blue = (0, 0, 255)
    pygame.draw.circle(screen, blue, [x+35, y-20], 20)

def printArea() :
    user_area = font.render("USER" , True, (255,255,255))
    com_area = font.render("COM" , True, (255,255,255))
    screen.blit(user_area, (20, player1_y))
    screen.blit(com_area, (20, player2_y+50))

def isEnd(argList):
    for i in argList:
        j = i.open
        if j == False:
            return False
    return True

screen.blit(background, (0, 0)) #배경
printArea()

evcount = 0
myTurn = True
isDraw = False
inputActive = False
run = True
#게임 실행 동안
while run:

    Player1arr = sorted(Player1arr, key=lambda Card: (Card.value, Card.colorNum))
    Player2arr = sorted(Player2arr, key=lambda Card: (Card.value, Card.colorNum))

    #화면에 그리기
    p1rectArr = []
    p2rectArr = []

    for p1 in Player1arr:
        p1.opened = True

    # 플레이어 1 카드 나열 (개수만큼 for문으로 출력)
    for p1 in Player1arr:
        width = 80 * Player1arr.index(p1)
        p1rect = p1.printCard(player1_x + width, player1_y-50)
        p1rectArr.append(p1rect)

    # 플레이어 2 카드 나열 (개수만큼 for문으로 출력)
    for p2 in Player2arr:
        width = 80 * Player2arr.index(p2)
        p2rect = p2.printCard(player2_x + width, player2_y)
        p2rectArr.append(p2rect)

    numOfHeap_black = str(len(blackCardArr))  # 블랙카드 더미 장수
    numOfHeap_white = str(len(whiteCardArr))  # 화이트카드 더미 장수

    # 카드더미 프린트
    rect = printHeap(numOfHeap_black, numOfHeap_white)
    # input box print
    pygame.draw.rect(screen, inputColor, inputRect)

    # text print
    textSurface = textFont.render(userText, True, (0, 0, 0))
    screen.blit(textSurface, (inputRect.x + 5, inputRect.y + 5))

    pygame.display.update()  # 이거 써야 적용됨

    if myTurn == False:
        p2ColorSelect   = rn.randint(0, 2)
        p2select        = rn.randint(0, len(Player1arr)-1)
        p2selectValue   = rn.randint(0, 12)
        if p2ColorSelect == 0 and len(blackCardArr) != 0:
            randomInt = rn.randrange(0, len(blackCardArr))
            newCard = Card(color_black, blackCardArr[randomInt])
            Player2arr.append(newCard)
            blackCardArr.remove(newCard.value)
        elif len(whiteCardArr) != 0:
            randomInt = rn.randrange(0, len(whiteCardArr))
            newCard = Card(color_white, whiteCardArr[randomInt])
            Player2arr.append(newCard)
            whiteCardArr.remove(newCard.value)
        if Player1arr[p2select].value == p2selectValue:
            Player1arr[p2select].open = True
        else:
            var = Player2arr.index(newCard)
            Player2arr[var].open = True
        myTurn = True
        isDraw = False
    else:
        for event in pygame.event.get():
            # print(evcount, end=' : ')
            # print(event) # 이벤트 발생횟수 / 좌표 출력
            evcount += 1
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN and myTurn == True and isDraw == False:
                for i in rect:
                    if i.collidepoint(event.pos):
                        isDraw = True
                        if i == rect[0] and len(blackCardArr) != 0:
                            randomInt = rn.randrange(0, len(blackCardArr))
                            newCard = Card(color_black, blackCardArr[randomInt])
                            Player1arr.append(newCard)
                            blackCardArr.remove(newCard.value)
                        elif len(whiteCardArr) != 0:
                            randomInt = rn.randrange(0, len(whiteCardArr))
                            newCard = Card(color_white, whiteCardArr[randomInt])
                            Player1arr.append(newCard)
                            whiteCardArr.remove(newCard.value)
            elif event.type == pygame.MOUSEBUTTONDOWN and myTurn == True:
                # print(event.pos[0], event.pos[1])
                for i in p2rectArr:
                    if i.collidepoint(event.pos):
                        # print(i)
                        temp = int((i[0] - 100) / 80)
                        p1select = Player2arr[temp]
                        # cir = pygame.draw.circle(screen, (255, 255, 0), [i[0]+40, i[1]-20], 15)
                        inputActive = True
            if event.type == pygame.KEYDOWN:
                if inputActive == True:
                    if event.key == pygame.K_RETURN:
                        inputValue = int(userText)
                        userText = ''
                        # print(inputValue)
                        inputActive = False
                        myTurn = False
                        if inputValue == p1select.value:
                            p1select.open = True
                            # p1select.opened = True
                        else:
                            var = Player1arr.index(newCard)
                            print(p1select.value)
                            Player1arr[var].open = True
                            # Player1arr[var].opened = True
                        if isEnd(Player1arr) or isEnd(Player2arr):
                            endMsg = textFont.render("GAME OVER", True, (255, 255, 255))
                            screen.blit(endMsg, (300, 300))
                    elif event.key == pygame.K_BACKSPACE:
                        userText = userText[:-1]
                    else:
                        userText += event.unicode



# X창을 누르면 게임종료  
pygame.quit()
sys.exit()
