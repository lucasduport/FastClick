import pygame
import time
from pygame.locals import *
from os import path
from random import randint

class Carre :
	def __init__(self):
		self.color=[255,140,0]
		self.position=[]

	def draw(self):
		pygame.draw.rect(fenetre, self.color, self.position, 0)

	def est_clique(self):
		(x,y)=pygame.mouse.get_pos()
		if x<=int(self.position[0]+self.position[2]) and x>=int(self.position[0]):
			if y<=int(self.position[1]+self.position[3]) and y>=int(self.position[1]):
				return True
		return False

def get_difficulty():
	fenetre.fill([255,140,0])

	easy , medium , difficult = Carre() , Carre(), Carre()
	easy.color , easy.position = [255,255,255],[100,135,600,140]
	easy.draw()
	medium.color , medium.position = [255,255,255],[100,310,600,140]
	medium.draw()
	difficult.color , difficult.position = [255,255,255],[100,485,600,140]
	difficult.draw()

	police=pygame.font.SysFont("rubikbold",100)
	image_texte=police.render("EASY",1,(153,50,204))
	fenetre.blit(image_texte,(260,150))

	police=pygame.font.SysFont("rubikbold",100)
	image_texte=police.render("MEDIUM",1,(153,50,204))
	fenetre.blit(image_texte,(190,325))

	police=pygame.font.SysFont("rubikbold",100)
	image_texte=police.render("DIFFICULT",1,(153,50,204))
	fenetre.blit(image_texte,(135,500))

	pygame.display.flip()
	while True :
		for event in pygame.event.get():
			if event.type == 1025:
				if easy.est_clique():
					return 4
				if medium.est_clique():
					return 16
				if difficult.est_clique():
					return 64
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
				pygame.display.quit()

def determiner_position(k,nb_carres):
	left=int((k-(int(((k/nb_carres)-0.001)*(nb_carres**0.5)))*nb_carres**0.5)*(cote/(nb_carres**0.5))-(cote/(nb_carres**0.5)))
	top=int((1+int(((k/nb_carres)-0.001)*(nb_carres**0.5)))*(cote/(nb_carres**0.5))-(cote/(nb_carres**0.5)))
	width=int(cote/(nb_carres**0.5))
	height=width
	return [left,top,width,height]

def carre_generation(nb_carres):
	liste_carres=[]
	for k in range(1,nb_carres+1):
		position=determiner_position(k,nb_carres)
		k=Carre()
		k.position=position
		liste_carres.append(k)
	return liste_carres

def generation_cible(nb_carres,liste_carres,ancienne_cible):
	liste_carres[ancienne_cible].color=[255,140,0]
	carre_rouge=randint(0,nb_carres-1)
	liste_carres[carre_rouge].color=[153,50,204]
	carre_rouge_pos=liste_carres[carre_rouge].position
	while liste_carres[ancienne_cible].position==liste_carres[carre_rouge].position:
		liste_carres[carre_rouge].color=[255,140,0]
		carre_rouge=randint(0,nb_carres-1)
		liste_carres[carre_rouge].color=[153,50,204]
		carre_rouge_pos=liste_carres[carre_rouge].position
	return carre_rouge

def cible_touchee(carre_rouge_pos, nb_carres):
	(x,y)=pygame.mouse.get_pos()
	if x<=int(carre_rouge_pos[0]+cote/(nb_carres**0.5)) and x>=int(carre_rouge_pos[0]) and pygame.mouse.get_pressed()[0]:
		if y<=int(carre_rouge_pos[1]+cote/(nb_carres**0.5)) and y>=int(carre_rouge_pos[1]):
			return True
	return False

def clique_menu(bouton):
	(x,y)=pygame.mouse.get_pos()
	if x<=int(bouton.position[0]+bouton.position[2]) and x>=int(bouton.position[0]) and pygame.mouse.get_pressed()[0]:
		if y<=int(bouton.position[1]+bouton.position[3]) and y>=int(bouton.position[1]):
			return True
	return False

def is_highscore(score,nb_carres):
	if nb_carres==4:
		difficulty=0
	elif nb_carres==16:
		difficulty=1
	else:
		difficulty=2
	try:
		file=open("highscore.txt","x")
		file.close()
	except:
		pass
	file=open("highscore.txt", "r")
	read_data=file.read()
	if read_data=='':
		file.close()
		file=open("highscore.txt", "w")
		file.write("0?0?0")
		file.close()
		return True
	else:
		read_data=read_data.split("?")
		ancien_hs=float(read_data[difficulty])
		if score>ancien_hs:
			file.close()
			return True
		else:
			file.close()
			return False

def get_highscore(nb_carres):
	if nb_carres==4:
		difficulty=0
	elif nb_carres==16:
		difficulty=1
	else:
		difficulty=2
	with open("highscore.txt", "r") as file:
		data = file.read()
		data = data.split("?")
	return float(data[difficulty])

def set_highscore(score,nb_carres):
	if nb_carres==4:
		difficulty=0
	elif nb_carres==16:
		difficulty=1
	else:
		difficulty=2
	with open("highscore.txt", "r") as file:
		data = file.read()
		data = data.split("?")
		data[difficulty]=score
		data="?".join(str(x) for x in data)
	with open("highscore.txt", "w") as file:
		file.write(data)

