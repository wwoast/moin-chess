"""
A parser gets created by a Page object, is given the text its supposed
to format and an HTTPRequest object. It mucks around with the text,
and writes the result to the HTTPRequest object it was given. 

To install:

Copy this file into data/plugins/parser in your moinmoin wiki instance.
Restart the wiki if necessary.
Edit a page and type in

{{{#!Chess Game-Name 
PGN / FEN notation, or just a new move
}}}

The result should be a chessboard matching the game state.

The way the chess games are tracked across multiple tags is with a
cache object. Each {{{#!Chess Game-Name }}} tag gets a cache object
named "(pagename)-(Game-Name)". The first chess tag should have the
cumulative game state, and then future tags should be either valid
moves or game resets of the initial state.



"""


from MoinMoin import wikiutil
from MoinMoin.parser import wiki
from MoinMoin import caching


class Parser:
    """ Insert chess boards into the MoinMoin wiki and write about chess games"""
    
    def __init__(self, raw, request, **kw):
        # 'init' is called once for each !# command but it doesnt do much.
        # Most of the work usually happens in the 'format' method.

        self.raw = raw
        # raw is the text inbetween the {{{ and }}} thingies. 
        # most parsers generally save it for use in the 'format'
        # method. 
        
        self.request = request
        # request is the HTTPRequest object
        # parsers generally save this during '__init__' for use later
        # on in 'format'. They have to write to it in fact to get
        # any results. 

        self.kw=kw
        # kw is is a dictionary with 'arguments' to the !# command.
        # for example: {{{!# HelloWorld a b c }}}
        # would give the following value for kw:
        # {'format_args': 'a b c '}

	# TODO: define the input formats here valid for python chess
	# Parse the argument text with python-chess
	# once we say we have a valid board, create the HTML board format

	# If the board is valid format, create a new cache file and store the game's state
	# to that cache file for later use. Construct a HTML chess board in the cache, and
	# for future page loads we can just grab this chess board and stick it into the page

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

        # the end
