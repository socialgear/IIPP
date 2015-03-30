# Implementation of classic arcade game Pong
# Copy the code in www.codeskulptor.org and run.

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]	# ball position initialized
    
    # Assigning random velocities to ball within an appropriate range
    if direction == RIGHT:
        ball_vel = [random.randrange(3, 6), -(random.randrange(1, 5))]
    elif direction == LEFT:
        ball_vel = [-(random.randrange(3, 6)), -(random.randrange(1, 5))]

# event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    
    # randomly choosing the side to which the ball will move
    if random.randrange(0, 2) == 0:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)
    
    # global variable initialization
    paddle1_vel = 0
    paddle2_vel = 0
    
    score1 = 0
    score2 = 0
    
    paddle2_vel = 0
    paddle1_vel = 0
    
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # drawing mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # ball position update
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Reflection from top and bottom wall
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]

    # drawing the ball 
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "yellow", "yellow")    
    
    # updating paddle's vertical position, keeping it on the screen (+-3 just to make it look nice on boundaries)
    
    if (paddle1_vel < 0) and (paddle1_pos[1] >= HALF_PAD_HEIGHT + 3):
        paddle1_pos[1] += paddle1_vel
    elif (paddle1_vel > 0) and (paddle1_pos[1] <= HEIGHT - HALF_PAD_HEIGHT - 3):
        paddle1_pos[1] += paddle1_vel
    
    if (paddle2_vel < 0) and (paddle2_pos[1] >= HALF_PAD_HEIGHT + 3):
        paddle2_pos[1] += paddle2_vel
    elif (paddle2_vel > 0) and (paddle2_pos[1] <= HEIGHT - HALF_PAD_HEIGHT - 3):
        paddle2_pos[1] += paddle2_vel
        

    # drawing paddles
    canvas.draw_polygon([(paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT),
                         (paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT),
                         (paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT),
                         (paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT)], 1, "white", "white")
    
    canvas.draw_polygon([(paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT),
                         (paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT),
                         (paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT),
                         (paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT)], 1, "white", "white")
    
    # paddle and ball collision detection
    
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if (ball_pos[1] >= paddle1_pos[1] - HALF_PAD_HEIGHT) and (ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT):
            ball_vel[0] = -ball_vel[0]	# reflection by reversing the horizontal velocity
            ball_vel[0] += 1			# increasing the velocity after reflection
        else:
            score2 += 1					# opposite scores
            spawn_ball(RIGHT)			# ball spawn to the scorer

    if ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        if (ball_pos[1] >= paddle2_pos[1] - HALF_PAD_HEIGHT) and (ball_pos[1] <= paddle2_pos[1] + HALF_PAD_HEIGHT):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] -= 1
        else:
            score1 += 1
            spawn_ball(LEFT)			# same as above
    
    
    # drawing scores
    canvas.draw_text(str(score1), [150, 50], 40, "white")
    canvas.draw_text(str(score2), [450, 50], 40, "white")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= 5
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 5
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= 5
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 5
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0


# frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.add_button('Restart', new_game, 100)

# start
new_game()
frame.start()
