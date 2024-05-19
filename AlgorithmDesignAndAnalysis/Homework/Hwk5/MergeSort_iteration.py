list=[]
# 一个Python风格的伪码
def MergeSort(list):
	for(length=2;length<=int(0.5*len(list));length*=2){ #每段的长度，从2增长到list长度的一半(向下取整)
		for(start=0;start+length<=len(list);start+=length){ #得到每段的起始点
			mid=int((start+length)/2)
			MergeList(list,start,mid-1,mid,start+length-1)
			}
		}
	return list