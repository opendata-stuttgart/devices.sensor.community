from flask import (Flask, Blueprint, render_template, current_app, request, flash, url_for, redirect, session, abort,
                   jsonify, send_from_directory)
frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    return redirect("/login", code=302)


@frontend.route('/imprint')
def imprint():
    return render_template('imprint.html')


@frontend.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')
