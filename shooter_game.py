from pygame import *
from random import randint 


#música de fondo
mixer.init()
mixer.music.load('fire.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont("Arial;", 40)
win = font1.render('¡victoria!', True,( 46, 168, 230))
lose = font1.render('fatallity!', True, (6, 55, 59))  

font2 = font.SysFont ("Arial", 40)

#necesitamos las siguientes imágenes:
img_back = "Luna.jpg" #fondo de juego
img_hero = "nave.png" #héroe
img_enemy = "alien.png"
img_bullet = 'bullet.png'

score = 0
lost = 0
max_lost = 5
goal = 20

#clase padre para otros objetos
class GameSprite(sprite.Sprite):
 #constructor de clase
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Llamada al constructor de la clase (Sprite):
       sprite.Sprite.__init__(self)


       #cada objeto debe almacenar la propiedad image
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       #cada objeto debe tener la propiedad rect – el rectángulo en el que está
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #método de dibujo del personaje en la ventana
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


#clase de jugador principal
class Player(GameSprite):
   #método para controlar el objeto con las teclas de las flechas
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #método para “disparar” (usa la posición del jugador para crear una bala)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost 
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0 
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 10:
            self.kill()

#Crea una ventana
win_width = 700
win_height = 500
display.set_caption("Tirador")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

#crea objetos
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), - 40, 80, 50,  randint(5, 10  ))
    monsters.add(monster)
 
bullets = sprite.Group()

#la variable “el juego terminó”: cuando sea True, los objetos dejan de funcionar en el ciclo principal
finish = False
#Ciclo de juego principal:
run = True #la bandera se restablece por el botón de cerrar ventana
while run:
   #Evento de pulsado del botón “Cerrar”
   for e in event.get():
       if e.type == QUIT:
           run = False

       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               fire_sound.play()
               ship.fire()



   if not finish:
       #actualiza el fondo
       window.blit(background,(0,0))


      

       #ejecuta los movimientos del objeto
       ship.update()
       monsters.update()
       bullets.update()



       #los actualiza en una nueva ubicación en cada iteración del ciclo
       ship.reset()
       monsters.draw(window)
       bullets.draw(window)

       collides = sprite.groupcollide(monsters, bullets, True, True)
       for c in collides:
            score = score  + 1 
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50,randint(5, 10))
            monsters.add(monster)


       if sprite.spritecollide(ship, monsters, False) or lost  >= max_lost:
            finish = True
            window.blit(lose, (200, 200))


       if score >= goal:
            finish = True 
            window.blit(win, (200, 200))


       text = font2.render("lista: " + str(score ), 1, (254, 59, 81))
       window.blit(text, (10, 20))


       text_lose = font2.render("fallado: " + str (lost), 1, (254, 59, 81))
       window.blit(text_lose, (10,50))


       display.update()

   else:
       finish = False 
       score = 0 
       lost = 0
       for b in bullets:
           b.kill()
       for m in monsters:
           m.kill()
   #el ciclo se ejecuta cada 0.05 seg
       time.delay(300)
       for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50,randint(5, 10))
            monsters.add(monster)
   time.delay(50)