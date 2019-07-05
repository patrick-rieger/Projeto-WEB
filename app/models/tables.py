from app import db
from flask_login import UserMixin, current_user, AnonymousUserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.username

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMIN)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

    def __repr__(self):
        return "<User %r>" % self.username


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if not self.has_permission(perm):
            self.permission -= perm

    def reset_permission(self):
        self.permission = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE
            ],
            'Moderator': [
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE,
                Permission.MODERATE
            ],
            'Administrator': [
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE,
                Permission.MODERATE,
                Permission.ADMIN
            ],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


class Noticia(db.Model):
    __tablename__ = 'noticias'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    titulo = db.Column(db.String)
    resumo = db.Column(db.String)
    imagem = db.Column(db.String)

    def __init__(self, **kwargs):
        super(Noticia, self).__init__(**kwargs)



# class Player(db.Model):
#     __tablename__ = 'jogadores'
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String)
#     posicao = db.Column(db.String)
#     height = db.Column(db.Float)
#     weight = db.Column(db.Float)
#     born = db.Column(db.DateTime)
#     team = db.relationship('Play',
#         foreign_keys=[],
#         backref=db.backref('play', lazy='joined'),
#         lazy='dynamic',
#         cascade='all, delete-orphan') 

#     def __init__(self, **kwargs):
#         super(Noticia, self).__init__(**kwargs)


# class Team(db.Model):
#     __tablename__ = 'teams'
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String)
#     creation_date = db.Column(db.DateTime)
#     height = db.Column(db.Float)
#     head_coach = db.Column(db.String)
#     born = db.Column(db.DateTime)
#     assistant_coaches = db.Column(db.)

#     def __init__(self, **kwargs):
#         super(Noticia, self).__init__(**kwargs)


# class Assistant(db.Model):
#     __tablename__ = 'assistants'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)

#     def __repr__(self):
#         return '<Category %r>' % self.name
