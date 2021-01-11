from flask import Flask,render_template, url_for, request, flash, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os.path import join, dirname, realpath
import os
from sqlalchemy_utils import create_view
from sqlalchemy import select, func

app = Flask(__name__)

#databse configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:androxus1@localhost:5432/postgres'
db=SQLAlchemy(app)
migrate = Migrate(app,db)


# app.secret_key = "123Meti123"


#MODELS
class Klient(db.Model):
    __tablename__ = 'klient'
    embg = db.Column(db.String(13), primary_key=True)
    ime = db.Column(db.String(20), nullable=False)
    prezime = db.Column(db.String(20), nullable=False)
    adresa = db.Column(db.String(30), nullable=False )
    id_grad = db.Column(db.Integer, nullable=False)

    def __init__(self, embg, ime, prezime, adresa, id_grad):
        self.embg = embg
        self.ime = ime
        self.prezime = prezime
        self.adresa = adresa
        self.id_grad = id_grad

    def __repr__(self):
        return "<Klient %s>" % self.ime


class Grad(db.Model):
    __tablename__= 'grad'
    id_grad = db.Column(db.Integer, primary_key=True)
    ime_grad = db.Column(db.String(25))

    def __init__(self,id_grad, ime_grad):
        self.id_grad = id_grad
        self.ime_grad = ime_grad

    def __repr__(self):
        return "<Grad %s>" % self.ime_grad


class Telefon(db.Model):
    __tablename__ = 'telefon'
    embg = db.Column(db.String(13))
    telefonski_broj = db.Column(db.String(15),primary_key=True)

    def __init__(self, embg, telefonski_broj):
        self.embg = embg
        self.telefonski_broj = telefonski_broj

    def __repr__(self):
        return "<Telefon %s>" % self.telefonski_broj


class Rezervacija(db.Model):
    __tablename__ = 'rezervacija'
    id_rezervacija = db.Column(db.Integer, primary_key=True)
    chech_in_date = db.Column(db.DateTime)
    chech_out_date = db.Column(db.DateTime)
    status = db.Column(db.Integer, nullable=False)
    embg = db.Column(db.String(13))
    id_patuvanje = db.Column(db.Integer)
    broj_soba = db.Column(db.Integer, nullable=False)

    def __init__(self, id_rezervacija, chech_in_date, chech_out_date, status, embg, id_patuvanje, broj_soba):
        self.id_rezervacija = id_rezervacija
        self.chech_in_date = chech_in_date
        self.chech_out_date = chech_out_date
        self.status = status
        self.embg = embg
        self.id_patuvanje = id_patuvanje
        self.broj_soba = broj_soba

    def __repr__(self):
        return "<Reservation %s>" % self.id_rezervacija


class Patuvanje(db.Model):
    __tablename__= 'patuvanje'
    id_patuvanje = db.Column(db.Integer, primary_key=True)
    cena = db.Column(db.Integer, nullable=False)
    tip_patuvanje = db.Column(db.String(25))
    patuva_od = db.Column(db.Integer)
    patuva_do = db.Column(db.Integer)
    id_grad = db.Column(db.Integer)

    def __init__(self, id_patuvanje, cena, tip_patuvanje, patuva_od, patuva_do, id_grad):
        self.id_patuvanje = id_patuvanje
        self.cena = cena
        self.tip_patuvanje = tip_patuvanje
        self.patuva_od = patuva_od
        self.patuva_do = patuva_do
        self.id_grad = id_grad

    def __repr__(self):
        return "<Patuvanje %s>" % self.id_patuvanje


class Sobi(db.Model):
    __tablename__ = 'sobi'
    broj_soba = db.Column(db.Integer, primary_key=True)
    cena_soba = db.Column(db.Integer)
    tip_soba = db.Column(db.String(30))
    id_hotel = db.Column(db.Integer)

    def __init__(self, broj_soba, cena_soba, tip_soba, id_hotel):
        self.broj_soba = broj_soba
        self.cena_soba = cena_soba
        self.tip_soba = tip_soba
        self.id_hotel = id_hotel

    def __repr__(self):
        return "<Soba %s>" % self.broj_soba


class Hoteli(db.Model):
    __tablename__ = 'hoteli'
    id_hotel = db.Column(db.Integer, primary_key=True)
    ime_hotel = db.Column(db.String(30), nullable=False)
    tip_hotel = db.Column(db.String(30))
    adresa = db.Column(db.String(25), nullable=False)
    id_grad = db.Column(db.Integer, nullable=False)

    def __init__(self, id_hotel, ime_hotel, tip_hotel, adresa, id_grad):
        self.id_hotel = id_hotel
        self.ime_hotel = ime_hotel
        self.tip_hotel = tip_hotel
        self.adresa = adresa
        self.id_grad = id_grad

    def __repr__(self):
        return "<Hotel %s>" % self.ime_hotel



