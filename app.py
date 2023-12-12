from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        existing_user_by_username = Usuario.query.filter_by(username=username).first()
        existing_user_by_email = Usuario.query.filter_by(correo=email).first()

        if existing_user_by_username or existing_user_by_email:
            flash('El nombre de usuario o correo electrónico ya está en uso. Prueba con otros.', 'error')
            return redirect(url_for('signup'))

        new_user = Usuario(correo=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()  # Confirmar los cambios en la base de datos

        flash('¡Cuenta creada con éxito! Ahora puedes iniciar sesión.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        flash('Ya hay una sesión iniciada. Por favor, cierra la sesión actual para iniciar una nueva.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Usuario.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = username
            flash('¡Inicio de sesión exitoso!')
            return redirect(url_for('index'))
        else:
            flash('Credenciales inválidas. Intenta de nuevo.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/credencialesinvalidas')
def invalid_credentials():
    return render_template('credencialesinvalidas.html')

def newton_raphson(f, df, x1, epsilon, nmax):
    iteration = 0
    x = x1
    roots = []
    errors = []

    while iteration < nmax:
        x_next = x - f(x) / df(x)
        error = abs(x_next - x)

        roots.append(x_next)
        errors.append(error)

        if error < epsilon:
            return x_next, iteration + 1, errors, roots

        x = x_next
        iteration += 1

    return x, iteration, errors, roots

@app.route('/newtonrhapson', methods=['GET', 'POST'])
def newtonrhapson():
    if request.method == 'POST':
        coeficientes = list(map(float, request.form['coeficientes'].split(',')))
        tolerancia = float(request.form['tolerancia'])
        estimacion_inicial = float(request.form['estimacion_inicial'])
        rango_inferior = float(request.form['rango_inferior'])
        rango_superior = float(request.form['rango_superior'])

        max_iterations = 1000  # Ajusta según sea necesario

        # Define la función f(x) con los coeficientes ingresados por el usuario
        def f(x):
            return sum(coeficientes[i] * x**i for i in range(len(coeficientes)))

        # Define la derivada de f(x)
        def df(x):
            return sum(i * coeficientes[i] * x**(i - 1) for i in range(1, len(coeficientes)))

        # Llamada a la función de Newton-Raphson con los datos proporcionados por el usuario
        raiz, iteraciones, errores, raices = newton_raphson(f, df, estimacion_inicial, tolerancia, max_iterations)

        # Verificar si la raíz está dentro del rango especificado
        if rango_inferior <= raiz <= rango_superior:
            resultado = raiz
        else:
            resultado = "La raíz está fuera del rango especificado."

        return render_template('newtonrhapson.html', resultado=resultado, iteraciones=iteraciones, errores=errores, raices=raices)

    return render_template('newtonrhapson.html')

@app.route('/crout')
def crout():
    return render_template('coming_soon.html')

@app.route('/diffin')
def diffin():
    return render_template('coming_soon.html')

@app.route('/cuadgauss')
def cuadgauss():
    return render_template('coming_soon.html')

if __name__ == '__main__':
    app.run(debug=True)