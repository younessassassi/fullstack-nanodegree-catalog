from flask import render_template, url_for, redirect, flash, jsonify, request
from flask_login import login_required, current_user

from . import categories
from .forms import CategoryForm
from .. import db
from ..models import User, Category


@categories.route('/list')
def list():
        return render_template('categories/categories.html')


@categories.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name, user=current_user)
        db.session.add(category)
        db.session.commit()
        flash("stored category '{}'".format(name))
        return redirect(url_for('main.index'))
    return render_template('categories/category_form.html',
                           form=form, title="Add new category")


@categories.route('/delete/<int:category_id>', methods=['POST', 'GET'])
@login_required
def delete(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        db.session.delete(category)
        db.session.commit()
        flash("Deleted '{}'".format(category.name))
        return redirect(url_for('main.index'))
    else:
        flash("Please confirm deleting the category.")
    return render_template('categories/confirm_delete.html',
                           category=category, nolinks=True)


@categories.route('/all/JSON')
def all_json():
    categories = Category.all()
    return jsonify(categories=[i.serialize for i in categories])
