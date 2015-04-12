from Tkinter import *
import sys, os
import pygame
import pygame.camera
import RPi.GPIO as GPIO
import thread, time
import MySQLdb as mdb
import dropbox


con = mdb.connect(
    host = 'proyectosuvg.db.5434369.hostedresource.com', # host, usualmente localhost
    user = 'proyectosuvg', # nombre de usuario
    passwd = 'dbAdmin!0', # password si lo tiene
    db = 'proyectosuvg') # nombre de la base de datos


cur = con.cursor()

app_key = 'y4p0gkil950k5fa'
app_secret = '8dhuzdrngcmu121'
sess = dropbox.session.DropboxSession(app_key,app_secret)

#flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
#authorize_url = flow.start()

pygame.init()
pygame.camera.init()
screen = pygame.display.set_mode((480,320),0)
cam_list = pygame.camera.list_cameras()
webcam = pygame.camera.Camera(cam_list[0],(32,24))
webcam.start()


GPIO.setmode(GPIO.BOARD)

GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(21, GPIO.OUT, initial=0)
GPIO.setup(22, GPIO.OUT, initial=0)
GPIO.setup(23, GPIO.OUT, initial=0)
GPIO.setup(24, GPIO.OUT, initial=0)

#21 22 delanteros
#23 24 traseros
#--------------------------------
#ventana


def keyUp(event):
    GPIO.output(21, 1)
    GPIO.output(23, 0)
    GPIO.output(22, 1)
    GPIO.output(24, 0)
    print "Avanzar"

def keyDown(event):
    GPIO.output(21, 0)
    GPIO.output(23, 1)
    GPIO.output(22, 0)
    GPIO.output(24, 1)
    print "Retroceder"

def keyRight(event):
    GPIO.output(21, 1)
    GPIO.output(23, 0)
    GPIO.output(22, 0)
    GPIO.output(24, 1)
    print "Derecha"

def keyLeft(event):
    GPIO.output(21, 0)
    GPIO.output(23, 1)
    GPIO.output(22, 1)
    GPIO.output(24, 0)
    print "Izquierda"

def keyRelease(event):
    GPIO.output(21, 0)
    GPIO.output(23, 0)
    GPIO.output(22, 0)
    GPIO.output(24, 0)
    print "Detenido"

def keyS(event):
    imagen = webcam.get_image()
    imagen = pygame.transform.scale(imagen,(480,320))
    name = time.strftime("%H;%M;%S")+"--"+time.strftime("%d_%m_%y")
    pygame.image.save(imagen, name+".bmp")
    print'ok'
    
    f = open(name+'.bmp', 'rb')
    print 'abrio imagen'
    response = client.put_file('/MarceloBot/'+name+'.bmp', f)
    print 'elimina'
    os.remove(name+'.bmp')

def manual(n):
    window = Toplevel(n)
    window.geometry("100x100")
    frame = Frame(window)
    frame.bind("<Up>", keyUp)
    frame.bind("<Down>", keyDown)
    frame.bind("<Left>", keyLeft)
    frame.bind("<Right>", keyRight)
    frame.bind("<KeyRelease-Up>", keyRelease)
    frame.bind("<KeyRelease-Down>", keyRelease)
    frame.bind("<KeyRelease-Left>", keyRelease)
    frame.bind("<KeyRelease-Right>", keyRelease)
    frame.bind("<s>", keyS)
    frame.focus_set()

    frame.pack()



def myfunc(n,m):
    while True:
        imagen = webcam.get_image()
        imagen = pygame.transform.scale(imagen,(320,240))
        screen.blit(imagen,(0,0))

        #draw all updates to display
        pygame.display.update()
        #root.after(100,task)
        time.sleep(0.2)

def main():
    
    root = Tk()
    btn = Button(root, text = "Manual", command = lambda n=root: manual(n))
    btn.configure(bg = 'gray', state= 'normal')
    btn.pack()
    btn.place(relx = 0.3, rely =0.3, relheight = 0.3, relwidth = 0.5)

    root.geometry("350x250")
    root.title("MARCELO")
    root.resizable(width=FALSE, height=FALSE)
    
    root.mainloop()

thread.start_new_thread(myfunc,('s','a'))
seguir = True
while seguir:
    with con:
        a = 0
        usuario = raw_input('Ingrese nombre de usuario: ')
        cur.execute("SELECT * FROM Marcelo WHERE ID= %s",usuario)
        resultado = cur.fetchall()
        for row in resultado:
            password = row[1]
            access = row[3]
            a = 1
        if a == 1:
            contrasena = raw_input('Ingrese contrasena: ')
            if contrasena == ""+password:
                seguir = False
                print 'Bienvenido '+usuario
                token_key,token_secret = row[3].split('|')
                sess.set_token(token_key,token_secret)
                client = dropbox.client.DropboxClient(sess)
                
                #access_token, user_id = flow.finish(access)
                #client = dropbox.client.DropboxClient(access_token)
                main()
            else:
                print 'Datos incorrectos'
        else:
            print 'Datos incorrectos'


#----------------------------------

GPIO.cleanup()
webcam.stop()
pygame.quit()
sys.exit()


