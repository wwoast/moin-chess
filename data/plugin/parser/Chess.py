"""
PGN Chess Illustrator for MoinMoin (Chess.py)
Justin Cassidy, November 2014

Installation
------------
Copy this file into data/plugins/parser in your MoinMoin wiki instance.
Restart the wiki if necessary. The name of this file must match the type
of tag in the wiki (Chess.py => {{{#!Chess ... }}}


Usage
-----
To insert a game into a wiki page, use a "Game" tag. Ideally the PGN is as 
simple as possible, all on one line.
{{{#!Chess Game Match-ID 
Raw-PGN 
}}}

By default, this just caches a copy of your game on the Wiki server, and
nothing outputs into the wiki page. To annotate and discuss your game with 
example boards, use a "Board" tag:
{{{#!Chess Board Match-ID 
23-White 
}}}   <-- Show White's 23rd move
{{{#!Chess Board Match-ID 
8-Black 
}}}    <-- Show Black's 8th move

Each time the chessboard is printed, the move being shown appears in a
drop-down widget, with the current move illustrated being shown. The entire
history of the game can be cycled through in each widget, though the move
being illustrated will be shown by default.
"""


from MoinMoin import caching, wikiutil
from MoinMoin.parser import text_moin_wiki
# import chess.pgn

MAX_PLAYS = 1000		# Longest recorded game is 269 moves

class Parser:
    """Insert chess boards into MoinMoin and write about chess games"""
    def __init__(self, raw, request, **kw):
        self.raw = raw           # words on each line inbetween the {{{ and }}}
        self.request = request   # request is the HTTPRequest object
        self.kw = kw             # for example: {{{!# HelloWorld a b c ...
                                 # {'format_args': 'a b c '}	
	self.error = ""          # Error message to print if necessary        
	self.game = ""           # The PGN chess game

	# The board can be constructed empty-form, or from a list of moves.
	# The moves may be in PGN format, readable by chess.pgn
	self.inputs = self.kw['format_args'].split(' ')
	self.mode = self.inputs[0]
	self.name = self.inputs[1]
	# Initiate the Moin cache entry object
        self.cache = caching.CacheEntry(self.request, "chess", self.name, scope='wiki')

	# Game tags:
	# If the name of the game exists, read a cachefile. Otherwise, create a
	# new one, containing the PGN of the game.
	if ( self.mode == "Game" ):
           # In a "Game" tag, other values are PGN moves. Space and new-line
           # delimited moves to give to the PGN engine
	   moves = self.raw.replace('\n', ' ').split(' ')[0:MAX_PLAYS]

	   # TODO: make the cachefiles JSON and read them as resources!	   
	   # Try to read from an existing cachefile
	   # If cache read turns up empty, make a new one with the PGN
	   # At the end, close the file
	   try:
              self.cache.open(mode='r')
              self.game = self.cache.read()
	      # TODO: If the cache already exists, verify moves are the same.
	      # If they are, print an error message and the link to the page
	      # where the game was first defined.
	      self.cache.close()

           except caching.CacheError as e:
	      # Game hasn't been defined yet. Write a PGN to the cache
	      self.error = "Cache error: %s" % e
              self.cache.open(mode='w')
	      self.game = ' '.join(moves)
	      # TODO: Check if the game is valid at (only!) this point!
	      self.cache.write(self.game)

	   except IOError as e:
	      # Can't write files? Bad news!
	      self.error = "I/O error({0}): {1}".format(e.errno, e.strerror)

	   finally:
	      self.cache.close()

	# Board tags:
	# TODO: determine how to draw boards in such a way that a drop-down menu
	# can control the output of the chessboard next to it. Need a performant
	# way to switch between multiple board divs, each of which contain 64
	# individual chess square DIV's. Use dropdowns and visibility: hidden. 
	elif ( self.mode == "Board" ):
	   try:
	      self.cache.open(mode='r')
	      self.game = self.cache.read()

           except caching.CacheError as e:
	      # Game hasn't been defined yet. For board references, print err
	      self.error = "Tag error: No {{{#!Chess Game %s}}} defined." % self.name

	   finally:
	      self.cache.close()

	else:
	   self.error = 'Tag error: Use {{{#!Chess Game}}} or {{{#!Chess Board}}}'	   


    def draw_menu(self):
	"""Given a PGN, create HTML for a menu."""
	pass
	# TODO


    def draw_board(self, current_move=""):
	"""Given self.game and current_move, draw the current chess board."""
	if ( current_move == "" ):
	   current_move = self.position


    def format(self, formatter):
	if ( self.error != "" ):
           self.request.write(formatter.preformatted(1))
           self.request.write(formatter.text(self.error))
           self.request.write(formatter.preformatted(0))
	   print self.error	# For uwsgi logs
	else:
           self.request.write(formatter.preformatted(1))
           self.request.write(formatter.text(self.name + ': ' + self.game))
           self.request.write(formatter.preformatted(0))
