import pygame
import random
import time

#기본 세팅
WHITE = (255,255,255)
CELL_SIZE = 30
CELL_COLOR = WHITE
grid = 0 #게임판 저장
ROW,COLUMN,MINE_COUNT = (0,0,0) 
around_coords = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)] # 주변 좌표 이용
click_cnt = 0 #클릭 횟수 저장 
start_time = 0 #게임 시작 시간 저장

#클릭한 부분이 맵 안인지 밖인지 / Out of Boundary / 0이면 안, 1이면 밖
def OOB(y, x):
    return (0 <= y < COLUMN and 0<= x < ROW)
#타일 열기
def open_tile(y, x):
    if not OOB(y, x) : return # 범위 밖 클릭시 무시
    tile = grid[y][x]
    
    if tile['flag'] : return # 깃발칸 무시

    if not tile['open'] : tile['open'] = True #닫힌칸은 열고, 열린칸은 무시
    else : return

    if tile['type'] == 0 : #빈칸은 주변칸 밝히기
        for dy, dx in around_coords : 
            open_tile(y+dy, x+dx)
#게임판 생성
def set_board(level):
    global ROW,COLUMN,MINE_COUNT,grid,SCREEN_SIZE,screen
    
    if level == 1 : ROW,COLUMN,MINE_COUNT = (9,9,10) # easy
    elif level == 2 : ROW,COLUMN,MINE_COUNT = (16,16,40) # normal
    elif level == 3 : ROW,COLUMN,MINE_COUNT = (16,30,90) # hard

    #칸이 지뢰인지, 열린칸인지, 칸의 숫자는 뭔지, 깃발을 새웠는지} grid에 2차원배열로 저장
    #0은 빈칸, 1~8은 주변 지뢰의 숫자, 9는 지뢰
    grid = [[{'type': 0, 'open': False, 'flag' : False, 'Mouse_on' : False} for _ in range(ROW)] for _ in range(COLUMN)]
    SCREEN_SIZE = (COLUMN*30, ROW*30)
    lv = ["EASY","NORMAL","HARD"]
    pygame.init()
    pygame.display.set_caption("Minesweeper - "+lv[level-1])
    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen.fill((0,0,0))
