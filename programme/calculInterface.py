from numpy import array, loadtxt, genfromtxt, random, sign,exp, where, sqrt, median, mean, float32
from scipy.stats import norm
from time import time,sleep
import csv
from Tkinter import *
import ttk
import os
import re

path=re.sub("python","outil",os.getcwd()+"\\")
###########
#Fonctions utiles#
###########

##ajout(system) -> ajoute au system le processus selectionne avec sa quantite, appele avec le bouton "ajout"
def ajout(sys_num):
	up=all_process[UP_nom[sys_num].get().strip("'")][1]
	quantity=Q[sys_num].get()
	unit=all_process[UP_nom[sys_num].get()][2]
	listes[sys_num].insert(END, up+" : "+quantity+" "+unit)
	UP[sys_num]['values'] =tuple(list(all_process)+["Write keywords to find the corresponding ecoinvent process"])
	UP[sys_num].current(len(all_process))
	system[sys_num].append([list(all_process_names).index(up),up,quantity,unit])
	system[3].append([list(all_process_names).index(up),up,(3-2*sys_num)*float(quantity),unit])

def click(elem):
	if elem.get()=="Write keywords to find the corresponding ecoinvent process":
		elem.set("")

def newliste(elem):
	chaine=elem.get()
	elem["values"]=[item for item in tuple(all_process) if all([chaineitem in item.lower() for chaineitem in chaine.lower().split(" ")])]


##etude_Nestle() -> remplie les listes de processus des system 1 et 2 avec les processus de l'etude de cas(fichiers csv)
def etude_Nestle():
	for sys in [1,2]:
		listes[sys].delete(0,100)
		system[sys]=[]
		for p in range(len(load_system[sys])):
			up=str(load_system[sys][p][0])
			quantity=float(load_system[sys][p][1])
			unit=str(load_system[sys][p][2])

			listes[sys].insert(END, up+" : "+str(quantity)+" "+unit)
			system[sys].append([list(all_process_names).index(up),up,quantity,unit])
			system[3].append([list(all_process_names).index(up),up,(3-2*sys)*float(quantity),unit])

##clean() -> nettoie les listes de processus pour en commencer des nouvelles
def clean():
	for sys in [1,2]:
		listes[sys].delete(0,100)
		system[sys]=[]
	system[3]=[]

##lecture_dommages(precision_correlation) -> lit les fichiers(dommages_light_x%.csv) avec les information d'impact et d'incertitude avec la precision de correlation=cut off de desagregation (100%=correle) **(veleure deterministe | mu | sigma)
def lecture_dommages(precision_correlation):
	t0=time()
	dommage[precision_correlation]=loadtxt(path+'dommages_light'+precision_correlation+'.csv',delimiter=',')
	print "dommages "+precision_correlation.strip("_")+" lue en "+str(time()-t0)+"s"

##lecture_covariances() -> lit les fichiers (vcv_XX.csv) avec les informations de correlation inter-system (ici 0.2 correspond au cut off de correltaion : si la correlation entre 2 processus <0.2, enne n'est pas retenue, il faut trouver un compromis entre la precision et le temps de chargement)
def lecture_covariances():
	t0=time()
	for c in range(len(cat)):
		vcvraw=loadtxt(path+"vcv"+"_"+cat[c]+".csv", str)
		VCV[cat[c]]=[]
		for i in range(len(vcvraw)):
			VCV[cat[c]].append(float32(vcvraw[i].split(",")))
	print "lues en "+str(time()-t0)+"s"

##graph(i) -> permute les graphs 1 et 2
def graph(i):
	cadresGraphs[i].pack()
	boutonGraph[i]["relief"]="sunken"
	cadresGraphs[3-i].pack_forget()
	boutonGraph[3-i]["relief"]="raised"

