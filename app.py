from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#------------------- creamos la instancia de Flask como app y la base de datos para esta app-----------------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SECRET_KEY']= 'Salas.13' #CONTRASENIA PARA LA DATABASE
db = SQLAlchemy(app)

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

with app.app_context():
    db.create_all()



# ------------------------------------------ rutas -----------------------------------     
@app.route('/')
def index():
    return render_template( 'index.html')

@app.route('/add_product')
def add_product():
    return render_template( 'add_product.html')

@app.route('/render')
def render ():
    with app.app_context():
        product = db.session.query(Product).all()
        print(product)
        print(type(product))

    return render_template ('index.html', product = product)

        
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
    print(form)
    if file and allowed_files(file_name):
        print ("permitido")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],file_name)) # guardar el archivo capturado con lalibreria os

    new_product = Product(producto = product_name, precio = product_price, artesano = vendedor, descripcion = product_desc)
    db.session.add(new_product)
    db.session.commit()

    return redirect(url_for('render'))#redireciona a la ruta render
#-----------------------------------------------------------------------------------------------------------------------------   
    
#------------------------------------ run app ----------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)