import random
import time
class Item:
    def __init__(self, selected, bomb=None, direction=None):
        self.x = 0
        self.y = 0
        self.selected = selected
        self.b_range = 0
        self.b_count = 0
        self.shield_value = 0
        self.throw_move= 6
        self.bomb=bomb
        self.direction=direction

        if selected == 5:
            self.range()
        elif selected == 6:
            self.count()
        elif selected == 7:
            self.shield()
        # elif selected == 8:
        #     self.throw()

    def range(self):
        self.b_range += 1
        print("폭탄 범위 증가")  # 중첩 가능
        return self.b_range

    def count(self):
        self.b_count += 1
        print("폭탄 개수 증가")  # 중첩 가능
        return self.b_count

    def shield(self):
        self.shield_value += 1
        print("방어")
        return self.shield_value

    def throw(self):
        self.x = self.bomb.get_bomb_imf()[0]
        self.y = self.bomb.get_bomb_imf()[1]
        if self.direction == 8:  # 'up':
            self.y += self.throw_move
        elif self.direction == 2:  # 'down':
            self.y -= self.throw_move
        elif self.direction == 4:  # 'left':
            self.x -= self.throw_move
        elif self.direction == 6:  # 'right':
            self.x += self.throw_move
        print("던지기")
        return (self.x, self.y)

    def get_item_imf(self):
        return [self.selected, self.b_range, self.b_count, self.shield_value, self.throw_move, self.bomb, self.direction]

class Bomb:
    def __init__(self, x, y, user_imf, ticks):
        self.x = x
        self.y = y
        self.user_imf = user_imf
        self.ticks = ticks
        self.original_ticks = ticks
        self.b_range = 3
        self.isalive = True

    def tick(self, external_ticks=None):
        if external_ticks is not None:
            self.ticks = external_ticks
        if self.ticks == self.original_ticks + 4:
            print("폭탄이 터졌습니다!")

        return self.ticks

    def bomb_range(self):
        coordinates = []
        for i in range(-self.b_range, self.b_range + 1):
            if i != 0:
                coordinates.append((self.x + i, self.y))
            else:
                for j in range(-self.b_range, self.b_range + 1):
                    coordinates.append((self.x, self.y + j))
        up, down, left, right, setpoint = [], [], [], [], []
        sort_list = []
        for x, y in coordinates:
            if x == self.x and y < self.y:  # 상
                up.append((x, y))
            elif x == self.x and y > self.y:  # 하
                down.append((x, y))
            elif y == self.y and x < self.x:  # 좌
                left.append((x, y))
            elif y == self.y and x > self.x:  # 우
                right.append((x, y))
        up.sort(reverse=True)
        down.sort()
        left.sort(reverse=True)
        right.sort()
        setpoint.append((self.x,self.y))
        sort_list.append(up)
        sort_list.append(down)
        sort_list.append(left)
        sort_list.append(right)
        sort_list.append(setpoint)
        return sort_list

    def get_bomb_imf(self):
        return [self.x, self.y, self.user_imf, self.ticks, self.b_range, self.isalive]

    def count(self):
        #Itemlist.user_items.append(name)
        game_item.b_count += 1
        print("폭탄 개수 증가")  # 중첩 가능
        return game_item.b_count, 2

    def bomb_box(self, bomb1): #폭탄이 담기는 리스트 함수
        for i in range(game_item.b_count):
            self.bomb_list.append(bomb1)

    def bomb_use(self): #폭탄을 사용하는 함수
        if game_item.b_count > 0:
            use_bomb = self.bomb_list.pop()
            print(f"폭탄 사용:{use_bomb}")
            game_item.b_count -= 1
            return use_bomb
        else:
            print("폭탄 부족")
            return None

    def use_bomb(self): #리스트에 담긴 폭탄 갯수만큼 사용 및 충전
        if 5 in self.user_items:
            print("폭탄을 사용합니다.")
            self.user_items.remove(6)
            self.user_items.append(6)
            print('폭탄이 충전되었습니다.')



