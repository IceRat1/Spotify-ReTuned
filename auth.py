import os

import functools

from flask import Blueprint, Flask, redirect, request, session, url_for

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

client_id = 'a01610d86da14c5fa1cb04bb24934bc1'
client_secret = '7056959b8e524b42a5d722ea283d4c54'
redirect_uri = 'http://127.0.0.1:5000/auth/callback'
scope = 'playlist-read-private user-read-currently-playing user-read-recently-played user-top-read'

cache_handler = FlaskSessionCacheHandler(session)

sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True)

sp = Spotify(auth_manager=sp_oauth)

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not sp_oauth.validate_token(cache_handler.get_cached_token()):
            auth_url = sp_oauth.get_authorize_url()
            return redirect(auth_url)
        return view(**kwargs)
    return wrapped_view

@bp.route('/login')
def login():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('index'))

@bp.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('index'))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
