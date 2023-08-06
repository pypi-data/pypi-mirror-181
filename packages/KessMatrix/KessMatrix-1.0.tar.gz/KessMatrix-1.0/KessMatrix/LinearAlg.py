import math
import numpy as np
import random as ran
import time


#class LinAlgebra:

    #def __init__():




def time_dec(func):
    ''' prints time it takes for a function to run
    Args: 
    function

    Returns:
    result: time it takes for a function to run
    
    '''
    def getTime(*args, **kwargs):
        start_time = time.time()  
        result  = func(*args,  **kwargs)
        
        timer = time.time() - start_time
        if timer > .10:

            print(func.__name__)
            print(timer)
        
        return result
    return getTime


def MatrixMult(mat1, mat2):
    '''multiplies to matrices
    Args:
    mat1:matrix to be multiplied
    mat2:matrix to be multiplied

    Return:
    prodMat: result of matrix multiplication

    '''
    prodMat = np.empty((mat2.shape[1], mat1.shape[0]))
    if mat1.shape[1] == mat2.shape[0]: # or mat1.shape[1] == mat2.shape[0]:

            for x in range(mat1.shape[0]):
                
                for i in range(mat2.shape[1]):
                    sum = 0
                    for j in range(mat1.shape[1]):
                        
                        sum +=  mat1[x][j] * mat2[j][i]
                    #print(sum)
                    prodMat[i][x] = int(sum)
            #print(prodMat)
            return prodMat

    else:
        print("matrices do not match")

import numpy as np

mata = np.array([[2,3,4], [3,5,2], [2,3,4]])
matb = np.array([[2,8,4], [3,5,9], [7,3,4]])    

testM = MatrixMult(mata, matb)

#print(testM)

#print(np.matmul(mata,matb))

def makeMatrix(dim1, dim2):
    ''' creates matrix of random integers
    Args;
    dim1: numbers of columns in the matrix
    dim2: number of rows in the matrix

    Returns:
    matrix of random ints
    '''
    matrix = np.empty((dim1, dim2))
    for i in range(dim1):
        for j in range(dim2):
            matrix[i][j] = ran.randint(-9, 9)
    
    return matrix


mat1 = makeMatrix(6, 6)

mat2 = makeMatrix(2, 2)

mat2 = makeMatrix(3, 8)

print("mat2 shape")
print(mat2.shape)
print(mat2)
print(mat2[1][3])

#print( MatrixMult(mat1, mat2))
#print( np.matmul(mat1, mat2))
#sums matrices



def matrixAdd(mat1, mat2):
    '''perform matrix additon
    Args:
    mat1: matrix to be added
    mat2: matrix to be added

    Return:
    sumMat: reulting matrix of addition 
    
    '''
    sumMat = np.zeros((mat1.shape[0], mat2.shape[1]))
    if mat1.shape[1] == mat2.shape[1] and  mat1.shape[0] == mat2.shape[0]:
        for i in range(mat1.shape[0]):
            for j in range(mat1.shape[1]):
                sum = mat1[i][j] +  mat2[i][j]
                
                sumMat[i][j]  = sum

        return sumMat

#subtaracts matrix
def matrixSub(mat1, mat2):
    '''subtracts two matrices

    Args:
    mat1: Matrix to be subtracted from
    mat2: Matrix to subtract

    Returns:
    subMatrix: result of subtraction

    '''
    subMat = np.zeros((mat1.shape[0],mat2.shape[1]))
    if mat1.shape[1] == mat2.shape[1]  and  mat1.shape[0] == mat2.shape[0]:
        for i in range(mat1.shape[0]):
            for j in range(mat1.shape[1]):
                diff = mat1[i][j] -  mat2[i][j]
                
                subMat[i][j]  = diff 

        return subMat


#sumM = matrixAdd(mat1, mat2)



          

#print(sumM)
#print(np.add(mat1, mat2))


#invM =  getTranspose(mat1)
# returns matrix with row removed
def chopRow(row, mat):
    '''removes a row from a matrix

    Args:
    row: row index to be removed
    mat: matrix to remove row from
      
    '''
    mata = mat[:row , :]
    matb = mat[row+1: , :]
    minor  = np.concatenate((mata, matb), axis = 0)
    return minor

# returns matrix with column removed
def chopCol(col, mat):
    '''removes column from matrix

    Args:
    col: column index to be removed
    mat: matrix to remove column from
    '''
    mata = mat[: , :col]
    matb = mat[: ,col+1:]

    minor  = np.concatenate((mata, matb), axis = 1)
    return minor

print(mat1)

tmat = chopRow(3, mat1)
print(tmat)
minor = chopCol(1, tmat)

print(minor)

# returns minor matrix
@time_dec
def getMinor(row, col, mat):
    '''get minor matrix from original matrix

    Args:
    row: row to be removed from matrix
    col: column to be removed from matrix

    Returns:
    minor: minor matrix of the original matrix 
    
    '''
    tmat = chopRow(row, mat)
        
    minor = chopCol(col, tmat)
    return minor


