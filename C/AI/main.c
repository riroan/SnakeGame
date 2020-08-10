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
int speed = 50;
int food = 0;
int d[4] = { UP,RIGHT,LEFT,DOWN };

void draw_field();
void draw_snake();
void erase_snake();
void move();
void create_food();
void change_direction(int key);
void status();
bool crash(int current);
bool crash_body(int next);

// AI source
void getAction();
void view_field()
{
	for (int i = 0; i < SIZE_Y; i++)
	{
		gotoxy(SIZE_X * 2 + 7, i + 1);
		for (int j = 0; j < SIZE_X; j++)
			printf(" %2d", field[i][j]);
	}
}

int main()
{
	setcursortype(NOCURSOR);
	randomize();
	snake[0] = rand() % (SIZE_X*SIZE_Y / 2);
	create_food();
	draw_field();
	while (1)
	{
		delay(speed);

		getAction();

		status();
		move();
		if (length == SIZE_X * SIZE_Y - 1)
			break;
		view_field();
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
	gotoxy(5, SIZE_Y + 5);
	if (direction == LEFT)
		printf("direction : ←");
	else if (direction == DOWN)
		printf("direction : ↓");
	else if (direction == RIGHT)
		printf("direction : →");
	else if (direction == UP)
		printf("direction : ↑");
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
	for (int i = 0; i < SIZE_X; i++)
		for (int j = 0; j < SIZE_Y; j++)
			if (field[j][i] == -1)
				field[j][i] = 0;
	for (int i = length - 2; i >= 0; i--)
		snake[i + 1] = snake[i];
	snake[0] = next_head;
	for (int i = 0; i < length; i++)
		field[snake[i] / SIZE_X][snake[i] % SIZE_X] = -1;
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
		food = random_number;
		return;
	}
}

void getAction()
{
	int px = snake[0] % SIZE_X;
	int py = snake[0] / SIZE_X;

	if (food / SIZE_X < py)		// food up
		if (direction != DOWN)
			direction = UP;
		else
			direction = LEFT;
	else if (food / SIZE_X > py)	// food down
		if (direction != UP)
			direction = DOWN;
		else
			direction = RIGHT;
	else if (food % SIZE_X > px)	// food right
		if (direction != LEFT)
			direction = RIGHT;
		else
			direction = DOWN;
	else if (food % SIZE_X < px)	// food left
		if (direction != RIGHT)
			direction = LEFT;
		else
			direction = UP;

	if (field[py - 1][px] == -1 && direction == UP)
	{
		if (field[py][px + 1] != -1)	direction = RIGHT;
		else if (field[py][px - 1] != -1) direction = LEFT;
	}
	else if (field[py + 1][px] == -1 && direction == DOWN)
	{
		if (field[py][px + 1] != -1)	direction = RIGHT;
		else if (field[py][px - 1] != -1) direction = LEFT;
	}
	else if (field[py][px + 1] == -1 && direction == RIGHT)
	{
		if (field[py + 1][px] != -1)	direction = DOWN;
		else if (field[py - 1][px] != -1)	direction = UP;
	}
	else if (field[py][px - 1] == -1 && direction == LEFT)
	{
		if (field[py + 1][px] != -1)	direction = DOWN;
		else if (field[py - 1][px] != -1)	direction = UP;
	}

	if (px == 0 && direction == LEFT)
		do
		{
			direction = d[rand() % 4];
		} while (direction != LEFT && direction != RIGHT);
	else if (py == 0 && direction == UP)
		do
		{
			direction = d[rand() % 4];
		} while (direction != UP && direction != DOWN);
	else if (px == SIZE_X - 1 && direction == RIGHT)
		do
		{
			direction = d[rand() % 4];
		} while (direction != LEFT && direction != RIGHT);
	else if (py == SIZE_Y - 1 && direction == DOWN)
		do
		{
			direction = d[rand() % 4];
		} while (direction != UP && direction != DOWN);
}