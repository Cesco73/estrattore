#!/usr/bin/python
# -*- coding: latin -*-

import string
import os 
import random
import re
import pygame
import time
import thread
from ocempgui.widgets import *
from ocempgui.widgets.Constants import *

debug = 1
suono = 0

inputfile = open("lista.txt")
invenduti = open("invenduti.txt","w")

# Definisco il vettore che conterrà la lista dei giocatori e lo riempio
giocatori = []
for giocatore in inputfile.readlines(): 
	giocatori.append(giocatore.strip())
inputfile.close()

# Creazione della finestra principale
finestra = Renderer ()
finestra.create_screen (1018,740) # Crea la finestra principale
finestra.color = (250,250,250)

# Definizione della strip del titolo
testo = Label ('Fantacalcio 2007/2008' )
testo.padding = 5
testo.create_style ()["font"]["size"] = 48
testo.create_style ()["font"]["name"] = "Georgia"
testo.create_style ()["font"]["color"] = (130, 210, 205)
testo.multiline = True
testo.set_minimum_size(1015,40)

# FUNZIONI RICHIAMATE NEL PROGRAMMA

# funzione CLICK per attivare la voce
def click (testo):
	global suono
	if suono == 1:
		suono = 0
		buttonSuono.set_text(text="Attiva Voce")
	else:
		suono = 1
		buttonSuono.set_text(text="Disattiva Voce")

# Estrai il giocatore scritto nella casella
def get_entry (entry):
    global preso
    preso = entry.get_text
    print preso

# funzione AUDIO per estrazione
def voce (estratto):
	voicefile =  open("estratto.txt","w")
	voicefile.write("Giocatore estratto:" + estratto)
	voicefile.flush()
	voicefile.close()
	os.system('text2wave estratto.txt > estratto.wav')
	os.system('mplayer -speed 0.95 estratto.wav')

# funzione AUDIO per acquisto
def comprato (acquisto):
	voicefile =  open("acquisto.txt","w")
	voicefile.write(squadra + " si aggiudica: " + acquisto + " peerr: " + prezzo + " milioni di euro" )
	voicefile.close()
	os.system('text2wave acquisto.txt > acquisto.wav')
	os.system('mplayer acquisto.wav')

# funzione per il bottone ESTRAI (la prima che viene chiamata all'atto dell'estrazione del giovatore)
def pesca (etichetta):
	global pescato
#	if len(giocatori) == 0:
#		etichetta.set_text("Estrazione conclusa")
#		return 0
#	else:
	estratto = random.choice(giocatori)
	giocatori.remove(estratto)
	outputfile = open("lista.txt","w")	
	for giocatore in giocatori: # riscrive tutta la lista dei giocatori escluso il giocatore rimosso
		outputfile.write(giocatore + "\n")
	outputfile.close()
	rimuovivirgolette = string.replace(estratto, "\"", "")
	pescato = string.replace(rimuovivirgolette, ",", " - ")
	pescasplit = string.split(pescato,"-")
	plextracted = pescasplit[2] + "-" + pescasplit[1] + "-" + pescasplit[3] + "-" + (pescasplit[0])
	etichetta.set_text(pescato)
	if suono == 1:
		voce(pescasplit[2])		
	buttonRej.sensitive = True
	buttonEst.sensitive = False
	p1.b.sensitive = True
	p2.b.sensitive = True
	p3.b.sensitive = True
	p4.b.sensitive = True
	p5.b.sensitive = True
	p6.b.sensitive = True
	p7.b.sensitive = True
	p8.b.sensitive = True


# funzione per INVENDUTI
def scarta (etichetta):
	invenduti.write(pescato + "\n")
	invenduti.flush()
	buttonEst.sensitive = True
	buttonRej.sensitive = False
	p1.b.sensitive = False
	p2.b.sensitive = False
	p3.b.sensitive = False
	p4.b.sensitive = False
	p5.b.sensitive = False
	p6.b.sensitive = False
	p7.b.sensitive = False
	p8.b.sensitive = False
	p1.entry.set_text("")
	p2.entry.set_text("")
	p3.entry.set_text("")
	p4.entry.set_text("")
	p5.entry.set_text("")
	p6.entry.set_text("")
	p7.entry.set_text("")
	p8.entry.set_text("")

