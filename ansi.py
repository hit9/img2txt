from graphics_util import alpha_blend


def getANSIcolor_for_rgb(rgb):
    # Convert to web-safe color since that's what terminals can handle in "256 color mode" 
    #   https://en.wikipedia.org/wiki/ANSI_escape_code
    #   http://misc.flogisoft.com/bash/tip_colors_and_formatting#bash_tipscolors_and_formatting_ansivt100_control_sequences
    #   http://superuser.com/questions/270214/how-can-i-change-the-colors-of-my-xterm-using-ansi-escape-sequences
    websafe_r = int(round((rgb[0] / 255.0) * 5) )
    websafe_g = int(round((rgb[1] / 255.0) * 5) )
    websafe_b = int(round((rgb[2] / 255.0) * 5) )

    # Return ANSI color - only using 216 colors since those are the only ones we can reliably map to   
    #   https://en.wikipedia.org/wiki/ANSI_escape_code (see 256 color mode section)    
    return int(((websafe_r * 36) + (websafe_g * 6) + websafe_b) + 16)   


def getANSIfgarray_for_ANSIcolor(ANSIcolor):
    "Return array of color codes to be used in composing an SGR escape sequence. Using array form lets us compose multiple color updates without putting out additional escapes"
    # We are using "256 color mode" which is available in xterm but not necessarily all terminals
    return ['38', '5', str(ANSIcolor)]      # To set FG in 256 color you use a code like ESC[38;5;###m


def getANSIbgarray_for_ANSIcolor(ANSIcolor):
    "Return array of color codes to be used in composing an SGR escape sequence. Using array form lets us compose multiple color updates without putting out additional escapes"
    # We are using "256 color mode" which is available in xterm but not necessarily all terminals
    return ['48', '5', str(ANSIcolor)]      # To set BG in 256 color you use a code like ESC[48;5;###m
    

def getANSIbgstring_for_ANSIcolor(ANSIcolor):
    # Get the array of color code info, prefix it with ESCAPE code and terminate it with "m"
    return "\x1b[" + ";".join(getANSIbgarray_for_ANSIcolor(ANSIcolor)) + "m"
    

def generate_ANSI_to_set_fg_bg_colors(cur_fg_color, cur_bg_color, new_fg_color, new_bg_color):
             
    # This code assumes that ESC[49m and ESC[39m work for resetting bg and fg 
    # This may not work on all terminals in which case we would have to use ESC[0m 
    # to reset both at once, and then put back fg or bg that we actually want
 
    # We don't change colors that are already the way we want them - saves lots of file size

    color_array = []        # use array mechanism to avoid multiple escape sequences if we need to change fg AND bg

    if new_bg_color != cur_bg_color:
        if new_bg_color is None:
            color_array.append('49')        # reset to default
        else:
            color_array += getANSIbgarray_for_ANSIcolor(new_bg_color)
                
    if new_fg_color != cur_fg_color:
        if new_fg_color is None:
            color_array.append('39')        # reset to default
        else:
            color_array += getANSIfgarray_for_ANSIcolor(new_fg_color)

    if len(color_array) > 0:
        return "\x1b[" + ";".join(color_array) + "m"
    else:
        return ""


def generate_optimized_y_move_down_x_SOL(y_dist):
    """ move down y_dist, set x=0 """

    # Optimization to move N lines and go to SOL in one command. Note that some terminals 
    # may not support this so we might have to remove this optimization or make it optional 
    # if that winds up mattering for terminals we care about. If we had to remove we'd
    # want to rework things such that we used "\x1b[{0}B" but also we would want to change
    # our interface to this function so we didn't guarantee x=0 since caller might ultimate 
    # want it in a different place and we don't want to output two x moves. Could pass in 
    # desired x, or return current x from here. 
          
    string = "\x1b[{0}E".format(y_dist)  # ANSI code to move down N lines and move x to SOL

    # Would a sequence of 1 or more \n chars be cheaper? If so we'll output that instead
    if y_dist < len(string):
        string = '\n' * y_dist
        
    return string
    

