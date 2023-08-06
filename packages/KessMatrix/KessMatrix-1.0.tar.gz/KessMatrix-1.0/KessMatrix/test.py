import numpy as np
from LinearAlg import *


mat1 = makeMatrix(4, 4)

mat2 = makeMatrix(4, 4)

mat3= makeMatrix(6, 6)
def testMult4():
    mat1 = makeMatrix(4, 4)
    mat2 = makeMatrix(4, 4)
    
    lin  = MatrixMult(mat1, mat2)
    npmult = np.matmul(mat1, mat2)
    if not lin.all() == npmult.all():
        print("calc")
        print(lin)
        print("np")
        print(npmult)
    assert(lin.all() == npmult.all())


def testMult10():
    mat1 = makeMatrix(5, 5)
    mat2 = makeMatrix(5, 5)
    lin  = MatrixMult(mat1, mat2)
    npmult = np.matmul(mat1, mat2)
    if not lin.all() == npmult.all():
        print("calc")
        print(lin)
        print("np")
        print(npmult)
    assert(lin.all() == npmult.all())

def testMult105():
    mat1 = makeMatrix(4, 3)
    mat2 = makeMatrix(3, 4)
    lin  = MatrixMult(mat1, mat2)
    npmult = np.matmul(mat1, mat2)
    
    if not lin.all() == npmult.all():
        print("calc")
        print(lin)
        print("np")
        print(npmult)
    assert(lin.all() == npmult.all())

def testMult34():
    mat1 = makeMatrix(5, 3)
    mat2 = makeMatrix(3, 7)
    lin  = MatrixMult(mat1,mat2 )
    npmult = np.matmul(mat1, mat2)
    if not lin.all() == npmult.all():
        print("calc")
        print(lin)
        print("np")
        print(npmult)
    assert(lin.all() == npmult.all())

def testMult79():
    mat1 = makeMatrix(9, 7)
    mat2 = makeMatrix(7, 6)
    lin  = MatrixMult(mat1,mat2 )
    npmult = np.matmul(mat1, mat2)
    if not lin.all() == npmult.all():
        print("calc")
        print(lin)
        print("np")
        print(npmult)
    assert(lin.all() == npmult.all())
    

def testAdd73():
    mat1 = makeMatrix(7, 3)
    mat2 = makeMatrix(7, 3)
    lin  = matrixAdd(mat1,mat2 )
    npadd = np.add(mat1, mat2)

    assert(lin.all() == npadd.all())

def testAdd54():
    mat1 = makeMatrix(5, 4)
    mat2 = makeMatrix(5, 4)
    lin  = matrixAdd(mat1,mat2 )
    npadd = np.add(mat1, mat2)
    assert(lin.all() == npadd.all())


def testSub38():
    mat1 = makeMatrix(3, 8)
    mat2 = makeMatrix(3, 8)
    lin  = matrixSub(mat2,mat1 )
    npsub = np.subtract(mat2, mat1)
    assert(lin.all() == npsub.all())



def testSub54():
    mat1 = makeMatrix(5, 4)
    mat2 = makeMatrix(5, 4)
    lin  = matrixSub(mat2,mat1 )
    npsub = np.subtract(mat2, mat1)
    assert(lin.all() == npsub.all())


def testDeterminant5():
    mat1 = makeMatrix(5, 5)
    subm = subMatrix(1.0, mat1)
    det1 = subm.getDeterminate()
    npdet = np.linalg.det(mat1)
    print(np.linalg.det(mat1))

    assert(round(det1) == round(npdet))


def testDeterminant8():
    mat1 = makeMatrix(8, 8)
    subm = subMatrix(1.0, mat1)
    det1 = subm.getDeterminate()
    npdet = np.linalg.det(mat1)
    print(np.linalg.det(mat1))

    assert(round(det1) == round(npdet))

def testCofactor7():
    mat1 = makeMatrix(7, 7)
    subm = subMatrix(1.0, mat1)
    print(mat1.shape)
    cofMat = subm.getCofactor()
    npCofactor = np.linalg.inv(mat1).T * np.linalg.det(mat1)
    assert(cofMat.all() == npCofactor.all())

def testCofactor3():
    mat1 = makeMatrix(3, 3)
    subm = subMatrix(1.0, mat1)
    print(mat1.shape)
    cofMat =  subm.getCofactor()
    npCofactor = np.linalg.inv(mat1).T * np.linalg.det(mat1)
    assert(cofMat.all() == npCofactor.all())

def testTranspose7():
    mat1 = makeMatrix(7, 7)
    subm = subMatrix(1.0, mat1)
    trans1 = subm.getTranspose()
    nptran = mat1.transpose()
    assert(trans1.all() == nptran.all())


def testTranspose3():
    mat1 = makeMatrix(3, 3)
    subm = subMatrix(1.0, mat1)
    trans1 = subm.getTranspose()
    nptran = mat1.transpose()
    assert(trans1.all() == nptran.all())


def testInverse3():
    mat1 = makeMatrix(3, 3)
    subm = subMatrix(1.0, mat1)
    inv1 = subm.getInverse()
    npinv =  np.linalg.inv(mat1)
    assert(inv1.all() == npinv.all())



def testInverse7():
    mat1 = makeMatrix(7, 7)
    subm = subMatrix(1.0, mat1)
    inv1 = subm.getInverse()
    npinv =  np.linalg.inv(mat1)
    assert(inv1.all() == npinv.all())


def testInverse5():
    mat1 = makeMatrix(5, 5)
    subm = subMatrix(1.0, mat1)
    inv1 = subm.getInverse()
    npinv =  np.linalg.inv(mat1)
    assert(inv1.all() == npinv.all())


def testInverse8():
    mat1 = makeMatrix(8, 8)
    subm = subMatrix(1.0, mat1)
    inv1 = subm.getInverse()
    npinv =  np.linalg.inv(mat1)
    assert(inv1.all() == npinv.all())

def testInverse2():
    mat1 = makeMatrix(2, 2)
    subm = subMatrix(1.0, mat1)
    inv1 = subm.getInverse()
    npinv =  np.linalg.inv(mat1)
    assert(inv1.all() == npinv.all())

