def max_min(list, start, end):
    if start == end:
        return (list[start], list[start]) # 只有一个元素时，最大值和最小值相同，这么做也是为了应对数组长为奇数的情况
    elif end-start ==1:
        return (max(list[start], list[end]), min(list[start], list[end])) # 有两个元素时，最大值和最小值只需用蛮力法即可
    else: #有多个元素时，采用分治，max是各部分max的最大值，min是各部分min的最小值
        mid = (start+end)//2 
        (max_l, min_l) = max_min(list, start, mid) # 左子数组的最大值和最小值
        (max_r, min_r) = max_min(list, mid+1, end) # 右子数组的最大值和最小值
        return (max(max_l, max_r), min(min_l, min_r))
    # 时间复杂度 O(n)