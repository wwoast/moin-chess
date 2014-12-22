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
from MoinMoin.config import url_prefix_static
from StringIO import StringIO   # read_game can ocur from a cache file this way
import chess.pgn

STUB_SCRIPT = url_prefix_static + "/chess/head.js"
MODE_LEN = 16
NAME_LEN = 128
RAW_LEN = 32768
MAX_PLAYS = 1000		# Longest recorded game is 269 moves

class Parser:
    """Insert chess boards into MoinMoin and write about chess games"""
    def __init__(self, raw, request, **kw):
        # words on each line inbetween the {{{ and }}}
        self.raw = raw[0:RAW_LEN]
        self.request = request   # request is the HTTPRequest object
        self.kw = kw             # for example: {{{!# HelloWorld a b c ...
                                 # {'format_args': 'a b c '}	
	self.error = ""          # Error message to print if necessary        
	self.game = ""           # The chess.pgn game object
	self.position = ""	 # Starting position to display

	# The board can be constructed empty-form, or from a list of moves.
	# The moves may be in PGN format, readable by chess.pgn
	self.inputs = self.kw['format_args'].split(' ')
	self.mode = self.inputs[0][0:MODE_LEN]
	self.name = self.sanitize_filename(self.inputs[1][0:NAME_LEN])
	# Initiate the Moin cache entry object
	# TODO: INPUT SANITIZATION (self.mode, self.name)
        self.cache = caching.CacheEntry(self.request, "chess", self.name, scope='wiki')

	# Game tags:
	# If the name of the game exists, read a cachefile. Otherwise, create a
	# new one, containing the PGN of the game.
	if ( self.mode == "Game" ):
	   # Try to read from an existing cachefile
	   # If cache read turns up empty, make a new one with the PGN
	   # At the end, close the file
	   try:
              self.cache.open(mode='r')
              vfh = StringIO(self.cache.read())
              self.game = chess.pgn.read_game(vfh)   # Are the moves sensible?

	      # TODO: If the cache already exists, verify moves are the same.
	      # If they are, print an error message and the link to the page
	      # where the game was first defined.
	      self.cache.close()

           except caching.CacheError as e:
	      # Don't print errors when adding a new game
	      # self.error = "Cache error: %s" % e

	      # Game hasn't been defined yet. Write a PGN to the cache
              # In a "Game" tag, other values are PGN moves. Space and new-line
              # delimited moves to give to the PGN engine
   	      moves = self.raw.replace('\n', ' ').split(' ')[0:MAX_PLAYS]
              self.cache.open(mode='w')

              vfh = StringIO(' '.join(moves))
	      self.game = chess.pgn.read_game(vfh)   # Are the moves sensible?
	      exporter = chess.pgn.StringExporter()
	      self.game.export(exporter, headers=False)
              moves = str(exporter)
	      self.cache.write(moves)

	   except ValueError as e:
	      # Error when importing the PGN moves from wiki {{{ }}} or a file
	      self.error = "PGN error in %s: %s" % ( self.name, e)

	   except IOError as e:
	      # Can't write files? Bad news!
	      self.error = "I/O error({0}): {1}".format(e.errno, e.strerror)

	   finally:
	      self.cache.close()

	# Board tags: Just draw a single move from an existing game
	elif ( self.mode == "Board" ):
	   try:
	      self.cache.open(mode='r')
              vfh = StringIO(self.cache.read())
              self.game = chess.pgn.read_game(vfh)   # Are the moves sensible?

	      self.position = self.raw
	      # TODO: Sanitization

           except caching.CacheError as e:
	      # Game hasn't been defined yet. For board references, print err
	      self.error = "Tag error: No {{{#!Chess Game %s}}} defined." % self.name

	   except ValueError as e:
	      # Error importing PGN moves from a file 
	      # (that never should have been written)
	      self.error = "PGN error in %s: %s" % ( self.name, e) 

	   finally:
	      self.cache.close()

	else:
	   self.error = 'Tag error: Use {{{#!Chess Game}}} or {{{#!Chess Board}}}'	   


    def sanitize_filename(self, filename):
	"""Given basic ASCII characters, remove any characters we don't want
	in a cachefile. Basically, permit digits, and a handful of symbols"""
	validChars = "-_.() %s%s" % (string.ascii_letters, string.digits)

	cleaned = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
	return ''.join(c for c in cleaned if c in validChars


    def draw_menu(self, formatter):
	"""Given a PGN, create HTML for a menu. This is a 8-column multi-column
	DIV with individual moves that are clickable to be shown on the board,
	in addition to the next and previous buttons."""
	# Write the game move select menu first. Like all link ids, have a 
	# pipe-delimited head, and an underscore-delimited foot, for js 
	# parsing consistency
	menu = '<div class="movemenu"><a class="moveitem" id="ch_pm|' + self.name + '_" href="#jslink">Previous</a> | <a class="moveitem" id="ch_nm|' + self.name + '_" href="#jslink">Next</a> &nbsp;&nbsp;&nbsp;<p class="focalwhite" id="' + self.name + '_white">&mdash;</p> <p class="focalblack" id="' + self.name + '_black">&mdash;</p>'
	self.request.write(formatter.rawHTML(menu))

	# Take self.game and loop through the different moves. Reconstruct 
	# these moves as links that would fit cleanly within an ordered list. 
	# For every pair of white-move, black-move that we parse, create a new
	# list item with clickable links.
	moves = []
	node = self.game
	while node.variations:
	   next_node = node.variation(0)
	   moves.append(node.board().san(next_node.move))
           node = next_node

	# Based on the list of moves, draw the ordered list
	turn = 1 
	self.request.write(formatter.rawHTML('<div class="movelist"><ol>'))
	for i, move in enumerate(moves):
	   if ( i % 2 == 0 ):
	      self.request.write(formatter.rawHTML('<li>'))
	      board_switch = self.name + "_" + str(turn) + "b"
	      move_link = '<p class="moveitem" id="ch_m|' + board_switch + '">' + move + '</p> &nbsp;'
	      self.request.write(formatter.rawHTML(move_link))
	      if ( i + 1 == len(moves)):   # White move ends game
	         self.request.write(formatter.rawHTML('</li>'))

	   else:
	      board_switch = self.name + "_" + str(turn+1) + "w"
	      move_link = '<p class="moveitem" id="ch_m|' + board_switch + '">' + move + '</p>'
	      turn = turn + 1
	      self.request.write(formatter.rawHTML(move_link))
	      self.request.write(formatter.rawHTML('</li>'))

	self.request.write(formatter.rawHTML('</ol></div>'))


    def draw_board(self, formatter):
	"""Given self.game and self.position, draw a single chess board. This
	   This function parses {{{#!Chess Board }}} tags."""
	[ show_turn, to_move ] = self.position.split('-')
	node = self.game
	board_html = ""
	turn = 0
	i = 0
	while node.variations:
	   next_node = node.variation(0)
	   node = next_node
	   if ( i % 2 == 0 ):   # White to move
	      turn = turn + 1
	      if ( turn == int(show_turn)) and ( to_move == "White" ):
	         board_id = self.name + "_" + str(turn) + "w"
	         board_html = '<div class="chessboard" id="ch_b|' + board_id + '"><pre class="chess_plain">' + "\n" + unicode(node.board()) + "\n" + '</pre></div>'
	         break

	   else:                # Black to move
	      if ( turn == int(show_turn)) and ( to_move == "Black" ):
	         board_id = self.name + "_" + str(turn) + "b"
	         board_html = '<div class="chessboard" id="ch_b|' + board_id + '"><pre class="chess_plain">' + "\n" + unicode(node.board()) + "\n" + '</pre></div>'
	         break

	   i = i+1

	# Last board b/c the variations loop misses it
	if ( turn == int(show_turn)):
	   board_id = self.name + "_" + str(turn) + "w"
	   board_html = '<div class="chessboard" id="ch_b|' + board_id + '"><pre class="chess_plain">' + "\n" + unicode(node.board()) + "\n" + '</pre></div>'

	self.request.write(formatter.rawHTML(board_html))


    def draw_game(self, formatter):
	"""All {{{#!Chess Game }}} tags follow this logic. Draw a game board
	   for every single position available, and insert them into the page.
	   Then, include a menu for switching between the game boards.
           Hide all game divs until they're ready to be shown."""
	boards = []
	node = self.game
        while node.variations:
           next_node = node.variation(0)
           boards.append(unicode(node.board()))
           node = next_node
	# Last board at the end of the variations list
        boards.append(unicode(node.board()))

	# And draw all boards
	turn = 1
	for i, board in enumerate(boards):
	   if ( i % 2 == 0 ):   # A board representing a white move
	      board_id = self.name + "_" + str(turn) + "w"
	   else:   # A board representing black moves
	      board_id = self.name + "_" + str(turn) + "b"
	      turn = turn + 1
	   board_html = '<div class="chessboard" id="ch_b|' + board_id + '"><pre class="chess_plain">' + "\n" + board + "\n" + '</pre></div>'
	   self.request.write(formatter.rawHTML(board_html))


    def format(self, formatter):
	"""Called by MoinMoin to draw content into the wiki page."""
	if ( self.error != "" ):
           self.request.write(formatter.preformatted(1))
           self.request.write(formatter.text(self.error))
           self.request.write(formatter.preformatted(0))
	   print self.error	# For uwsgi logs
	else:
	   # Sadly no better way to include these styles unless
	   # all themes supported moin-chess. :(
	   # TODO: If STUB_SCRIPT doesn't exist, write a new one with 
	   # the correct paths in place to the other files
	   path = '<script type="text/javascript">var moin_chess_root = "'+url_prefix_static+'/chess/"</script>'
	   tag = '<script type="text/javascript" src="' + STUB_SCRIPT + '"></script>'

	   self.request.write(formatter.rawHTML(path))
	   self.request.write(formatter.rawHTML(tag))
	   self.request.write(formatter.rawHTML('<div class="chess-container">'))
	   if ( self.mode == "Board" ):
 	      self.draw_board(formatter)

	   if ( self.mode == "Game" ):
	      # Only full game mode gets the menus
 	      self.draw_game(formatter)
	      self.draw_menu(formatter)

	   self.request.write(formatter.rawHTML('</div>'))
