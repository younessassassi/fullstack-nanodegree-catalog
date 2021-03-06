from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Regexp
from ..models import Category


class ItemForm(Form):
    """Item Form """
    name = StringField(
        'Title:',
        validators=[DataRequired(),
                    Regexp(r'^[A-Za-z0-9, ]*$',
                    message="A name can only contain letters and numbers")])
    description = StringField('Add an optional description:',
                              widget=TextArea())
    category = StringField('Category:', validators=[DataRequired()])

    def validate(self):
        if not Form.validate(self):
            return False

        # fill the description field with name if left empty
        if not self.description.data:
            self.description.data = self.name.data

        self.category.data = Category.get_by_category_id(self.category.data)

        return True
