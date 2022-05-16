# from curses.ascii import isblank
from ast import dump
from enum import unique
from flask import Flask, make_response, abort
# importation de flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from flask import jsonify, request, json
from sqlalchemy import ForeignKey

app = Flask(__name__)  # lancement application Flask
motdepasse = quote_plus('moise@12345')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:{}@localhost:5432/apilivre'.format(
    motdepasse)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20), nullable=False)
    libelle_categorie = db.Column(db.String(20), nullable=False)
    livres = db.relationship('Livres', backref='categories', lazy=True)

    def __init__(self, nom, libelle_categorie):
        self.nom = nom
        self.libelle_categorie = libelle_categorie

    def format(self):
        return{
            "id": self.id,
            "nom": self.nom,
            "libelle_categorie": self.libelle_categorie
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Livres(db.Model):
    __tablename__ = 'livres'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), nullable=False)
    titre = db.Column(db.String(30), nullable=False)
    date_publication = db.Column(db.Date(), nullable=False)
    auteur = db.Column(db.String(30), nullable=False)
    editeur = db.Column(db.String(30), nullable=False)
    categorie_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), nullable=False)

    def __init__(self, isbn, titre, date_publication, auteur, editeur, categorie_id):

        self.isbn = isbn
        self.titre = titre
        self.date_publication = date_publication
        self.auteur = auteur
        self.editeur = editeur
        self.categorie_id = categorie_id

    def format(self):
        return{
            "id":self.id,
            "isbn": self.isbn,
            "titre": self.titre,
            "date publication": self.date_publication,
            "auteur": self.auteur,
            "editeur": self.editeur,
            "id categorie": self.categorie_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


db.create_all()

#############################################################
#                                                           #
#                                                           #
#      TEST DE L'API                                        #
#                                                           #
#                                                           #
#############################################################


@app.route('/', methods=['GET'])
def test():
    return jsonify({"message": "bonjour"})


#############################################################
#                                                           #
#                                                           #
#      AFFICHAGE DE TOUS LES LIVRES                         #
#                                                           #
#                                                           #
#############################################################

# affiche tous les livres
@app.route('/livres', methods=['GET'])
def glivres():
    tlivres = Livres.query.order_by(Livres.id).all()
    Livres_format = [livre.format() for livre in tlivres]

    return jsonify({
        'success': True,
        'Livres': Livres_format,
        'nombre de livres': len(tlivres)
    })


#############################################################
#                                                           #
#                                                           #
#      SUPPRESSION D'UN LIVRE                               #
#                                                           #
#                                                           #
#############################################################
# suppression d'un livre
@app.route('/livres/<int:id>', methods=['DELETE'])
def supLivre(id):
    try:
        livre = Livres.query.get(id)
        if livre is None:
            abort(404)
        livre.delete()
        return jsonify({
            'success': True,
            'Livre supprimé': livre.id,
            'Nombre livre': len(Livres.query.all())
        })
    except:
        return abort(422)
    

#############################################################
#                                                           #
#                                                           #
#      MODIFICATION D'UN LIVRE                              #
#                                                           #
#                                                           #
#############################################################

# modifier un livre


@app.route('/livres/<int:id>', methods=['PATCH'])
def modifier_Livre(id):
    try:
        # recuperation de l'info passer en body
        body = request.get_json()
        livre = Livres.query.get(id)
        if livre is None:
            abort(404)
        else:

            livre.isbn = body.get('isbn')
            livre.titre = body.get('titre')
            livre.date_publication = body.get('date_publication')
            livre.auteur = body.get('auteur')
            livre.editeur = body.get('editeur')
            livre.categorie_id = body.get('categorie_id')

            categorie = Categories.query.get(body.get('categorie_id'))
            if categorie is None:
                abort(404)
            livre.update()
            livres = Livres.query.all()
            return ({
                "success": True,
                #"id livre": livres.id,
                "Nombre de livre": len(livres),
                #"Liste de livres": [livree.format() for livree in livres]

            })
    except:
        return abort(400)


#############################################################
#                                                           #
#                                                           #
#      SELECTION D'UN LIVRE                                 #
#                                                           #
#                                                           #
#############################################################

# afficher un Livre par rapport a son id
@app.route('/livres/<int:id>')
def selectionner_Livre(id):
    try:
        livre = Livres.query.get(id)
        if livre is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'livre': livre.format()
            })
    except:
        return jsonify({
                'success': False,
                'msg': 'Not Found'
        })


#############################################################
#                                                           #
#                                                           #
#      ENREGISTREMENT DES LIVRES                            #
#                                                           #
#                                                           #
#############################################################

