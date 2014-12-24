# moin-chess
### A Chess notation plugin for MoinMoin
##### Justin Cassidy, December 2014


## About
Moin-Chess is a Wiki parser for MoinMoin that turns a PGN-formatted chess game
into a visual chessboard, with menus for navigation. It's designed to turn a
MoinMoin wiki into a knowledge management system for your chess games.

![example](https://raw.githubusercontent.com/wwoast/moin-chess/master/tests/moin-chess.png)

Moin-Chess is released under the GPLv2 license or (at the user's option) any 
later version, the same as MoinMoin itself.


## Features
* Polished-looking chessboards in pure HTML
 * Uses your browser's native font to display chess pieces
* Menus and page layouts designed for paper-printing


## Usage
To insert a chess board, including a full menu for navigating through a game, 
create a "Chess Game" tag, with a unique "Game ID".

    {{{#!Chess Game Tournament-Round-1
    PGN-or-FEN-moves
    }}}


To insert a board without menus that references an existing game, create a
"Chess Board" tag. As long as the "Game ID" exists in the wiki as a "Chess 
Game" tag, and that game tag has been viewed at least once, it can be
referenced by a "Chess Board" tag. 

    {{{#!Chess Board Tournament-Round-1
    8-White
    }}}


## Current Limitations
To change the moves in a "Chess Game" tag, you currently need to change the
"Game ID" you use. This is protection against a "Game ID" getting redefined
elsewhere in the wiki. New versions of Moin Chess may remove this limitation.


## Installation
Moin-Chess is tested on Python 2.7 on Debian wheezy. It comes bundled with 
`zepto.js` and requires MoinMoin libraries as well as `python-chess`.

* Install python-chess (tested on 0.60 and later)
 * `pip install python-chess` or `apt-get install python-chess`
* Check out the source code from GitHub
* Browse to the source code directory
* Tarball the data and htdocs directories
* Copy the tarball to your wiki's root directory
* Untar the contents
* Validate that the following files are owned by your webserver:
 * `$MOIN/data/plugin/parser/Chess.py`
 * `$MOIN/htdocs/chess/*`
* Restart MoinMoin's WSGI/uwsgi service


## Administration
When a new "Chess Game" tag is parsed, it creates an entry in the MoinMoin
cache, stored under `$MOIN/data/cache/wikiconfig/chess`. As long as this cache
file exists, the contents of the Chess Game tag become "secondary" to the
cached version.

Server admins may delete these files freely, in case there are problems caused 
by cached chess games in the Wiki. When the "Chess Game" tag is reloaded, it
will recreate the game's Wiki cache entry.


## Upcoming Features
* Use standard MoinMoin plugin installer
* Better menu notation for the game's end-state (draw/win/mate)
* Better board / move highlighting in the menus
* Game tags with a predefined starting position
* Fix caching behavior with respect to the first appearance of a Game tag


## Changelog
#### 0.1.0 - Initial Release
