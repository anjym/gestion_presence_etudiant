from flask import Flask,render_template,url_for,request,jsonify,Response, redirect, url_for, flash,session
from flask_table import Table, Col
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_session import Session

import geocoder
import os.path
import sqlite3
import folium
import cv2
import numpy as np
import face_recognition
import time
import asyncio
import aiohttp


#Init App
app = Flask(__name__)
app.secret_key = "Secret Key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# A utiliser pour une base Sqlite3
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///appges.sqlite3'
#db=SQLAlchemy(app)
#camera = cv2.VideoCapture(0)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/appgestionetudiant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)

##------------------------------------------------------------------------------------------------------------------------------------------
#Différentes classe du schema de BD

class Registres(db.Model):
    idregistre=db.Column(db.Integer,primary_key=True)
    code_regis=db.Column(db.String(50))
    nom_appr=db.Column(db.String(50))
    prenom_appr=db.Column(db.String(50))
    heure_app=db.Column(db.String(50))
    date_appr=db.Column(db.String(50))
    marque_pc=db.Column(db.String(50))
    heure_sr=db.Column(db.String(50))

    def __init__(self,idregistre,code_regis,nom_appr,prenom_appr,heure_app,date_appr,marque_pc,heure_sr):

        self.idregistre=idregistre
        self.code_regis=code_regis
        self.nom_appr=nom_appr
        self.prenom_appr=prenom_appr
        self.heure_app=heure_app
        self.date_appr=date_appr
        self.marque_pc=marque_pc
        self.heure_sr=heure_sr

class Apprenants(db.Model):
    Matricule_appr=db.Column(db.String(50),primary_key=True)
    nom_appr=db.Column(db.String(50))
    prenom_appr=db.Column(db.String(50))
    pseudo=db.Column(db.String(50))
    password=db.Column(db.String(50))
    id_formation=db.Column(db.Integer)

    def __init__(self,Matricule_appr,nom_appr,prenom_appr,pseudo,password,id_formation):

        self.Matricule_appr=Matricule_appr
        self.nom_appr=nom_appr
        self.prenom_appr=prenom_appr
        self.pseudo=pseudo
        self.password=password
        self.id_formation=id_formation

class Partenaires(db.Model):
    id_partenaire=db.Column(db.Integer,primary_key=True)
    nom_partenaire=db.Column(db.String(50))

    def __init__(self,id_partenaire,nom_partenaire):

        self.id_partenaire=id_partenaire
        self.nom_partenaire=nom_partenaire

class Formations(db.Model):
    id_formation=db.Column(db.Integer,primary_key=True)
    nom_formation=db.Column(db.String(50))
    id_referentiel=db.Column(db.Integer)



    def __init__(self,id_formation,nom_formation,id_referentiel):
        
        self.id_formation=id_formation
        self.nom_formation=nom_formation
        self.id_referentiel=id_referentiel

class Formateurs(db.Model):
    Matricule_for=db.Column(db.String(50),primary_key=True)
    nom_for=db.Column(db.String(50))
    prenom_for=db.Column(db.String(50))
    login=db.Column(db.String(50))
    passwordfrx=db.Column(db.String(50))

    def __init__(self,Matricule_for,nom_for,prenom_for,login,passwordfrx):

        self.Matricule_for=Matricule_for
        self.nom_for=nom_for
        self.prenom_for=prenom_for
        self.login=login
        self.passwordfrx=passwordfrx


class Competences(db.Model):
    id_compt=db.Column(db.Integer,primary_key=True)
    nom_compt=db.Column(db.String(50))
    description=db.Column(db.String(50))

    def __init__(self,id_compt,nom_compt,description):

        self.id_compt=id_compt
        self.nom_compt=nom_compt
        self.description=description

class Bloc_competences(db.Model):
    id_bloc_comp=db.Column(db.Integer,primary_key=True)
    nom_bloc=db.Column(db.String(50))

    def __init__(self,id_bloc_comp,nom_bloc):

        self.id_bloc_comp=id_bloc_comp
        self.nom_bloc=nom_bloc