#VIEWS
class Airplane_Reservations(db.Model):
    __tablename__ = 'airplane_reservations'
    id_rezervacija = db.Column(db.Integer,primary_key=True)
    id_patuvanje = db.Column(db.Integer)
    tip_patuvanje = db.Column(db.String(25))
    patuva_od_grad = db.Column(db.String(25))
    patuva_do_grad = db.Column(db.String(25))
    cena = db.Column(db.Integer)

    def __init__(self,id_rezervacija,id_patuvanje,tip_patuvanje,patuva_od_grad,patuva_do_grad,cena):
        self.id_rezervacija = id_rezervacija
        self.id_patuvanje = id_patuvanje
        self.tip_patuvanje = tip_patuvanje
        self.patuva_od_grad = patuva_od_grad
        self.patuva_do_grad = patuva_do_grad
        self.cena = cena

    def __repr__(self):
        return "<AirplaneReservation %s>" % self.id_rezervacija



class Client_reservation(db.Model):
    __tablename__ = 'clients_reservation'
    ime = db.Column(db.String(20),primary_key=True)
    prezime = db.Column(db.String(20))
    patuva_od_grad = db.Column(db.String(25))
    patuva_do_grad = db.Column(db.String(25))
    chech_in_date = db.Column(db.DateTime)
    chech_out_date = db.Column(db.DateTime)
    cena = db.Column(db.Integer)

    def __init__(self,ime,prezime,patuva_od_grad,patuva_do_grad,chech_in_date,chech_out_date,cena):
        self.ime = ime
        self.prezime = prezime
        self.patuva_od_grad = patuva_od_grad
        self.patuva_do_grad = patuva_do_grad
        self.chech_in_date = chech_in_date
        self.chech_out_date = chech_out_date
        self.cena = cena

    def __repr__(self):
        return "<Client Reservations %s>" % self.ime



#Routes

@app.route('/')
def index():
    # grad = Grad.query.first()
    # return grad.ime_grad + str(grad.id_grad)
    # hotels = Hoteli.query.all()
    return render_template('homepage.html')

@app.route('/reservation', methods=["GET","POST"])
def reservation():
    if request.method == "POST":
        destination = request.form.get('destination')
        checkin = request.form.get('checkin')
        checkout = request.form.get('checkout')
        cena = request.form.get('cena')

        #check type of travelling
        type = request.form.get('type')

        hotel = request.form.get('hotel')


        city_start = request.form.get('city_start')

        soba = request.form.get('soba')

        embg= request.form.get('embg')

        klient = Klient.query.filter_by(embg=embg).first()
        grad_od = Grad.query.filter_by(ime_grad=city_start).first()
        grad_do = Grad.query.filter_by(ime_grad=destination).first()

        hotelObjekt = Hoteli.query.filter_by(ime_hotel=hotel).first()
        sobaObjekt = Sobi.query.filter_by(tip_soba=soba).first()

        tip=None
        if type =='Airplane':
            tip='Avion'
        else:
            tip='Avtobus'

        last_patuvanje = Patuvanje.query.order_by(Patuvanje.id_patuvanje.desc()).first()

        patuvanje = Patuvanje(last_patuvanje.id_patuvanje+1, cena, tip, grad_od.id_grad, grad_do.id_grad, grad_od.id_grad)
        db.session.add(patuvanje)
        db.session.commit()

        last_reservation = Rezervacija.query.order_by(Rezervacija.id_rezervacija.desc()).first()
        rezervacija = Rezervacija(last_reservation.id_rezervacija+1, checkin, checkout, 1, embg, patuvanje.id_patuvanje, sobaObjekt.broj_soba)

        db.session.add(rezervacija)
        db.session.commit()
        return render_template('homepage.html')
        #return "<h1>You have succesffuly made reservation!</h1>"
    else:
        all_cities = Grad.query.all()
        all_hotels = Hoteli.query.all()
    return render_template('reservation.html',cities=all_cities,hotels=all_hotels)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        embg = request.form['embg']
        username = request.form['username']
        surname = request.form['surname']
        address = request.form['address']
        if not_empty([username, surname]):
                user = Klient(embg, username, surname, address, 1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("reservation"))
        else:
            flash("All fields are required!")

    return render_template('register.html')



@app.route("/dashboard")
def dashboard():
    clientreservations = Client_reservation.query.all()
    return render_template('dashboard.html', clientreservations=clientreservations)



@app.route("/history")
def history():
    airplanereservations = Airplane_Reservations.query.all()
    return render_template('history.html', airplanereservations=airplanereservations)


@app.route("/reservation/<int:reservation_id>/delete")
def delete_reservation(reservation_id):
    rezervacija = Rezervacija.query.get_or_404(reservation_id)
    db.session.delete(rezervacija)
    db.session.commit()
    flash("Reservation was deleted successfully")
    return redirect(url_for('reservation'))


def not_empty(form_fields):
    for field in form_fields:
        if len(field) == 0:
            return False
    return True


if __name__ == '__main__':
    app.run(debug=True)