##errorBar(system, categorie,bord_gauche,epaisseur, haut, sd) -> construit les barres d'erreures (+-sd)
def errorBar(system, categorie,bord_gauche,epaisseur, haut, sd):
	centre=bord_gauche+epaisseur/2

	Graphs[1].coords(Graphs[(system,categorie,11)],centre, haut+sd,centre,haut-sd)
	Graphs[1].coords(Graphs[(system,categorie,12)],centre-3, haut+sd,centre+3,haut+sd)
	Graphs[1].coords(Graphs[(system,categorie,13)],centre-3, haut-sd,centre+3,haut-sd)

##clacul() -> fait le calcul principale du calculateur (bouton calculer)
def calcul():
	deterministe={}
	deterministe[1]=[0.0]*5;
	deterministe[2]=[0.0]*5;
	deterministe[3]=[0.0]*5;
	impacts={}
	impacts[1]=[0.0]*5;
	impacts[2]=[0.0]*5;
	impacts[3]=[0.0]*5;
	var={}
	var[1]=[0.0]*5;
	var[2]=[0.0]*5;
	var[3]=[0.0]*5;
	var_cov={}
	var_cov[1]=[0.0]*5;
	var_cov[2]=[0.0]*5;
	var_cov[3]=[0.0]*5;
	corr=correlation.get()

	for sys_num in [1,2,3]: # sys_num correspond au system
		#print "system "+str(sys_num)
		for c in range(len(cat)): # c correspond ) ma categoris de dommage
			#print "categorie "+cat[c]
			for i in range(len(system[sys_num])): # i parcours les processus du system sys_num
				
				q_i=float(system[sys_num][i][2]); #quantite du processus i
				deterministe_i=dommage[corr][system[sys_num][i][0],1+3*c] #valeur deterministe de l'impact
				signe_i=sign(deterministe_i) #signe (necessaire pour la suite)
				mu_log_i=dommage[corr][system[sys_num][i][0],2+3*c] #parametre mu de la distribution du processu i
				sigma_log_i=dommage[corr][system[sys_num][i][0],3+3*c] #parametre mu de la distribution du processu i
				var_i=(exp(sigma_log_i**2)-1)*exp(2*mu_log_i+sigma_log_i**2)
				
				deterministe[sys_num][c]=deterministe[sys_num][c]+q_i*deterministe_i #on cumule les valeurs deterministes des processus du system
				impacts[sys_num][c]= impacts[sys_num][c]+q_i*signe_i*float(exp(mu_log_i-sigma_log_i**2))#mode = sgn*exp(mu-sigma**2)
				var[sys_num][c]=var[sys_num][c]+q_i*q_i*var_i #variance sans les correlations inter-system (n'apparaissent pas dans l'outil)
				for j in range(len(system[sys_num])):#on complete var2 avec les correlations inter-system
					q_j=float(system[sys_num][j][2]);
					if system[sys_num][j][0]==system[sys_num][i][0]:
						var_cov[sys_num][c]=var_cov[sys_num][c]+q_i*q_j*var_i
						#print str(q_i)+"*"+str(q_j)+"*var("+str(system[sys_num][i][0])+")="+str(var_i/(q_i*q_i))
					else:
						var_cov[sys_num][c]=var_cov[sys_num][c]+q_i*q_j*VCV[cat[c]][max(system[sys_num][i][0],system[sys_num][j][0])-1][min(system[sys_num][i][0],system[sys_num][j][0])]
						#print str(q_i)+"*"+str(q_j)+"*cov("+str(system[sys_num][i][0])+","+str(system[sys_num][j][0])+")="+str(VCV[cat[c]][max(system[sys_num][i][0],system[sys_num][j][0])-1][min(system[sys_num][i][0],system[sys_num][j][0])])
	
	result = csv.writer(open("result.csv", "wb"))
	for sys_num in [1,2]: # sys_num correspond au system
		for c in range(len(cat)): # c correspond ) ma categoris de dommage
			#on insert les valeurs dans les tableaux (les conditions servent a avoir le bon format pour les nombres)
			if abs(deterministe[sys_num][c])<1 or abs(deterministe[sys_num][c])>100:
				valeurTableau[(sys_num,cat[c],"determinist")]['text']="%.2e"%deterministe[sys_num][c] #valeur deterministe
			else:
				valeurTableau[(sys_num,cat[c],"determinist")]['text']=round(deterministe[sys_num][c],3)
			
			if abs(impacts[sys_num][c])<1 or abs(impacts[sys_num][c])>100:
				valeurTableau[(sys_num,cat[c],"mode")]['text']="%.2e"%impacts[sys_num][c] #mode
			else:
				valeurTableau[(sys_num,cat[c],"mode")]['text']=round(impacts[sys_num][c],3)
			
			if abs(sqrt(var_cov[sys_num][c]))<1 or abs(sqrt(var_cov[sys_num][c]))>100:
				valeurTableau[(sys_num,cat[c],"SD")]['text']="%.2e"%sqrt(var_cov[sys_num][c]) #SD
			else:
				valeurTableau[(sys_num,cat[c],"SD")]['text']=round(sqrt(var_cov[sys_num][c]),3)
			
			if abs((sqrt(var_cov[sys_num][c])/impacts[sys_num][c]))<1 or abs((sqrt(var_cov[sys_num][c])/impacts[sys_num][c]))>100:
				valeurTableau[(sys_num,cat[c],"CV")]['text']="%.2e"%(sqrt(var_cov[sys_num][c])/impacts[sys_num][c]) #CV
			else:
				valeurTableau[(sys_num,cat[c],"CV")]['text']=round((sqrt(var_cov[sys_num][c])/impacts[sys_num][c]),3)


			#graph avec les impacts et incertitudes (Graphs[1].coords(rectangle a modifier,x0,y0, x1,y1) -> modifie le rectangle comme suite : (x0,y0) coords du coin HautGauche et (x1,y1) coords du coin BasDroite)
			Graphs[1].coords(Graphs[(sys_num,cat[c],1)],bordGraph +c*3*largeurBarre+(sys_num-1)*largeurBarre,hauteur-100*(impacts[sys_num][c]/max(impacts[1][c],impacts[2][c])),bordGraph+c*3*largeurBarre+sys_num*largeurBarre,hauteur)
			#barre d'erreure errorBar(system, categorie, bord_gauche de la barre, epaisseur de la barre, haut dela barre, sd)
			errorBar(sys_num,cat[c], bordGraph +c*3*largeurBarre+(sys_num-1)*largeurBarre,largeurBarre,hauteur-100*(impacts[sys_num][c]/max(impacts[1][c],impacts[2][c])),100*sqrt(var_cov[sys_num][c])/max(impacts[1][c],impacts[2][c]))
		
			result.writerow([sys_num,cat[c],"det : ",deterministe[sys_num][c],"mode : ",impacts[sys_num][c],"var_cov : ",var_cov[sys_num][c],"var : ",var[sys_num][c], "CV_cov", sqrt(var_cov[sys_num][c])/impacts[sys_num][c], "CV",sqrt(var[sys_num][c])/impacts[sys_num][c]])
			result.writerow([3,cat[c],"det : ",deterministe[3][c],"mode : ",impacts[3][c],"var_cov : ",var_cov[3][c],"var : ",var[3][c], "CV_cov", sqrt(var_cov[3][c])/impacts[3][c], "CV",sqrt(var[3][c])/impacts[3][c]])
			
	
	for c in range(len(cat)):
		#print "categorie : "+cat[c]
		#print "difference : moyenne : "+str(impacts[3][c])+" , var_cov : "+str(var_cov[3][c])+" , var : "+str(var[3][c])
		proba=norm.cdf(0,loc=impacts[3][c],scale=sqrt(var_cov[3][c]))
		#graph de preference suite au Monte Carlo (Graphs[2].coords(rectangle a modifier,x0,y0, x1,y1) -> modifie le rectangle comme suite : (x0,y0) coords du coin HautGauche et (x1,y1) coords du coin BasDroite)
		Graphs[2].coords(Graphs[(1,cat[c],2)],     bordGraph +c*3*largeurBarre,     20     ,bordGraph+c*3*largeurBarre+2*largeurBarre,     220-(1-proba)*200)
		Graphs[2].coords(Graphs[(2,cat[c],2)],     bordGraph +c*3*largeurBarre,     20+proba*200     ,bordGraph+c*3*largeurBarre+2*largeurBarre,     220)

	

