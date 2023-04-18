from flask import Flask, request, render_template, redirect, url_for, flash, session #Bruh...
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#------------------- creamos la instancia de Flask como app y la base de datos para esta app-----------------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SECRET_KEY']= 'Salas.13' #CONTRASENIA PARA LA DATABASE
db = SQLAlchemy(app)
app.secret_key = 'cualquieraxd' #Pa probar auxilio

#------------------------------ Crear motor de base de datos para poder extraer los datos----------------------------------

engine = create_engine('sqlite:///database.db')
Session = sessionmaker( bind = engine)
session = Session()

#-------------------- Enviar imagenes subidas a la carpeta upload------------------

app.config['UPLOAD_FOLDER'] = 'static/uploads' #carpeta donde se guardan fisicamente las imagenes subidas
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'gif'])

def allowed_files(file):
    file = file.split('.')
    if file[1] in ALLOWED_EXTENSIONS:
        return True
    else:
        return False
    
#-----------------------------------------------------------------------------------

# --------------------------- Creacion de la tabla product en db--------------------    
class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    producto = db.Column(db.String(20))
    precio = db.Column(db.Integer())
    artesano = db.Column(db.String(50))
    descripcion = db.Column(db.String(100))
    file_name = db.Column(db.String(100))

# --------------------------- Creacion de la tabla Artesano en db--------------------
class Artesano(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    penitenciaria = db.Column(db.String(50))

# --------------------------- Creacion de la tabla Penitenciaria en db--------------------
class Penitenciaria(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    ciudad = db.Column(db.String(50))
    nombre = db.Column(db.String(50))

# --------------------------- Creacion de la tabla de Usuarios en db--------------------
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# --------------------------- Creacion de la tabla Compras en db--------------------
class Compra(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    producto = db.Column(db.String(20))
    precio = db.Column(db.Integer())
    fecha = db.Column(db.DateTime)
    total = db.Column(db.Integer())

# --------------------------- Creacion de la tabla Datos del cliente--------------------
class Datos_cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    ruc = db.Column(db.Integer(), nullable=False)
    ciudad = db.Column(db.String(50), nullable=False)
    barrio = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.Integer(), nullable=False)
    email = db.Column(db.String(50))
    pago = db.Column(db.String(50))

    
with app.app_context():
    db.create_all()

# ------------------------------------------ rutas -----------------------------------     
@app.route('/')
def index():
    return render_template('templates_finales/home.html')

@app.route("/admin_view")
def admin_view():
    with app.app_context():
        artesano = db.session.query(Artesano).all()
        penitenciaria = db.session.query(Penitenciaria).all()
        print(artesano)
        print(penitenciaria)
    return render_template("admin_view.html", artesano = artesano, penitenciaria = penitenciaria)


@app.route('/add_product')
def add_product():
    artesano = db.session.query(Artesano).all()
    return render_template( 'templates_finales/page_load.html', artesano = artesano)

@app.route('/render')
def render ():
    with app.app_context():
        product = db.session.query(Product).all()

    return render_template ('index.html', product = product)

@app.route('/catalogo')
def catalogo():
    return render_template( 'templates_finales/catalogo.html')

@app.route('/render_catalogo')
def render_catalogo ():
    with app.app_context():
        product = db.session.query(Product).all()
        print(product)
        print(type(product))

    return render_template ('templates_finales/catalogo.html', product = product)



@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/pago")
def pago():

    return render_template("pago.html")

#------------------formulario para agregar producto --------------------------------------------------------------------
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    
    form = request.form
    product_name = form['product_name']
    product_price = form['product_price']
    vendedor = form['vendedor']
    product_desc = form['product_desc']
    file = request.files ['upload_file']
    file_name = secure_filename(file.filename)
    
    if file and allowed_files(file_name):
        print ("permitido")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],file_name)) # guardar el archivo capturado con lalibreria os

    new_product = Product(producto = product_name, precio = product_price, artesano = vendedor, descripcion = product_desc, file_name = file_name)
    db.session.add(new_product)
    db.session.commit()

    return redirect(url_for('render_catalogo'))#redireciona a la ruta render


#------------------formulario para agregar Artesano --------------------------------------------------------------------
@app.route('/upload_artesano', methods=['GET', 'POST'])
def upload_artesano():

    form = request.form
    nombre_artesano = form["nombre_artesano"]
    apellido_artesano = form["apellido_artesano"]
    penitenciaria_artesano = form ['penitenciaria_artesano']

    nuevo_artesano = Artesano(nombre = nombre_artesano, apellido = apellido_artesano, penitenciaria = penitenciaria_artesano)
    db.session.add(nuevo_artesano)
    db.session.commit()

    return redirect(url_for("admin_view")) 

#------------------formulario para agregar Penitenciaria --------------------------------------------------------------------
@app.route('/upload_penitenciaria', methods=['GET', 'POST'])
def upload_penitenciaria():

    form = request.form
    ciudad_penitenciaria = form["ciudad_penitenciaria"]
    nombre_penitenciaria = form["nombre_penitenciaria"]

    nueva_penitenciaria = Penitenciaria(ciudad = ciudad_penitenciaria, nombre = nombre_penitenciaria)
    db.session.add(nueva_penitenciaria)
    db.session.commit()

    return redirect(url_for("admin_view")) #Ambos redireccionan a "admin_view"

#------------------formulario para agregar Registro -----
@app.route('/register', methods=['GET', 'POST'])
def new_register():

    form = request.form
    username = form["username"]
    password = form["password"]

    usuario = Usuario.query.filter_by(username=username).first()
    print(form)
    if usuario:
        return render_template("login.html")
    nuevo_usuario = Usuario(username = username, password = password)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return redirect(url_for("login"))

   
#------------------ Login -----------------------
@app.route('/login', methods=['GET', 'POST'])
def new_login():
    username = request.form.get("username")
    password = request.form.get("password")


    username = Usuario.query.filter_by(username = username).first()
    password = Usuario.query.filter_by(password = password).first()
    if username and password:
        return redirect(url_for('admin_view'))
    else:
        flash('Usuario o contraseña incorrectos')
        return redirect(url_for("login"))
    
@app.route('/pago', methods=['GET', 'POST'])
def new_pago():

    form = request.form

    nombre = form["nombre"]
    apellido = form["apellido"]
    ruc = form["ruc"]
    ciudad = form["ciudad"]
    barrio = form["barrio"]
    direccion = form["direccion"]
    telefono = form["telefono"]
    email = form["email"]
    pago = form["pago"]

    new_pago = Datos_cliente(nombre = nombre, apellido = apellido, ruc = ruc, ciudad = ciudad, barrio= barrio, direccion = direccion, telefono = telefono, email = email, pago = pago)
    db.session.add(new_pago)
    db.session.commit()

    return redirect(url_for("pago"))

#-----------------------------------------------------------------------------------------------------------------------------   
    
#------------------------------------ run app ----------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)