# funzione per COMPRA
def compra (etichetta, pl):
	if pl.entry.text.isdigit() and ( int(pl.entry.text) < int(pl.soldi) ):
		filtro = re.compile('(^\S*) - (\S*) - (.*) - (\S*)')
		if pescato:
			risultato = filtro.match(pescato)
			ruolo = risultato.group(2)
			nomegiocatore = risultato.group(3)
			portieri = ""
			difensori = ""
			centrocampisti = ""
			attaccanti = ""
			sortedP = ""
			sortedD = ""
			sortedC = ""
			sortedA = ""
			if ruolo == "P":
				pl.hashP[pescato] = pl.entry.text
				for chiave in pl.hashP.iterkeys():
					match=filtro.match(chiave)
					portieri = portieri + match.group(3) + " " + "(" + pl.hashP[chiave] + ")" + "\n"
				pl.fileP.write(risultato.group(3) + " " + "(" + pl.entry.text + ")" + "\n")
				pl.fileP.flush()
				global squadra
				squadra = pl.nomesquadra
				global acquisto
				acquisto = match.group(3) + ":"
				global prezzo
				prezzo = pl.entry.text
				pl.soldi = pl.soldi - int(pl.entry.text)
				pl.labsoldi.set_text (u'\u20ac ' + str(pl.soldi))
				pl.l1.set_text (portieri)
				pl.entry.set_text("")
				if suono == 1:
					comprato(acquisto)

			elif ruolo == "D":
				pl.hashD[pescato] = pl.entry.text
				for chiave in pl.hashD.iterkeys():
					match=filtro.match(chiave)
					difensori = difensori + match.group(3) + " " + "(" + pl.hashD[chiave] + ")" + "\n"
				pl.fileD.write(risultato.group(3) + " " + "(" + pl.entry.text + ")" + "\n")
				pl.fileD.flush()
				global squadra
				squadra = pl.nomesquadra
				global acquisto
				acquisto = match.group(3) + ":"
				global prezzo
				prezzo = pl.entry.text
				pl.soldi = pl.soldi - int(pl.entry.text)
				pl.labsoldi.set_text (u'\u20ac ' + str(pl.soldi))
				pl.l2.set_text (difensori)
				pl.entry.set_text("")
				if suono == 1:
					comprato(acquisto)

			elif ruolo == "C":
				nomefile = pl.fileC.name
				pl.hashC[pescato] = pl.entry.text
				for chiave in pl.hashC.iterkeys():
					match=filtro.match(chiave)
					centrocampisti = centrocampisti + match.group(3) + " " + "(" + pl.hashC[chiave] + ")" + "\n" 
				#pl.vecC = centrocampisti.split("\n")
				#pl.vecC.sort(reverse=True)
				#centrocampisti = "\n".join(pl.vecC)
				pl.fileC.write(nomegiocatore + " " + "(" + pl.entry.text + ")" + "\n")
				pl.fileC.flush()
				global squadra
				squadra = pl.nomesquadra
				global acquisto
				acquisto = match.group(3) + ":"
				global prezzo
				prezzo = pl.entry.text
				pl.soldi = pl.soldi - int(pl.entry.text)
				pl.labsoldi.set_text (u'\u20ac ' + str(pl.soldi))
				pl.l3.set_text (centrocampisti)
				pl.entry.set_text("")
				if suono == 1:
					comprato(acquisto)

			else: 
				pl.hashA[pescato] = pl.entry.text
				for chiave in pl.hashA.iterkeys():
					match=filtro.match(chiave)
					attaccanti = attaccanti + match.group(3) + " " + "(" + pl.hashA[chiave] + ")" + "\n"
				pl.fileA.write(risultato.group(3) + " " + "(" + pl.entry.text + ")" + "\n")
				pl.fileA.flush()
				global squadra
				squadra = pl.nomesquadra
				global acquisto
				acquisto = match.group(3) + ":"
				global prezzo
				prezzo = pl.entry.text
				pl.soldi = pl.soldi - int(pl.entry.text)
				pl.labsoldi.set_text (u'\u20ac ' + str(pl.soldi))
				pl.l4.set_text (attaccanti)
				pl.entry.set_text("")
				if suono == 1:
					comprato(acquisto)

			buttonRej.sensitive = False
			buttonEst.sensitive = True
			p1.b.sensitive = False
			p2.b.sensitive = False
			p3.b.sensitive = False
			p4.b.sensitive = False
			p5.b.sensitive = False
			p6.b.sensitive = False
			p7.b.sensitive = False
			p8.b.sensitive = False
	else:
		pass