@app.route('/enrgLivre', methods=['POST'])
def enregistrer_livres():
    try:
        # recuperation des donnees envoye par json dans une variable body
        body = request.get_json()
        new_isbn = body.get('isbn')
        new_titre = body.get('titre')
        new_date = body.get("date_publication")
        new_auteur = body.get('auteur')
        new_editeur = body.get('editeur')
        new_categorie = body.get('categorie_id')

        categoriees = Categories.query.get(new_categorie)
        if categoriees is None:
            abort(404)
        else:

            livre = Livres(isbn=new_isbn, titre=new_titre, auteur=new_auteur, date_publication=new_date,
                        editeur=new_editeur, categorie_id=new_categorie)
            livre.insert()
            return jsonify({
                "success": True,
                "id_livre": livre.id,
                "Nombre_livres": len(Livres.query.all()),
                "Liste_livres": [livres.format() for livres in Livres.query.all()]
            })
    except:
        return abort(400)


#############################################################
#                                                           #
#                                                           #
#      SUPPRESSION D'UNE CATEGORIE                          #
#                                                           #
#                                                           #
#############################################################
@app.route('/supCat/<int:id>', methods=['DELETE'])
def suppCat(id):
    try:
        categ = Categories.query.get(id)
        catego = Categories.query.all()
        if categ is None:
            abort(404)
        categ.delete()
        return ({
            "success": True,
            "deleted": categ.id,
            "Nombre categorie": len(catego),
            # "Liste categorie": [catg.format() for catg in catego]
        })
    except:
        return abort(422)


#############################################################
#                                                           #
#                                                           #
#      MODIFICATION D'UNE CATEGORIE                         #
#                                                           #
#                                                           #
#############################################################
@app.route('/upCat/<int:id>', methods=['PATCH'])
def modifier_Cat(id):
    try:
        body = request.get_json()
        categ = Categories.query.get(id)
        if categ is None:
            abort(404)
        else:
            categ.libelle_categorie = body.get('libelle_categorie', None)
            categ.nom=body.get('nom')
            categ.update()
            return jsonify({
                'success': True,
                'id categorie': categ.id
            })
    except:
        return abort(400)


#############################################################
#                                                           #
#                                                           #
#      ENREGISTREMENT DES CATEGORIES                        #
#                                                           #
#                                                           #
#############################################################
@app.route('/enrgCat', methods=['POST'])
def pCat():
    try:
        body = request.get_json()
        new_nom = body.get('nom')
        new_libelle = body.get('libelle_categorie')

        #   vCat = Categories.query.filter_by(new_nom)
        #   if vCat is not None:
        #          return jsonify({
        #                 "msg":"cette categorie existe deja!"
        #          })
        #   else:
        categorie = Categories(nom=new_nom, libelle_categorie=new_libelle)
        categorie.insert()
        categs = Categories.query.order_by(Categories.id).all()

        return jsonify({
            "msg": "La categorie est enregistre avec success",
            "id categorie": categorie.id,
            "Nombre de categorie": len(Categories.query.all()),
            "Liste Categorie": [categories.format() for categories in categs]

        })
    except:
        return abort(400)

#############################################################
#                                                           #
#                                                           #
#      AFFICHAGE DE TOUTES LES CATEGORIES                   #
#                                                           #
#                                                           #
#############################################################
@app.route('/categorie', methods=['GET'])
def Liste_Cat():
    try:
        ListeCategorie = Categories.query.order_by(Categories.id).all()
        categs = [categoriees.format() for categoriees in ListeCategorie]
        if ListeCategorie is None:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "Liste categories": categs,
                "nombre categories": len(ListeCategorie)
            })
    except:
        return abort(400)


#############################################################
#                                                           #
#                                                           #
#      SELECTION D'UNE CATEGORIE                            #
#                                                           #
#                                                           #
#############################################################
@app.route('/categorie/<int:id>')
def selectionner_categorie(id): 
    try:
        categorie = Categories.query.get(id)
        if categorie is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'Categorie': categorie.format()
            })
    except:
        return abort(404)
        
#############################################################
#                                                           #
#                                                           #
#      GESTION DES ERREURS                                  #
#                                                           #
#                                                           #
#############################################################

@app.errorhandler(404)
def handle_404_error(_error):
    return make_response(jsonify({
        "success":False,
        "error_type":"404",
        "error": "Non retrouvé parmis ceux existant!!"
        }),404)

@app.errorhandler(500)
def handle_500_error(_error):
    return make_response(jsonify({
        "success":False,
        "error_type":"500",
        "error": "Erreur en interne(base ou code) !!"
        }),500)

@app.errorhandler(405)
def handle_405_error(_error):
    return make_response(jsonify({
        "success":False,
        "error_type":"405",
        "error": "Méthode non autorisé!!"
                                  }),405)

@app.errorhandler(401)
def handle_401_error(_error):
    return make_response(jsonify({
        "success":False,
        "error_type":"401",
        "error": "Cette action ne peut être autorisé!!"
        }),401)

@app.errorhandler(400)
def handle_400_error(_error):
    return make_response(jsonify({
        "success":False,
        "error_type":"400",
        "error": "Mauvaise requête!!"
        }),400)
    
@app.errorhandler(422)
def handle_422_error(_error):
    return make_response(jsonify({
        "success":False,
        "error_type":"422",
        "error": "Unprocessable ou Syntaxe requete incorrecte!!"
        }),422)
