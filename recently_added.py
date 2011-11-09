from flask import Flask, render_template
import jsonrpclib

from maraschino import app
from settings import *
from noneditable import *
from tools import *

@app.route('/xhr/recently_added')
@requires_auth
def xhr_recently_added():
    return render_recently_added(
        itemtype = 'episodes'
    )

@app.route('/xhr/recently_added/<int:offset>')
@requires_auth
def xhr_recently_added_offset(offset):
    return render_recently_added(
        itemtype = 'episodes',
        offset = offset,
    )

@app.route('/xhr/recently_added_movies')
@requires_auth
def xhr_recently_added_movies():
    return render_recently_added(
        itemtype = 'movies'
    )

@app.route('/xhr/recently_added_movies/<int:offset>')
@requires_auth
def xhr_recently_added_movies_offset(offset):
    return render_recently_added_movies(
        itemtype = 'movies',
        offset = offset,
    )

def render_recently_added(itemtype='episodes', offset=0):
    xbmc = jsonrpclib.Server(server_api_address())
    vfs_url = '%s/vfs/' % (safe_server_address())

    try:
        if itemtype == 'episodes':
            template = 'recently_added.html'
            recently_added = xbmc.VideoLibrary.GetRecentlyAddedEpisodes(properties = ['title', 'season', 'episode', 'showtitle', 'lastplayed', 'thumbnail'])

            try:
                num_recent = int(get_setting('num_recent_episodes').value)

            except:
                num_recent = 5

        elif itemtype == 'movies':
            template = 'recently_added_movies.html'
            recently_added = xbmc.VideoLibrary.GetRecentlyAddedMovies(properties = ['lastplayed', 'thumbnail'])

            try:
                num_recent = int(get_setting('num_recent_movies').value)

            except:
                num_recent = 5

            print recently_added

        else:
            raise Exception

        recently_added = recently_added[itemtype][offset:num_recent + offset]

    except:
        recently_added = []
        vfs_url = None

    return render_template(template,
        recently_added = recently_added,
        vfs_url = vfs_url,
        offset = offset,
    )
