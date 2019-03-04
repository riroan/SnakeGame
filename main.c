#include"util.h"
#define SIZE_X 20	// 가로길이
#define SIZE_Y 20	// 세로길이
#define FOOD 10
#define LEFT 75
#define RIGHT 77
#define UP 72
#define DOWN 80
#define SPEED_DISCOUNT 3
#define SPEED_MIN 30

int length = 1;
int direction = DOWN;
int snake[SIZE_X*SIZE_Y];
int field[SIZE_Y][SIZE_X] = { 0 };
int speed = 100;

void draw_field();
void draw_snake();
void erase_snake();
void move();
void create_food();
void change_direction(int key);
void status();
bool crash(int current);
bool crash_body(int next);

int main()
{
	setcursortype(NOCURSOR);
	randomize();
	snake[0] = 0;
	create_food();
	draw_field();
	while (1)
	{
		int key = 0;

		if (_kbhit())
			do
			{
				key = _getch();
			} while (key == 224);

		delay(speed);

		if (key == RIGHT || key == LEFT || key == UP || key == DOWN)
			change_direction(key);

		move();
		status();
		if (length == SIZE_X * SIZE_Y - 1)
			break;
	}
	clrscr();
	gotoxy(20, 10);
	SetColor(GREEN);
	printf("YOU WIN!!");
	SetColor(WHITE);
}

void status()
{
	gotoxy(5, SIZE_Y + 3);
	printf("speed  : %3d", speed);
	gotoxy(5, SIZE_Y + 4);
	printf("length : %3d", length);
}

void change_direction(int key)
{
	switch (key)
	{
	case RIGHT:
		if (direction != LEFT)
			direction = RIGHT;
		return;
	case LEFT:
		if (direction != RIGHT)
			direction = LEFT;
		return;
	case UP:
		if (direction != DOWN)
			direction = UP;
		return;
	case DOWN:
		if (direction != UP)
			direction = DOWN;
		return;
	}
}

void draw_field()
{
	for (int i = 0; i < SIZE_X + 2; i++)
		printf("■");
	printf("\n");
	for (int i = 0; i < SIZE_Y; i++)
	{
		printf("■");
		for (int j = 0; j < SIZE_X; j++)
			printf("  ");
		printf("■\n");
	}
	for (int i = 0; i < SIZE_X + 2; i++)
		printf("■");
}

void draw_snake()
{
	SetColor(YELLOW);
	for (int i = 0; i < SIZE_Y; i++)
		for (int j = 0; j < SIZE_X; j++)
		{
			gotoxy(2 * j + 2, i + 1);
			if (field[i][j] == FOOD)
				printf("★");
			else
				printf("  ");
		}
	SetColor(GREEN);
	for (int i = 0; i < length; i++)
	{
		gotoxy(2 * (snake[i] % SIZE_X) + 2, snake[i] / SIZE_X + 1);
		printf("●");
		SetColor(WHITE);
	}
}

void erase_snake()
{
	gotoxy(2 * (snake[length - 1] % SIZE_X) + 2, snake[length - 1] / SIZE_X + 1);
	printf("  ");
}

void move()
{
	int next_head;
	switch (direction)
	{
	case LEFT:
		next_head = snake[0] - 1;
		break;
	case RIGHT:
		next_head = snake[0] + 1;
		break;
	case UP:
		next_head = snake[0] - SIZE_X;
		break;
	case DOWN:
		next_head = snake[0] + SIZE_X;
		break;
	}

	if (crash(snake[0]) || crash_body(next_head))
	{
		printf("Game OVER\n");
		exit(0);
	}
	if (field[next_head / SIZE_X][next_head%SIZE_X] == FOOD)
	{
		field[next_head / SIZE_X][next_head%SIZE_X] = 0;
		length++;
		create_food();
		if (speed > SPEED_MIN)
			speed -= SPEED_DISCOUNT;
	}
	else
		erase_snake();
	for (int i = length - 2; i >= 0; i--)
		snake[i + 1] = snake[i];
	snake[0] = next_head;
	draw_snake();
}

bool crash(int current)
{
	if (current / SIZE_X == 0 && direction == UP)
		return true;
	if (current / SIZE_X == SIZE_X - 1 && direction == DOWN)
		return true;
	if (current%SIZE_X == 0 && direction == LEFT)
		return true;
	if (current%SIZE_X == SIZE_Y - 1 && direction == RIGHT)
		return true;
	return false;
}

bool crash_body(int next)
{
	for (int i = 0; i < length; i++)
		if (snake[i] == next)
			return true;
	return false;
}

void create_food()
{
	int random_number;

	while (1)
	{
LABEL:
		random_number = rand() % (SIZE_X*SIZE_Y);
		for (int i = 0; i < length; i++)
			if (random_number == snake[i])
				goto LABEL;

		field[random_number / SIZE_X][random_number%SIZE_X] = FOOD;
		return;
	}
}