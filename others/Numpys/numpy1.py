import numpy as np

arry_a = np.array([1,2,3])
arry_b = np.array(arry_a,copy=True)
print(arry_b)

arry_c = np.array([[1,2,3,4],[6,7,8,9],[3,4,5,5]])
arry_d = np.array(arry_c,ndmin=3)
print(arry_d)

arry_empty = np.empty([2,3])
print(arry_empty)

arry_linspace = np.linspace(7000,10000,num=4)
print(arry_linspace)

arry_logspace = np.logspace(0, 63, num=64, base=2, dtype=np.uint64)
print(arry_logspace)

arry_rand = np.random.rand(2,3,2)
print(arry_rand)

arry_randn = np.random.randn(23)
print(arry_randn)

arry_randint = np.random.randint(1,100,size=(2,3))
print(f"arry_randint:{arry_randint}")

arry_normal = np.random.normal(0,10,size=(13))
print(f"arry_normal:{arry_normal}")

arry_buffer = np.frombuffer(b"Hello World",dtype=np.uint8)
print(f"arry_buffer:{arry_buffer}")

def func(x:int):
    for i in range(x):
        yield i**3

iter = func(50)
arry_fromiter = np.fromiter(iter,dtype=np.int32)
print(f"arry_fromiter:{arry_fromiter}")

arry_full_like = np.full_like(arry_fromiter,fill_value=100)
print(f"arry_full_like:{arry_full_like}")