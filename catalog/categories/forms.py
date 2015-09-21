from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired, Regexp


class CategoryForm(Form):
    """Category form """
    name = StringField('Title:',
                       validators=[DataRequired(),
                                   Regexp(r'^[A-Za-z ]*$',
                                   message="A category name can only contain "
                                           "letters and spaces")])

    def validate(self):
        if not Form.validate(self):
            return False

        return True
