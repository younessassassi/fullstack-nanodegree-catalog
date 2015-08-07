from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import login_required, current_user

from . import items
from .forms import ItemForm
from .. import db
from ..models import User, Category, Item

@items.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    form = ItemForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        item = Item(name=name, description=description, user=current_user)
        db.session.add(item)
        db.session.commit()
        flash("stored item '{}'".format(description))
        return redirect(url_for('main.index'))
    return render_template('item_form.html', form=form, title="Add new item")

@items.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user != item.user:
        abort(403)
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash("Stored '{}'".format(item.description))
        return redirect(url_for('.user', username=current_user.username))
    return render_template('item_form.html', form=form, title="Edit item")

@items.route('/delete/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user != item.user:
        abort(403)
    if request.method == "POST":
        db.session.delete(item)
        db.session.commit()
        flash("Deleted '{}'".format(item.description))
        return redirect(url_for('.user', username=current_user.username))
    else:
        flash("Please confirm deleting the item.")
    return render_template('confirm_delete.html', item=item, nolinks=True)


@items.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

# @items.route('/tag/<name>')
# def tag(name):
#     tag = Tag.query.filter_by(name=name).first_or_404()
#     return render_template('tag.html', tag=tag)