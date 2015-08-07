from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import login_required, current_user

from . import categories
from .forms import CategoryForm
from .. import db
from ..models import User, Category

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
    return render_template('categories/category_form.html', form=form, title="Add new category")

# @items.route('/edit/<int:item_id>', methods=['GET', 'POST'])
# @login_required
# def edit(item_id):
#     item = Item.query.get_or_404(item_id)
#     if current_user != item.user:
#         abort(403)
#     form = ItemForm(obj=item)
#     if form.validate_on_submit():
#         form.populate_obj(item)
#         db.session.commit()
#         flash("Stored '{}'".format(item.description))
#         return redirect(url_for('.user', username=current_user.username))
#     return render_template('items/item_form.html', form=form, title="Edit item")

# @items.route('/delete/<int:item_id>', methods=['GET', 'POST'])
# @login_required
# def delete(item_id):
#     item = Item.query.get_or_404(item_id)
#     if current_user != item.user:
#         abort(403)
#     if request.method == "POST":
#         db.session.delete(item)
#         db.session.commit()
#         flash("Deleted '{}'".format(item.description))
#         return redirect(url_for('.user', username=current_user.username))
#     else:
#         flash("Please confirm deleting the item.")
#     return render_template('items/confirm_delete.html', item=item, nolinks=True)


# @items.route('/user/<username>')
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template('items/user.html', user=user)