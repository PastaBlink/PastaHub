from flask import Blueprint, render_template, redirect, url_for, session
from flask import request
from .models import db, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register')
def register():
    return render_template('register.html')

@main.route('/submit_form', methods=['POST'])
def submit_form():
        
        # Obtener datos del formulario
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Verificar si las contraseñas coinciden
        if password != confirm_password:
            # Manejar el caso de contraseñas no coincidentes, por ejemplo, redirigir a la página de registro con un mensaje de error
            return render_template('register.html', error_message='Las contraseñas no coinciden')

        existing_user = User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first()

        if existing_user:
            # El correo electrónico ya está en uso, manejar el error aquí
            return render_template('register.html', error_message='El usuario/correo ya está en uso')
        # Crear un nuevo usuario
        new_user = User(username=username, email=email, password=password)

        # Agregar el nuevo usuario a la base de datos
        db.session.add(new_user)
        db.session.commit()

        return render_template('login.html')  # Después del registro exitoso, ir a la página de login

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.form.get('username')
        password = request.form.get('password')

        # Buscar al usuario en la base de datos
        user = User.query.filter_by(username=username).first()

        if user and password == user.password:
            # Redirigir al dashboard después del inicio de sesión exitoso
            return redirect(url_for('main.dashboard', username=username))
        else:
            # Manejar el caso de credenciales incorrectas, por ejemplo, redirigir al formulario de inicio de sesión con un mensaje de error
            return render_template('login.html', error_message='El usuario no existe o contraseña incorrecta')

    # Renderizar el formulario de inicio de sesión (GET)
    return render_template('login.html')

# Nueva ruta para el dashboard
@main.route('/dashboard/<username>')
def dashboard(username):
    return render_template('dashboard.html', username=username)

@main.route('/character_info/<character_name>')
def character_info(character_name):
    return render_template('character_info.html', character_name=character_name)

@main.route('/logout')
def logout():
    # Limpiar la sesión (sesión de usuario)
    session.clear()
    # Redirigir al índice después de cerrar sesión
    return redirect(url_for('main.index'))