class Map:
    def __init__(self, size=15): #size= 15 범위설정
        self.size = size
        self.map = self.create_map() #맵만드는 함수 구현
        self.map[1][1] = 2
        self.map[13][13] = 3
        self.selected_items =[]
        self.a = 1
        self.b = self.size - 1
        self.end_map_phase = 0
        self.end_map_index = 1
    def set_user_position(self,x,y):
        # if Item.shield_value==0:
        #     self.map[x][y] = 2
        # else:
        #     self.map[x][y] = 12
        self.map[y][x] = 2
    def set_ai_position(self,x,y):
        self.map[y][x] = 3
    def del_user(self,x = 1,y = 1):
        if self.map[y][x] != 11:
            del self.map[y][x]
            self.map[y].insert(x, "-")
    def create_map(self): #맵만들기
        # 맵 초기화
        game_map = [] #빈리스트 만들기

        for i in range(self.size):#15 행
            row = [] #행
            for j in range(self.size): #15 열
                if i == 0 or i == self.size - 1 or j == 0 or j == self.size - 1: #i가 0이거나 14이거나 j가 0이거나 j=14이거나
                    row.append(0)  # 외벽
                elif i % 2 == 0 and j % 2 == 0:
                    row.append(1)  # 고정 벽
                else:
                    row.append('-')  # 빈 공간
            game_map.append(row)
        return game_map

    def set_bomb_position(self, x, y):
        self.map[y][x] = 11

    def break_wall(self): #아이템이 나오는 벽 만들기
        for i in range(1,self.size-1): #외곽 제외
            for j in range(1,self.size-1): #외곽 제외
                if self.map[i][j]=='-': #빈칸이라면?
                    if not (i<=3 and j<=3) or (i>=11 and j>=11) : #처음 위치에서 제외범위 만들기
                        if (i % 3 == 0 and j % 3 ==0)or(i % 3 == 1 and j % 3 ==1): #규칙성 식
                            self.map[i][j]=4 #좌표에 4찍기
    def remove_wall_in_bomb_range(self, bomb):
        sorted_ranges = bomb.bomb_range() #이중리스트
        if bomb.ticks==bomb.original_ticks+4:
            self.map[bomb.x][bomb.y] = "+"
            for direction_range in sorted_ranges:  # 상, 하, 좌, 우 방향별로 순회 밑에서 브레이크만나면 다음방향으로
                for x, y in direction_range: #상방향이면 거기안 원소들 x,y로 출력
                    if 0 <= x < self.size and 0 <= y < self.size:
                        # 장애물에 따라 처리
                        if self.map[x][y] in [0, 1,'$']:
                            break  # 해당 방향으로의 폭발 중단 아무일도 안벌어지게하는거임
                        elif self.map[y][x] == 3:
                            self.map[y][x] = 9
                        elif self.map[x][y] == 4:
                            ran_list = ['-', 5, 6, 7, 8]
                            probabilities = [0.2,0.2, 0.2, 0.2, 0.2]  # 각 아이템의 확률
                            # 무작위로 아이템 선택
                            selected = random.choices(ran_list, weights=probabilities)[0]
                            self.map[x][y] = selected  # 아이템 벽은 공백으로 제거
                            self.selected_items.append(selected)
                            break
                        else:
                            self.map[x][y] = 9  # 폭발 범위 표시
    def clear_explosion(self,bomb):
        if bomb.ticks == bomb.original_ticks + 5: #5틱지났으면 범위 삭제
            for i in range(self.size):
                for j in range(self.size):
                    if self.map[i][j] in [9, '+']:  # 폭발 범위 또는 폭탄 위치
                        self.map[i][j] = '-'
    def display_map(self): #사이사이 띄어쓰기넣어서 출력
        for row in self.map:
            row_string = ''
            for cell in row:
                row_string += str(cell) + ' '
            print(row_string)

    def end_map(self):
        #        self.a = 1
        # self.b = self.size - 1
        # self.end_map_phase = 0
        # self.end_map_index = 1
        if tick111 > 50:  # 50 틱 이후에 시작
            if self.a < self.b:
                if self.end_map_phase == 0:
                    if self.end_map_index < self.b:
                        self.map[self.a][self.end_map_index] = '$'
                        self.end_map_index += 1
                    else:
                        self.end_map_phase = 1
                        self.end_map_index = self.a + 1

                elif self.end_map_phase == 1:
                    if self.end_map_index < self.b:
                        self.map[self.end_map_index][self.b - 1] = '$'
                        self.end_map_index += 1
                    else:
                        self.end_map_phase = 2
                        self.end_map_index = self.b - 2

                elif self.end_map_phase == 2:
                    if self.end_map_index >= self.a:
                        self.map[self.b - 1][self.end_map_index] = '$'
                        self.end_map_index -= 1
                    else:
                        self.end_map_phase = 3
                        self.end_map_index = self.b - 2

                elif self.end_map_phase == 3:
                    if self.end_map_index > self.a:
                        self.map[self.end_map_index][self.a] = '$'
                        self.end_map_index -= 1
                    else:
                        self.a += 1
                        self.b -= 1
                        self.end_map_phase = 0
                        self.end_map_index = self.a

    def item_coordinate(self):
        item_coor=[]
        for i in range(1, self.size - 1):  # 외곽 제외
            for j in range(1, self.size - 1):  # 외곽 제외
                if self.map[i][j] in [5,6,7,8]:
                    item_type=self.map[i][j]
                    item_coor.append((item_type,(i,j)))
        return item_coor


    def get(self):
        return self.map




