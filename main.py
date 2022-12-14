import pygame
from pygame import mixer
pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (0,0,0)
white = (255,255,255)
gray = (128,128,128)
green = (0,255,0) 
red = (255,0,0) 
gold = (212,175,55)
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("Beat Maker")
label_font = pygame.font.Font("OpenSans-Regular.ttf",32)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
bpm = 240 
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
playing = True
active_len = 0
active_beat = 0
beat_changed = True


#loading sounds
hi_hat = mixer.Sound("sound\kit2\hihat.WAV")
kick = mixer.Sound("sound\kit2\kick.WAV")
snare = mixer.Sound("sound\kit2\snare.WAV")
floor_Tom = mixer.Sound("sound\kit2\\tom.WAV")
clap = mixer.Sound("sound\kit2\clap.WAV")
crash = mixer.Sound("sound\kit2\crash.WAV")

def playNotes():
	for i in range(len(clicked)):
		if clicked[i][active_beat] == 1:
			if i == 0:
				hi_hat.play()
			if i == 1:
				snare.play()
			if i == 2:
				kick.play()
			if i == 3:
				crash.play()
			if i == 4:
				clap.play()
			if i == 5:
				floor_Tom.play()

def draw_grid(clicked,beat):
	boxes = []
	left_box = pygame.draw.rect(screen, gray,[0,0,200,HEIGHT-195],5)
	bottom_box = pygame.draw.rect(screen,gray,[0,HEIGHT-200,WIDTH,200],5)
	colors = [gray,white,gray]
	hi_hat_text = label_font.render("Hi Hat", True,white)
	screen.blit(hi_hat_text,(30,30))
	snare_text = label_font.render("Snare", True,white)
	screen.blit(snare_text,(30,130))
	kick_text = label_font.render("Kick", True,white)
	screen.blit(kick_text,(30,230))
	crash_text = label_font.render("Crash", True,white)
	screen.blit(crash_text,(30,330))
	clap_text = label_font.render("Clap", True,white)
	screen.blit(clap_text,(30,430))
	floor_tom_text = label_font.render("Floor Tom", True,white)
	screen.blit(floor_tom_text,(30,530))
	for i in range(1,instruments):
		pygame.draw.line(screen,gray,(0,(i*100)),(195,(i*100)),4)
	for i in range(beats):
		for j in range(instruments):
			if clicked[j][i] == -1:
				color = gray
			else:
				color = green
			rect = pygame.draw.rect(screen,color,[(i * ((WIDTH-200) // beats) + 205,(j * 100)+5),(((WIDTH - 200) //beats)-10,((HEIGHT - 200) // instruments)-10)],0,3) 
			rect = pygame.draw.rect(screen,gold,[(i * ((WIDTH-200) // beats) + 200,(j * 100)),(((WIDTH - 200) //beats),((HEIGHT - 200) // instruments))],7,5) 
			rect = pygame.draw.rect(screen,gray,[(i * ((WIDTH-200) // beats) + 200,(j * 100)),((WIDTH - 200) //beats,(HEIGHT - 200) // instruments)],2,5) 
			boxes.append((rect,(i,j)))
		active = pygame.draw.rect(screen,red,[(beat * (WIDTH-200) //beats)+200,0,(WIDTH-200)//beats,(HEIGHT - 200)],7,3)
	return boxes



run = True
while run:
	timer.tick(fps)
	screen.fill(black)
	boxes = draw_grid(clicked,active_beat)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			for i in range(len(boxes)):
				if boxes[i][0].collidepoint(event.pos):
					coords = boxes[i][1]
					clicked[coords[1]][coords[0]] *= -1
	beat_len = 3600 // bpm

	if playing:
		if active_len < beat_len:
			active_len += 1
		else:
			active_len = 0
			if active_beat < beats-1 :
				active_beat += 1
				beat_changed = True
			else:
				active_beat = 0
				beat_changed = True
	if beat_changed:
		playNotes()
		beat_changed = False
	pygame.display.flip()
pygame.quit()