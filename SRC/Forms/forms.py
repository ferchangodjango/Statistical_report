from wtforms import StringField,IntegerField,EmailField,PasswordField,FloatField
from wtforms import validators
from wtforms import Form

class Forms(Form):
    USERNAME=StringField('Username',[validators.data_required(),validators.length(min=5,max=20)])
    PASSWORD=PasswordField('Password',[validators.data_required()])
    ID=IntegerField('ID',[validators.data_required(),validators.number_range(min=1,max=10)])
    SAMPLE_RIVERUP=FloatField('SAMPLE_RIVERUP',[validators.data_required()])
    SAMPLE_RIVERDOWN=FloatField('SAMPLE_RIVERUP',[validators.data_required()])
    FORCE_APPLY=FloatField('FORCE_APPLY',[validators.data_required()])
    QUANTITY_AMONIAC=FloatField('QUANTITY_AMONIAC',[validators.data_required()])