class Ai:
    def __init__(self, map, tick, map_class):     # 1. 설치된 폭탄 위치, 2. 사람 위치, 3.
        self.ai_tick = 0
        self.tick = tick
        # self.ai_direction = random.random()

        # print("---- 초기화")
        self.ai_loc_x = 13
        self.ai_loc_y = 13

        self.map = map
        self.mask = []

        self.map_c = map_class

        self.life_count = 1
        self.shield = 0

        self.case = 10

        self.ai_item_list = {5:0, 6:0, 7:0, 8:0}

    def make_mask(self):     # ai 주변 오브젝트 정보 추출
        mask = []
        for i in range(self.ai_loc_y-2, self.ai_loc_y+3):
            line = []
            for j in range(self.ai_loc_x-2, self.ai_loc_x+3):
                line.append([i, j])
            mask.append(line)
        return mask

    def find_bomb(self, bomb_temp_loc, bomb_instance):        # 폭탄 탐색
        bomb_infm = bomb_instance.get_bomb_imf()

        bomb_y = bomb_temp_loc[0]
        bomb_x = bomb_temp_loc[1]
        # bomb_x = bomb_infm[1]
        # bomb_y = bomb_infm[0]
        bomb_r = bomb_infm[4]

        self.bomb_range = []
        # for i in range(bomb_x-self.bomb_b, bomb_x+self.bomb_b+1):
        for i in range(bomb_y-bomb_r, bomb_y+bomb_r+1):
            self.bomb_range.append([i,bomb_x])
        # for j in range(bomb_y-self.bomb_b, bomb_y+self.bomb_b+1):
        for j in range(bomb_x-bomb_r, bomb_x+bomb_r+1):
            self.bomb_range.append([bomb_y, j])
        # print(self.bomb_range,"\n-------------폭탄 범위")

        if [self.ai_loc_y, self.ai_loc_x] in self.bomb_range:
            self.case = 1
        # self.bomb_range.sort()
        # print(self.bomb_range, "----------- 폭탄 범위")

    def find_item_and_block(self):
        ai_fw = [
            [self.ai_loc_y, self.ai_loc_x],
            [self.ai_loc_y + 1, self.ai_loc_x],
            [self.ai_loc_y - 1, self.ai_loc_x],
            [self.ai_loc_y, self.ai_loc_x - 1],
            [self.ai_loc_y, self.ai_loc_x + 1],
        ]
        for i in ai_fw:
            if str(self.map[i[0]][i[1]]) in "5678" and self.case >= 3:
                self.case = 3
                self.ai_loc_y = i[0]
                self.ai_loc_x = i[1]
                self.ai_item_list[self.map[i[0]][i[1]]] += 1
                # print(self.ai_item_list, "---------item")
                break
            elif self.map[i[0]][i[1]] == 4 and self.case >= 4:
                self.case = 4
                break

    def action(self, bomb_temp_loc, tick, bomb_instance):
        if tick > self.ai_tick:
            self.ai_life_count()
            self.ai_tick = tick
            mask = self.make_mask()
            # ai 기준 상하좌우 1칸씩(다음 이동 위치)
            ai_fw = [
                [self.ai_loc_y, self.ai_loc_x],
                [self.ai_loc_y+1, self.ai_loc_x],
                [self.ai_loc_y-1, self.ai_loc_x],
                [self.ai_loc_y, self.ai_loc_x-1],
                [self.ai_loc_y, self.ai_loc_x+1],
            ]
            self.find_bomb(bomb_temp_loc, bomb_instance)
            self.find_item_and_block()

            self.shield = self.ai_item_list[7]

            if self.case == 1:      # 폭탄 범위안에 ai가 있다면
                # print("폭탄 감지")
                # print(self.ai_loc_y, self.ai_loc_x, "-------------- ai 좌표")
                w = 0
                while w < 100:
                    ct = 0
                    for f in ai_fw:
                        if f in self.bomb_range or str(self.map[f[0]][f[1]]) in "014$":
                            ct += 1
                    ct2 = 0
                    for f2 in ai_fw:
                        if self.map[f2[0]][f2[1]] == 11 or str(self.map[f2[0]][f2[1]]) in "014$":
                            ct2 +=1

                    ai_fw_rand = round(random.random()*4)
                    if ct > 4:  # count >= 4 : 모든 방향이 폭탄 범위거나 벽임
                        if ct2 == 5:
                            break
                        elif str(map[ai_fw[ai_fw_rand][0]][ai_fw[ai_fw_rand][1]]) not in "0411" and ai_fw_rand != 0:
                            self.ai_loc_y = ai_fw[ai_fw_rand][0]
                            self.ai_loc_x = ai_fw[ai_fw_rand][1]
                            break

                    # ai 다음 이동위치가 폭탄 범위가 아니고 / 외벽, 내벽, 깨지는 벽이 아님
                    elif ai_fw[ai_fw_rand] not in self.bomb_range and str(map[ai_fw[ai_fw_rand][0]][ai_fw[ai_fw_rand][1]]) not in "014$":
                        self.ai_loc_y = ai_fw[ai_fw_rand][0]
                        self.ai_loc_x = ai_fw[ai_fw_rand][1]
                        print(self.ai_loc_y, self.ai_loc_x)
                        self.case = 10
                        break
                    else:
                        break
                    w +=1

            # elif self.case == 2:
            #     print("유저 감지")
            #     print("폭탄 설치")      # 폭탄 설치 함수로 대체
            #     self.case = 1

            elif self.case == 3:
                # print("아이템 감지")
                pass

            # elif self.case == 4:
            #     print("폭탄 설치")  # 폭탄 설치 함수로 대체
            #     game_map.set_bomb_position(self.ai_loc_y, self.ai_loc_x)
            #     # self.case = 1


            else:   # 주변에 아무것도 없음
                ai_direction = random.random()
                if ai_direction < 0.4 and (str(self.map[self.ai_loc_y-1][self.ai_loc_x]) not in "014$" and [self.ai_loc_y-1, self.ai_loc_x] not in self.bomb_range):
                    self.ai_loc_y -= 1
                elif ai_direction < 0.8 and (str(self.map[self.ai_loc_y][self.ai_loc_x-1]) not in "014$" and [self.ai_loc_y, self.ai_loc_x-1] not in self.bomb_range):
                    self.ai_loc_x -= 1
                elif ai_direction < 0.9 and (str(self.map[self.ai_loc_y+1][self.ai_loc_x]) not in "014$" and [self.ai_loc_y+1, self.ai_loc_x] not in self.bomb_range):
                    self.ai_loc_y += 1
                elif ai_direction < 1 and (str(self.map[self.ai_loc_y][self.ai_loc_x+1]) not in "014$" and [self.ai_loc_y, self.ai_loc_x+1] not in self.bomb_range):
                    self.ai_loc_x += 1
                else:
                    pass
        self.case = 10

    def ai_life_count(self):
        if str(self.map[self.ai_loc_y][self.ai_loc_x]) in "9$": #  폭탄 터졌을 때 범위에 있다면
            if self.shield >= 1:    # 쉴드 있다면
                self.shield -= 1
            else:   # 쉴드 없다면
                self.life_count -= 1
        return self.life_count

    def set_ai_xy(self, x, y):
        self.ai_loc_x = x
        self.ai_loc_y = y

    def get_ai_xy(self):
        return self.ai_loc_x, self.ai_loc_y

    def get_ai_item_list(self):
        return self.ai_item_list