def generate_ANSI_to_move_cursor(cur_x, cur_y, target_x, target_y):
    """
        Note that x positions are absolute (0=SOL) while y positions are relative. That is,
        we move the y position the relative distance between cur_y and target_y. It doesn't
        mean that cur_y=0 means we are on the first line of the screen. We have no way of
        knowing how tall the screen is, etc. at draw-time so we can't know this. 
    """


    """
        **SIZE - this code (in concert with its caller) implements what I would call "local optimizations"
        to try to minimize the number and size of cursor movements outputted. It does not attempt "global
        optimizations" which I think are rarely going to be worthwhile. See the DESIGN NOTE on global
        optimizations in this file for more details 
    """        


    string = ""

    if cur_y < target_y:    # MOVE DOWN
        y_dist = target_y - cur_y

        # See if we can optimize moving x and y together
        if cur_x == target_x: 
        
            # Need to move in y only
            if target_x != 0: 
                # Already in correct x position which is NOT SOL. Just output code to move cursor 
                # down. No special optimization is possible since \n would take us to SOL and then 
                # we'd also need to output a move for x. 
                return "\x1b[{0}B".format(y_dist)  # ANSI code to move down N lines
            else:
                # Already in correct x position which is SOL. Output efficient code to move down.
                return generate_optimized_y_move_down_x_SOL(y_dist)
        else:
        
            # Need to move in x and y
            if target_x != 0: 
                # x move is going to be required so we'll move y efficiently and as a side
                # effect, x will become 0. Code below will move x to the right place
                string += generate_optimized_y_move_down_x_SOL(y_dist)
                cur_x = 0
            else:
                # Output move down that brings x to SOL. Then we're done.
                return generate_optimized_y_move_down_x_SOL(y_dist)
                
    elif cur_y > target_y:  # MOVE UP
        if target_x == 0:        
            # We want to move up and be at the SOL. That can be achieved with one command so we're
            # done and we return it. However note that some terminals may not support this so we
            # might have to remove this optimization or make it optional if that winds up mattering for terminals we care about.  
            return "\x1b[{0}F".format(cur_y - target_y)     # ANSI code to move up N lines and move x to SOL
        else:
            string += "\x1b[{0}A".format(cur_y - target_y)  # ANSI code to move up N lines 

    if cur_x < target_x:    # MOVE RIGHT
        # **SIZE - Note that when the bgcolor is specified (not None) and not overdrawing another drawing (as in an animation case)
        # an optimization could be performed to draw spaces rather than output cursor advances. This would use less
        # size when advancing less than 3 columns since the min escape sequence here is len 4. Not implementing this now
        # \t (tab) could also be a cheap way to move forward, but not clear we can determine how far it goes or if that would
        # be consistent, nor whether it is ever destructive.
        string += "\x1b[{0}C".format(target_x - cur_x)  # ANSI code to move cursor right N columns
    elif cur_x > target_x:  # MOVE LEFT
        # **SIZE - potential optimizations: \b (backspace) could be a cheaper way to move backwards when there is only a short
        # way to go. However, not sure if it is ever destructive so not bothering with it now.    
        # If we need to move to x=0, \r could be a cheap way to get there. However not entirely clear whether some terminals
        # will move to next line as well, and might sometimes be destructive. Not going to research this so not doing it now. 
        string += "\x1b[{0}D".format(cur_x - target_x)  # ANSI code to move cursor left N columns 

    return string


