from ursina import *
app = Ursina()
def toggle_fullscreen():
    window.fullscreen = not window.fullscreen
    if window.fullscreen:
        button_fullscreen.text = 'Minimize'
    else:
        button_fullscreen.text = 'Fullscreen'

button_fullscreen = Button(
    text='Fullscreen',  
    position=(0.50, -0.15), 
    scale=(0.2, 0.1), 
    color=color.azure, 
    on_click=toggle_fullscreen
)
meja = Entity(
    model='cube',
    color=color.black,
    scale=(2,1,3),
    rotation=(90,0,0)
)


bola = Entity(
    model='sphere',
    color=color.orange,
    z=-1,
    scale=0.1,
    collider='box'
)


player1 = Entity(
    model='cube',
    color=color.blue,
    scale=(0.6,0.1,1),
    position=(0,-1.5,-1),
    collider='box'
)
player2 = Entity(
    model='cube',
    color=color.red,
    scale=(0.6,0.1,1),
    position=(0,1.5,-1),
    collider='box'
)


speed_x = speed_y = 0  

score_player1 = 0
score_player2 = 0


tampilan_score_p1 = Text(text=str(score_player1), position=(-0.25, -0.4), scale=2)
tampilan_score_p2 = Text(text=str(score_player2), position=(0.25, 0.4), scale=2)


def start_game():
    global speed_x, speed_y
    speed_x = speed_y = 1 


pause_game = False
prev_speed_x = prev_speed_y = 0  

def pause():
    global pause_game, speed_x, speed_y, prev_speed_x, prev_speed_y, button_pause
    if pause_game:
        speed_x, speed_y = prev_speed_x, prev_speed_y  
        button_pause.text = 'Pause'
    else:
        prev_speed_x, prev_speed_y = speed_x, speed_y  
        speed_x = speed_y = 0  
        button_pause.text = 'Resume'
    pause_game = not pause_game


button_start = Button(
    text="Start Game", 
    position=(0.50, 0.30), 
    scale=(0.2, 0.1), 
    color=color.azure,
    on_click=start_game)


button_pause = Button(
    text="Pause", 
    position=(0.50, 0.15), 
    scale=(0.2, 0.1), 
    color=color.azure, 
    on_click=pause)

def restart_game():
    global score_player1, score_player2, speed_x, speed_y
    score_player1 = score_player2 = 0
    speed_x = speed_y = 0  # Reset kecepatan bola
    tampilan_score_p1.text = str(score_player1)
    tampilan_score_p2.text = str(score_player2)
    bola.position = (0, 0, -1)
    button_pause.text = 'Pause' 

button_restart = Button(
    text="Restart Game", 
    position=(0.50, 0.0), 
    scale=(0.2, 0.1), color=color.azure, 
    on_click=restart_game
    )


def update():
    global speed_x, speed_y, score_player1, score_player2
    if not pause_game:
        player1.x += held_keys['d'] * time.dt
        player1.x -= held_keys['a'] * time.dt
        player2.x += held_keys['right arrow'] * time.dt
        player2.x -= held_keys['left arrow'] * time.dt
        bola.x += speed_x * time.dt
        bola.y += speed_y * time.dt

        if abs(bola.x) > 1:
            speed_x = -speed_x

        if bola.y < -1.5: 
            bola.x = bola.y = 0
            score_player2 += 1
            tampilan_score_p2.text = str(score_player2)
        elif bola.y > 1.5: 
            bola.x = bola.y = 0
            score_player1 += 1
            tampilan_score_p1.text = str(score_player1)

        if bola.intersects(player1).hit or bola.intersects(player2).hit:
            speed_y = -speed_y

camera.orthographic = True
camera.fov = 4
app.run()