#게임판에 지뢰 배치 / 첫 클릭시 실행
def set_mines(event):
    global start_time
    start_time = time.time()
    click_y,click_x = (event.pos[0] // CELL_SIZE, event.pos[1] //CELL_SIZE)
    #지뢰 배치
    for _ in range(MINE_COUNT):
        while True:
            y = random.randint(0,COLUMN-1)
            x = random.randint(0,ROW-1)
            tile = grid[y][x]

            if click_y == y and click_x == x : continue # 클릭한칸은 지뢰설치 X

            flag = False # while문 탈출을 위한 변수
            for dy, dx in around_coords : #주변칸에도 지뢰설치 X
                cury,curx = (click_y+dy, click_x+dx) #주변칸의 좌표
                
                if y==cury and x==curx : #첫번째 클릭칸
                    flag +=1
                    break
            if flag : 
                continue

            if tile['type'] != 9 : # 지뢰가 아닌 칸
                tile['type'] = 9
                break

    for i in range(COLUMN):
        for j in range(ROW):
            if grid[i][j]['type'] == 9 : continue #지뢰칸은 건너뛰기
            cnt = 0 
            for dy, dx in around_coords :
                cury,curx = (i+dy,j+dx)
                if not OOB(cury,curx) : continue
                if grid[cury][curx]['type'] != 9 : continue #범위 밖이거나, 지뢰칸이 아니거나
                cnt += 1
            grid[i][j]['type'] = cnt
#게임판 클릭 반응
def click_event(event):
    global click_cnt
    if click_cnt == 0 : set_mines(event)
    click_cnt+=1
    y,x = (event.pos[0] // CELL_SIZE, event.pos[1] //CELL_SIZE)
    if not OOB(y,x): return #범위 밖
    tile = grid[y][x]

    if event.button == 1 : #좌클릭
        if tile['flag'] : return #깃발칸은 무시
        open_tile(y,x)
        # 열려있는 숫자칸 중 주변 지뢰를 다 찾은 숫자칸은 주변칸 열기
        if tile['open'] and 0 < tile['type'] < 9 : 
            cnt_around_mine = 0 #주변 지뢰 개수 저장
            for dy, dx in around_coords:
                cury,curx = (y+dy, x+dx)
                if not OOB(cury,curx) : continue
                if grid[cury][curx]['flag'] == 1 : cnt_around_mine+=1

            if (int)(tile['type']) == cnt_around_mine:
                for dy, dx in around_coords :
                    cury,curx = (y+dy, x+dx)
                    open_tile(cury,curx)
            else : return

        if check_gameover() : return
        
    elif event.button == 3 : #우클릭 / 깃발설치
        if tile['open']: return #열린칸은 깃발설치 X
        if not tile['flag']: tile['flag'] = True #깃발이 설치 안돼있으면 설치
        else: tile['flag'] = False #설치 돼있으면 해제
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
#게임판 출력
def print_board():
    BLACK = (0,0,0) #닫힌칸
    GRAY = (128,128,128) #열린칸
    YELLOW = (255,255,0) #숫자칸
    RED = (255,0,0) #지뢰
    for i in range(COLUMN):
            for j in range(ROW):
                tile = grid[i][j]

                if tile['open'] == True: #열린칸
                    pygame.draw.rect(screen, GRAY, pygame.Rect(i*CELL_SIZE,j*CELL_SIZE,CELL_SIZE,CELL_SIZE))

                if tile['type']!=0 and tile['type'] != 9 : #숫자칸
                    mine_count_around_image = pygame.font.SysFont(None, 36).render('{}'.format(tile['type']),True,YELLOW)
                    screen.blit(mine_count_around_image,mine_count_around_image.get_rect(centerx=i*CELL_SIZE+CELL_SIZE//2, centery=j*CELL_SIZE+CELL_SIZE//2))
                    
                if tile['type'] == 9 : #지뢰칸
                    mine_image = pygame.font.SysFont(None, 36).render('x',True,RED)
                    screen.blit(mine_image,mine_image.get_rect(centerx=i*CELL_SIZE+CELL_SIZE//2, centery=j*CELL_SIZE+CELL_SIZE//2))

                if tile['open'] == False: #닫힌칸
                    pygame.draw.rect(screen, BLACK, pygame.Rect(i*CELL_SIZE,j*CELL_SIZE,CELL_SIZE,CELL_SIZE))

                if tile['flag']==True: #깃발칸
                    v_image = pygame.font.SysFont(None, 36).render('v',True,WHITE)
                    screen.blit(v_image,v_image.get_rect(centerx=i*CELL_SIZE+CELL_SIZE//2, centery=j*CELL_SIZE+CELL_SIZE//2))
                    
                #격자 출력
                pygame.draw.rect(screen, CELL_COLOR, (i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
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
                # EASY, NORMAL, HARD 클릭
                if X//2-X//4 < x < X//2-X//4 +  X//2 and Y//5*2-Y//18 < y < Y//5*2-Y//18 + Y//10 : set_board(1)
                elif X//2-X//4 < x < X//2-X//4 +  X//2 and Y//5*3-Y//18 < y < Y//5*3-Y//18 + Y//10 : set_board(2)
                elif X//2-X//4 < x < X//2-X//4 +  X//2 and Y//5*4-Y//18 < y < Y//5*4-Y//18 + Y//10 : set_board(3)
                else : continue
                print_game_screen()
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
#게임 화면 출력
def print_game_screen():
    while True:
        for event in pygame.event.get():
            print_board()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEMOTION: # 마우스가 올려졌을때
                change_color(event)
            elif event.type == pygame.MOUSEBUTTONDOWN : #클릭
                click_event(event)
#게임 종료 화면 출력 / result가 0이면 패배 1이면 승리
def print_end_screen(result):
    print_board()
    global start_time,click_cnt
    end_time = time.time()-start_time
    time.sleep(0.5)
    global click_cnt
    click_cnt = 0
    pygame.init()
    pygame.display.set_caption("Minesweeper_end")
    X,Y = (300,300)
    end_screen = pygame.display.set_mode((X,Y))
    res = ["DEFEAT","VICTORY"]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT : 
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN : 
                x,y = event.pos[0],event.pos[1]
                if X//2-X//4 < x < X//2-X//4 + X//2 and Y//2+Y//27 < y < Y//2+Y//27 + Y//8: #AGAIN 클릭
                    print_start_screen()
                    return

        result_image = pygame.font.SysFont(None, 45).render(res[result],True,WHITE)
        end_screen.blit(result_image,result_image.get_rect(centerx=X//2, centery=Y//6))

        if result == 1 : # 승리시 게임시간 출력
            record_str = str((int)(end_time)) + " seconds"
            time_image = pygame.font.SysFont(None, 30).render("{}".format(record_str),True,WHITE)
            end_screen.blit(time_image,time_image.get_rect(centerx=X//2, centery=Y//6*1.5))
        
        title_image = pygame.font.SysFont(None, 45).render("PLAY AGIAN?",True,WHITE)
        end_screen.blit(title_image,title_image.get_rect(centerx=X//2, centery=Y//6*2.5))

        again_image = pygame.font.SysFont(None, 45).render("AGAIN",True,WHITE)
        end_screen.blit(again_image,again_image.get_rect(centerx=X//2, centery=Y//5*3))
        pygame.draw.rect(end_screen, CELL_COLOR, (X//2-X//4, Y//2+Y//27, X//2, Y//8), 1)

        pygame.time.Clock().tick(30)
        pygame.display.flip()
#마우스 올라간 칸 색 변경
def change_color(event):
    y, x = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
    if(grid[y][x]['open'] or grid[y][x]['flag']): return

    pygame.draw.rect(screen, (25,25,25), pygame.Rect(
        y*CELL_SIZE,x*CELL_SIZE,CELL_SIZE,CELL_SIZE
    ))
    pygame.display.flip()

#main
print_start_screen()
