# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['melodine',
 'melodine.models',
 'melodine.models.base',
 'melodine.models.spotify',
 'melodine.models.youtube',
 'melodine.models.ytmusic',
 'melodine.player']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'ffpyplayer>=4.3.5,<5.0.0',
 'python-youtube>=0.8.3,<0.9.0',
 'requests>=2.28.1,<3.0.0',
 'spotipy>=2.21.0,<3.0.0',
 'typing-extensions>=3.7.4',
 'youtube_dl>=2021.12.17,<2022.0.0',
 'ytmusicapi>=0.24.0,<0.25.0']

setup_kwargs = {
    'name': 'melodine',
    'version': '0.2.5',
    'description': 'cohesive models for seamlessly interacting with the Spotify and YouTube Music APIs',
    'long_description': '# melodine\n\nmelo provides consistent data models over Spotify and YouTube Music API objects.\nit\'s main purpose is to model objects from both platforms in a way that requires no distinction based on it\'s source while using them\n\nfor example, a Track object from melo provides the same properties and behaviour irrespective of wether the concerned track is from Spotify or YouTube Music.\n\n# Installation\n\n    pip install melodine\n\n# Usage and Features\n\n## Consistent Data Models\n\nthe term "consistent" here implies that the models work the same way without having to care about it\'s source.\n\nThe Spotify and YouTube Music API provide similar attributes related to objects like a song\'s title, the artists related to the song, the album it\'s from and so on. However their schemas and the way in which objects interrelate wiht each other is totally different. Thus it becomes a pain when integrating both services into a singe application.\n\nmelo tries to solve this problem by internally separating the modelling of objects from both the services with the same structure and exporting them as global melo models, thus resulting in a robust abstraction over both services.\n\nthat means that a YouTube Music track and Spotify track can be handled as the same global melo Track object. This is done by having common attributes between the two separate internal models, like a track\'s name, it\'s artists and the album it\'s from, etc. such gloabl attributes that all melo tracks have (wether from Spotify or YouTube Music) are -\n  \n| attribute           | description                                                                               |\n|---------------------|-------------------------------------------------------------------------------------------|\n| album               | the melo album object for a track                                                         |\n| artists             | the melo artist object for a track                                                        |\n| name                | the name of the track                                                                     |\n| duration            | duration of the track (in seconds)                                                        |\n| href                | link to the track\'s source page                                                           |\n| id                  | the id of the track (the video for the track on ytmusic)                                  |\n| uri                 | a uri of the format `source:type:id` for example - `spotify:track:0hz0bTQC2VVb4CEjLxmKiH` |\n| url                 | the url to the song playback for streaming                                                |\n| images              | a list of `Image` objects (the cover art for the track)                                   |\n| get_recommendations | a getter for track recommendations related to this track                                  |\n\n_Note: there are some extra attributes for a spotify track, but are irrelevant to the core attributes_\n\nthe same applies to other models as well (artist, album, playlists, vidoes, and shows, etc)\n\n## search\n\nmelo allows searching content from both services. Results from specific source or of specific types can be fetched.\n\n### Spotify\n\n```py\nimport melodine as melo\n\nresults = melo.spotify.search(\'Martin Garrix\')\n```\n\n### YT Music\n\n```py\nimport melodine as melo\n\nresults = melo.ytmusic.search(\'Martin Garrix\')\n```\n\nthe `search` function fetches results based on the model used. It returns a `SearchResults` instance. separated the search results based on result types. for example, only tracks results can be accessed as `SearchResults.tracks` which returns an array of Track objects (an empty array if there\'s no tracks in the results).\n\n```py\nresults = melo.spotify.search(\'sewerslvt\') \n\nprint(results.tracks)\n\n# [<melo.Track - \'Cyberia Lyr1\'>, <melo.Track - \'Ecifircas\'>, <melo.Track - \'goodbye\'>]\n```\n\nto fetch specific types of results\n\n```py\nimport melo\n\nresults = melo.spotify.search(\'sewerslvt\', types=[\'track\', \'playlist\'])  \n\nprint(results.playlists)\n\n# [<melo.Playlist - \'This Is Sewerslvt\'>, <melo.Playlist - \'Breakcore Heaven\'>]\n\nprint(results.tracks)   \n\n# [<melo.Track - \'Ecifircas\'>, <melo.Track - \'goodbye\'>, <melo.Track - \'Newlove\'>]\n\nprint(results.albums)\n\n# []\n```\n\nOnly the specified types of results are fetched and the other fields remain empty.\n\n```py\nimport melo\n\nytsearch = melo.ytmusic.search(\'sewerslvt\', source=[\'ytmusic\'], types=[\'album\']) \n\nytsearch.albums  \n\n# [melo.Album - \'Sewer//slvt\', melo.Album - "we had good times together, don\'t forget that"]\n```\n\nOnly YouTube Music albums will be fetched. Any combination of parameters can be used as per convinience.\n\n## Nested Models\n\nmelo models are connected to each other. a track object has an Artist object as it\'s artist parameter, that artist in turn has it\'s own top tracks, albums and those albums have the tracks in them which are fully fledged track objects themselves which means they can lead to other recommended tracks.\n\nas extensive as it gets, an artist could also lead to other similar artists with their own tracks tracks and albums. there\'s a lot of exploring to do out there\n\nit\'s understandable if all thats too mind boggling, here\'s a code example\n\n```py\nimport melo\n\nresults = melo.spotify.search(\'potsu\', source=[\'ytmusic\'], types=[\'artist\'])\n\ntrack_name = results.artists[0].albums[3].get_tracks()[0].name  # \'bird\'\n```\n\nthis crazy chaining implies getting the name of the 1st track from an artist\'s 3rd album where the artist is the 1st search result for a search term.\n\neach step in fetching the desired metric is done lazily which implies melo\'s idea usage for using in TUI application where details need to be loaded only on clicks or other interactions.\n\n## Spotify Authorization\n\nmelo can be used to access data to a user\'s spotify data. the user needs to provide consent to the developer to be able to use their spotify data.\n\nThe purpose for including this functionality is to be able to use melo\'s models with a user\'s spotify library which includes lot of liked tracks, saved albums, artists and curated playlists to extend it to the user\'s content.\n\nto invoke spotify authorization\n\n```py\nimport melo\n\nmelo.spotify.client.authorize()\n```\n\nthis is a one-time action and does not need to be repeated once fulfilled. it is this way in order to emulate usage in a CLI or TUI application where user signin needs to be done just once.\n\nOnce authorized, the `melo.spotify.client` object can be used to make authenticated requests to the Spotify API to get the user\'s liked playlsits, saved albums & artists, a user\'s top & recently played track, and much more.\n\n```py\nfrom melo import spotify.client as client\n\n# assumes the client is already authorized\nrecent_tracks = client.recently_played()\n\n# [<melo.Track - \'Star Shopping\'>, <melo.Track - \'Rum & Her\'>, <melo.Track - \'違う\'>]\n```\n\n# Planned Features\n\n- Implementing YouTube OAuth to retrieve a user\'s YouTube playlists\n- fetching the lyrics / captions for a track\n- transferring spotify playlists to youtube / youtube music and vice versa\n',
    'author': 'addyett',
    'author_email': 'g.aditya2048@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
