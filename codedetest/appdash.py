from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
 
 
 
 
app = Flask(__name__)
app.secret_key = "Secret Key"
 
#SqlAlchemy Database Configuration With Mysql
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/appgestionetudiant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
 
 
#Creating model table for our CRUD database
# class Data(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(100))
#     phone = db.Column(db.String(100))
 
 
#     def __init__(self, name, email, phone):
 
#         self.name = name
#         self.email = email
#         self.phone = phone

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
    password=db.Column(db.String(50))

    def __init__(self,Matricule_for,nom_for,prenom_for,login,password):

        self.Matricule_for=Matricule_for
        self.nom_for=nom_for
        self.prenom_for=prenom_for
        self.login=login
        self.password=password

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

 
 
 
 
 
#This is the index route where we are going to
#query on all our employee data
# @app.route('/')
# def Index():
#     all_data = Data.query.all()
 
#     return render_template("index.html", employees = all_data)

@app.route('/')
def Index():
    all_data = Registres.query.all()
 
    return render_template("registres.html", employ = all_data)
 #"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 
 
#this route is for inserting data to mysql database via html forms
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
#--------------------------------------------------------------------------------------------------------------
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
 
##--------------------------------------------------------------------------------------------------------------------
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
##-------------------------------------------------------------------------------------------------------------------

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
##--------------------------------------------------------------------------------------------------------------------
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


##--------------------------------------------------------------------------------------------------------------------

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



##--------------------------------------------------------------------------------------------------------------------
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



if __name__ == "__main__":
    app.run(debug=True)