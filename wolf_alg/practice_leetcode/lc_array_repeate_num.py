#coding=utf-8

"""

"""

def removeDuplicates(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    """
    if len(nums) <= 0:
        return 0
    j = 0
    for i in range(len(nums)):
        if nums[i] != nums[j]:
            nums[j] = nums[i]
            j += 1
    return j+1
    """

    if len(nums) <= 1:
        return nums
    j = 1
    for i in range(1,len(nums)):
        if nums[i] != nums[i-1]:
            nums[j] = nums[i]
            j += 1
    return nums[:j]


if __name__ == '__main__':
    print(removeDuplicates([1,2,2,2,2,3,4,6,7,9]))
