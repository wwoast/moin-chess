/* moin-chess Javascript helper
 * Justin Cassidy, December 2014
 *
 * Turns plain-jane ASCII chessboards into resolution-independent sets of
 * ASCII chess pieces laid across off-white/off-black DIV squares.
 *
 * Requires zepto.js
 */

var PIECE = new Object;
PIECE['P'] = '&#9823;'   // '♟';
PIECE['N'] = '&#9822;'   // '♞';
PIECE['B'] = '&#9821;'   // '♝';
PIECE['R'] = '&#9820;'   // '♜';
PIECE['Q'] = '&#9819;'   // '♛';
PIECE['K'] = '&#9818;'   // '♚';
PIECE['.'] = '&nbsp;';   // w/o a non-breaking space, empty squares are 
                         // smaller than ones with pieces in them!


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
   start = rank*8;
   end = start + 8;
   for ( var j = start; j < end ; j++ ) {
      var piece = board[j];
      var sq_color = "bs";
      if ( j % 2 == rank % 2 ) {
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


function create_menu_listeners() {
   // Look at all link ids. Anything with a game name in it gets a
   // switch_board click listener. Anything with a previous_move or
   // next_move in it gets a adjacent_board click listener.
   
   // Finally, add event listeners for any menu link buttons. Function
   // argument inside an anonymous function will act on the click,
   // rather than firing on the immediate page loading.
   document.getElementById('previous_move').addEventListener('click', function() {
      adjacent_board('previous')});
   document.getElementById('next_move').addEventListener('click', function() {
      adjacent_board('next')});
}


$(function() {
   var chessboards = document.body.querySelectorAll('.chessboard');
   var output = new Object;

   for ( var i = 0; i < chessboards.length; i++ ) {
      var board = chessboards[i].childNodes[0].innerHTML;
      board = board.split(' ').join('').split('\n').join('');
      var id = chessboards[i].id;

      var e_board = document.createElement('div');
      e_board.className = "polishboard"; 
      e_board.id = id;

      // The current board is a string representing the board, from upper-left
      // to lower-right squares. Upper-left first square and odd squares are
      // white, and even squares are black. Uppercase pieces are white, and
      // lowercase pieces are black.
      for ( var j = 0; j < board.length; j=j+8 ) {
         var e_rank = create_rank(board, j/8);
         e_board.appendChild(e_rank);
      }

      output[id] = e_board;
   }

   // Now, replace ASCII boards with div-pretty polishboards
   for ( var i = 0; i < chessboards.length ; i++ ) {
      var id = chessboards[i].id;
      chessboards[i].innerHTML = output[id].innerHTML;
      chessboards[i].className = "polishboard";
   }
});


function switch_board(this_board, to_id) {
   var new_board = document.getElementById(to_id);

   this_board.style.display = "none";
   new_board.style.display = "table";
}


function adjacent_board(this_board, direction) {
   var chessboards = document.querySelectorAll(".polishboard");
   var previous_board = "";
   var next_board = "";

   for ( var i = 0; i < chessboards.length; i++ ) {
      if ( chessboards[i].id == this_board.id ) {
         if ( i-1 >= 0 ) {
            previous_board = chessboards[i-1];
         } 
         if ( i+1 < chessboards.length ) {
            next_board = chessboards[i+1];     
         }
         break;
      }
   }

   if ( direction == "previous" && previous_board != "" ) {
      this_board.style.display = "none";
      previous_board.style.display = "table";
   }
   if ( direction == "next" && next_board != "" ) {
      this_board.style.display = "none";
      next_board.style.display = "table";
   }
}
