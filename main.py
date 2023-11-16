from extensions import *
from config import *
import random
from time import sleep


class Board:
    def __init__(self):
        self.matrix = self.create_board()
        self.enemy_matrix = self.create_board()
        self.limit = [('■', '■', '■'), ('■', '■'), ('■', '■'), ('■'), ('■'), ('■'),
                      ('■')]  # Если список окажется пуст, вызовем ошибку
        self.list_of_indeces = []  # Будем сюда добавлять индексы расположения кораблей во время их создания
        self.list_of_indeces_shots = [[]]  # Индексы выстрелов
        self.counter_of_ships = 0
        self.hid = bool(0)

    def get_my_board(self):
        for i in range(len(self.matrix)):
            print(*self.matrix[i], end='')
            print()

    def get_enemy_board(self):
        for i in range(len(self.enemy_matrix)):
            print(*self.enemy_matrix[i], end='')
            print()

    def get_board(self):
        return self.matrix

    @staticmethod
    def create_board():
        matrix = []
        for _ in range(7):
            temp = [i for i in range(7)]
            matrix.append(temp)
        for row in range(1, 7):
            for col in range(7):
                if col == 0:
                    matrix[row][col] = row
                else:
                    matrix[row][col] = FREE_CELL
        matrix[0][0] = ' '
        return matrix

    def add_ship(self, row, col, route, length):
        try:
            @staticmethod
            def check_used_ships(limit,
                                 length):  # Если корабль доступен в списке, возвращает список, вычеркивая из него этот корабль
                flag = False
                for i in limit:
                    if len(i) == length:
                        flag = True
                        limit.remove(i)
                        break
                if not flag:
                    raise UserException('Корабли этого типа закончились.')
                return limit

            @staticmethod
            def is_available_indeces_of_ship(matrix, row, col, route, length):
                if matrix[row][col] == MARK_OF_SHIP:
                    raise UserException
                if route != 0 and route != 1:
                    raise UserException
                if length > 3 or length < 0:
                    raise UserException
                if (0 < row < len(matrix)) and (0 < col < len(matrix)):
                    if (row > 4 and route == 1 and length == 3) or (row == 6 and route == 1 and length > 1):
                        raise IndexException
                    if (col > 4 and route == 0 and length == 3) or (col == 6 and route == 0 and length > 1):
                        raise IndexException
                else:
                    raise IndexException(f'Введены неверные координаты: ({row};{col})')
                s = Ship(length, (row, col), route).dots()
                if route:
                    for i in s:
                        dot = Dot(*i)
                        if matrix[dot.x - 1][dot.y] == MARK_OF_SHIP or matrix[dot.x - 1][dot.y - 1] == MARK_OF_SHIP:
                            raise IndexException
                        try:
                            if matrix[dot.x - 1][dot.y + 1] == MARK_OF_SHIP:
                                raise IndexException
                        except IndexError:
                            pass
                        try:
                            if matrix[dot.x][dot.y - 1] == MARK_OF_SHIP:
                                raise IndexException
                            if matrix[dot.x][dot.y + 1] == MARK_OF_SHIP:
                                raise IndexException
                        except IndexError:
                            pass
                        try:
                            if matrix[dot.x + 1][dot.y] == MARK_OF_SHIP:
                                raise IndexException
                            if matrix[dot.x + 1][dot.y - 1] == MARK_OF_SHIP:
                                raise IndexException
                            if matrix[dot.x + 1][dot.y + 1] == MARK_OF_SHIP:
                                raise IndexException
                        except IndexError:
                            pass
                else:
                    for i in s:
                        dot = Dot(*i)
                        if matrix[dot.x][dot.y - 1] == MARK_OF_SHIP or matrix[dot.x - 1][dot.y - 1] == MARK_OF_SHIP:
                            raise IndexException
                        try:
                            if matrix[dot.x + 1][dot.y - 1] == MARK_OF_SHIP:
                                raise IndexException
                        except IndexError:
                            pass
                        try:
                            if matrix[dot.x - 1][dot.y] == MARK_OF_SHIP:
                                raise IndexException
                            if matrix[dot.x + 1][dot.y] == MARK_OF_SHIP:
                                raise IndexException
                        except IndexError:
                            pass
                        try:
                            if matrix[dot.x][dot.y + 1] == MARK_OF_SHIP:
                                raise IndexException
                            if matrix[dot.x - 1][dot.y + 1] == MARK_OF_SHIP:
                                raise IndexException
                            if matrix[dot.x + 1][dot.y + 1] == MARK_OF_SHIP:
                                raise IndexException
                        except IndexError:
                            pass

            is_available_indeces_of_ship(self.matrix, row, col, route, length)
            limit = check_used_ships(self.limit, length)
        except (IndexException, UserException) as e:
            pass
        else:
            self.list_of_indeces.append(Ship(length, (row, col), route).dots())
            self.limit = limit.copy()
            for i in self.list_of_indeces[self.counter_of_ships]:
                dot = Dot(*i)
                self.matrix[dot.x][dot.y] = MARK_OF_SHIP
            self.matrix = self.countour(route, self.matrix, self.counter_of_ships, self.list_of_indeces)
            self.counter_of_ships += 1

    @staticmethod
    def countour(route, matrix, counter, indeces):
        COUNTOUR_RAISE = MARK_OF_SHIP + '-123456' + HIT_MISS + HIT_IN_SHIP
        if route:
            for i in indeces[counter]:
                dot = Dot(*i)
                try:
                    if str(matrix[dot.x - 1][dot.y]) not in COUNTOUR_RAISE:
                        matrix[dot.x - 1][dot.y] = TERRYTORY_OF_SHIP
                        if str(matrix[dot.x - 1][dot.y - 1]) not in COUNTOUR_RAISE:
                            matrix[dot.x - 1][dot.y - 1] = TERRYTORY_OF_SHIP
                    if str(matrix[dot.x - 1][dot.y + 1]) not in COUNTOUR_RAISE:
                        matrix[dot.x - 1][dot.y + 1] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass

                if str(matrix[dot.x][dot.y - 1]) not in COUNTOUR_RAISE:
                    matrix[dot.x][dot.y - 1] = TERRYTORY_OF_SHIP
                try:
                    if matrix[dot.x][dot.y + 1] not in COUNTOUR_RAISE:
                        matrix[dot.x][dot.y + 1] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass
                try:
                    if str(matrix[dot.x + 1][dot.y]) not in COUNTOUR_RAISE:
                        matrix[dot.x + 1][dot.y] = TERRYTORY_OF_SHIP
                        if str(matrix[dot.x + 1][dot.y - 1]) not in COUNTOUR_RAISE:
                            matrix[dot.x + 1][dot.y - 1] = TERRYTORY_OF_SHIP
                    if str(matrix[dot.x + 1][dot.y + 1]) not in COUNTOUR_RAISE:
                        matrix[dot.x + 1][dot.y + 1] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass
            return matrix
        else:
            for i in indeces[counter]:
                dot = Dot(*i)
                try:
                    if str(matrix[dot.x][dot.y - 1]) not in COUNTOUR_RAISE:
                        matrix[dot.x][dot.y - 1] = TERRYTORY_OF_SHIP
                        if str(matrix[dot.x - 1][dot.y - 1]) not in COUNTOUR_RAISE:
                            matrix[dot.x - 1][dot.y - 1] = TERRYTORY_OF_SHIP
                    if str(matrix[dot.x + 1][dot.y - 1]) not in COUNTOUR_RAISE:
                        matrix[dot.x + 1][dot.y - 1] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass

                if str(matrix[dot.x - 1][dot.y]) not in COUNTOUR_RAISE:
                    matrix[dot.x - 1][dot.y] = TERRYTORY_OF_SHIP
                try:
                    if matrix[dot.x + 1][dot.y] not in COUNTOUR_RAISE:
                        matrix[dot.x + 1][dot.y] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass
                try:
                    if str(matrix[dot.x][dot.y + 1]) not in COUNTOUR_RAISE:
                        matrix[dot.x][dot.y + 1] = TERRYTORY_OF_SHIP
                        if str(matrix[dot.x - 1][dot.y + 1]) not in COUNTOUR_RAISE:
                            matrix[dot.x - 1][dot.y + 1] = TERRYTORY_OF_SHIP
                    if str(matrix[dot.x + 1][dot.y + 1]) not in COUNTOUR_RAISE:
                        matrix[dot.x + 1][dot.y + 1] = TERRYTORY_OF_SHIP
                except IndexError:
                    pass
            return matrix

    def shot(self, x, y):
        dot = Dot(x, y)
        if (0 < x < len(self.matrix)) and (0 < y < len(self.matrix)):
            if HIT_IN_SHIP in self.matrix[dot.x][dot.y] or HIT_MISS in self.matrix[dot.x][dot.y]:
                raise UserException('Нельзя стрелять в одну и ту же точку')
        else:
            raise IndexException('Координаты выходят за пределы поля')
        if MARK_OF_SHIP in self.matrix[dot.x][dot.y]:
            self.matrix[dot.x][dot.y] = HIT_IN_SHIP
            self.enemy_matrix[dot.x][dot.y] = HIT_IN_SHIP
            self.list_of_indeces_shots[0].append((dot.x, dot.y))
            for index in range(len(self.list_of_indeces)):
                if (dot.x, dot.y) in self.list_of_indeces[index]:
                    los1 = len(self.list_of_indeces[index]) - self.list_of_indeces[index].count(HIT_IN_SHIP)
                    self.list_of_indeces[index].append(HIT_IN_SHIP)
                    hp = self.is_ship_killed(los1, self.list_of_indeces[index])
                    return True, hp
        else:
            self.matrix[dot.x][dot.y] = HIT_MISS
            self.enemy_matrix[dot.x][dot.y] = HIT_MISS
            return False, False

    def is_ship_killed(self, los1, los2):
        hp = Ship(los1, los2[0]).check_hp(len(los2))
        if hp == 0:
            if los1 != 1:
                route = Ship(los2, los2[0]).get_route()
            else:
                route = 1
            self.enemy_matrix = self.countour(route, self.enemy_matrix, 0, self.list_of_indeces_shots)
            self.list_of_indeces_shots = [[]]
            self.counter_of_ships -= 1
            return hp
        return hp


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_dots(self):
        return self.x, self.y


