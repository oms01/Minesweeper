import pygame
import random

#지뢰찾기 세팅
#가로줄수X,세로줄수Y,지뢰수
ROW,COLUMN,MIN_COUNT = (9,9,10)
#게임 화면 세팅
pygame.init()
CELL_SIZE = 30
CELL_COLOR = (255,255,255)
large_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)
BLACK = (0,0,0) #닫힌칸
GRAY = (128,128,128) #열린칸
YELLOW = (255,255,0) #숫자칸
RED = (255,0,0) #지뢰
WHITE = (255,255,255) #깃발

#칸이 지뢰인지, 열린칸인지, 칸의 숫자는 뭔지, 깃발을 새웠는지} grid에 2차원배열로 저장
#0은 빈칸, 1~8은 주변 지뢰의 숫자, 9는 지뢰
grid = [[{'type': 0, 'open': False, 'flag' : False} for _ in range(ROW)] for _ in range(COLUMN)]

#클릭한 부분이 맵 안인지 밖인지 / Out of Boundary
def OOB(y, x):
    return (0 <= y < COLUMN and 0<= x < ROW)
#타일 열기
def open_tile(y, x):
    if not OOB(y, x): #범위 밖
        return
    
    tile = grid[y][x] 
    if tile['flag']: return #깃발칸은 무시

    if not tile['open']: #닫힌 칸
        tile['open'] = True
    else:
        return
    
    if tile['type'] == 9 : #지뢰 칸
        return
    
    if tile['type'] == 0 : #빈 칸
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            cury,curx = (y+dy, x+dx)
            open_tile(cury,curx)