###############
#Fin des fonctions utiles#
###############


#################
#Chargement des donnees#
#################

system={}	#system[numero du system]=[[id, name, quantity, unit], ...]
system[1]=[]
system[2]=[]
system[3]=[] #comparison

#preparer des systems de processus : ici c'est l'etude de cas Nestle
load_system={}
with open(path+"system1.csv") as load_sys:
	load_system[1]=[ row for row in csv.reader(load_sys,delimiter=",")]
with open(path+"system2.csv") as load_sys:
	load_system[2]=[ row for row in csv.reader(load_sys,delimiter=",")]

all_process_names=loadtxt(path+"process.csv", dtype=str, delimiter="//")
all_process_units=loadtxt(path+"units.csv", dtype=str, delimiter="//")
all_process={}
VCV={}
dommage={}
cat_unit=[" (kg CO2 eq)"," (DALY)"," (PDF*m2*yr)"," (MJ primary)"," (m3)"]
cat=["CC","HH","EQ","R","WW"]

print "lectures des donnees en cours"
# Thread nous permet de faire des actions en parallele : ici on va lire les dommages et les covariances tout en continuant d'executer le reste du programme (cela nous permet d'utiliser le temps de construction des systems par l'utilisateur)
#affichage des temps de chargements dans la fenetre de commande
lecture_dommages("_1%")
lecture_dommages("_100%")
print "Covariances ",
lecture_covariances()

