"""
Copyright 2022  Salvatore Barone <salvatore.barone@unina.it>
                Filippo Ferrandino <fi.ferrandino@studenti.unina.it>

This is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation; either version 3 of the License, or any later version.

This is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
RMEncoder; if not, write to the Free Software Foundation, Inc., 51 Franklin
Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""
from numba import cuda, int32, int8

@cuda.jit
def max_example_3d(result, values):
    """
    Find the maximum value in values and store in result[0].
    Both result and values are 3d arrays.
    """
    i, j, k = cuda.grid(3)
    # Atomically store to result[0,1,2] from values[i, j, k]
    cuda.atomic.max(result, (0, 1, 2), values[i, j, k])

 
TPB=16 #TODO:calcolare il tpb dinamicamente   
@cuda.jit
def pool(R, inputv, stride, pool_size):#, pooling):
    x, y = cuda.grid(2)
    if x < R.shape[0] and y < R.shape[1]:
        h_start = x * stride[0]
        h_end = h_start + pool_size[0]
        w_start = y * stride[1]
        w_end = w_start + pool_size[1]
        temp_max = cuda.local.array(shape=(TPB), dtype=int32)
        for i in range(h_start,h_end):
            for j in range(w_start,w_end,):
                for k in range(R.shape[2]):
                    if(inputv[i,j,k]>temp_max[k]):
                        temp_max[k]=inputv[i,j,k]
        for k in range(R.shape[2]):
            R[x, y, k]=temp_max[k]

@cuda.jit
def matmul(R, A, B, bias, M, offset1, offset2, activation, quant_nbits):
    """
    Perform matrix di multiplication of C = A * B
    """
    result_max = cuda.shared.array(shape=(8,8), dtype=int32)
    row, col = cuda.grid(2)
    if row < R.shape[0] and col < R.shape[1]:
        tmp = bias[row] #TODO: rendere bias[row,col]
        for k in range(A.shape[1]):
            #tmp +=  M[int8(A[row, k])+offset1 , int(B[k, col])+offset2]
            tmp += A[row, k]*B[k, col]
        #activation rele
        if activation and tmp < 0:
            tmp = 0
        R[row, col] = tmp
    cuda.syncthreads()
    cuda.atomic.max(result_max, (0, 1), R[row, col])
    cuda.syncthreads()
    total_max = result_max[0,0]
    R[row, col] = int8(round(( R[row, col]/total_max)*(2**quant_nbits-1)))
        
@cuda.jit
def convolve(result, a, b, bias, n_channels, M, offset1, offset2, quant_nbits):
    x, y = cuda.grid(2) 
    max_x=a.shape[0]-b.shape[0]+1
    max_y=a.shape[1]-b.shape[1]+1   
    #if the thread coordinates are outside of the image, we ignore the thread:
    if ((x >= max_x)  or (y >= max_y)): 
        return
    #area per fare la max della quantizazione
    #TODO: capire come calcolare lo shape 
    result_max = cuda.shared.array(shape=(4,4,4), dtype=int32)
    #todo: ripassare vettorializazione dati in memoria e assicurarsi che thread dello stesso gruppo usino dati vicini
    for p in range(n_channels):   
        s=bias[p]
        for k in range(a.shape[2]):
            #calcolo cella convoluzione
            #todo: aggiungere lo step
            for i in range(b.shape[0]):
                for j in range(b.shape[1]):
                    s += a[i+x,j+y,k]*b[i,j,k,p]
                    #s += M[int8(a[i+x,j+y,k])+offset1 , int8(b[i,j,k,p])+offset2]
        #TODO supportare altre attivazioni (e.g., softmax, tanh)
        if s < 0:
            s=0
        result[x,y,p] = s
    i, j, k = cuda.grid(3)
    cuda.syncthreads()
    cuda.atomic.max(result_max, (0, 1, 2), result[i, j, k])
    cuda.syncthreads()
    total_max=result_max[0,0,0]
    for p in range(n_channels): 
         result[x,y,p] = int8(round(( result[x,y,p]/total_max)*(2**quant_nbits-1)))
        