def generate_ANSI_from_pixels(pixels, width, height, bgcolor_rgba, current_ansi_colors = None, current_cursor_pos = None, get_pixel_func = None, is_overdraw = False, x_offset = 0):
    """
    Generate ANSI codes for passed pixels
       
    Does not include a final newline or a reset to any particular colors at end of returned output string.
    Caller should take care of that if desired.
     
    :param pixels: if get_pixel_func is None, 2D array of RGBA tuples indexed by [x,y]. 
       Otherwise given to get_pixel_func as param.
    :param width: number of pixels to output on each row
    :param height: number of rows to output 
    :param bgcolor_rgba: Optional background color used to fill new lines (produced when is_ovedraw is False)
       and a net new line to the terminal (as opposed to drawing on a current line - e.g. if the cursor was moved
       up) is produced. Also used as background color for any characters we output that don't fill the entire 
       character area (e.g. a space fills the entire area, while X does not). Non-space only used if get_pixel_func
       returns it. If bgcolor_rgba is None, then the background is treated as the terminal's default background color
       which also means that partially transparent pixels will be treated as non-transparent (since we don't know 
       bg color to blend them with).   
    :param current_ansi_colors: Optional dict holding "current" ANSI colors - allows optimization where 
       we don't switch to these colors if already set. See info on return values for format of dict.
    :param current_cursor_pos: Optional dict holding current cursor position - allows optimization where 
       we don't output extra moves to get to the right place to draw. Consider the passed position relative
       to where we want to draw the top/left for the current call. Note that a negative value for 
       current_cursor_pos['y'] can be used to start drawing futher down the screen. Don't use ['x'] similarly 
       since x is reset for each line. Use the x_offset param instead. 
    :param get_pixel_func: Optional function that allows using custom "pixel" formats. If not None, function 
       that will be passed pixels and a current x,y value and must return character to draw and RGBA to draw it in. 
    :param is_overdraw: if True, drawing code can assume that all lines are being drawn on lines that were already
       established in the terminal. This allows for optimizations (e.g. not needing to output \n to fill blank lines).
    :param x_offset: If not zero, allows drawing each line starting at a particular X offset. Useful if 
       you don't want it drawn at x=0. Must be >=0 

    Returns tuple:
      string containing ANSI codes
      dict of form {'fg': (r,g,b,a), 'bg': (r,g,b,a)} holding current fg/bg color - suitable for passing as current_ansi_colors param
      dict of form {'x': <integer>, 'y': <integer>} holding final x,y cursor positions - x is absolute since \n sends it to 0. y is relative to incoming y (or 0 if none). Suitable for passing as current_cursor_pos param
    """

    if get_pixel_func is None:
        get_pixel_func = lambda pixels, x, y: (" ", pixels[x, y])      # just treat pixels as 2D array 

    # Compute ANSI bg color and strings we'll use to reset colors when moving to next line   
    if bgcolor_rgba is not None:
        bgcolor_ANSI = getANSIcolor_for_rgb(bgcolor_rgba)
        # Reset cur bg color to bgcolor because \n will fill the new line with this color
        bgcolor_ANSI_string = getANSIbgstring_for_ANSIcolor(bgcolor_ANSI)
    else:
        bgcolor_ANSI = None        
        # Reset cur bg color default because \n will fill the new line with this color (possibly only if BCE supported by terminal)
        bgcolor_ANSI_string = "\x1b[49m"     # reset bg to default (if we want to support terminals that can't handle this will need to instead use 0m which clears fg too and then when using this reset prior_fg_color to None too
    
    # Do we know the current ANSI colors that have been set? 
    if current_ansi_colors is not None:    
        string = ""
        prior_fg_color = current_ansi_colors['fg']       # Value of None is OK - means default
        prior_bg_color = current_ansi_colors['bg']       # Value of None is OK - means default
    else:
        # We don't know the current colors so output a reset to terminal defaults - we want to be in a known state
        # **SIZE - could suppress outputting this here, and remember that we have unknown (not same as default)
        # colors. Then when we need to output we can take this into account. If we wind up setting both fg and bg colors
        # for output (as for a non-space) then we'd never need to output the reset.  
        # I'm not going to implement this now since the better thing to do for repeated calls is to pass current_ansi_colors
        # so we'd never get to this case.
        string = "\x1b[0m"          # removes all attributes (formatting and colors) to start in a known state
        prior_fg_color = None       # this is an ANSI color not rgba. None means default.
        prior_bg_color = None       # this is an ANSI color not rgba. None means default.
    
    # Do we know the cursor pos?
    if current_cursor_pos is not None:
        cursor_x = current_cursor_pos['x']
        cursor_y = current_cursor_pos['y']
    else:
        cursor_x = 0
        cursor_y = 0

    for h in range(height):  
        for w in range(width):

            draw_char, rgba = get_pixel_func(pixels, w, h)

            # Handle fully or partially transparent pixels - but not if it is the special "erase" character (None)
            skip_pixel = False
            if draw_char is not None:
                alpha = rgba[3]
                if alpha == 0:
                    skip_pixel = True       # skip any full transparent pixel. Note that we don't output a bgcolor space (in specified or default cases). Why? In overdraw mode, that would be wrong since whatever is already drawn should show through. In non-overdraw, assumption is that any line we're drawing on has already been filled with bgcolor so lets not do extra output. If this was an issue in practice, could make it an option.                        
                elif alpha != 255 and bgcolor_rgba is not None:
                    rgba = alpha_blend(rgba, bgcolor_rgba)  # non-opaque so blend with specified bgcolor
                        
            if not skip_pixel:

                this_pixel_str = ""

                # Throw away alpha channel - can still have non-fully-opaque alpha value here if
                # bgcolor was partially transparent or if no bgcolor and not fully transparent
                # Could make argument to use threshold to decide if throw away (e.g. >50% transparent) 
                # vs. consider opaque (e.g. <50% transparent) but at least for now we just throw it away 
                # which means we treat the pixel as fully opaque.
                rgb = rgba[:3]   
                
                # If we've got the special "erase" character turn it into outputting a space using the bgcolor
                # which if None will just be a reset to default bg which is what we want
                if draw_char is None:
                    draw_char = " "
                    color = bgcolor_ANSI
                else:
                    # Convert from RGB to ansi color, using closest color. Conceivably we could optionally support
                    # dithering to spread the color error. Problematic when dealing with transparency (see cmt in dither_image_to_web_palette())
                    # or unknown/default bgcolor, and currently not worthwhile since either easy (img2txt) or more correct (graphics) to do 
                    # dithering upstream. 
                    color = getANSIcolor_for_rgb(rgb)
                
                    # Optimization - if we're drawing a space and the color is the same as a specified bg color
                    # then just skip this pixel. We need to make this check here because the conversion to ANSI above can 
                    # cause colors that didn't match to now match
                    # We cannot do this optimization in overdraw mode because we cannot assume that the bg color
                    # is already drawn at this location. We could presumably pass in the known state of the screen
                    # and thus have this knoweldge if the optimization was worthwhile. 
                    if not is_overdraw and (draw_char == " ") and (color == bgcolor_ANSI):
                        skip_pixel = True

                if not skip_pixel:
      
                    if len(draw_char) > 1:
                        raise ValueError("Not allowing multicharacter draw strings")

                    # If we are not at the cursor location where we need to draw (happens if we skip pixels or lines)
                    # then output ANSI sequence to move cursor there.
                    # This is how we implement transparency - we don't draw spaces, we skip via cursor moves
                    # We take the x_offset (if any) into account here
                    ofsetted_w = x_offset + w
                    if (cursor_x != ofsetted_w) or (cursor_y != h):
                        string += generate_ANSI_to_move_cursor(cursor_x, cursor_y, ofsetted_w, h)
                        cursor_x = ofsetted_w
                        cursor_y = h
          
                    # Generate the ANSI sequences to set the colors the way we want them
                    if draw_char == " ":
                
                        # **SIZE - If we are willing to assume terminals that support ECH (Erase Character) as specified
                        #   in here http://vt100.net/docs/vt220-rm/chapter4.html we could replace long runs of same-color
                        #   spaces with single ECH codes. Seems like it is only correct to do this if BCE is supported
                        #   though (http://superuser.com/questions/249898/how-can-i-prevent-os-x-terminal-app-from-overriding-vim-colours-on-a-remote-syst)
                        #   else "erase" would draw the _default_ background color not the currently set background color
                        #   Note that if we implement this by accumulating spaces (as opposed to lookahead), need to output that 
                        #   before any different output be that a color change, or if we need to output a \n (if line ended 
                        #   in same-color spaces in non-overdraw)
                                        
                        # We are supposed to output a space, so we're going to need to change the background color.
                        # No, we can't output an "upper ascii" character that fills the entire foreground - all terminals
                        # don't display such characters the same way, if at all. e.g. Mac terminal outputs ? for "upper ascii" chars
                        # Since we're outputting a space we can leave the prior fg color intact as it won't be used      
                        string += generate_ANSI_to_set_fg_bg_colors(prior_fg_color, prior_bg_color, prior_fg_color, color)
                        prior_bg_color = color
                    
                    else:
                        # We're supposed to output a non-space character, so we're going to need to change the foreground color
                        # and make sure the bg is set appropriately
                        string += generate_ANSI_to_set_fg_bg_colors(prior_fg_color, prior_bg_color, color, bgcolor_ANSI)
                        prior_fg_color = color
                        prior_bg_color = bgcolor_ANSI

                    # Actually output the character
                    string += draw_char                               

                    cursor_x = cursor_x + 1
 
        # Handle end of line - unless last line which is NOP because we don't want to do anything to the _line after_ our drawing
        # and outputting \n would establish it and fill it
        if (h + 1) != height:
                      
            # Move to next line. If this establishes a new line in the terminal then it fills the _newly established line_
            # up to EOL with current bg color. Filling with the current bg color vs. default might be dependent on terminal's
            # support for BCE (Background Color Erase) - I'm not sure.
            # If cursor had been moved up and this just goes back down to an existing line, no filling occurs
            # In overdraw mode, we are going to assume we don't need to establish/fill a new line (which could be untrue
            # if we are overdrawing some lines but going further down too - if that becomes important can allow passing
            # in how many lines we can go down before hitting that). Next time we need to draw in overdraw mode we'll
            # move the cursor down as needed.
            if not is_overdraw:

                # If not already desired color, reset bg color so \n fills with it
                # NOTE: it would be ideal to optionally dither the background color if it is not perfectly resolvable
                # in the palette we have to work with. However, we can't actually do this in the general case because
                # we don't know the width of the terminal (which can be different at display-time) and because we
                # don't always know the bg color ("default" is not known by us, and not known by anybody until display-time) 
                if prior_bg_color != bgcolor_ANSI:
                    string += bgcolor_ANSI_string;    
                    prior_bg_color = bgcolor_ANSI       
         
                # If the cursor is not at the correct y, move it there before outputting the newline
                # In current use this will only occur if current_cursor_pos includes a y offset and
                # the first line was entirely transparent. We pass 0/0 for cur/target x because no need
                # to adjust x as it will be changed by the \n 
                if (cursor_y != h):
                    string += generate_ANSI_to_move_cursor(0, cursor_y, 0, h)
                    cursor_y = h
              
                string += "\n"      
                cursor_y += 1
                cursor_x = 0        # we are assuming UNIX-style \n behavior - if it were windows we'd have to output \r to get cursor_x to 0

    return string, {'fg': prior_fg_color, 'bg': prior_bg_color}, { 'x': cursor_x, 'y': cursor_y }


