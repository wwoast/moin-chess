/* head.js: Moin Chess Plugin "stub" script
 * December 2014
 *
 * Load this script with every {{{#!Chess}}} tag in the wiki. Upon first
 * run, this script inserts the remaining CSS and JS code into the DOM to
 * support nice-looking CSS chessboards and menus.
 *
 * For subsequent {{{#!Chess}}} tags in the page after the first one, we have
 * to still insert this stub script, but inspection of the DOM will show that
 * further inserts are unnecessary.
 */

// Expects moin_chess_root in the current DOM, from the plugin output
// var moin_chess_root = "/moin_static194/chess/"

var style = document.createElement('link');
style.rel = "stylesheet";
style.href = moin_chess_root + "chess.css";

var zeptojs = document.createElement('script');
zeptojs.type = "text/javascript";
zeptojs.src = moin_chess_root + "zepto.js";

var behavior = document.createElement('script');
behavior.type = "text/javascript";
behavior.src = moin_chess_root + "chess.js";

// Have we loaded the Chess JS? If so, don't load any of these 
// resources a second time! Also, try and insert zepto to load
// before anything else
if ( ! behavior.isEqualNode(document.head.lastChild)) {
   var first = document.getElementsByTagName('script')[0];
   first.parentNode.insertBefore(zeptojs, first);

   document.head.appendChild(style);
   document.head.appendChild(behavior);
}