class User:
    user_items = [7]

    def __init__(self):  # 시작 좌표 (1, 1)
        self.x = 1
        self.y = 1
        self.has_bomb = False
        self.is_die = False
        self.life_count = 3
        self.items = []
        self.shield_value = self.user_items.count(7)
        self.b_count = self.user_items.count(6)

    # def get_list(self):
    #     if (self.x == item x 좌표) and (self.y == item y 좌표):
    #         result = self.items.append()
    #         return result

    def move_x(self, direction):
        if direction == 4:
            self.x -= 1  # 왼쪽으로 이동
        elif direction == 6:
            self.x += 1  # 오른쪽으로 이동
        return self.x

    def move_y(self, direction):
        if direction == 2:
            self.y += 1  # 아래쪽으로 이동
        elif direction == 8:
            self.y -= 1  # 위쪽으로 이동
        return self.y

    def bomb(self, direction):
        if direction == 5:
            print("폭탄이 설치되었습니다.")
            self.has_bomb = True
            return True
        return False

    def die(self, bomb):
        player_x = self.x
        player_y = self.y
        bomb = bomb.bomb_range()
        for direction_range in bomb:
            if (direction_range[0][0] <= player_x <= direction_range[-1][0] and direction_range[-1][1] <= player_y <=
                    direction_range[0][1]):
                return True
        return False

    def life(self, bomb):
        if self.die(bomb_instance):
            if self.activate_shield():
                print("쉴드가 사용되었습니다.")
            elif self.life_count > 0:
                self.life_count -= 1
                print(f"목숨 -1, 남은 목숨 {self.life_count}개")
            elif self.life_count == 0:
                self.is_die = True
        return self.life_count

    def activate_shield(self):
        if game_item.shield_value == 1 and self.die(bomb_instance):  # 쉴드가 한 개 있을 때 폭탄에 닿게 되면
            game_item.shield_value = 0  # 쉴드가 0개로 됨
            return True
        return False

    def set_xy(self, x, y):
        self.x = x
        self.y = y
    def get_xy(self):
        return self.x, self.y