"""
DESIGN NOTE (Global Optimization)

The code in this file currently implements "local optimization" to minimize the cost of moving
the cursor around and changing colors. However, it always follows a top-to-bottom left-to-right
path. There are scenarios where choosing a different path would yield a more optimal result
(smaller output size). I have not bothered to implement any global optimization because I
think it will rarely produce a better output.

Here's an example of a scenario where a global optimization of cursor movements that didn't just
 go scanline by scanline top to bottom left to right would be a win:

For example, assume this pattern is to be drawn, beginning at x=0 (SOL)
XXX      XXX
   XXX      XXX
      XXX      XXX              
Drawing it top down/left to right we must do 13 operations: 
    XXX, move right, XXX, \n, move right, XXX, move right, XXX, \n, move right, XXX, move right, XXX  
Drawing it in an optimal sequence we can do 11 operations:
    XXX, move down, XXX, move down, XXX, move up, XXX, move down, XXX, move down, XXX
However, since \n is cheaper than move down, we actually would need blank lines between the XXX lines
to really make the second case smaller in terms of bytes (vs operations).

The discussion above covers cursor changes, but of cours color changes play a role as well. If we were
to assume the XXX on the left were one color while the XXX on the right were another, we'd also save four
color change operations.

To perfectly implement global optimization, you essentially need to solve a variant of the Traveling 
Salesman Path Problem (TSPP) as I discuss here: http://stackoverflow.com/questions/20032768/graph-traversal-with-shortest-path-with-any-source/33601043#33601043
We could use the single fixed endpoint variant (P*s) from the Hoogeveen paper. Note that each character
we want to output is essentially a node in the graph, and the graph is fully connected (can move from
any character to any other via cursor moves, changing color as needed). Some edges are free (moving right
while outputting character of same color). It is actually an asymmetric TSP because there are cases
where e.g. moving right is free and moving left is not, and moving down to SOL via \n costs 1 while moving
back up to the x pos could be several bytes. Can solve asymmetric TSP via conversion to symmetric.
Solving a TSPP is generally computationally infeasible, so approximation algorithms such as Hoogeveen's are used.
Hoogeveen run O(n^3) so it too may be too slow. Can reduce n by combining runs of same color - I haven't bothered
to prove it but I believe that this does not harm the optimality of the result. Note that this does not reduce
the worst case n - you can a case where there are no such runs. I believe that there are faster algorithms
that provide worse (or zero) optimality guarantees - e.g. Lin Kernighan or nearest neighbor. These might be geared
to solve TSP vs TSPP - though a solution to TSP is also a solution to TSPP, just with the cycle completed and 
no prescribed starting location. We would remove the cycle completing hop, and output a move to the chosen start
location as needed. The algorithms might also be adaptable to TSPP directly. 
If TSPP solvers can never be made fast enough, heuristics can likely be employed to good effect.
Solutions from a TSPP solver might be a good way to find such heuristics.

ANSI codes to save/restore cursor pos could open new vistas of global optimization since you can
restore x/y in only 3 bytes but they are seemingly not supported in Mac xterm so I don't use them.
"""