# definizione della CLASSE player
class player:
	"informazioni sui giocatori e (soprattutto) le loro rispettive squadre"
	def __init__(self, bname, filenameP, filenameD, filenameC, filenameA, bx, by, lx, ly, nome, bminsizex=125, bminsizey=25, lminsizex=125, lminsizey=600):
		self.hashP = {}
		self.hashD = {}
		self.hashC = {}
		self.hashA = {}
		self.vecP = []
		self.vecD = []
		self.vecC = []
		self.vecA = []
		self.soldi = 300
		self.fileP = open (filenameP, "w")
		self.fileD = open (filenameD, "w")
		self.fileC = open (filenameC, "w")
		self.fileA = open (filenameA, "w")
		self.b = Button ('Compra')
		self.la = Label ('PORTIERI') 
		self.la.set_align(ALIGN_TOP)
		self.lb = Label ('DIFENSORI') 
		self.lb.set_align(ALIGN_TOP)
		self.lc = Label ('CENTROCAMPISTI') 
		self.lc.set_align(ALIGN_TOP)
		self.ld = Label ('ATTACCANTI') 
		self.ld.set_align(ALIGN_TOP)
		self.l1 = Label ('') # Colonna dove vengono inseriti i portieri comprati
		self.l1.set_align(ALIGN_TOP | ALIGN_LEFT)
		self.l2 = Label ('') # Colonna dove vengono inseriti i difensori comprati
		self.l2.set_align(ALIGN_TOP | ALIGN_LEFT)
		self.l3 = Label ('') # Colonna dove vengono inseriti i centrocampisti comprati
		self.l3.set_align(ALIGN_TOP | ALIGN_LEFT)
		self.l4 = Label ('') # Colonna dove vengono inseriti i attaccanti comprati
		self.l4.set_align(ALIGN_TOP | ALIGN_LEFT)
		self.labsq = Label (bname)
		self.labsq.create_style ()["font"]["size"] = 22
		self.labsoldi = Label ( u'\u20ac ' + str(self.soldi))
		self.labsoldi.create_style ()["font"]["size"] = 32
		self.nomesquadra = (nome)
		self.entry = Entry ()

		self.b.sensitive = False
		self.b.topleft = (bx+60,by+2)
		self.b.minsize = (65, 20)
		self.b.padding = 3
		self.b.create_style ()["font"]["size"] = 22
		self.b.connect_signal (SIG_CLICKED, compra, testo, self )

		self.la.padding = 0
		self.la.multiline = True
		self.la.topleft = (lx, 158)
		self.la.set_minimum_size(lminsizex,10)
		self.la.set_maximum_size(lminsizex,10)
		self.la.create_style ()["font"]["size"] = 16
		self.la.create_style ()["fgcolor"][STATE_NORMAL] = (255,255,255)
		self.la.create_style ()["bgcolor"][STATE_NORMAL] = (0, 102, 204)

		self.l1.padding = 0
		self.l1.multiline = True
		self.l1.topleft = (lx, 169)
		self.l1.set_minimum_size(lminsizex,75)
		self.l1.set_maximum_size(lminsizex,75)
		self.l1.create_style ()["font"]["size"] = 16
		self.l1.create_style ()["bgcolor"][STATE_NORMAL] = (238,237,116)

		self.lb.padding = 0
		self.lb.multiline = True
		self.lb.topleft = (lx, 245)
		self.lb.set_minimum_size(lminsizex,10)
		self.lb.set_maximum_size(lminsizex,10)
		self.lb.create_style ()["font"]["size"] = 16
		self.lb.create_style ()["fgcolor"][STATE_NORMAL] = (255,255,255)
		self.lb.create_style ()["bgcolor"][STATE_NORMAL] = (0, 102, 204)

		self.l2.padding = 0
		self.l2.multiline = True
		self.l2.topleft = (lx, 256)
		self.l2.set_minimum_size(lminsizex,169)
		self.l2.set_maximum_size(lminsizex,169)
		self.l2.create_style ()["font"]["size"] = 16
		self.l2.create_style ()["bgcolor"][STATE_NORMAL] = (199,255,155)

		self.lc.padding = 0
		self.lc.multiline = True
		self.lc.topleft = (lx, 426)
		self.lc.set_minimum_size(lminsizex,10)
		self.lc.set_maximum_size(lminsizex,10)
		self.lc.create_style ()["font"]["size"] = 16
		self.lc.create_style ()["fgcolor"][STATE_NORMAL] = (255,255,255)
		self.lc.create_style ()["bgcolor"][STATE_NORMAL] = (0, 102, 204)

		self.l3.padding = 0
		self.l3.multiline = True
		self.l3.topleft = (lx, 437)
		self.l3.set_minimum_size(lminsizex,169)
		self.l3.set_maximum_size(lminsizex,169)
		self.l3.create_style ()["font"]["size"] = 16
		self.l3.create_style ()["bgcolor"][STATE_NORMAL] = (194, 208,242)

		self.ld.padding = 0
		self.ld.multiline = True
		self.ld.topleft = (lx, 607)
		self.ld.set_minimum_size(lminsizex,10)
		self.ld.set_maximum_size(lminsizex,10)
		self.ld.create_style ()["font"]["size"] = 16
		self.ld.create_style ()["fgcolor"][STATE_NORMAL] = (255,255,255)
		self.ld.create_style ()["bgcolor"][STATE_NORMAL] = (0, 102, 204)

		self.l4.padding = 0
		self.l4.multiline = True
		self.l4.topleft = (lx, 618)
		self.l4.set_minimum_size(lminsizex,150)
		self.l4.set_maximum_size(lminsizex,150)
		self.l4.create_style ()["font"]["size"] = 16
		self.l4.create_style ()["bgcolor"][STATE_NORMAL] = (255,200,143)

		self.labsq.set_minimum_size(bminsizex,bminsizey)
		self.labsq.topleft = (bx, by-30)

		self.labsoldi.topleft = (bx, by+35)
		self.labsoldi.minsize = (125, 30)
		self.labsoldi.maxsize = (125, 40)

		self.entry.topleft = (bx, by+3)
		self.entry.set_maximum_size = (50, by)
		self.entry.create_style ()["font"]["size"] = 22
		self.entry.minsize= (58, 20)

		finestra.add_widget (self.b)
		finestra.add_widget (self.la)
		finestra.add_widget (self.lb)
		finestra.add_widget (self.lc)
		finestra.add_widget (self.ld)
		finestra.add_widget (self.l1)
		finestra.add_widget (self.l2)
		finestra.add_widget (self.l3)
		finestra.add_widget (self.l4)
		finestra.add_widget (self.labsq)
		finestra.add_widget (self.entry)
		finestra.add_widget (self.labsoldi)

