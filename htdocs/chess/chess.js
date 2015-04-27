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


function link_id_names(lid) {
   // Standard format: First is the link type: ch_m for a move,
   // ch_pm for "Previous" button, and ch_nm for "Next" button.
   // Then a | and the name of the game, followed by an _. Finally,
   // the number of the move and who's going. Return an array with
   // all of the relevant values that will match board/link ids.
   var tmp = lid.split("|");
   var type = tmp.shift(1);
   var state = tmp.pop();
   tmp = tmp.join("|").split("_");
   var turn = tmp.pop();
   var game_name = tmp.join("_");
   var game_move = game_name + "_" + turn;  
   return [ type, game_name, game_move, state ];
}


function create_listener(link, callback, game_name, game_move, game_state) {
   // For scoping functions (closures), the addEventListeners must
   // be inside a scope outside the create_menu_listeners loop.
   // Otherwise the environment of the event callbacks is equivalent
   // to the last iteration of the loop. It's super annoying!
   link.addEventListener('click', function() {
      callback(game_name, game_move, game_state)});
}


function create_menu_listeners() {
   // Look at all link ids. Anything with a game name in it gets a
   // switch_board click listener. Anything with a previous_move or
   // next_move in it gets a adjacent_board click listener.
   links = document.getElementsByClassName('moveitem');

   // NOTE: Function argument inside an anonymous function will act 
   // on the click, rather than firing on the immediate page loading.
   for ( var i = 0; i < links.length; i++ ) {
      var link_id = links[i].id;
      if ( link_id.indexOf("ch_") == 0 ) {
         var id_splits = link_id_names(link_id);
         var game_name = id_splits[1];
         var game_move = id_splits[2];
         var game_state = id_splits[3];
         if ( id_splits[0] == "ch_m" ) {
            // This is a chess move link
            create_listener(links[i], switch_board, game_name, game_move, game_state);
         }
         if ( id_splits[0] == "ch_pm" ) {
            // This is a previous move link
            create_listener(links[i], adjacent_board, game_name, "previous", game_state);
         }
         if ( id_splits[0] == "ch_nm" ) {
            // This is a next move link
            create_listener(links[i], adjacent_board, game_name, "next", game_state);
         }
      }
   }
}


Zepto(function($) {
   var chessboards = document.body.querySelectorAll('.chessboard');
   var output = new Object;
   var game_name = "";

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
      
      // If this is the first board drawn for a new game, make it displayable
      output[id] = e_board;
   }

   // Now, replace ASCII boards with div-pretty polishboards
   for ( var i = 0; i < chessboards.length ; i++ ) {
      var id = chessboards[i].id;
      chessboards[i].innerHTML = output[id].innerHTML;
      chessboards[i].className = "polishboard";
      // Every time we have a new game, print the first table
      var id_split = link_id_names(id);     
      if ( id_split[1] != game_name ) {
         chessboards[i].style.display = "table";
         game_name = id_split[1];
      }
   }

   // And now that the boards are drawn, draw menus using the game
   // id name from the first chessboard
   create_menu_listeners();
});


function current_board(game_name) {
   // Given a game name, find the board that's currently being displayed
   var chessboards = document.querySelectorAll(".polishboard");
   for ( var i = 0 ; i < chessboards.length; i++ ) {
      var board = chessboards[i];
      if ( board.id.indexOf(game_name) >= 0 && 
           board.style.display == "table" ) {
         return board;
      }
   }
}


function update_focal_move(game_name, to_id, state) {
   // Update the focal move text, including current move state. 
   // TODO: make clickable
   // URG: must have previous and next move state, not this move's state!
   var move = to_id.split("_").pop();
   var color = move.split('').pop();
   var move_n = Number(move.replace(color, ''));
   var white_turn = move_n;
   var black_turn = move_n;   

   if ( color == "b" ) {
      white_turn = white_turn + 1;
   }
   if ( color == "w" ) {
      black_turn = black_turn - 1;
   }

   var white = game_name + "_" + white_turn + "w" + "|" + state;
   var black = game_name + "_" + black_turn + "b" + "|" + state;

   var focal_white = document.getElementById(game_name + "_white");
   var focal_black = document.getElementById(game_name + "_black");

   // Board link states point at the next person's turn, so the white move
   // is the black turn pointer's link text, and vice versa
   var white_move = document.getElementById("ch_m|" + black);
   var black_move = document.getElementById("ch_m|" + white);
   var white_text = "&mdash;";
   var black_text = "&mdash;";
   // First move is dash-dash unless non-null
   if ( white_move != null ) {
      white_text = black_turn + ". " + white_move.innerHTML;
   }
   // If game ended with a white move, replace with mdash
   if ( black_move != null && white_move != null ) {
      black_text = black_move.innerHTML;
   }

   focal_white.innerHTML = white_text;
   focal_black.innerHTML = black_text;
}


function switch_board(game_name, to_id, state) {
   // Used for the individual chess moves, to allow the board to be changed
   var this_board = current_board(game_name);
   var new_board = document.getElementById("ch_b|" + to_id + "|" + state);

   this_board.style.display = "none";
   new_board.style.display = "table";

   update_focal_move(game_name, to_id, state); 
}


function adjacent_board(game_name, direction, state) {
   var this_board = current_board(game_name);
   var id_split = link_id_names(this_board.id);

   var chessboards = document.querySelectorAll(".polishboard");
   var previous_board = "";
   var next_board = "";
   var prev_split = "";
   var next_split = "";

   for ( var i = 0; i < chessboards.length; i++ ) {
      if ( chessboards[i].id == this_board.id ) {
         if ( i-1 >= 0 ) {
            previous_board = chessboards[i-1];
            prev_split = link_id_names(chessboards[i-1].id);
            if ( id_split[1] != prev_split[1] ) {
               // Not the same game names
               previous_board = '';
            }
         } 
         if ( i+1 < chessboards.length ) {
            next_board = chessboards[i+1]; 
            next_split = link_id_names(chessboards[i+1].id);
            if ( id_split[1] != next_split[1] ) {
               // Not the same game names
               next_board = '';
            }
         }
         break;
      }
   }

   if ( direction == "previous" && previous_board != "" ) {
      this_board.style.display = "none";
      previous_board.style.display = "table";
      update_focal_move(game_name, prev_split[2], state); 
   }
   if ( direction == "next" && next_board != "" ) {
      this_board.style.display = "none";
      next_board.style.display = "table";
      update_focal_move(game_name, next_split[2], state); 
   }
}