def get_score(sec,score,clique,nb_carres):
	mins = sec // 60
	sec = sec % 60
	hours = mins // 60
	mins = mins % 60
	secondes=round(sec+60*mins+60*60*hours,2)
	pygame.event.pump()
	fenetre.fill([255,140,0])

	police=pygame.font.SysFont("rubikbold",23)
	image_texte=police.render("Vous avez une moyenne de "+str(round(score*5/sec,2))+" cibles par 5 secondes",1,(255,255,255))
	fenetre.blit(image_texte,(60,200))

	police=pygame.font.SysFont("rubikbold",23)
	image_texte=police.render("et une précision moyenne de "+str(round(score/clique,2)*100)+"% en "+str(round(sec,1))+" secondes de jeu",1,(255,255,255))
	fenetre.blit(image_texte,(50,250))

	police=pygame.font.SysFont("rubikbold",62)
	image_texte=police.render("FastClick",1,(153,50,204))
	fenetre.blit(image_texte,(270,50))

	if is_highscore(round(score*5/sec,2),nb_carres):
		police=pygame.font.SysFont("rubikbold",35)
		image_texte=police.render("Bravo ! Vous avez réalisé votre record !",1,(255,255,255))
		fenetre.blit(image_texte,(65,300))

		police=pygame.font.SysFont("rubikbold",35)
		image_texte=police.render(str("L'ancien record était de "+str(get_highscore(nb_carres))+""),1,(255,255,255))
		fenetre.blit(image_texte,(145,350))

		set_highscore(round(score*5/sec,2),nb_carres)

	else:
		police=pygame.font.SysFont("rubikbold",35)
		image_texte=police.render("Dommage, vous allez y arriver...",1,(255,255,255))
		fenetre.blit(image_texte,(135,350))

		police=pygame.font.SysFont("rubikbold",35)
		image_texte=police.render(str("Le record a battre est de "+str(get_highscore(nb_carres))+""),1,(255,255,255))
		fenetre.blit(image_texte,(135,400))

	police=pygame.font.SysFont("rubikbold",15)
	image_texte=police.render("by Lucas Duport ©",1,(153,50,204))
	fenetre.blit(image_texte,(655,770))

	pygame.display.flip()
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				menu()
			if event.type == pygame.QUIT:
				pygame.display.quit()

def menu():
	menu=1
	fenetre.fill([255,140,0])

	jouer=Carre()
	jouer.color,jouer.position=[153,50,204],[200,300,400,100]
	jouer.draw()

	quitter=Carre()
	quitter.color,quitter.position=[153,50,204], [300,500,200,50]
	quitter.draw()

	police=pygame.font.SysFont("arialblack",40)
	image_texte=police.render("JOUER",1,(255,255,255))
	fenetre.blit(image_texte,(330,320))

	police=pygame.font.SysFont("arialblack",20)
	image_texte=police.render("QUITTER",1,(255,255,255))
	fenetre.blit(image_texte,(350,510))

	police=pygame.font.SysFont("rubikbold",62)
	image_texte=police.render("Bienvenue sur FastClick",1,(153,50,204))
	fenetre.blit(image_texte,(20,50))

	police=pygame.font.SysFont("rubikbold",15)
	image_texte=police.render("by Lucas Duport ©",1,(153,50,204))
	fenetre.blit(image_texte,(655,770))

	pygame.display.flip()
	while menu==1:
		pygame.event.pump()
		if pygame.mouse.get_pressed()[0]:
			if jouer.est_clique():
				menu=0
			if quitter.est_clique():
				pygame.display.quit()
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
				pygame.display.quit()
	jeu()

def compte_a_rebours():
	fenetre.fill([255,140,0])

	pygame.display.flip()
	police=pygame.font.SysFont("rubikbold",200)
	image_texte=police.render("3",1,(153,50,204))
	fenetre.blit(image_texte,(340,280))
	pygame.display.flip()
	time.sleep(0.60)

	fenetre.fill([255,140,0])
	police=pygame.font.SysFont("rubikbold",200)
	image_texte=police.render("2",1,(153,50,204))
	fenetre.blit(image_texte,(340,280))
	pygame.display.flip()
	time.sleep(0.60)

	fenetre.fill([255,140,0])
	police=pygame.font.SysFont("rubikbold",200)
	image_texte=police.render("1",1,(153,50,204))
	fenetre.blit(image_texte,(340,280))
	pygame.display.flip()
	time.sleep(0.60)

def jeu():
	start_time=time.time()
	nb_carres=get_difficulty()
	liste_carres=carre_generation(nb_carres)
	carre_rouge=generation_cible(nb_carres,liste_carres,1)
	score , clique, jeu= 0,0.00001,1
	compte_a_rebours()
	while jeu:
		for carre in liste_carres:
			carre.draw()
		for event in pygame.event.get():
			if event.type == 1025:
				if liste_carres[carre_rouge].est_clique():
					carre_rouge=generation_cible(nb_carres,liste_carres,carre_rouge)
					score+=1
				clique+=1
			if event.type == pygame.KEYDOWN:
				get_score(time.time()-start_time,score,clique,nb_carres)
			if event.type == pygame.QUIT:
				pygame.display.quit()

		pygame.display.flip()
		time.sleep(0.0002)
#PYGAME INIT
cote=800
ecran = (cote,cote)
pygame.display.init()
pygame.font.init()
pygame.display.set_caption('FastClick by Lucas Duport')
#programIcon = pygame.image.load('FastClick.png')
#pygame.display.set_icon(programIcon)
fenetre = pygame.display.set_mode(ecran)
#--
menu()
