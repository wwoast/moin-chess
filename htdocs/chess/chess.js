// moin-chess Javascript helper
// Justin Cassidy, December 2014
//
// Turns plain-jane ASCII chessboards into resolution-independent sets of
// ASCII chess pieces laid across off-white/off-black DIV squares.
//
// Requires zepto.js


function create_square(rank, square, piece_color, piece) {
   // Even ranks' odd squares are white, and even squares are black.
   // Odd ranks' odd squares are black, and even squares are white.


   // Replace each character with the corresponding piece. All pieces
   // are "solid black-chess-piece" unicode characters, but colored to be 
   // either white or black.



function create_rank(rank, rank_string) {
   // Number is odd or even. Even ranks start with white squares on the left,
   // odd ranks start with black squares on the left.
   // The rank string will get converted into squares by create_square



$(function() {
   var chessboards = document.body.querySelectorAll('.chessboard');

   // White pieces: pnbrqk, Black pieces: PNBRQK
   // Replace each line of text with a rank <div>
   // Replace each piece with the appropriate bs/ws <div>
   // Top of the board is 8th rank, and then count down.   
