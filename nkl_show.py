# Drawing evolutions of Arrighi's Necklaces
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle


import necklaces as nkl

def nkl_subplot( ax, nl, fig_width, fig_height, W, h, gens, fwd ):
    ax.set_xlim(0, fig_width)
    ax.set_ylim(fig_height, 0)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()
    ax.set_title( "Forward in time" if fwd else "Backward in time" )
    x, y = W, 0
    for generation in range( gens ):
        # Build current state as a line array
        arr = np.zeros( (nl.current_size,2), dtype=np.ushort )
        it, itx = iter(nl), 0
        for pearl in it:
            arr[ itx ] = [ (2 if pearl.L else 0) + (1 if pearl.R else 0), pearl.width ]
            itx += 1
        # Draw left header
        left, width    = W-2, W
        bottom, height = y+h, h
        right          = left + width
        top            = bottom + height
        val            = nl.as_int()
        ax.text( left, bottom, f'{val:e}' if val > (1 << 30) else f'{val}',
                 horizontalalignment='right',
                 verticalalignment='bottom' )
        # Draw line array
        x = W
        for i in range( len(arr) ):
            ax.add_patch( Rectangle( xy=(x, y), width=arr[i][1], height=h,
                                     facecolor=colors[ arr[i][0] ], edgecolor='0.7') )
            x += arr[i][1]
        # Draw left header
        left, width    = W+N*W+W, W
        bottom, height = y+h, h
        right          = left + width
        top            = bottom + height
        ax.text( left, bottom, ' {:.2f}'.format( nl.m_entropy() ),
                 horizontalalignment='right',
                 verticalalignment='bottom' )
        #
        y += h
        if fwd :
            nl.step()
        else:
            nl.unstep()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='nkl_show',
                    description='Displays the evolution of an Arrighi Necklace.',
                    epilog='See original article for details.')
    parser.add_argument('-i', '--init', type=int, default=143,
                        help='The int representation of the initial state (default: %(default)s.)') 
    parser.add_argument('-s', '--size', type=int, default=5,
                        help='The number of pearls (default: %(default)s.).') 
    parser.add_argument('-g', '--gens', type=int, default=25,
                        help='The number of steps to evolve (default: %(default)s.).') 
    parser.add_argument('-w', '--wide', type=int, default=64,
                        help='The initial width of pearls (default: %(default)s.).') 
    parser.add_argument('-r', '--reverse', action='store_true',
                        help='If present, evolves towards past.') 
    args = parser.parse_args()
    #
    N, W  = args.size, args.wide
    FRWRD = False if args.reverse else True
    # Set up display
    colors        = [ '#f0f0f0', '#e3c634', '#347ae3', '#32a852' ]
    h = 2
    fig_width, fig_height = W + N*W + W, args.gens * h
    fig, (ax1, ax2)       = plt.subplots( 1, 2 )
    nl = nkl.Necklace(N, W)
    nl.from_int( args.init )
    nkl_subplot( ax1, nl, fig_width, fig_height, W, h, args.gens, FRWRD )
    del nl
    nl = nkl.Necklace(N, W)
    nl.from_int( args.init )
    nkl_subplot( ax2, nl, fig_width, fig_height, W, h, args.gens, not FRWRD )
    #
    plt.show()