for p in range(len(all_process_names)): #on ajoute l'unite des processus a la fin de leurs nom dans la liste des processus a selectionner
	all_process[all_process_names[p]+" ("+all_process_units[p]+")"]=[p,all_process_names[p],all_process_units[p]]

#####################
#fin du Chargement des donnees #
#####################

#################
#Construction de interface #
#################

#cree la fenetre principale
fenetre = Tk()

#donne un titre a la fenetre
fenetre.title('Impact calculator with uncertainty')

### cree les 2 cadres principaux
cadreDonnees=Frame(fenetre, borderwidth=5)
cadreResultats=Frame(fenetre, borderwidth=5)
cadreDonnees.pack(side=LEFT)
cadreResultats.pack(side=LEFT)

###Dans le Cadre de gauche###
titreCalculateur=Label(cadreDonnees,text='Built systems to analyze', width=50) #Label : pour afficher du text
etude= Button(cadreDonnees, text ='Import your recipes from "system1.csv" and "system2.csv"', command = etude_Nestle)
titreCalculateur.pack()
etude.pack()

cadreSystem1 = Frame(cadreDonnees, borderwidth=5)
cadreSystem1.pack()
cadreSystem2 = Frame(cadreDonnees, borderwidth=15)
cadreSystem2.pack()


cadreAjout1 = Frame(cadreSystem1, borderwidth=5)
cadreListe1 = Frame(cadreSystem1, borderwidth=5)
cadreAjout1.pack()
cadreListe1.pack()

cadreAjout2 = Frame(cadreSystem2, borderwidth=5)
cadreListe2 = Frame(cadreSystem2, borderwidth=5)
cadreAjout2.pack()
cadreListe2.pack()

cadreCalcul = Frame(cadreDonnees, borderwidth=5)
cadreCalcul.pack()


#zone de choix des processus a ajouter
UP_nom={}
UP_nom[1] = StringVar()
UP_nom[2] = StringVar()

UP_label={}
UP_label[1]=Label(cadreAjout1,text="Process : ", fg="blue")
UP_label[2]=Label(cadreAjout2,text="Process : ",fg="red")
UP_label[1].pack(side=LEFT)
UP_label[2].pack(side=LEFT)


UP={}
UP[1] = ttk.Combobox(cadreAjout1, width=60, textvariable=UP_nom[1])
UP[1]['values'] =tuple(list(all_process)+["Write keywords to find the corresponding ecoinvent process"])
UP[1]['height'] =20
UP[1].current(len(all_process))
UP[1].pack(side=LEFT)
UP[1].bind('<KeyRelease>',lambda evente : newliste(UP[1]))
UP[1].bind('<Button-1>',lambda evente : click(UP[1]))

