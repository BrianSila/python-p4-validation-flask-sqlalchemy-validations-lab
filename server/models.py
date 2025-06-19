from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validates_name(self, key, name):
        if not name or name.strip() == '':
            raise ValueError('Author name is required')
        existing = Author.query.filter(Author.name == name).first()
        if existing and existing.id != self.id:
            raise ValueError('Author name must be unique')
        return name

    @validates('phone_number')
    def validates_phone_no(self, key, phone_number):
        if not phone_number or len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be exactly 10 digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validates_title(self, key, title):
        if not title or title.strip() == '':
            raise ValueError('Post title is required')
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase.lower() in title.lower() for phrase in clickbait_phrases):
            raise ValueError('Title must be clickbait-y!')
        return title

    @validates('content')
    def validates_content(self, key, content):
        if not content or len(content) < 250:
            raise ValueError("Content must be at least 250 characters long")
        return content

    @validates('summary')
    def validates_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError('Summary must be at most 250 characters long')
        return summary

    @validates('category')
    def validates_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
