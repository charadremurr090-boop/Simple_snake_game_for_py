import curses
import random
 
HEIGHT = 20   # высота поля
WIDTH = 40    # ширина поля
 
 
def main(stdscr):
    stdscr.keypad(True)       # чтобы работали стрелки
    stdscr.timeout(150)       # ждать клавишу не дольше 150 мс скорость игры
 
    # змейка - список клеток [строка, столбец], голова первая
    snake = [[10, 20], [10, 19], [10, 18]]
 
    # направление движения: сначала вправо
    dy = 0
    dx = 1

    score = 0
    food_y = 0   # 0 значит "еды пока нет"
    food_x = 0
 
    while True:
        # если еды нет или она попала в змейку, создаём новую
        while food_y == 0 or [food_y, food_x] in snake:
            food_y = random.randint(1, HEIGHT - 2)
            food_x = random.randint(1, WIDTH - 2)
 
        # рисуем
        stdscr.clear()
        stdscr.border()
        stdscr.addstr(food_y, food_x, "*")
        stdscr.addstr(0, 2, " Score: " + str(score) + " ")
        for part in snake:
            stdscr.addstr(part[0], part[1], "o")
        stdscr.addstr(snake[0][0], snake[0][1], "@")
 
        # читаем клавишу если не нажата, вернётся -1
        key = stdscr.getch()
 
        if key == ord("q"):
            break
        elif key == curses.KEY_UP and dy != 1:
            dy = -1
            dx = 0
        elif key == curses.KEY_DOWN and dy != -1:
            dy = 1
            dx = 0
        elif key == curses.KEY_LEFT and dx != 1:
            dy = 0
            dx = -1
        elif key == curses.KEY_RIGHT and dx != -1:
            dy = 0
            dx = 1
 
        # новая часть
        new_head = [snake[0][0] + dy, snake[0][1] + dx]
 
        # проверка: врезались в стену или в себя
        if new_head[0] == 0 or new_head[0] == HEIGHT - 1:
            break
        if new_head[1] == 0 or new_head[1] == WIDTH - 1:
            break
        if new_head in snake:
            break
 
        # двигаем змейку
        snake.insert(0, new_head)
 
        if new_head == [food_y, food_x]:
            score = score + 1     # съели еду - змейка растёт
            food_y = 0            # сигнал, что нужна новая еда
        else:
            snake.pop()           # не съели - убираем хвост
 
    # конец игры
    stdscr.timeout(-1)            # теперь ждём нажатия клавиши без ограничения
    stdscr.addstr(HEIGHT // 2, 8, "GAME OVER!")
    stdscr.addstr(HEIGHT // 2 + 1, 8, "Press any key")
    stdscr.getch()
 
 
curses.wrapper(main)