#처음 시작 화면 출력 / 난이도 선택창
def print_start_screen():
    pygame.init()
    pygame.display.set_caption("Minesweeper_start")
    X,Y = (300,400)
    start_screen = pygame.display.set_mode((X,Y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = (event.pos[0],event.pos[1])
                if X//2-X//4 < x < X//2-X//4 +  X//2 and Y//5*2-Y//18 < y < Y//5*2-Y//18 + Y//10: # EASY 클릭
                    make_board(1)
                    return

                if X//2-X//4 < x < X//2-X//4 +  X//2 and Y//5*3-Y//18 < y < Y//5*3-Y//18 + Y//10: # NORAML 클릭
                    make_board(2)
                    return

                if X//2-X//4 < x < X//2-X//4 +  X//2 and Y//5*4-Y//18 < y < Y//5*4-Y//18 + Y//10: #HARD 클릭
                    make_board(3)
                    return

        title_image = pygame.font.SysFont(None, 45).render("MINESWEEPER",True,WHITE)
        start_screen.blit(title_image,title_image.get_rect(centerx=X//2, centery=Y//6))

        easy_image = pygame.font.SysFont(None, 45).render("EASY",True,WHITE)
        start_screen.blit(easy_image,easy_image.get_rect(centerx=X//2, centery=Y//5*2))
        pygame.draw.rect(start_screen, CELL_COLOR, (X//2-X//4, Y//5*2-Y//18, X//2, Y//10), 1)

        normal_image = pygame.font.SysFont(None, 45).render("NORMAL",True,WHITE)
        start_screen.blit(normal_image,normal_image.get_rect(centerx=X//2, centery=Y//5*3))
        pygame.draw.rect(start_screen, CELL_COLOR, (X//2-X//4, Y//5*3-Y//18, X//2, Y//10), 1)

        hard_image = pygame.font.SysFont(None, 45).render("HARD",True,WHITE)
        start_screen.blit(hard_image,hard_image.get_rect(centerx=X//2, centery=Y//5*4))
        pygame.draw.rect(start_screen, CELL_COLOR, (X//2-X//4, Y//5*4-Y//18, X//2, Y//10), 1)

        pygame.time.Clock().tick(30)
        pygame.display.flip()
#지뢰찾기 판 생성
def make_board(level):
    global ROW,COLUMN,MINE_COUNT,grid,SCREEN_SIZE,screen
    
    if level == 1 : ROW,COLUMN,MINE_COUNT = (9,9,10) # easy
    elif level == 2 : ROW,COLUMN,MINE_COUNT = (16,16,40) # normal
    elif level == 3 : ROW,COLUMN,MINE_COUNT = (16,30,90) # hard
    grid = [[{'type': 0, 'open': False, 'flag' : False} for _ in range(ROW)] for _ in range(COLUMN)]
    SCREEN_SIZE = (COLUMN*30, ROW*30)
    lv = ["EASY","NORMAL","HARD"]
    pygame.init()
    pygame.display.set_caption("Minesweeper - "+lv[level-1])
    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen.fill((0,0,0))

    #지뢰 배치
    for _ in range(MINE_COUNT):
        while True:
            y = random.randint(0,COLUMN-1)
            x = random.randint(0,ROW-1)
            tile = grid[y][x]
            if tile['type'] != 9 : # 지뢰가 아닌 칸
                tile['type'] = 9
                break

    for i in range(COLUMN):
        for j in range(ROW):
            if grid[i][j]['type'] == 9 : continue #지뢰칸은 건너뛰기
            cnt = 0 
            for dy, dx in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
                cury,curx = (i+dy,j+dx)
                if not OOB(cury,curx) : continue
                if grid[cury][curx]['type'] != 9 : continue #범위 밖이거나, 지뢰칸이 아니거나
                cnt += 1
            grid[i][j]['type'] = cnt
    
    #임시 : 터미널에 게임판 출력
    # for j in range(ROW):
    #     for i in range(COLUMN):
    #         if grid[i][j]['type'] == 9:
    #             print('*',end='')
    #         else:
    #             print(grid[i][j]['type'],end='')
    #     print()

#게임판 클릭 반응
def click_event(event):
    y = event.pos[0] // CELL_SIZE
    x = event.pos[1] // CELL_SIZE
    if not OOB(y,x): return
    tile = grid[y][x]

    if event.button == 1 : #좌클릭

        if tile['flag']: return #깃발칸은 무시

        if tile['type'] == 9 : #지뢰칸은 게임오버
            tile['open'] = True
        else:
            open_tile(y,x)

        if tile['open'] and tile['type'] !=9 and tile['type'] !=0 :
            cnt_around_mine = 0
            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                cury,curx = (y+dy, x+dx)
                if not OOB(cury,curx) : continue
                if grid[cury][curx]['flag']==1: 
                    cnt_around_mine+=1

            if (int)(tile['type']) == cnt_around_mine:
                print(tile['type'])
                print(cnt_around_mine)
                for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    cury,curx = (y+dy, x+dx)
                    open_tile(cury,curx)
            else :
                return
        

    elif event.button == 3 : #우클릭 / 깃발설치
        if tile['open']: return #열린칸은 깃발설치 X
        if not tile['flag']: #깃발이 설치 안돼있으면 설치
            tile['flag'] = True
        else: #설치 돼있으면 해제
            tile['flag'] = False
#게임 결과 판별
def check_gameover():
    cnt_open = 0
    for i in range(COLUMN):
        for j in range(ROW):
            tile = grid[i][j]

            if tile['type']==9 and tile['open']==True: #지뢰칸이 열렸을때
                print_end_screen(0)
                return 1
            if tile['type']!=9 and tile['open']==True: #지뢰가 아닌 칸 개수 카운트
                cnt_open+=1

    if cnt_open == COLUMN*ROW - MINE_COUNT:
        print_end_screen(1)
        return 1
#게임 종료 화면 출력 / result가 0이면 패배 1이면 승리
def print_end_screen(result):
    pygame.init()
    pygame.display.set_caption("Minesweeper_end")
    X,Y = (300,300)
    end_screen = pygame.display.set_mode((X,Y))
    res = ["DEFEAT","VICTORY"]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if X//2-X//4 < x < X//2-X//4 + X//2 and Y//2+Y//27 < y < Y//2+Y//27 + Y//8: #AGAIN 클릭
                    print_start_screen()
                    print_game_screen()
                    return

        result_image = pygame.font.SysFont(None, 45).render(res[result],True,WHITE)
        end_screen.blit(result_image,result_image.get_rect(centerx=X//2, centery=Y//6))
        
        
        title_image = pygame.font.SysFont(None, 45).render("PLAY AGIAN?",True,WHITE)
        end_screen.blit(title_image,title_image.get_rect(centerx=X//2, centery=Y//6*2))

        again_image = pygame.font.SysFont(None, 45).render("AGAIN",True,WHITE)
        end_screen.blit(again_image,again_image.get_rect(centerx=X//2, centery=Y//5*3))
        pygame.draw.rect(end_screen, CELL_COLOR, (X//2-X//4, Y//2+Y//27, X//2, Y//8), 1)

        pygame.time.Clock().tick(30)
        pygame.display.flip()

    if result == 0:
        print("defeat")
    elif result == 1 :
        print("victory")
    return
#게임판 출력
def print_game_screen():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN : #클릭
                click_event(event)

            
        for i in range(COLUMN):
            for j in range(ROW):
                tile = grid[i][j]

                if tile['open'] == True: #열린칸
                    pygame.draw.rect(screen, GRAY, pygame.Rect(
                        i*CELL_SIZE,j*CELL_SIZE,CELL_SIZE,CELL_SIZE
                    ))

                if tile['type']!=0 and tile['type'] != 9 : #숫자칸
                    mine_count_around_image = small_font.render('{}'.format(tile['type']),True,YELLOW)
                    screen.blit(mine_count_around_image,mine_count_around_image.get_rect(
                        centerx=i*CELL_SIZE+CELL_SIZE//2, centery=j*CELL_SIZE+CELL_SIZE//2))
                    
                if tile['type'] == 9 : #지뢰칸
                    mine_image = small_font.render('x',True,RED)
                    screen.blit(mine_image,mine_image.get_rect(
                        centerx=i*CELL_SIZE+CELL_SIZE//2, centery=j*CELL_SIZE+CELL_SIZE//2))


                if tile['open'] == False: #닫힌칸
                    pygame.draw.rect(screen, BLACK, pygame.Rect(
                        i*CELL_SIZE,j*CELL_SIZE,CELL_SIZE,CELL_SIZE
                    ))

                if tile['flag']==True: #깃발칸
                    v_image = small_font.render('v',True,WHITE)
                    screen.blit(v_image,v_image.get_rect(
                        centerx=i*CELL_SIZE+CELL_SIZE//2, centery=j*CELL_SIZE+CELL_SIZE//2))
                    
                #격자 출력
                pygame.draw.rect(screen, CELL_COLOR, (i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        if check_gameover()==1: break

        pygame.time.Clock().tick(30)
        pygame.display.flip()

# main
print_start_screen()
print_game_screen()

