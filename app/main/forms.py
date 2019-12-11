from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, StringField, SubmitField

class AppSettingsForm(FlaskForm):
    chat_enabled = BooleanField('Chat enabled?')
    homepage_title = StringField('Homepage Title')
    hex_value = StringField('6 digit hex code for home background color...')
    submit_1 = SubmitField('Update')

class MediaFileUploadForm(FlaskForm):
    media_file = FileField('Media file to display on home page...', validators=[FileAllowed(['jpg', 'png', 'gif',
                                                                                             'webm', 'mp4'])])
    submit_2 = SubmitField('Submit')