class Ship:
    def __init__(self, length, dot, route=None):
        self.length = length
        self.dot = Dot(*dot)
        self.route = route
        self.hp = None

    def dots(self):
        list_of_indeces = []
        if self.route:
            for i in range(self.length):
                tpl = (self.dot.x + i, self.dot.y)
                list_of_indeces.append(tpl)
        else:
            for i in range(self.length):
                tpl = (self.dot.x, self.dot.y + i)
                list_of_indeces.append(tpl)
        return list_of_indeces

    def check_hp(self, los2):
        self.hp = self.length - los2 + self.length
        return self.hp

    def get_route(self):
        if self.length[0][0] != self.length[1][0]:
            return 1
        else:
            return 0


class Player:
    def __init__(self):
        self.moves = Board()

    def ask(self):
        pass

    def move(self):
        return self.moves.shot(*self.ask())


class User(Player):  # Этим классом пользуется AI, чтобы передать нужную доску в Board()
    def ask(self):
        x = random.randint(1, 6)
        y = random.randint(1, 6)
        return x, y


class AI(Player):
    def ask(self):
        print('Введите координаты точки, куда хотите выстрелить')
        s = [int(i) for i in input().split()]
        if len(s) != 2:
            raise UserException('Должно быть только 2 аргумента')
        x, y = s
        return x, y


