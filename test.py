import numpy as np

all_enroll={
        "362":1,
        "364":2,
        "365":3,
        "367":4,
        "368":5,
        "369":6,
        "370":7,
        "371":8,
        "372":9,
        "373":10,
        "374":11,
        "375":12,
        "376":13,
        "377":14,
        "378":15,
        "379":16,
        "380":17,
        "381":18,
        "382":19,
        "383":20,
        "384":21,
        "385":22,
        "386":23,
        "387":24,
        "388":25,
        "389":26,
        "390":27,
        "394":28,
        "395":29,
        "398":30,
        "399":31,
        "400":32,
        "401":33,
        "403":34,
        "404":35,
        "406":36,
        "407":37,
        "408":38,
        "409":39,
        "410":40,
        "411":41,
        "412":42,
        "414":43,
        "415":44,
        "416":45,
        "417":46,
        "418":47,
        "419":48,
        "420":49,
        "421":50,
        "422":51,
        "423":52,
        "756":53,
        "757":54,
        "758":55}

inv_dict={v: k for k, v in all_enroll.items()}

def convert_to_no(last_3_digits,condition):# if condition is false inverse it
    if condition:
        return all_enroll[str(last_3_digits)]
    else:
        return inv_dict[last_3_digits]

def cons(arr): # worst case nlogn
    arr=sorted(arr,key=lambda x:x[0])
    i=0
    while i<len(arr)-1:
        if arr[i][0]+1==arr[i+1][0] and arr[i][1]!=arr[i+1][1]:
            # print("there is the breaking point",arr[i],arr[i+1])
            breakpoints.append([arr[i+1][0],arr[i+1][1]])
            return
        i+=1
    print("not enough data yet")

def makegrid1(start):
    arr=[0]*(6*10)
    arr[0]=start
    for i in range(2,len(arr)):
        if i%2!=0 or arr[i]>55:
            continue
        arr[i]=arr[i-2]+1
    for i in range(len(arr)):
        if arr[i]==0 or arr[i]>55:
            arr[i]=0
            continue
        arr[i]=convert_to_no(arr[i],False)
    return np.array(arr).reshape((6,10))

def makegrid2(start):
    arr=[0]*(6*10)
    arr[1]=start
    for i in range(2,len(arr)):
        if i%2==0 or arr[i]>55:
            continue
        arr[i]=arr[i-2]+1
    for i in range(len(arr)):
        if arr[i]==0 or arr[i]>55:
            arr[i]=0
            continue
        arr[i]=convert_to_no(arr[i],False)
    return np.array(arr).reshape((6,10))

array = np.loadtxt('path_of_file/data.csv', delimiter=',', dtype='int')

for i in range(len(array)):
    # print(array[i][0])
    array[i][0]=convert_to_no(array[i][0],True)

breakpoints=[]
cons(array)
if not breakpoints:
    print("not enough data")
if breakpoints[0][0]<25:
    breakpoints.append([breakpoints[0][0]+30,breakpoints[0][1]+1])
elif breakpoints[0][0]>30:
    breakpoints.append([breakpoints[0][0]-30,breakpoints[0][1]-1])

# print(array) # testing
# arr=[[375,211],[376,211],[374,210],[373,210]]
# print([i[0] for i in arr])

for start,clas in breakpoints:
    grid1=makegrid1(start)
    print(grid1,clas)
    grid2=makegrid2(start)
    print(grid2,clas)
cons(array)

