from flask_wtf import Form
from wtforms.fields import StringField, SelectField
from wtforms.validators import DataRequired, Regexp


class ItemForm(Form):
    name = StringField(
        'Title:', validators=[DataRequired(), Regexp(r'^[A-Za-z0-9, ]*$',
         message="A name can only contain letters and numbers")])
    description = StringField('Add an optional description:', validators=[Regexp(r'^[A-Za-z0-9, ]*$',
         message="A description can only contain letters and numbers")])
    # category = SelectField(
    #     'Category:',
    #     choices=[('tennis', 'Tennis'), ('soccer', 'Soccer')])
    
    def validate(self):
        if not Form.validate(self):
            return False

        if not self.description.data:
            self.description.data = self.name.data

        return True