UP[2] = ttk.Combobox(cadreAjout2, width=60, textvariable=UP_nom[2])
UP[2]['values'] =tuple(list(all_process)+["Write keywords to find the corresponding ecoinvent process"])
UP[2]['height'] =20
UP[2].current(len(all_process))
UP[2].pack(side=LEFT)
UP[2].bind('<KeyRelease>',lambda evente : newliste(UP[2]))
UP[2].bind('<Button-1>',lambda evente : click(UP[2]))


Q_label={}
Q_label[1]=Label(cadreAjout1,text="Quantity : ")
Q_label[2]=Label(cadreAjout2,text="Quantity : ")
Q_label[1].pack(side=LEFT)
Q_label[2].pack(side=LEFT)

Q={}
Q[1]=Entry(cadreAjout1, width=5)
Q[2]=Entry(cadreAjout2, width=5)
Q[1].pack(side=LEFT)
Q[2].pack(side=LEFT)
ajouter={}
ajouter[1] = Button(cadreAjout1, text =' add', command = lambda: ajout(1)) # ici lambda nous permet d'entreer la fonction avec son parametre
ajouter[2] = Button(cadreAjout2, text =' add', command = lambda: ajout(2))
ajouter[1].pack(side=LEFT)
ajouter[2].pack(side=LEFT)

#liste des processus ajoutes
listes={}
listes[1] = Listbox(cadreListe1, width=100)
listes[1].pack()
listes[2] = Listbox(cadreListe2, width=100)
listes[2].pack()

#choix de la correlation intra-system
cadreCor=Frame(cadreCalcul)
cadreCor.pack()

correlation=StringVar()
case = Checkbutton(cadreCor, text="Non correlated database (cutoff 1%)", variable=correlation, onvalue="_1%", offvalue="_100%")
case.deselect()
case.pack();

#Calcul
boutonCalcul = Frame(cadreCalcul, borderwidth=5)
boutonCalcul.pack()
bouton=Button(boutonCalcul, text="Calculate", command=calcul)
clean_listes= Button(boutonCalcul, text ='Reset', command = clean)
bouton.pack(side=LEFT)
clean_listes.pack(side=LEFT)


###Dans le cadre de droite###
titreResultats=Label(cadreResultats,text='Results', width=50)
titreResultats.pack(side=TOP)

cadreGraph = Frame(cadreResultats, borderwidth=5)
cadreTableau={}
cadreTableau[1] = Frame(cadreResultats, borderwidth=5)
cadreTableau[2] = Frame(cadreResultats, borderwidth=5)
cadreGraph.pack()
cadreTableau[1].pack()
cadreTableau[2].pack()

##Zone des graphs
cadreBoutonsGraphs=Frame(cadreGraph, borderwidth=5)
boutonGraph={}
boutonGraph[1] = Button(cadreBoutonsGraphs, text="Graph 1", command=lambda: graph(1))
boutonGraph[2] = Button(cadreBoutonsGraphs, text="Graph 2", command=lambda: graph(2))
cadreBoutonsGraphs.pack()
boutonGraph[1].pack(side=LEFT)
boutonGraph[2].pack(side=LEFT)
cadresGraphs={}
Graphs={}
Graphs_notice={}
legendGraphs={}
color={}
color[1]="blue"
color[2]="red"

#Graph 1 : Impacts avec incertitude
cadresGraphs[1] = Frame(cadreGraph, borderwidth=5)

largeurBarre=16
bordGraph=10
hauteur=220

Graphs[1]=Canvas(cadresGraphs[1], height=hauteur, width=200)
Graphs[1].pack(side=LEFT)
Graphs_notice[1]=Frame(cadresGraphs[1], borderwidth=20)
Label(Graphs_notice[1],text="").pack()
Label(Graphs_notice[1],text="Compared impacts").pack()
Label(Graphs_notice[1],text="System 1 : blue").pack()
Label(Graphs_notice[1],text="System 2 : red").pack()
Label(Graphs_notice[1],text="").pack()
Label(Graphs_notice[1],text="Uncertainty : +- STD").pack()
Graphs_notice[1].pack()

