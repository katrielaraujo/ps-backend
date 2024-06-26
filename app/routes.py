from flask import Blueprint, request, jsonify, make_response
from .models import db, Usuario, Aluno, Professor, TipoUsuario, Modalidade, Turma, Pagamento

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET'])
def index():
    return "Marcial Gym API"


@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    nome = data.get('nome')
    contato = data.get('contato')
    data_nascimento = data.get('data_nascimento')
    email = data.get('email')
    senha = data.get('senha')
    tipo_usuario = data.get('tipo_usuario')

    if tipo_usuario not in [TipoUsuario.ALUNO.value, TipoUsuario.PROFESSOR.value]:
        return jsonify({"error": "Invalid user type"}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    if tipo_usuario == TipoUsuario.ALUNO.value:
        usuario = Aluno(nome=nome, contato=contato, data_nascimento=data_nascimento, email=email,
                        tipo_usuario=TipoUsuario.ALUNO)
    else:
        usuario = Professor(nome=nome, contato=contato, data_nascimento=data_nascimento, email=email,
                            tipo_usuario=TipoUsuario.PROFESSOR)

    usuario.set_password(senha)
    db.session.add(usuario)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario is None or not usuario.check_password(senha):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful",
                    "user": {"id": usuario.id, "nome": usuario.nome, "tipo_usuario": usuario.tipo_usuario.value}}), 200


def init_app(app):
    app.register_blueprint(bp)
