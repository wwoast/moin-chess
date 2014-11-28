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


# from MoinMoin import wikiutil
# from MoinMoin.parser import wiki
# from MoinMoin import caching
# import chess.pgn

MAX_MOVES = 300		# Longest recorded game is 269 moves

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
        self.cache = CacheEntry(request, self.name, self.name, scope='item')

	# Game tags:
	# If the name of the game exists, read a cachefile. Otherwise, create a
	# new one, containing the PGN of the game.
	if ( self.mode == "Game" ):
           # In a "Game" tag, other values are PGN moves. Space and new-line
           # delimited moves to give to the PGN engine
	   moves = self.raw.replace('\n', ' ').split(' ')[0:MAX_MOVES]
	   
	   # Try to read from an existing cachefile
	   # If cache read turns up empty, make a new one with the PGN
	   # At the end, close the file
	   try:
              # self.cache.open('r')
              # self.game = cache.read()
	      self.game = ' '.join(moves)
	      # TODO: If the cache already exists, verify moves are the same.
	      # If they are, print an error message and the link to the page
	      # where the game was first defined.

	      # Game hasn't been defined yet. Write a PGN to the cache
	      # if ( len(self.game) == 0 ):
	      #    self.cache.close()
              #    self.cache.open('w')
	      #    self.game = ' '.join(moves)
	      #    self.cache.write(self.game)

	      # TODO: IS THIS A PROPERLY FORMATTED GAME?

	   except IOError as e:
	      # File read silently fails in the caching object, but file write
	      # could screw things up. Print error when this happens
	      self.error = "I/O error({0}): {1}".format(e.errno, e.strerror)

	   finally:
	      self.cache.close()

	# Board tags:
	# TODO: determine how to draw boards in such a way that a drop-down menu
	# can control the output of the chessboard next to it. Need a performant
	# way to switch between multiple board divs, each of which contain 64
	# individual chess square DIV's. Use dropdowns and visibility: hidden. 
	# elif ( self.mode == "Board" ):
	#   try:
	      # self.cache.open('r')
	      # self.game = cache.read()
	      # if ( len(self.game) == 0 ):
	      #    self.error = "Cache error: Game not found: " + self.name

	      # TODO: IS THIS A PROPERLY FORMATTED GAME?

	#   finally:
	 #     pass
	      # self.cache.close()

	else:
	   self.error = 'Tag error: Use {{{#!Chess Game}}} or {{{#!Chess Board}}}'	   

    def format(self, formatter):
	# TODO: Write the exact style and board code
	# from MoinMoin import formatter <<- has the methods we can use here  
        self.request.write(formatter.paragraph(0))
        self.request.write(formatter.text('pgn: ' + self.game))
        self.request.write(formatter.paragraph(1))
        self.request.write(formatter.text('error: ' + self.error))
        self.request.write(formatter.paragraph(2))
        self.request.write(formatter.text('mode: ' + self.mode ))
