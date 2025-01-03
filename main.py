from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from .auth import login_required, sp

from random import shuffle

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():

    user = sp.current_user()
    current_track = sp.current_user_playing_track()

    recently_played = sp.current_user_recently_played(5)
    playlists = sp.current_user_playlists()

    return render_template('main/home.html', user=user, current_track=current_track, recently_played=recently_played['items'], user_playlists=playlists['items'])

@bp.route('/statistics')
@login_required
def statistics():

    recent_artists = sp.current_user_top_artists(5, 0, 'short_term')
    alltime_artists = sp.current_user_top_artists(5, 0, 'long_term')

    recent_tracks = sp.current_user_top_tracks(5, 0, 'short_term')
    alltime_tracks = sp.current_user_top_tracks(5, 0, 'long_term')

    return render_template('main/stats.html', recent_artists=recent_artists['items'], alltime_artists=alltime_artists['items'], recent_tracks=recent_tracks['items'], alltime_tracks=alltime_tracks['items'])

@bp.route('/recommendations')
@login_required
def recommendations():

    # recommendations
    #most played artist
    #songs from this artist
    # artists similar to this artist
    # featured playlists
    # new albums releases

    recommended = []

    top_artists = sp.current_user_top_artists(4, 0, 'medium_term')
    for artist in top_artists['items']:
        search = sp.search("artist: " + artist['name'], 2, 0, "track")
        recommended += search['tracks']['items']

    top_tracks = sp.current_user_top_tracks(4, 0, 'medium_term')
    for track in top_tracks['items']:
        search = sp.search("album: " + track['album']['name'], 2, 0, "track")
        recommended += search['tracks']['items']

    shuffle(recommended)
    
    new = sp.new_releases(None, 5)

    return render_template('main/recommendations.html', recommended=recommended)

