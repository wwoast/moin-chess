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
{{{#!Chess Game Match-ID Raw-PGN }}}

By default, this just caches a copy of your game on the Wiki server, and
nothing outputs into the wiki page. To annotate and discuss your game with 
example boards, use a "Board" tag:
{{{#!Chess Board Match-ID 23-White }}}   <-- Show White's 23rd move
{{{#!Chess Board Match-ID 8-Black }}}    <-- Show Black's 8th move

Each time the chessboard is printed, the move being shown appears in a
drop-down widget, with the current move illustrated being shown. The entire
history of the game can be cycled through in each widget, though the move
being illustrated will be shown by default.
"""


from MoinMoin import wikiutil
from MoinMoin.parser import wiki
from MoinMoin import caching
import chess.pgn


class Parser:
    """ Insert chess boards into the MoinMoin wiki and write about chess games"""
    def __init__(self, raw, request, **kw):
        self.raw = raw
        # raw is the text inbetween the {{{ and }}} thingies. 
        
        self.request = request
        # request is the HTTPRequest object

        self.kw=kw
        # for example: {{{!# HelloWorld a b c }}}
        # {'format_args': 'a b c '}

	# The board can be constructed empty-form, or from a list of moves.
	# The moves may be in PGN format, readable by chess.pgn
	inputs = self.kw['format_args'].split(' ')
	name = inputs[0]
	mode = inputs[1]	# Either "Game" or "Board"
	board = inputs[2]	# In a "Board" tag, what move to display
	action = inputs[2:]	# In a "Game" tag, the list of moves


	# Game tags:
	# If the name of the game exists, read a cachefile. Otherwise, create a
	# new one, containing the PGN of the game.



	# Board tags:
	# TODO: determine how to draw boards in such a way that a drop-down menu
	# can control the output of the chessboard next to it. Need a performant
	# way to switch between multiple board divs, each of which contain 64
	# individual chess square DIV's. Use dropdowns and visibility: hidden. 


	try {
	   board = chess.Bitboard(kw['format_args'])
	} except {
	   





    def format(self, formatter):
        #n format is also called for each !# command. its called after __init__
        # is called. this is where parsers do most of their work.
        # they write their results into the Httprequest object
        # which is usually stored from __init__ in self.request. 
        
        # print "formatter",dir(formatter)
        # formatter is a special object in MoinMoin that
        # is supposed to help people who write extensions to have
        # sort of a uniform looking thing going on.
        # see http://moinmoin.wikiwikiweb.de/ApplyingFormatters?highlight=%28formatter%29
                
        # but formatter is not documented well. you have to look at
        # moinmoin/formatter/base.py. And if you do, you will see that half of
        # the methods raise a 'not implemented' error.
        # formatter is also being refactored alot so dont get used to it. 
        # if all else fails just use formatter.rawHTML which will
        # screw up XML output but at least it will work.

	# from MoinMoin import formatter <<- has the methods we can use here  
        self.request.write(formatter.text("hello world begin"))
        self.request.write(formatter.paragraph(1))
        self.request.write(formatter.text('raw: ' + self.raw))
        self.request.write(formatter.paragraph(0))
        self.request.write(formatter.paragraph(1))
        self.request.write(formatter.text('kw:' + str(self.kw)))
        self.request.write(formatter.paragraph(0))
        self.request.write(formatter.text("hello world end"))
        self.request.write(formatter.paragraph(1))
        self.request.write(formatter.paragraph(0))