# Definizione dei tipi di pulsanti

buttonSuono = Button ("Attiva Voce")
buttonSuono.topleft = (20,10)
buttonSuono.set_depth(1)
buttonSuono.sensitive = True
buttonSuono.connect_signal (SIG_CLICKED, click, testo)

entry = Entry ("")
entry.topleft = (855,12)
entry.minsize = (85, 22)
entry.set_depth(1)

buttonEst = Button ("#Estrai")
buttonEst.topleft = (805,10)
#buttonEst.connect_signal (SIG_CLICKED, pesca, testo )
buttonEst.connect_signal (SIG_CLICKED, get_entry, entry)
buttonEst.minsize = (45, 20)
buttonEst.set_depth(1)
buttonEst.color = (249,247,57)

buttonRej = Button ("#Scarta")
buttonRej.topleft = (950,10)
buttonRej.connect_signal (SIG_CLICKED, scarta, testo )
buttonRej.set_depth(1)
buttonRej.color = (249,247,57)
buttonRej.sensitive = False

p1 = player ("A.C. IgorMonda", "squadre/IgorMonda/P.txt", "squadre/IgorMonda/D.txt", "squadre/IgorMonda/C.txt", "squadre/IgorMonda/A.txt", 0, 90, 0, 158, "A C IgorMonda")
p2 = player ("A.C. G.B.Simo", "squadre/Simo/P.txt", "squadre/Simo/D.txt", "squadre/Simo/C.txt", "squadre/Simo/A.txt", 635, 90, 635, 158, "A C GIBI Simo")
p3 = player ("A.C. Lollo", "squadre/Lollo/P.txt", "squadre/Lollo/D.txt", "squadre/Lollo/C.txt", "squadre/Lollo/A.txt", 254, 90, 254, 158, "A C Lollo")
p4 = player ("A.C. Luca", "squadre/Luca/P.txt", "squadre/Luca/D.txt", "squadre/Luca/C.txt", "squadre/Luca/A.txt", 127, 90, 127, 158, "A C Luca")
p5 = player ("Lanzi C.S.L.A.C.", "squadre/Lanzi/P.txt", "squadre/Lanzi/D.txt", "squadre/Lanzi/C.txt", "squadre/Lanzi/A.txt", 381, 90, 381, 158, "Lanzi C S L A C")
p6 = player ("Mlak F.C.", "squadre/Mlak/P.txt", "squadre/Mlak/D.txt", "squadre/Mlak/C.txt", "squadre/Mlak/A.txt", 508, 90, 508, 158, "Mlak FC")
p7 = player ("TordoPaolo F.C.", "squadre/Tordo/P.txt", "squadre/Tordo/D.txt", "squadre/Tordo/C.txt", "squadre/Tordo/A.txt", 762, 90, 762, 158, "TordoPaolo FC")
p8 = player ("T.T.&T.", "squadre/TT/P.txt", "squadre/TT/D.txt", "squadre/TT/C.txt", "squadre/TT/A.txt", 889, 90, 889, 158, "TT en T")

finestra.add_widget (buttonSuono)
finestra.add_widget (buttonEst)
finestra.add_widget (entry)
finestra.add_widget (buttonRej)
finestra.add_widget (testo)
finestra.start()

