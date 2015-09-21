from flask import render_template, url_for, redirect
from flask import flash, request, abort, jsonify
from flask_login import login_required, current_user

from . import items
from .forms import ItemForm
from .. import db
from ..models import User, Category, Item


@items.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    """return template for adding an item """
    form = ItemForm()
    if form.validate_on_submit():
        item_name = form.name.data
        description = form.description.data
        category = form.category.data
        try:
            i = Item.query.filter_by(name=item_name).one()
            flash("item '{}' already exists.".format(item_name))
        except:
            item = Item(name=item_name, description=description,
                        user=current_user, category=category)
            db.session.commit()
            flash("stored item '{}'".format(item_name))
        return redirect(url_for('main.index'))
    return render_template('items/item_form.html',
                           form=form,
                           title="Add new item")


@items.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit(item_id):
    """return template for editing an item """
    item = Item.query.get_or_404(item_id)
    if current_user != item.user:
        abort(403)
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash("Stored '{}'".format(item.name))
        return redirect(url_for('.user', username=current_user.username))
    return render_template('items/item_form.html',
                           form=form,
                           title="Edit item")


@items.route('/delete/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete(item_id):
    """return template for deleting an item """
    item = Item.query.get_or_404(item_id)
    if current_user != item.user:
        abort(403)
    if request.method == "POST":
        db.session.delete(item)
        db.session.commit()
        flash("Deleted '{}'".format(item.name))
        return redirect(url_for('.user', username=current_user.username))
    else:
        flash("Please confirm deleting the item.")
    return render_template('items/confirm_delete.html',
                           item=item,
                           nolinks=True)


@items.route('/user/<username>')
def user(username):
    """return template items created by a specific user """
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('items/user.html', user=user)


@items.route('/category/<int:category_id>')
def category(category_id):
    """return template for an item """
    category = Category.query.filter_by(id=category_id).first_or_404()
    return render_template('items/category.html', category=category)


@items.route('/item/<int:item_id>/json')
def item_json(item_id):
    """return a json object for a specific item """
    item = Item.query.filter_by(id=item_id).first()
    return jsonify(item=item.serialize)


@items.route('/all/json')
def all_json():
    """return a json all items """
    items = Item.all()
    return jsonify(items=[i.serialize for i in items])
