# moin-chess
### A Chess notation plugin for MoinMoin
##### Justin Cassidy, April 2015


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


## Installation
Moin-Chess is tested on Python 2.7 on Debian Wheezy and Jessie. It comes 
bundled with `zepto.js` and requires `MoinMoin` and `python-chess`.

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
* If upgrading from 0.1.0, you'll need to regenerate your MoinMoin cache
 * Remove your data/cache/wikiconfig/chess/* files


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
* Better menu notation for drawn games in the game's end-state
* Better board / move highlighting in the menus
* Game tags with a predefined starting position


## Changelog
#### 0.2.0 - Game state notifications
* Added check/checkmate/stalemate detection and reporting
* Fixed game updating on a single page when a move was invalid

#### 0.1.5 - Caching and Bugfixes
* Fixed div closure issues
* Fixed issues where Zepto wouldn't guaranteeably show the chessboards
* Allow edits to a chessboard on a single wiki page
 * Caches the name of the wiki page where a chess game appears

#### 0.1.0 - Initial Release
