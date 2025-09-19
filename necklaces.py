# Exploration of Arrighi's Necklaces [[https://arxiv.org/pdf/2306.07121]]
# See also: [[https://hal.science/hal-04911679v1/file/BackToReichenbach.pdf]]
import math
import numpy as np;

class DLPearl:
    def __init__( self, idx, w=64 ):
        self.n, self.p = None, None
        self.L, self.R = False, False
        self.idx       = idx
        self.width     = w

    
class Necklace:
    def __init__( self, n, w ):
        self.size, self.current_size, self.w   = n, n, w
        self.cursor = DLPearl( 0, w )
        cur         = self.cursor
        for i in range(n-1):
            pearl = DLPearl( i+1, w )
            cur.n = pearl
            pearl.p = cur
            cur = pearl
        pearl.n = self.cursor
        self.cursor.p = pearl


    def __repr__( self ):
        it  = iter( self )
        str = ""
        for pearl in it:
            str +=  f'{pearl.idx}: <{pearl.L}|{pearl.R}>' + '\n'
        return str + f'> {self.as_int()}'


    def __iter__( self ):
        self.iterate = None
        return self


    def __next__( self ):
        if None == self.iterate:
            self.iterate = self.cursor.n
            return self.cursor
        else:
            pearl = self.iterate
            if pearl != self.cursor:
                self.iterate = self.iterate.n
                return pearl
            else:
                raise StopIteration

        
    def as_int( self ):
        n = 0
        it = iter(self)
        for pearl in it:
            n = (n<<2) + (2 if pearl.L else 0) + (1 if pearl.R else 0)
        return n

# Creation and initial values
    
    def randomize( self, rng ):
        it = iter(self)
        for pearl in it:
            pearl.L = rng.random() >= 0.5
            pearl.R = rng.random() >= 0.5


    def from_int( self, n ):
        if n >= (1 <<  (1+2*self.size) ):
            return -1
        else:
            cur, q = self.cursor.p, 0
            for p in range( self.size ):
                m = n >>  q
                cur.R = (1 == m % 2)
                cur.L = (1 == (m >> 1) % 2)
                q += 2
                cur = cur.p

# Quantitative measures

    def m_entropy( self ):
        it, n_p = iter(self), 0
        for pearl in it:
            n_p += (1 if pearl.L else 0) + (1 if pearl.R else 0)
        return math.log2( math.comb( self.current_size << 1, n_p ) )
                
# Transition rules

    def tr_roll( self ):
        keep = self.cursor.L
        it   = iter(self)
        for pearl in it:
            pearl.L = pearl.n.L
        self.cursor.p.L = keep


    def tr_unroll( self ):
        keep = self.cursor.p.L
        curp = None
        while curp != self.cursor.p :
            if None == curp:
                curp = self.cursor.p
            curp.L = curp.p.L
            curp = curp.p
        self.cursor.L = keep
        

    def tr_reduce( self ):
        cur, curnext = None, None
        while self.cursor != cur:
            if None == cur:
                cur, curnext = self.cursor, self.cursor.n
            if (not cur.R) and cur.L and (not curnext.L) and curnext.R:
                pearl = DLPearl( f'({cur.idx} {curnext.idx})' )
                pearl.L, pearl.R = True, True
                pearl.width = cur.width + curnext.width
                pearl.p, pearl.n = cur.p, curnext.n
                cur.p.n = pearl
                curnext.n.p = pearl
                new_cur = curnext.n
                new_curnext = new_cur.n
                #
                if self.cursor == cur:
                    self.cursor = pearl
                else:
                    if self.cursor == curnext:
                        self.cursor = new_cur
                del cur
                del curnext
                self.current_size -= 1
                cur, curnext = new_cur, new_curnext
            else:
                cur = curnext
                curnext = curnext.n


    def tr_expand( self ):
        cur = None
        while self.cursor != cur:
            if None == cur:
                cur = self.cursor
            if cur.L and cur.R:
                left             = DLPearl( f'{cur.idx}L' )
                right            = DLPearl( f'{cur.idx}R' )
                left.width, right.width = cur.width >> 1, cur.width >> 1
                left.L, right.R  = True, True
                left.n, right.p  = right, left
                left.p, right.n  = cur.p, cur.n
                cur.p.n, cur.n.p = left, right
                #
                new_cur = cur.n
                if self.cursor == cur:
                    self.cursor = left
                del cur
                self.current_size += 1
                cur = new_cur
            else:
                cur = cur.n

                    
    def step( self, n=1 ):
        for i in range(n):
            self.tr_reduce()
            self.tr_expand()
            self.tr_roll()


    def unstep( self, n=1 ):
        for i in range(n):
            self.tr_unroll()
            self.tr_expand()
            self.tr_reduce()

# Some simple dataviz

def fileto_eplot( arr ):
    with open( "eplot.plt", "w") as f:
        f.write( "Format: bar-chart\nLayout: compact\nWidth: 300\nHeight: 200\n\nColor: green\n" )
        for x in arr:
            f.write( f'{x}\n' )
        
if __name__ == '__main__':
    # rng = np.random.default_rng()
    N   = 5
    nl = Necklace(N,64)
    nl.from_int(143)
    print( "INIT>", nl.as_int(), nl.current_size )
    nl.step()
    nl.step()
    print( "ROLL>", nl.as_int(), nl.current_size )
    nl.unstep()
    nl.unstep()
    print( "UNRO>", nl.as_int(), nl.current_size )
    #
    # hmax, harg = 0, 0
    # hsize = np.zeros( 2*N+1 )
    # for x in range( 1 << (2*N+1) ):
    #     nl  = Necklace(N, 64)
    #     nl.from_int(x)
    #     nl.step()
    #     y = nl.as_int()
    #     #
    #     if( y > hmax ):
    #         hmax, harg = y, x
    #     hsize[nl.current_size] += 1
    #     print( f'{x}, {y}, {nl.current_size}' )
    #     del nl
    # print( f'Max: x={harg}, y={hmax}' )
    # fileto_eplot( hsize )
    #
    
        
        