class Referentiels(db.Model):
    id_referentiel=db.Column(db.Integer,primary_key=True)
    nom_referetiel=db.Column(db.String(50))

    def __init__(self,id_referentiel,nom_referetiel):

        self.id_referentiel=id_referentiel
        self.nom_referetiel=nom_referetiel
##------------------------------------------------------------------------------------------------------------------------------------------

def carte():
	addr_mtnacad_Goog = [5.3509125,-4.0108828]
	myAdress = addr_mtnacad_Goog
	my_map = folium.Map(location=myAdress,zoom_start=19)
	folium.CircleMarker(location=myAdress,radius=50,popup="votre position").add_to(my_map)
	folium.Marker(location=myAdress,tooltip='<b>MTN ACADEMY</b><br><br> Cocody',popup='<h1>Vous&nbsp;êtes&nbsp;connecté!</h1>').add_to(my_map)
	return my_map.__repr__html()
	#my_map.save("templates/my_position.html") sauvegarde en mode page html
	#return (my_map)


def valid_test(result,cam):
    #time.sleep(30)
    if(result==True):
    	cam.release()
    	return render_template('dash_apprenants.html')
        
    else:
    	pass
    



camera = cv2.VideoCapture(0)
def reconf():
		# Get a reference to webcam #0 (the default one)
	#camera = cv2.VideoCapture(0)

	# Load a sample picture and learn how to recognize it.
	michael_image = face_recognition.load_image_file("michael.jpg")
	michael_face_encoding = face_recognition.face_encodings(michael_image)[0]

	# Load a second sample picture and learn how to recognize it.
	# biden_image = face_recognition.load_image_file("Sandy.jpg")
	# biden_face_encoding = face_recognition.face_encodings(Sandy_image)[0]

	# Create arrays of known face encodings and their names
	known_face_encodings = [
	    michael_face_encoding,
	    #Sandy_face_encoding
	]
	known_face_names = [
	    "ASSEMIAN",
	    "Sandy"
	]

	a=True
	count=0

	while a:
	    # Grab a single frame of video
	    ret, frame = camera.read()

	    imgS=cv2.resize(frame,(0,0),None,0.25,0.25)
	    imgS =cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

	    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	   # rgb_frame = frame[:, :, ::-1]

	    # Find all the faces and face enqcodings in the frame of video
	    face_locations = face_recognition.face_locations(imgS)
	    face_encodings = face_recognition.face_encodings(imgS, face_locations)

	    # Loop through each face in this frame of video
	    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
	        # See if the face is a match for the known face(s)
	        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
	        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

	        name = "Unknown"


	        mindis=np.argmin(face_distances)

	        face_distances1=face_distances[mindis]

            # Code de test pour inserer le timer

	        # if matches and (round(face_distances1,1)<0.5):
	        # 	a=False
	        # 	#time.sleep(1)
	        # else:
	        # 	a=True

	        # a=True
	        # count+=1

	        # if (count>20) and (round(face_distances1,1)<0.5):
	        # 	a=False
	        # elif (count>20) and (round(face_distances1,1)>0.5):
	        # 	pass
	        # elif (count<20) and (round(face_distances1,1)<0.5):
	        # 	pass
	        # elif (count<20) and (round(face_distances1,1)>0.5):
	        # 	pass

	        	#print("condition supérieur")
	        print(face_locations)
	        #print(round(face_distances1,1))



	        # If a match was found in known_face_encodings, just use the first one.
	        # if True in matches:
	        #     first_match_index = matches.index(True)
	        #     name = known_face_names[first_match_index]

	        # Or instead, use the known face with the smallest distance to the new face
	        #face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
	        #accur=face_distance_to_conf(face_distances, face_match_threshold=0.6)
	        #print(face_distances)
	        best_match_index = np.argmin(face_distances)
	        best_match_index1 = np.argmin(face_distances)
	        bb=np.argmin(face_distances)
	        #print(bb)
	        if matches[best_match_index]:
	            name = known_face_names[best_match_index]
	            dist=face_distances[bb]#print(matches[best_match_index])
	            # Draw a box around the face
	            left,top,right,bottom=left*4,top*4,right*4,bottom*4
	            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
	            # Draw a label with a name below the face
	            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
	            font = cv2.FONT_HERSHEY_DUPLEX
	            msgk="[{:4.2f}] {}".format(dist, name)
	            cv2.putText(frame, msgk, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
	        #valid_test(matches,camera)

	        # if name==session.name:
	        # 	print("ok")
	        #print(msgk[1:5])

	       # print("ok",dist)
	        
	        # if disto<0.45:
	        # 	break
	    # Display the resulting image
	    #cv2.imshow('Video', frame)

	    ret, buffer = cv2.imencode('.jpg', frame)
	    frame = buffer.tobytes()
	    yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

	    if cv2.waitKey(1) & 0xFF == ord('q'):
	     	break
	    
	# Release handle to the webcam
	#print(time.sleep(30))
	#camera.release()
	#print("1")
	#return render_template('dash_apprenants.html')
	#return 1

		#cv2.destroyAllWindows()

		#Release handle to the webcam
		#camera.release()
		#cv2.destroyAllWindows()

##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # fonction de test pour insertion du timer et recuperer le frame video sur la page html
# def gen_frames():  
#     while True:
#         success, frame = camera.read()  # read the camera frame
#         if not success:
#             break
#         else:
#             detector=cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
#             eye_cascade = cv2.CascadeClassifier('Haarcascades/haarcascade_eye.xml')
#             faces=detector.detectMultiScale(frame,1.1,7)
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#              #Draw the rectangle around each face
#             for (x, y, w, h) in faces:
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
#                 roi_gray = gray[y:y+h, x:x+w]
#                 roi_color = frame[y:y+h, x:x+w]
#                 eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
#                 for (ex, ey, ew, eh) in eyes:
#                     cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# def generate_frames():
#     while True:
            
#         ## read the camera frame
#         success,frame=camera.read()
#         if not success:
#             break
#         else:
#             ret,buffer=cv2.imencode('.jpg',frame)
#             frame=buffer.tobytes()

#         yield(b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#------------------------------------------------------------------------------------------------------------------------------------------
# Route par defaut d'insertion et de MAJ

@app.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
 
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
 
 
        my_data = Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Employee Inserted Successfully")
 
        return redirect(url_for('Index'))
 

#Route de modification Formateur
@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        my_data1 = Formateurs.query.get(request.form.get('matricule'))
        
 
        my_data1.Matricule_for = request.form['matricule']
        my_data1.nom_for = request.form['nom']
        my_data1.prenom_for = request.form['prenom']
        my_data1.login=request.form['login']
        my_data1.password=request.form['password']
 
        db.session.commit()
        flash("Modification éffectuée avec succès")
 
        return redirect(url_for('Index'))

#-------------------------------------------------------------------------------------------------------------------------------------------
#Route d'insertion Formateur
@app.route('/insert_for', methods = ['POST'])
def insert_for():
 
    if request.method == 'POST':
 
        Matricule_for = request.form['matricule']
        nom_for = request.form['nom']
        prenom_for = request.form['Prenom']
        login=request.form['login']
        password=request.form['password']
 
 
        my_dataf = Formateurs(Matricule_for, nom_for, prenom_for,login,password)
        db.session.add(my_dataf)
        db.session.commit()
        print('ok')

        all_data = Formateurs.query.all()
 
        flash("Ajout Terminé !!!")
 
        return render_template('dash_formateurs.html',format=all_data)

#Route de Suppression Formateur
@app.route('/delete_for/<mat>', methods = ['GET', 'POST'])
def delete_for(mat):
    my_data = Formateurs.query.get_or_404(mat)
    db.session.delete(my_data)
    db.session.commit()

    all_data = Formateurs.query.all()
    flash("Formateur Supprimé !!")
 
    return render_template('dash_formateurs.html',format=all_data)
 
 
#Route de Mise a jours Formateurs
@app.route('/update_for', methods = ['GET', 'POST'])
def update_for():
 
    if request.method == 'POST':
        my_data = Formateurs.query.get(request.form.get('matricule'))
        print(my_data)
 
        my_data.Matricule_for = request.form['matricule']
        my_data.nom_for = request.form['nom']
        my_data.prenom_for = request.form['prenom']
        my_data.login=request.form['login']
        my_data.password=request.form['password']
 
        db.session.commit()
        all_data = Formateurs.query.all()

        flash("Modification éffectuée avec succès")
        
 
        return render_template('dash_formateurs.html',format=all_data)
 

#-------------------------------------------------------------------------------------------------------------------------------------------
#Route d'insertion Partenaires
@app.route('/insert_part', methods = ['POST'])
def insert_part():

    if request.method == 'POST':
        id_partenaire = request.form['partid']
        nom_partenaire = request.form['nom_part1']

        # @app.before_first_request
        # def insertpat():
        #     #nom_partena = request.form['nom_part1']
        #     part=Partenaires(nom_partenaire='DSK')
        
 
        datparte = Partenaires(id_partenaire,nom_partenaire)
        db.session.add(datparte)
        db.session.commit()
        print('ok')

        all_data = Partenaires.query.all()
        
 
        flash("Ajout Terminé !!!")
 
        return render_template('partenaires.html',parten=all_data)


#Route de Suppression Partenaires
@app.route('/delete_part/<mat>', methods = ['GET', 'POST'])
def delete_part(mat):
    my_data = Partenaires.query.get_or_404(mat)
    db.session.delete(my_data)
    db.session.commit()

    all_data = Partenaires.query.all()
    flash("Partenaire Supprimé !!")
 
    return render_template('partenaires.html',parten=all_data)
 
 
#Route modification Partenaires
@app.route('/update_part', methods = ['GET', 'POST'])
def update_part():
 
    if request.method == 'POST':
        my_dataPr = Partenaires.query.get(request.form.get('partdd'))
        print(my_dataPr)
 
        my_dataPr.id_partenaire = request.form['partdd']
        my_dataPr.nom_partenaire = request.form['nom_part']
 
        db.session.commit()
        all_data = Partenaires.query.all()

        flash("Modification éffectuée avec succès")
        
 
        return render_template('partenaires.html',parten=all_data)


#-------------------------------------------------------------------------------------------------------------------------------------------

#Route d'insertion Formations
@app.route('/insert_form', methods = ['POST'])
def insert_form():

    if request.method == 'POST':
        id_formation = request.form['formdd']
        nom_formation = request.form['nom_form']
        id_referentiel = request.form['idrefe']

        # @app.before_first_request
        # def insertpat():
        #     #nom_partena = request.form['nom_part1']
        #     part=Partenaires(nom_partenaire='DSK')
        
 
        formins = Formations(id_formation,nom_formation,id_referentiel)
        db.session.add(formins)
        db.session.commit()
        print('ok')

        all_data = Formations.query.all()
        flash("Ajout Terminé !!!")
 
        return render_template('formations.html',forma = all_data)


#Route de Suppression Formations
@app.route('/delete_form/<mat>', methods = ['GET', 'POST'])
def delete_form(mat):
    my_dataform = Formations.query.get_or_404(mat)
    db.session.delete(my_dataform)
    db.session.commit()

    all_data = Formations.query.all()
    flash("Formation Supprimé !!")
 
    return render_template('formations.html',forma = all_data)
 
 
#Route modification Formations
@app.route('/update_form', methods = ['GET', 'POST'])
def update_form():
 
    if request.method == 'POST':
        my_dataFr = Formations.query.get(request.form.get('idfor'))
        print(my_dataFr)
 
        my_dataFr.id_formation = request.form['idfor']
        my_dataFr.nom_formation = request.form['nomfor']
        my_dataFr.id_referentiel = request.form['idref']
 
        db.session.commit()
        all_data = Formations.query.all()

        flash("Modification éffectuée avec succès")
        
 
        return render_template('formations.html',forma = all_data)


#-------------------------------------------------------------------------------------------------------------------------------------------
#Route d'insertion Apprenants
@app.route('/insert_appren', methods = ['POST'])
def insert_appren():

    if request.method == 'POST':
        Matricule_appr = request.form['matappr']
        nom_appr = request.form['nomneappr']
        prenom_appr = request.form['prenomneappr']
        pseudo = request.form['pseudoneappr']
        password = request.form['passwordneappr']
        id_formation = request.form['formatioidne']

        # @app.before_first_request
        # def insertpat():
        #     #nom_partena = request.form['nom_part1']
        #     part=Partenaires(nom_partenaire='DSK')
        
 
        formins = Apprenants(Matricule_appr,nom_appr,prenom_appr,pseudo,password,id_formation)
        db.session.add(formins)
        db.session.commit()
        print('ok')

        all_data = Apprenants.query.all()
        flash("Ajout Terminé !!!")
 
        return render_template('apprenants.html',appren = all_data)


#Route de Suppression Apprenants
@app.route('/delete_appren/<mat>', methods = ['GET', 'POST'])
def delete_appren(mat):
    my_dataform = Apprenants.query.get_or_404(mat)
    db.session.delete(my_dataform)
    db.session.commit()

    all_data = Apprenants.query.all()
    flash("Apprenant Supprimé !!")
 
    return render_template('apprenants.html',appren = all_data)
 
 
#Route modification Apprenants
@app.route('/update_appren', methods = ['GET', 'POST'])
def update_appren():
 
    if request.method == 'POST':
        my_dataAr = Apprenants.query.get(request.form.get('matriculeappr'))
        print(my_dataAr)
 
        my_dataAr.Matricule_appr = request.form['matriculeappr']
        my_dataAr.nom_appr = request.form['nomappr']
        my_dataAr.prenom_appr = request.form['prenomappr']
        my_dataAr.pseudo = request.form['pseudoappr']
        my_dataAr.password = request.form['passwordappr']
        my_dataAr.id_formation = request.form['formation_id']
 
        db.session.commit()
        all_data = Apprenants.query.all()

        flash("Modification éffectuée avec succès")
        
 
        return render_template('apprenants.html',appren = all_data)


#-------------------------------------------------------------------------------------------------------------------------------------------

#Route d'insertion Referentiels
@app.route('/insert_ref', methods = ['POST'])
def insert_ref():

    if request.method == 'POST':
        id_referentiel = request.form['refneid']
        nom_referetiel = request.form['nom_neref']
        
        
 
        formins = Referentiels(id_referentiel,nom_referetiel)
        db.session.add(formins)
        db.session.commit()
        print('ok')

        all_data = Referentiels.query.all()
        flash("Ajout Terminé !!!")
 
        return render_template('referentiel.html',refe = all_data)


#Route de Suppression Referentiels
@app.route('/delete_ref/<mat>', methods = ['GET', 'POST'])
def delete_ref(mat):
    my_dataform = Referentiels.query.get_or_404(mat)
    db.session.delete(my_dataform)
    db.session.commit()

    all_data = Referentiels.query.all()
    flash("Referentiel Supprimé !!")
 
    return render_template('referentiel.html',refe = all_data)
 
 
#Route modification Referentiels
@app.route('/update_ref', methods = ['GET', 'POST'])
def update_ref():
 
    if request.method == 'POST':
        my_dataRf = Referentiels.query.get(request.form.get('idref'))
        print(my_dataRf)
 
        my_dataRf.id_referentiel = request.form['idref']
        my_dataRf.nom_referetiel = request.form['nomref']

 
        db.session.commit()
        all_data = Referentiels.query.all()

        flash("Modification éffectuée avec succès")
        
 
        return render_template('referentiel.html',refe = all_data)


#--------------------------------------------------------------------------------------------------------------------------------------------
# Filitre sur les différents Dashbord

@app.route('/filtre_appre', methods=['GET', 'POST'], defaults={"page": 1})
def filtre_appre(page):
    page = page
    pages = 5
    appren = Apprenants.query.order_by(Apprenants.Matricule_appr.asc()) 
    if request.method == 'POST' and 'tag6' in request.form:
       tag = request.form["tag6"]
       search = "%{}%".format(tag)
       appren = Apprenants.query.filter(Apprenants.Matricule_appr.like(search))
       return render_template('apprenants.html', appren=appren, tag=tag)
    elif request.method=='POST' and 'tag7' in request.form:
        tag = request.form["tag7"]
        search = "%{}%".format(tag)
        appren = Apprenants.query.filter(Apprenants.nom_appr.like(search))
        return render_template('apprenants.html', appren=appren, tag=tag)
    return render_template('apprenants.html', appren=appren)

@app.route('/filtre_registr', methods=['GET', 'POST'], defaults={"page": 1})
def filtre_registr(page):
    page = page
    pages = 5
    #employ = Registres.query.order_by(Registres.code_regis.asc()) 
    if request.method == 'POST' and 'tag2' in request.form:
       tag = request.form["tag2"]
       search = "%{}%".format(tag)
       employ = Registres.query.filter(Registres.code_regis.like(search))
       return render_template('registres.html', employ=employ, tag=tag)
    elif request.method == 'POST' and 'tag3' in request.form:
        tag = request.form["tag3"]
        search = "%{}%".format(tag)
        employ = Registres.query.filter(Registres.date_appr.like(search))
        return render_template('registres.html', employ=employ, tag=tag)
    elif request.method == 'POST' and 'tag4' in request.form:
        tag = request.form["tag4"]
        search = "%{}%".format(tag)
        employ = Registres.query.filter(Registres.nom_appr.like(search))
        return render_template('registres.html', employ=employ, tag=tag)
    return render_template('registres.html', employ=employ)


@app.route('/filtre_registrappr', methods=['GET', 'POST'], defaults={"page": 1})
def filtre_registrappr(page):
    page = page
    pages = 5
    #employ = Registres.query.order_by(Registres.code_regis.asc()) 
    if request.method == 'POST' and 'tag2' in request.form:
       tag = request.form["tag2"]
       search = "%{}%".format(tag)
       employ = Registres.query.filter(Registres.code_regis.like(search))
       return render_template('dash_apprenants.html', employ=employ, tag=tag)
    elif request.method == 'POST' and 'tag3' in request.form:
        tag = request.form["tag3"]
        search = "%{}%".format(tag)
        employ = Registres.query.filter(Registres.date_appr.like(search))
        return render_template('dash_apprenants.html', employ=employ, tag=tag)
    elif request.method == 'POST' and 'tag4' in request.form:
        tag = request.form["tag4"]
        search = "%{}%".format(tag)
        employ = Registres.query.filter(Registres.nom_appr.like(search))
        return render_template('dash_apprenants.html', employ=employ, tag=tag)
    return render_template('dash_apprenants.html', employ=employ)  



#---------------------------------------------------------------------------------------------------------------------------------------------

# Route vers le dasbord formateur et apprenants

@app.route('/partenaires')
def partenaires():
    all_data = Partenaires.query.all()

    inde=[]
    for row in all_data:
        inde.append(row.id_partenaire)
    inde2=max(inde)+1
    print(len(inde)+1)
    return render_template('partenaires.html',parten = all_data,inde2=inde2)

@app.route('/formations')
def formations():
    all_data = Formations.query.all()

    infor=[]
    for row in all_data:
        infor.append(row.id_formation)
    infor2=max(infor)+1
    print(len(infor)+1)
    return render_template('formations.html',forma = all_data,infor2=infor2)

@app.route('/formateurs')
def formateurs():
    all_data = Formateurs.query.all()
    print(all_data)
    return render_template('dash_formateurs.html',format = all_data)

@app.route('/apprenants')
def apprenants(methods=['GET', 'POST']):
    all_data = Apprenants.query.all()
    return render_template('apprenants.html',appren = all_data)


@app.route('/registres')
def registres():
    all_data = Registres.query.all()
    return render_template("registres.html", employ = all_data)

@app.route('/referentiel',methods=['GET', 'POST'])
def referentiel():
    all_data=Referentiels.query.all()
    refinfo=[]
    for row in all_data:
        refinfo.append(row.id_referentiel)
    refinfo2=max(refinfo)+1
    print(len(refinfo)+1)
    return render_template("referentiel.html",refe=all_data,refinfo2=refinfo2)



#---------------------------------------------------------------------------------------------------------------------------------------------
##route vers la page index
@app.route('/')
def index():
	return render_template('index.html ')

#route login formateurs
@app.route('/loginformateurs')
def loginformateurs():
	return render_template('loginformateurs.html')

##Route vers le login apprenants
@app.route('/valid_position')
def valid_position():
	
    #print(len(refinfo)+1)
	#IP_router = '105.235.111.211'
	IP_router ='196.47.134.51'
	g = geocoder.ip("me")
	#print(g.geojson['features'][0]['properties']['ip'])


	try:
		if g.geojson['features'][0]['properties']['ip'] == IP_router:
			return render_template('/loginappren.html')
		else:
			msg = "Vous n'êtes pas a MTN ACADEMY,relancer une fois sur place!!"
			return render_template('index.html',msg=msg)
	except:
		msg4 = "Vous n'êtes pas connecté a internet, Ressayer !!"
		return render_template('index.html',msg4=msg4)

##Route Dashbord Formateurs
@app.route('/dashbord_for',methods=['GET','POST'])
def dashbord_for():
	if request.method == 'POST':
		matricufor = request.form['matricufor']
		loginfor= request.form['loginfr']
		passwordfr = request.form['passwordfr']
		data_form=Formateurs.query.get(request.form.get('matricufor'))
	print(data_form)
	print(matricufor,loginfor,passwordfr)
	passfor=data_form.passwordfrx
	if (passfor==passwordfr):
		all_data = Registres.query.all()
		return render_template("registres.html",employ = all_data)
	else:
		msg6="Login ou mot de pass incorect, Ressayer!!"
		return render_template('loginformateurs.html',msg6=msg6)

#Route dashbord Apprenants

@app.route('/dashbord_appr',methods=['GET','POST'])
def dashbord_appr():
	if request.method == 'POST':
		matricufor = request.form['matricufor']
		loginfor= request.form['loginfr']
		passwordfr = request.form['passwordfr']
		data_form=Formateurs.query.get(request.form.get('matricufor'))
	print(matricufor,loginfor,passwordfr)
	passfor=data_form.passwordfrx
	if (passfor==passwordfr):
		all_data = Registres.query.all()
		return render_template("registres.html",employ = all_data)
	else:
		msg6="Login ou mot de pass incorect, Ressayer!!"
		return render_template('loginformateurs.html',msg6=msg6)

@app.route('/table')
def table():
	return render_template('pages/tables.html')

@app.route('/bill')
def bill():
	return render_template('pages/billing.html')
#Route validation de presence
@app.route('/valid_presence',methods=['GET','POST'])
def valid_presence():

	if request.method == 'POST':
		idregistre=request.form['idapprt']
		coderegis= int(request.form['coderegis'])
		nom = request.form['nom']
		prenom = request.form['prenom']
		heuarrv = request.form['heuarrv']
		datjour = request.form['datjour']
		marquepc = request.form['marquepc']
		heure_sr=''
		#print(coderegis,nom,prenom,heuarrv,datjour,marquepc)


		my_datareg = Registres(idregistre,coderegis, nom, prenom,heuarrv,datjour,marquepc,heure_sr)
		db.session.add(my_datareg)
		db.session.commit() 
			
        #Connection sur la base de données SQilte3
		# conn=sqlite3.connect('appges.sqlite3')
		# cur=conn.cursor()
		# cur.execute("INSERT INTO Registres(code_regis,nom_appr,prenom_appr,heure_app,date_appr,marque_pc) VALUES (?,?,?,?,?,?)",(coderegis,nom,prenom,heuarrv,datjour,marquepc))
		# conn.commit()
		# conn.close()
		#print("ok")
		# addr_mtnacad_Goog = [5.3509125,-4.0108828]
		# myAdress = addr_mtnacad_Goog
		# my_map = folium.Map(location=myAdress,zoom_start=19)
		# folium.CircleMarker(location=myAdress,radius=50,popup="votre position").add_to(my_map)
		# folium.Marker(location=myAdress,tooltip='<b>MTN ACADEMY</b><br><br> Cocody',popup='<h1>Vous&nbsp;êtes&nbsp;connecté!</h1>').add_to(my_map)
		# cart=folium.Marker(location=myAdress,tooltip='<b>MTN ACADEMY</b><br><br> Cocody',popup='<h1>Vous&nbsp;êtes&nbsp;connecté!</h1>').add_to(my_map)
		# my_map.save("templates/my_position.html")
	else:
		msg1="erreur d'enregistrement"
		return render_template('index.html',msg1=msg1)
	return render_template('recon_face.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(reconf(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/macrte')
def macrte():
	return Response(carte(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/loginap1')
def loginap1():
	return render_template('/loginappren.html')

@app.route('/loginappr',methods=['GET','POST'])
def loginappr():

	all_data=Registres.query.all()
	reginfo=[]
	for row in all_data:
		reginfo.append(row.idregistre)
	reginfo2=max(reginfo)+1

	if request.method == 'POST':
		matricu_appr = request.form['matricu_appr']
		login_appr = request.form['login_appr']
		passwordapp = request.form['passwordapp']
		data_appre=Apprenants.query.get(request.form.get('matricu_appr'))
	session["name"] = data_appre.nom_appr
	passw=data_appre.password
	#logw=data_appre.pseudo
	print(data_appre)

    #Connection sur la base de données SQilte3
	# conn=sqlite3.connect('appges.sqlite3')
	# cur=conn.cursor()
	# cur.execute("SELECT * FROM Apprenants WHERE `matricule_appr` = ?",(matricu_appr,))
	# datadb=cur.fetchall()
	# cur.close()

	#dat=np.array(data_appre)
	#print(dat[0])
	#print(dat[0][4])
	if (passwordapp==passw):
		return render_template('/registres_logappr.html',reginfo2=reginfo2)
	else:
		msg2 = "Login ou Mot de passe invalid Ressayer !!"
		return render_template('loginappren.html',msg2=msg2)
@app.route('/video_feed')
def video_feed():
    return Response(reconf(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/recon_face', methods=['GET','POST'])
def recon_face() :
	return render_template('recon_face.html')


#utilisation de la page HTML de position
# @app.route('/map_posi',methods=['GET','POST'])
# def map_posi():
# 	addr_mtnacad_Goog = [5.3509125,-4.0108828]
# 	myAdress = addr_mtnacad_Goog
# 	my_map = folium.Map(location=myAdress,zoom_start=19)
# 	folium.CircleMarker(location=myAdress,radius=50,popup="votre position").add_to(my_map)
# 	folium.Marker(location=myAdress,tooltip='<b>MTN ACADEMY</b><br><br> Cocody',popup='<h1>Vous&nbsp;êtes&nbsp;connecté!</h1>').add_to(my_map)
# 	my_map.save("templates/my_position.html")
# 	return render_template('my_position.html')



## Route vers la page de prédiction Multiple
# @app.route('/predictplus')
# def predictplus():
# 	return render_template('predictmul.html')



@app.route('/dash_apprenants', methods=['GET','POST'] )
def dash_apprenants():
	print("1")
	camera.release()
	all_data = Registres.query.all()
	return render_template('dash_apprenants.html',employ = all_data)

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")
	

if __name__=='main__':
	app.run(debug=True)