/* moin-chess Javascript helper
 * Justin Cassidy, December 2014
 *
 * Turns plain-jane ASCII chessboards into resolution-independent sets of
 * ASCII chess pieces laid across off-white/off-black DIV squares.
 *
 * Requires zepto.js
 */

PIECE = new Object;
PIECE['P'] = '♟';
PIECE['N'] = '♞';
PIECE['B'] = '♝';
PIECE['R'] = '♜';
PIECE['Q'] = '♛';
PIECE['K'] = '♚';
PIECE['.'] = '';

function create_square(sq_color, piece_color, piece) {
   var e_square = document.createElement('div');

   // Replace each character with the corresponding piece. All pieces
   // are "solid black-chess-piece" unicode characters, but colored to be 
   // either white or black.
   var graphic = PIECE[piece.toUpperCase()];

   // The square's properties are determined by piece color and square color
   e_square.className = sq_color + piece_color;
   e_square.innerHTML = graphic;

   return e_square;
}


function create_rank(board, rank) {
   var e_rank = document.createElement('div');
   e_rank.className = "rank"; 

   // Number is odd or even. Even ranks start with white squares on the left,
   // odd ranks start with black squares on the left.
   // The rank string will get converted into squares by create_square
   for ( var j = rank*8; j < j+8 ; j++ ) {
      var piece = board[j];
      var sq_color = "bs";
      if ( j % 2 == 0 ) {
         sq_color = "ws";
      }
      var piece_color = "_wp";
      // Lowercase characters are black pieces
      if ( piece == piece.toLowerCase() ) {
         piece_color = "_bp";
      }
      // Don't care what color pieces in empty squares are
      if ( piece == "." ) {
         piece_color = "";
      }

      var e_square = create_square(sq_color, piece_color, piece);
      e_rank.appendChild(e_square);      
   }

   return e_rank;
}


$(function() {
   var chessboards = document.body.querySelectorAll('.chessboard');
   var output = []

   for ( var i = 0; i < chessboards.length; i++ ) {
      var board = chessboards[i].childNodes[0].innerHTML.split(' ').join('');

      var e_board = document.createElement('div');
      e_board.className = "chessboard"; 

      // The current board is a string representing the board, from upper-left
      // to lower-right squares. Upper-left first square and odd squares are
      // white, and even squares are black. Uppercase pieces are white, and
      // lowercase pieces are black.
      for ( var j = 0; j < board.length; j+8 ) {
         var e_rank = create_rank(board, j%8);
         e_board.appendChild(e_rank);
      }

      // Add chessboards to the output[]
   }

   // TODO: For each chessboard, replace the corresponding chessboard div
   // with the constructed outputs
}      
