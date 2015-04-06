# implementation of card game - Memory
import simplegui
import random

l1 = range(8)
l2 = range(8)
deck = l1+l2
exposed = []
turns = 0
state = 0

temp = []

# function to initialize globals
def new_game():
    global deck, exposed, turns, state, temp
    temp = [-1, -1]
    turns = 0
    state = 0
    exposed = [0] * 16
    random.shuffle(deck)
    label.set_text("Turns = "+str(turns))

# event handlers
def mouseclick(pos):
    global state, turns, temp
    
    index = int(pos[0]//50)
    if state == 0:
        if exposed[index] == 0:
            if deck[temp[0]] != deck[temp[1]]:
                exposed[temp[0]] = 0
                exposed[temp[1]] = 0
            exposed[index] = 1
            state = 1
            temp[0] = index
    elif state == 1:
        if(exposed[index] == 0):
            state=0
            exposed[index] = 1
            temp[1] = index
            turns += 1  
            label.set_text("Turns = "+str(turns))
                      
# cards are logically 50x100 pixels in size    
def draw(canvas):
    p = [20, 60]
    
    for i in range(len(deck)):
        if exposed[i] == 0:
            canvas.draw_polygon([[50*i, 0], [50*(i+1),0],
                                 [50*(i+1),100], [50*i, 100]],
                                2, "white", "green")
        else:
            canvas.draw_text(str(deck[i]), [50*i + p[0], p[1]], 30, 'Red')

# frame, buttons and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