for sys_num in [1,2]:
		for c in range(len(cat)):
			#initialise les rectangles a plats
			Graphs[(sys_num,cat[c],1)]=Graphs[1].create_rectangle(bordGraph +c*3*largeurBarre+(sys_num-1)*largeurBarre,hauteur,bordGraph+c*3*largeurBarre+sys_num*largeurBarre,hauteur, fill=color[sys_num])
			#initialise les barres d'erreur nulles
			Graphs[(sys_num,cat[c],11)]=Graphs[1].create_line(0,0,0,0, width=2)
			Graphs[(sys_num,cat[c],12)]=Graphs[1].create_line(0, 0, 0, 0, width=2)
			Graphs[(sys_num,cat[c],13)]=Graphs[1].create_line( 0,  0, 0, 0, width=2)
	

#Graph 2 : preference suite au Monte Carlo
cadresGraphs[2] = Frame(cadreGraph, borderwidth=5)

Graphs[2]=Canvas(cadresGraphs[2], height=hauteur,  width=200)
Graphs[2].pack(side=LEFT)
Graphs_notice[2]=Frame(cadresGraphs[2], borderwidth=20)
Label(Graphs_notice[2],text="").pack()
Label(Graphs_notice[2],text="Best choice of system").pack()
Label(Graphs_notice[2],text="System 1 : blue").pack()
Label(Graphs_notice[2],text="System 2 : red").pack()
Graphs_notice[2].pack()

for sys_num in [1,2]:
		for c in range(len(cat)):
			#initialise les graphes de preferences a 50% chacuns
			Graphs[(sys_num,cat[c],2)]=Graphs[2].create_rectangle(bordGraph +c*3*largeurBarre,20+(sys_num-1)*100,bordGraph+c*3*largeurBarre+2*largeurBarre,hauteur-(2-sys_num)*100,fill=color[sys_num])
			
for i in [1,2]:
	for c in range(len(cat)):
		Graphs[i].create_text(bordGraph +c*3*largeurBarre+largeurBarre,10, text=cat[c])


#Zone des tableaux : construction et initialisations des tableaux avec des "-" partout

titreTableau=["Determinist","Mode", "SD", "CV"]

for sys in [1,2]:
	for k in range(len(titreTableau)):
		b=Button(cadreTableau[sys], text=titreTableau[k], width=12, state=NORMAL)
		b.grid(row=0,column=k+1,sticky=NSEW)
	for m in range(len(cat)):
		b=Button(cadreTableau[sys], text=cat[m]+cat_unit[m], state=NORMAL)
		b.grid(row=m+1,column=0,sticky=NSEW)

valeurTableau={}
for sys_num in [1,2]:
	for c in range(len(cat)):
		valeurTableau[(sys_num,cat[c],"determinist")]=Label(cadreTableau[sys_num], text="-", justify=CENTER, borderwidth=2) #deterministe
		valeurTableau[(sys_num,cat[c],"determinist")].grid(row=c+1, column=1) 
		valeurTableau[(sys_num,cat[c],"mode")]=Label(cadreTableau[sys_num], text="-", justify=CENTER, borderwidth=2) #mode
		valeurTableau[(sys_num,cat[c],"mode")].grid(row=c+1, column=2) 
		valeurTableau[(sys_num,cat[c],"SD")]=Label(cadreTableau[sys_num], text="-", justify=CENTER, borderwidth=2) #SD
		valeurTableau[(sys_num,cat[c],"SD")].grid(row=c+1, column=3)
		valeurTableau[(sys_num,cat[c],"CV")]=Label(cadreTableau[sys_num], text="-", justify=CENTER, borderwidth=2) #CV
		valeurTableau[(sys_num,cat[c],"CV")].grid(row=c+1, column=4)	

###lance le programme###
fenetre.mainloop()
