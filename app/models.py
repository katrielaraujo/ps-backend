from .database import db
from enum import Enum
from .utils import generate_password_hash, check_password_hash


class TipoUsuario(Enum):
    PROFESSOR = 'PROFESSOR'
    ALUNO = 'ALUNO'


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), nullable=False)
    contato = db.Column(db.String(128), nullable=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    tipo_usuario = db.Column(db.Enum(TipoUsuario), nullable=False)
    __mapper_args__ = {'polymorphic_identity': 'usuario', 'polymorphic_on': tipo_usuario}

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)


class Aluno(Usuario):
    __tablename__ = 'aluno'

    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    modalidades_praticadas = db.relationship('Modalidade', secondary='aluno_modalidade', back_populates='alunos')
    historico_pagamento = db.relationship('Pagamento', back_populates='aluno')
    __mapper_args__ = {'polymorphic_identity': 'ALUNO'}


class Professor(Usuario):
    __tablename__ = 'professor'

    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    modalidades_ensinadas = db.relationship('Modalidade', secondary='professor_modalidade', back_populates='professores')
    turmas_lecionadas = db.relationship('Turma', back_populates='professor_responsavel')
    __mapper_args__ = {'polymorphic_identity': 'PROFESSOR'}


class Modalidade(db.Model):
    __tablename__ = 'modalidade'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), nullable=False)
    tipo_graduacao = db.Column(db.String(128), nullable=True)
    nivel_graduacao = db.Column(db.String(128), nullable=True)
    alunos = db.relationship('Aluno', secondary='aluno_modalidade', back_populates='modalidades_praticadas')
    professores = db.relationship('Professor', secondary='professor_modalidade', back_populates='modalidades_ensinadas')


class Turma(db.Model):
    __tablename__ = 'turma'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), nullable=False)
    modalidade = db.Column(db.String(128), nullable=False)
    horarios = db.Column(db.String(128), nullable=False)
    dias_semana = db.Column(db.String(128), nullable=False)
    professor_responsavel_id = db.Column(db.Integer, db.ForeignKey('professor.id'))
    professor_responsavel = db.relationship('Professor', back_populates='turmas_lecionadas')
    alunos_matriculados = db.relationship('Aluno', secondary='turma_aluno', back_populates='turmas')


class Pagamento(db.Model):
    __tablename__ = 'pagamento'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'))
    aluno = db.relationship('Aluno', back_populates='historico_pagamento')
    valor = db.Column(db.Float, nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(128), nullable=False)
    qr_code_pix = db.Column(db.String(128), nullable=True)


aluno_modalidade = db.Table('aluno_modalidade',
                            db.Column('aluno_id',  db.Integer, db.ForeignKey('aluno.id'), primary_key=True),
                            db.Column('modalidade_id', db.Integer, db.ForeignKey('modalidade.id'), primary_key=True))

professor_modalidade = db.Table('professor_modalidade',
                                db.Column('professor_id', db.Integer, db.ForeignKey('professor.id'), primary_key=True),
                                db.Column('modalidade_id', db.Integer, db.ForeignKey('modalidade.id'), primary_key=True))

turma_aluno = db.Table('turma_aluno',
                       db.Column('turma_id', db.Integer, db.ForeignKey('turma.id'), primary_key=True),
                       db.Column('aluno_id', db.Integer, db.ForeignKey('aluno.id'), primary_key=True))
