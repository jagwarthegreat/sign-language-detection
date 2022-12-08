from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, DocumentType, Document, AccreditationTask, AccreditationTaskDetail
from . import db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
import json
from sqlalchemy import desc
from werkzeug.utils import secure_filename
import os

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/doc/type', methods=['GET', 'POST'])
@login_required
def document_type():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')

        doctype = DocumentType(doc_type_title=title, doc_type_desc=desc)
        db.session.add(doctype)
        db.session.commit()

        flash('Document Type added!', category='success')
        return redirect(url_for('views.document_type'))

    doctypes = DocumentType.query.all()
    return render_template("doc_types.html", user=current_user, doctypes=doctypes)

@views.route('/docs', methods=['GET', 'POST'])
@login_required
def docs():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No selected file')
            return redirect(url_for('views.docs'))

        doc_type = request.form.get('doc_type')
        doc_name = request.form.get('doc_name')
        desc = request.form.get('desc')
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('views.docs'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filePath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filePath)

            # add to database
            doctype = Document(doc_type_id=doc_type, doc_name=doc_name, doc_desc=desc, doc_file=filePath, user_id=current_user.id)
            db.session.add(doctype)
            db.session.commit()

            return redirect(url_for('views.docs'))

    doc_types = DocumentType.query.all()
    documents = Document.query.all()
    return render_template("documents.html", user=current_user, documents=documents, doc_types=doc_types)

@views.route('/task', methods=['GET', 'POST'])
@login_required
def task():
    if request.method == 'POST':
        task = request.form.get('task')
        remarks = request.form.get('remarks')

        task = AccreditationTask(at_task=task, at_remarks=remarks)
        db.session.add(task)
        db.session.commit()

        flash('Task added!', category='success')
        return redirect(url_for('views.task'))

    tasks = AccreditationTask.query.all()
    return render_template("tasks.html", user=current_user, tasks=tasks)

@views.route('/task/<id>', methods=['GET', 'POST'])
@login_required
def task_details(id):
    if request.method == 'POST':
        task_id = request.form.get('task_id')
        doc = request.form.get('doc')
        desc = request.form.get('desc')
        status = request.form.get('status')

        taskdetail = AccreditationTaskDetail(at_id=task_id, doc_id=doc, atd_desc=desc, user_id=current_user.id, status=status)
        db.session.add(taskdetail)
        db.session.commit()

        flash('Task Detail added!', category='success')
        return redirect(url_for('views.task_details', id=task_id))

    documents = Document.query.all()
    task = AccreditationTask.query.filter_by(at_id=id).first()
    tasks_details = AccreditationTaskDetail.query.filter_by(at_id=id).all()
    return render_template("task_details.html", user=current_user, task=task, tasks_details=tasks_details, documents=documents)

@views.route('/task/destroy', methods=['POST'])
@login_required
def delete_task():
    requestData = json.loads(request.data)
    requestID = requestData['taskId'] 
    task = AccreditationTask.query.get(requestID)
    db.session.delete(task)
    db.session.commit()

    return jsonify({})

@views.route('/task/detail/destroy', methods=['POST'])
@login_required
def delete_task_detail():
    requestData = json.loads(request.data)
    requestID = requestData['taskDetailId'] 
    taskdetail = AccreditationTaskDetail.query.get(requestID)
    db.session.delete(taskdetail)
    db.session.commit()

    return jsonify({})

@views.route('/doc/type/destroy', methods=['POST'])
@login_required
def delete_doc_type():
    requestData = json.loads(request.data)
    requestID = requestData['docTypeId'] 
    asdsign = DocumentType.query.get(requestID)
    db.session.delete(asdsign)
    db.session.commit()

    return jsonify({})

@views.route('/docs/destroy', methods=['POST'])
@login_required
def delete_document():
    requestData = json.loads(request.data)
    requestID = requestData['docId'] 
    docdata = Document.query.get(requestID)
    rmessage = "";
    ctStatus = "";

    if os.path.exists(docdata.doc_file):
        test = os.remove(docdata.doc_file)
        db.session.delete(docdata)
        db.session.commit()
        rmessage = "Deleted";
        ctStatus = "success"
    else:
        rmessage = "not exist";
        ctStatus = "error"

    flash('Document '+rmessage+'!', category=ctStatus)
    return jsonify({ "delete_response": rmessage })

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS