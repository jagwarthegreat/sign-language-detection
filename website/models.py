from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__ = 'tbl_user'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(150))
    mname = db.Column(db.String(150))
    lname = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    category = db.Column(db.String(150))
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())

class DocumentType(db.Model):
    __tablename__ = 'tbl_document_types'
    doc_type_id = db.Column(db.Integer, primary_key=True)
    doc_type_title = db.Column(db.String(150))
    doc_type_desc = db.Column(db.Text())
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())

class Document(db.Model):
    __tablename__ = 'tbl_documents'
    doc_id = db.Column(db.Integer, primary_key=True)
    doc_type_id = db.Column(db.Integer, db.ForeignKey('tbl_document_types.doc_type_id', ondelete="SET NULL"))
    doc_name = db.Column(db.String(150), nullable=True)
    doc_desc = db.Column(db.Text(), nullable=True)
    doc_file = db.Column(db.Text(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('tbl_user.id', ondelete="SET NULL"))
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
    doc_type = db.relationship('DocumentType')
    user = db.relationship('User')

class AccreditationTask(db.Model):
    __tablename__ = 'tbl_accreditation_tasks'
    at_id = db.Column(db.Integer, primary_key=True)
    at_task = db.Column(db.Text())
    at_remarks = db.Column(db.Text())
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())

class AccreditationTaskDetail(db.Model):
    __tablename__ = 'tbl_accreditation_task_details'
    atd_id = db.Column(db.Integer, primary_key=True)
    at_id = db.Column(db.Integer, db.ForeignKey('tbl_accreditation_tasks.at_id', ondelete="SET NULL"))
    doc_id = db.Column(db.Integer, db.ForeignKey('tbl_documents.doc_id', ondelete="SET NULL"))
    atd_desc = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('tbl_user.id'))
    status = db.Column(db.String(50), nullable=True)
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
    doc = db.relationship('Document')
    user = db.relationship('User')
    task = db.relationship('AccreditationTask')