class Game:
    def __init__(self):
        self.user = User()
        self.ai = AI()
        self.whose_move = random.randint(0, 1)
        self.flag = False

    def start(self):
        self.clear_user_board()
        self.clear_ai_board()
        self.greet()
        print(f'Хотите, чтобы корабли расставились автоматически?\nY - Да\nN - Нет')
        ans = input().lower()
        if ans == 'y':
            self.flag = True
            self.random_board()
            print('Ваша доска:\n')
            self.ai.moves.get_enemy_board()
            print('-------------')
            self.user.moves.get_my_board()
            print()
        else:
            self.random_board()
            self.own_board()
        self.loop()

    def loop(self):
        if self.whose_move:
            print('Ваш ход\n')
            self.ai.moves.get_enemy_board()
            print('-------------')
            self.user.moves.get_my_board()
            if self.ai.moves.hid > 0:
                print('-------------')
                self.ai.moves.get_my_board()
            while True:
                try:
                    is_hit, hp = self.ai.move()
                    if is_hit:
                        if hp == 0:
                            print('Корабль врага уничтожен!\n')
                        else:
                            print('Корабль врага подбит!\n')
                        sleep(2)
                        self.ai.moves.get_enemy_board()
                        print('-------------')
                        self.user.moves.get_my_board()
                        if self.ai.moves.hid > 0:
                            print('-------------')
                            self.ai.moves.get_my_board()
                        if self.ai.moves.counter_of_ships == 0:
                            break
                        continue
                    print('Промах.\n')
                    self.whose_move = 0
                    break
                except Exception as e:
                    print(e)
        if self.ai.moves.counter_of_ships == 0:
            print('\nВсе корабли уничтожены!\n')
            print('Победил игрок!\n')
            ask = input('Желаете начать новую игру?\nY - Да\nN - Нет\n').lower()
            if ask == 'y':
                self.start()
            else:
                raise SystemExit('Конец игры')
        print('Ход противника\n')
        while True:
            try:
                is_hit, hp = self.user.move()
                if is_hit:
                    sleep(2)
                    if hp == 0:
                        print('Ваш корабль уничтожен.\n')
                    else:
                        print(f'Противник попал по вашему кораблю.\nУ него осталось {hp} ед. здоровья.\n')
                        sleep(4)
                    self.user.moves.get_my_board()
                    print()
                    if self.user.moves.counter_of_ships == 0:
                        break
                    continue
                sleep(2)
                print('Противник промахнулся!\n')
                sleep(1)
                self.whose_move = 1
                break
            except UserException:
                pass
        if self.user.moves.counter_of_ships == 0:
            print('\nВсе корабли уничтожены!\n')
            print('Победил компьютер!\n')
            ask = input('Желаете начать новую игру?\nY - Да\nN - Нет\n').lower()
            if ask == 'y':
                self.start()
            else:
                raise SystemExit('Конец игры')
        self.loop()

    def own_board(self):
        print(f'Список доступных кораблей:\n{self.user.moves.limit}')
        print(
            'Введите параметры корабля в формате:\n<Номер строки> <Номер столбца> <Направление (1 - вертикально, 0 - горизонтально> <Длина>')
        print('Если после ввода доска не изменилась, значит вы допустили ошибку при вводе данных')
        while True:
            if len(self.user.moves.limit) <= 2:
                print('Если вы не смогли разместить все корабли на поле, пропишите clear')
                ask = input().lower()
                if ask == 'clear':
                    self.clear_user_board()
            try:
                s = [int(i) for i in input().split()]
                row, col, route, length = s
                self.user.moves.add_ship(row, col, route, length)
            except (ValueError, IndexError) as e:
                print(f'Данные введены неверно\n{e}')
                print(
                    'Введите параметры корабля в формате:\n<Номер строки> <Номер столбца> <Направление (1 - вертикально, 0 - горизонтально> <Длина>')
            else:
                self.ai.moves.get_enemy_board()
                print('-------------')
                self.user.moves.get_my_board()
                if len(self.user.moves.limit) == 0:
                    break

    def random_board(self):
        counter = 0
        if self.flag:
            while counter < 100:
                length = len(self.user.moves.limit[0])
                row = random.randint(1, 6)
                col = random.randint(1, 6)
                route = random.randint(0, 1)
                self.user.moves.add_ship(row, col, route, length)
                if len(self.user.moves.limit) == 0:
                    self.flag = False
                    self.random_board()
                    break
                counter += 1
            if len(self.user.moves.limit) != 0:
                self.clear_user_board()
                self.random_board()
        else:
            counter = 0
            while counter < 100:
                length = len(self.ai.moves.limit[0])
                row = random.randint(1, 6)
                col = random.randint(1, 6)
                route = random.randint(0, 1)
                self.ai.moves.add_ship(row, col, route, length)
                if len(self.ai.moves.limit) == 0:
                    break
                counter += 1
            if len(self.ai.moves.limit) != 0:
                self.clear_ai_board()
                self.random_board()

    def clear_user_board(self):
        self.user.moves.matrix = self.user.moves.create_board()
        self.user.moves.enemy_matrix = self.user.moves.create_board()
        self.user.moves.limit = [('■', '■', '■'), ('■', '■'), ('■', '■'), ('■'), ('■'), ('■'), ('■')]
        self.user.moves.list_of_indeces = []
        self.user.moves.counter_of_ships = 0

    def clear_ai_board(self):
        self.ai.moves.matrix = self.ai.moves.create_board()
        self.ai.moves.enemy_matrix = self.ai.moves.create_board()
        self.ai.moves.limit = [('■', '■', '■'), ('■', '■'), ('■', '■'), ('■'), ('■'), ('■'), ('■')]
        self.ai.moves.list_of_indeces = []
        self.ai.moves.counter_of_ships = 0

    def greet(self):
        print('Приветствуем вас в игре "Морской бой".')
        print('В начале игры у вас будет выбор, самому распределить корабли на доске или случайным образом.')
        print('Верхнее поле - поле врага, там будут помечаться ваши попадания и промахи. Нижнее поле - ваша доска.')
        print('Координаты выстрела указываются в формате <x> <y> (через пробел).')
        print('Кто делает первый ход, определяется случайно\n')
        ask = input('Хотите, чтобы доска врага выводилась на экран?\nY - Да\nN - Нет\n').lower()
        if ask == 'y':
            self.ai.moves.hid = bool(1)
        else:
            self.ai.moves.hid = bool(0)


Game().start()