class subMatrix:
    ''' subMatrix class for calculating inverse of a matrix

    Attributes:
        mat: matrix
        coef: coef to mutiply matrix 
    
    
    '''
    def __init__(self, coef, mat):
        self.coef = coef
        self.mat = mat

    def getMinorList(self):
        '''gives initial list of minors for every element of the matrix
        Args: 
        self: self subMatrix object

        Returns: 
        List of minor matrices, one for each element of the array
        
        
        '''
        subMatList = []
        size = self.mat.shape[0]
        mat = self.mat
        if size > 2:
            for x in range(size):
                Ncoef = mat[0][x]
                
                if x%2 ==0:
                    sign = 1
                else:
                    sign = -1
                NewMat = getMinor(0, x, mat)
                     
                newSub = subMatrix(sign *self.coef*Ncoef, NewMat)
                subMatList.append(newSub)
            
            return subMatList
        else:
            subList = []
            #print(self.mat)
            subList.append(self)
            return subList

    @time_dec
    def getTranspose(self):
        '''calculates transpose of a matrix

        Args: 
        self: self subMatrix object

        Return:
        adjMat: Transposed Matrix
        
        '''
        mat = self.mat
        tranMat = np.zeros((mat.shape[1], mat.shape[0]))
        for i in range(mat.shape[0]):
                for j in range(mat.shape[1]):
                    tranMat[j][i] = mat[i][j]
        return tranMat

    @time_dec
    def getDeterminate(self):
        '''Calculates the determinate of a matrix

        Args:
        self: self subMatrix class object
        
        Returns
        determinate of a matrix'''

        #print("determinate twos for two")
        #print(subMat.mat)
        matList = self.getMinorList()
    
        twoList = getListOfTwos(matList)
        deter = calcDeterminantFromTwos(twoList)

        return deter

    @time_dec
    def getCofactor(self):
        '''returns the cofactor for a matrix
        Args:
        self: self subMatrix object

        Returns:
        cofMat: Cofactor Matrix

        '''
        mat = self.mat
        print(mat.shape)
        cofMat = np.zeros((mat.shape[1],mat.shape[0]))
        #if mat.shape[0] > 2:
        for row  in range(mat.shape[0]):
                for col in range(mat.shape[0]):
                            submat = getMinor(row, col, mat)
                            
                            subMat = subMatrix(1, np.array(submat))                           
                            if subMat.mat.shape[0] > 1:
                                total  = subMat.getDeterminate()
                            else:
                                total = subMat.mat[0]
                            
                            total = total * (-1)**(row+col+2)
                            cofMat[row][col] = total
                
        return cofMat

    def getInverse(self):
        ''' calculates the inverse of a matrix
        
        Args:
        self: self subMatrix object

        Returns:
        inverse matrix of hte input matrix
        '''
        if self.mat.shape[0] == self.mat.shape[1]:
            cof = self.getCofactor()
            deter = self.getDeterminate()
            cofSumMat = subMatrix(1.0, cof)
            Tcof = cofSumMat.getTranspose()
            inverse = Tcof/deter

            return inverse
        else: 
            print("this is not a square matrix")




     
 

testSub = subMatrix(1, mat1)
newList = testSub.getMinorList()

'''@time_dec
def getDeterminate(subMat):
    Calculates the determinate of a matrix

    Args:
    SubMatrix class object
    
    Returns
    determinate of a matrix

    #print("determinate twos for two")
    #print(subMat.mat)
    matList = subMat.getMinorList()
  
    twoList = getListOfTwos(matList)
    deter = calcDeterminantFromTwos(twoList)
    return deter'''

@time_dec
def getListOfTwos(matList): 
    '''get a list of 2x2 matrices for calculatiing the original matrix determinant

    Args:
    list of subMatrix class objects

    Returns:
    a list of 2x2 subMatrices for the purpose of calculating the determinant
    
    ''' 
    if matList[0].mat.shape[0] >2:
        while(matList[0].mat.shape[0]>2):
            newList = []
            for mat in matList:
                #print("here's matt")
                #print(mat)
                mats = mat.getMinorList()
                #print("two mats")
                #print(mats)
                for item in mats:

                    newList.append(item)
                #print(newList)
            matList = newList
        return matList
    else:
        #print(matList[0].mat)
        #print("list of twos for 2")
        #print(matList[0].mat)
        return matList

twoList = getListOfTwos(newList)



i = 0
#for mat in twoList:
 
    #i += 1

@time_dec
def calcDeterminantFromTwos(matList):

    """calculates the determinate from a list of 2x2 sub matrices

    Args:
    List of 2x2 subMatrices

    Return:
    total float which is the calculated determinant """

    total= 0
    for mat in matList:
       
        total += mat.coef*(mat.mat[0][0] * mat.mat[1][1] - mat.mat[0][1] * mat.mat[1][0])

    return total

determin =  calcDeterminantFromTwos(twoList)




#print(determin)

subMat1 = subMatrix(1.0, mat1)
cofMat = subMat1.getCofactor()
matAdj = np.matrix(mat1)


#print(matAdj.getH())

subMat2 = subMatrix(1.0, cofMat)
adjMat = subMat2.getTranspose()
npCofactor = np.linalg.inv(mat1).T * np.linalg.det(mat1)
#print(mat1)
'''print(npCofactor)

print(cofMat)
#print(adjMat)'''
inverse = subMat1.getInverse()
#print(adjMat/determin)
print(inverse)
print(np.linalg.inv(mat1))

#adjM = getAdjoint(cofMat)
#print(getDeterminate(testSub))

#print(np.linalg.det(mat1))