class Game():
    def __init__(self):
        pass

    def gui(self, tick ,user_life,ai_life,map= [[]]):
        print("\n" * 12)
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 0:
                    print("🟫", end=" ")  # 외벽
                elif map[i][j] == 1:
                    print("🟫", end=" ")  # 벽
                elif map[i][j] == 2:
                    print("🤖", end=" ")  # user
                elif map[i][j] == 3:
                    print("👾", end=" ")  # ai
                elif map[i][j] == 4:
                    print("🗑️", end=" ")  # 부숴지는 벽
                elif map[i][j] == 11:
                    print("💣", end=" ")  # user 폭탄
                elif map[i][j] == 9:
                    print("🎇", end=" ")  # user 폭탄 터지는 것
                elif map[i][j] == 5:
                    print("💥", end=" ")  #print("폭탄 범위 증가")  # 중첩 가능
                elif map[i][j] == 6:
                    print("➕", end=" ")  #print("폭탄 개수 증가")  # 중첩 가능
                elif map[i][j] == 7:
                    print("🛡️", end=" ")  #print("방어")  # 중첩 불가능
                elif map[i][j] == 8:
                    print("🏏", end=" ")  #print("던지기")  # 중첩 불가능
                # elif self.map[i][j] == 8:
                #     print("🧨", end=" ")  # ai 폭탄
                # elif self.map[i][j] == 4:
                #     print("🎆", end=" ")  # ai 폭탄 터지는 것
                elif map[i][j] == "*":
                    print("⬛", end=" ")  # 지나다닐수있는 길
                elif map[i][j] == "-":
                    print("⬛", end=" ")  # 지나다닐수있는 길
                # elif map[i][j] == "+":
                #     print("⬛", end=" ")  # 지나다닐수있는 길
                elif map[i][j] == "$":
                    print("🟥", end=" ")
                else:
                    print("🍀", end=" ")  # 아이템박스
            print()
        print("[Tick = {}]   [남은 목숨 = {}]    [AI 남은 목숨 = {}]".format(tick, user_life, ai_life))
        print("\n" * 12)

    def win_lose_gui(self,user_life, ai_life):
        if ai_life <= 0:
            print("\n" * 10)
            print("=" * 65)
            print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
            print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
            print("░░░░▓▓░░░░░░▓▓░░░░░░▓▓░░░░░▓▓▓▓▓▓▓▓░░░░░░░▓▓▓░░░░░░▓▓░░░░░▓▓░░░░░")
            print("░░░░░▓▓░░░░▓▓▓▓░░░░▓▓░░░░░░░░░▓▓░░░░░░░░░░▓▓░▓▓░░░░▓▓░░░░░▓▓░░░░░")
            print("░░░░░░▓▓░░▓▓░░▓▓░░▓▓░░░░░░░░░░▓▓░░░░░░░░░░▓▓░░▓▓░░░▓▓░░░░░▓▓░░░░░")
            print("░░░░░░░▓▓▓▓░░░░▓▓▓▓░░░░░░░░░░░▓▓░░░░░░░░░░▓▓░░░░▓▓░▓▓░░░░░░░░░░░░")
            print("░░░░░░░░▓▓░░░░░░▓▓░░░░░░░░░▓▓▓▓▓▓▓▓░░░░░░░▓▓░░░░░░▓▓▓░░░░░▓▓░░░░░")
            print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
            print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
            print("=" * 65)
            print("\n" * 10)
        elif user_life <= 0:
            print("\n" * 10)
            print("=" * 65)
            print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
            print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
            print("░░░░░▓▓░░░░░░░░░░▓▓▓▓▓▓░░░░░░░▓▓▓▓▓▓░░░░░░▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░")
            print("░░░░░▓▓░░░░░░░░░▓▓░░░░▓▓░░░░░▓▓░░░░░░░░░░░▓▓░░░░░░░░░░░░░░░░░░░░░")
            print("░░░░░▓▓░░░░░░░░░▓▓░░░░▓▓░░░░░░░▓▓░░░░░░░░░▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░")
            print("░░░░░▓▓░░░░░░░░░▓▓░░░░▓▓░░░░░░░░░░▓▓░░░░░░▓▓░░░░░░░░░░░░░░░░░░░░░")
            print("░░░░░▓▓▓▓▓▓▓░░░░░▓▓▓▓▓▓░░░░░░░▓▓▓▓▓▓░░░░░░▓▓▓▓▓▓▓░░░▓▓░░▓▓░░▓▓░░░")
            print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
            print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
            print("=" * 65)
            print("\n" * 10)

    def collision_check(self,x,y,dir,map = [[]]):
        if map[y][x] == 0 or map[y][x] == 1 or map[y][x] == 4 or map[y][x]=='$':
            if dir == 2:
                y -= 1
            elif direction == 8:
                y += 1
            elif direction == 4:
                x += 1
            elif direction == 6:
                x -= 1
            return x, y
        else:
            return x, y

    def item_check(self, x, y, map=[[]]):
        item_no = 200
        if map[y][x] == 5:
            item_no = 5
        elif map[y][x] == 6:
            item_no = 6
        elif map[y][x] == 7:
            item_no = 7
        elif map[y][x] == 8:
            item_no = 8
        return item_no



tick111 = 1
max = 10000
game_user = User()
game_map = Map()
game = Game()
game_map.create_map()
game_map.break_wall()

x_ai_set = 13
y_ai_set = 13
bomb_instance = Bomb(0, 0, "user1", max)
x_set = 1
y_set = 1
b1 = 0
b2 = 0
ai_map = Map()
game_ai = Ai(game_map.get(), tick111, ai_map)
while True:
    if game_user.life_count <= 0 or game_ai.life_count <= 0:
        game.win_lose_gui(game_user.life_count, game_ai.life_count)
        break
    map = game_map.get()
    game.gui(tick111, game_user.life_count, game_ai.life_count, map)
    #game_map.display_map()
    try:
        direction = int(input("이동 방향을 입력하세요 (2: 아래, 4: 왼쪽, 6: 오른쪽, 8: 위쪽): "))
    except Exception as E:
        print("잘못 입략")
    game_user.move_x(direction)
    game_user.move_y(direction)
    game_map.del_user(x_set, y_set)
    x_set, y_set = game_user.get_xy()
    x_set, y_set = game.collision_check(x_set, y_set, direction, map)
    item = game.item_check(x_set, y_set, map)
    game_item = Item(item)
    print(item)
    game_user.set_xy(x_set, y_set)
    game_map.set_user_position(x_set, y_set)
    print(y_set, x_set)
    if direction == 5:
        game_map.set_bomb_position(x_set, y_set)
        bomb_instance = Bomb(y_set, x_set, "user1", tick111)
        b1 = y_set
        b2 = x_set
    bomb_coordinates = bomb_instance.bomb_range()
    for i in range(len(bomb_coordinates)):
        if (y_set, x_set) in bomb_coordinates[i]:
            print("위험")
            if game_user.life_count > 0:
                pass
                #bomb_instance.use_bomb()
            else:
                print("Game Over")
                break
            break
    game_user.life(bomb_instance)
    bomb_instance.tick(tick111)
    # game_user.die(bomb_instance)
    game_map.remove_wall_in_bomb_range(bomb_instance)
    game_map.clear_explosion(bomb_instance)

    game_ai.action([b1, b2], tick111, bomb_instance)
    game_map.del_user(x_ai_set, y_ai_set)
    x_ai_set, y_ai_set = game_ai.get_ai_xy()


    game_ai.set_ai_xy(x_ai_set, y_ai_set)
    game_map.set_ai_position(x_ai_set, y_ai_set)
    game_ai.ai_life_count()
    game_map.end_map()
    tick111 += 1