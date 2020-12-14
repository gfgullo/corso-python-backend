from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import QuestionForm, CommentForm
from . import main
from ..models import Question, Comment
from .. import db

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.order_by(Question.timestamp.desc()).paginate(page, per_page=5,
        error_out=False)
    questions = pagination.items
    return render_template('index.html',  questions=questions, pagination=pagination)


@main.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):

    page = request.args.get('page', 1, type=int)
    question = Question.query.get(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          question=question,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.question', id=question.id))

    pagination = question.comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=5,error_out=False)
    #pagination = question.comments.filter(Comment.id != question.correct_answer.id).order_by(Comment.timestamp.desc()).paginate(page, per_page=5,error_out=False)
    comments = pagination.items

    return render_template('question.html', question=question, correct_answer=question.correct_answer, comments=comments, form=form, pagination=pagination)


@main.route('/new_question', methods=['GET', 'POST'])
@login_required
def new_question():

    form = QuestionForm()

    if(form.validate_on_submit()):
        question = Question(title=form.title.data, body=form.body.data, author=current_user._get_current_object())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template('new_question.html', form=form)


@main.route('/delete_question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def delete_question(question_id):

    question = Question.query.filter_by(id=question_id).first_or_404()
    if question.author_id == current_user.id or current_user.is_admin():
        db.session.delete(question)
        db.session.commit()
        flash('The question has been deleted.')
        return redirect(url_for("main.index"))
    else:
        flash("You don't have permission to perform this action")
    return redirect(request.referrer)


@main.route('/delete_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):

    comment = Comment.query.filter_by(id=comment_id).first_or_404()
    if comment.author_id == current_user.id or current_user.is_admin():
        question = comment.question
        if(question.correct_answer != None and question.correct_answer.id == comment.id):
            question.correct_answer = None
            db.session.commit()
        db.session.delete(comment)
        db.session.commit()
        flash('The comment has been deleted.')
    else:
        flash("You don't have permission to perform this action")
    return redirect(request.referrer)


@main.route('/upvote/<int:question_id>/<action>')
@login_required
def upvote(question_id, action):
    question = Question.query.filter_by(id=question_id).first_or_404()
    if action == 'upvote':
        current_user.upvote(question)
        db.session.commit()
    if action == 'downvote':
        current_user.downvote(question)
        db.session.commit()
    return redirect(request.referrer)


@main.route('/correct/<int:question_id>/<int:comment_id>')
@login_required
def correct(question_id, comment_id):
    question = Question.query.filter_by(id=question_id).first_or_404()
    if(current_user.id == question.author_id):
        comment = Comment.query.filter_by(id=comment_id).first_or_404()
        question.correct_answer = comment
        db.session.commit()
    return redirect(request.referrer)