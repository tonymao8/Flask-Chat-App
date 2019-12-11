from flask import current_app, render_template, url_for, flash, redirect, request

import os
import secrets

from app import database
from . import main
from .forms import AppSettingsForm, MediaFileUploadForm
from .models import Instance, Message

@main.route("/")
def home_page():
    instance = Instance.query.first()
    image_file = url_for('static', filename=f'media/{instance.media_file}')
    messages = Message.query.order_by(Message.id.desc()).all()
    room_name = 'home'
    return render_template('home.html', title=instance.homepage_title, image_file=image_file, views=instance.page_views,
                           is_video = instance.media_is_video, chat_enabled = instance.chat_enabled, room=room_name,
                           messages=messages, color=instance.homepage_hex_color,
                           is_default=instance.media_file_is_default)

@main.route('/super-secret-admin-page', methods=['GET', 'POST'])
def admin_page():
    instance = Instance.query.first()

    app_settings_form = AppSettingsForm(prefix='app_form')
    media_upload_file_form = MediaFileUploadForm(prefix='media_form')

    if app_settings_form.validate_on_submit():
        instance.chat_enabled = app_settings_form.chat_enabled.data
        instance.homepage_title = app_settings_form.homepage_title.data
        instance.homepage_hex_color = app_settings_form.hex_value.data
        database.session.commit()
        flash('General settings updated!', 'info')
        return redirect(url_for('main.admin_page'))

    elif media_upload_file_form.validate_on_submit():
        if media_upload_file_form.media_file.data:

            random_name = secrets.token_hex(8)
            _, file_extension = os.path.splitext(media_upload_file_form.media_file.data.filename)
            new_file_name = random_name + file_extension
            picture_path = os.path.join(current_app.root_path, 'static/media', new_file_name)

            media_upload_file_form.media_file.data.save(picture_path)

            if file_extension == '.webm' or file_extension == '.mp4':
                instance.media_is_video = True
            else:
                instance.media_is_video = False
            if instance.media_file_is_default == False:
                remove_path = os.path.join(os.getcwd(), f'app/static/media/{instance.media_file}')
                os.remove(remove_path)
            instance.media_file_is_default = False

            instance.media_file = new_file_name
            database.session.commit()
        flash('Media file replaced!', 'info')
        return redirect(url_for('main.admin_page'))

    elif request.method == 'GET':
        app_settings_form.homepage_title.data = instance.homepage_title
        app_settings_form.chat_enabled.data = instance.chat_enabled
        app_settings_form.hex_value.data = instance.homepage_hex_color
        media_upload_file_form.media_file.data = instance.media_file

    return render_template('admin.html', app_settings_form=app_settings_form,
                           media_upload_file_form=media_upload_file_form, is_default = instance.media_file_is_default)

@main.route('/super-secret-admin-page/reset-comments', methods=['GET'])
def reset_comments():
    Message.query.delete()
    database.session.commit()
    flash('Comments have been reset!', 'info')
    return redirect(url_for('main.admin_page'))

@main.route('/super-secret-admin-page/reset-views', methods=['GET'])
def reset_views():
    instance = Instance.query.first()
    instance.page_views = 0
    database.session.commit()
    flash('Page views have been reset!', 'info')
    return redirect(url_for('main.admin_page'))

@main.route('/super-secret-admin-page/remove-media-file', methods=['GET'])
def remove_media_file():
    instance = Instance.query.first()
    if instance.media_file_is_default == False:
        remove_path = os.path.join(os.getcwd(), f'app/static/media/{instance.media_file}')
        os.remove(remove_path)
    instance.media_file = 'default.jpg'
    instance.media_file_is_default = True
    instance.media_is_video = False
    database.session.commit()
    flash('Media file has been removed!', 'info')
    return redirect(url_for('main.admin_page'))