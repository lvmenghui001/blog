from flask_sqlalchemy import SQLAlchemy
from run import app
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    student_number = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    head_portrait = db.Column(db.String(255))
    realname = db.Column(db.String(255))
    sex = db.Column(db.String(255))
    age = db.Column(db.Integer)
    institute = db.Column(db.String(255))
    identity = db.Column(db.String(255))

    def __init__(self,username):
        self.username = username
    def __repr__(self):
        return "<Users%r>" % self.id


class StudentNumbers(db.Model):
    __tablename__  = 'student_numbers'
    id = db.Column(db.Integer, primary_key=True)
    student_number =  db.Column(db.String(255))
    realname =  db.Column(db.String(255))
    sex  =  db.Column(db.String(255))
    age  =  db.Column(db.Integer)
    identity =  db.Column(db.String(255))
    institude = db.Column(db.String(255))

    def __init__(self):
        pass
    def __repr__(self):
        return "<StudentNumbers%r>" % self.id


class ArticleTypes(db.Model):
    __tablename__ = "article_types"
    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.Integer())

    def __init__(self):
        pass
    def __repr__(self):
        return "<Types%r>" % self.id


class Articles(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    type_id = db.Column(db.Integer(), db.ForeignKey("article_types.id"))
    type = db.relationship(ArticleTypes, backref='articles')
    description = db.Column(db.Text())
    content = db.Column(db.Text())
    picture = db.Column(db.String(255))
    publish_time = db.Column(db.DateTime())
    author_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    author = db.relationship(Users, backref='articles')

    click_num = db.Column(db.Integer())
    praise_num = db.Column(db.Integer())
    public = db.Column(db.String)

    def __init__(self):
        pass
    def __repr__(self):
        return "<Articles%r>" % self.id


class Gbooks(db.Model):
    __tablename__ = "gbooks"
    id = db.Column(db.Integer(), primary_key=True)
    gbook_content = db.Column(db.Text())
    gbook_persion = db.Column(db.String)
    gbook_time = db.Column(db.DateTime())

    def __init__(self):
        pass
    def __repr__(self):
        return "<Gbooks%r>" % self.id


class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer(), primary_key=True)
    article_id = db.Column(db.Integer(), db.ForeignKey("articles.id"))
    article = db.relationship(Articles, backref='comments')
    comment_content = db.Column(db.Text())
    comment_persion_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    comment_persion = db.relationship(Users, backref='comments')
    comment_time = db.Column(db.DateTime())
    parent_id = db.Column(db.Integer(), db.ForeignKey("comments.id"))
    parent = db.relationship("Comments",backref="comments", remote_side=[id])

    def __init__(self):
        pass
    def __repr__(self):
        return "<Comments%r>" % self.id


class ArticlePraise(db.Model):
    __tablename__ = "article_praise"
    id = db.Column(db.Integer(), primary_key=True)
    article = db.Column(db.Integer())
    author = db.Column(db.Integer())

    def __init__(self):
        pass

    def __repr__(self):
        return "<ArticlePraise%r>" % self.id



