def bubble_sort(alist):
    for i in range(len(alist) - 1, 0, -1):
        print(i)
        isChange = False
        for j in range(i):
            if alist[j] > alist[j + 1]:
                isChange = True
                alist[j], alist[j + 1] = alist[j + 1], alist[j]
        if not isChange:
            break
    return alist

  
def quick_sort(alist, start, end):
    #quick_sort(a, 0, len(a) - 1)
    if start >= end:
        return
    mid = alist[start]
    low = start
    high = end
    while low < high:

        while low < high and alist[high] >= mid:
            high -= 1
        alist[low] = alist[high]
        while low < high and alist[low] < mid:
            low += 1
        alist[high] = alist[low]

    alist[low] = mid
    quick_sort(alist, start, low - 1)
    quick_sort(alist, low + 1, end)
    
    
class TreeNode(object):
    """
        原理：二叉搜索树是排序过的 ，位于左子树的结点都比父结点小，位
        于右子树的结点都比父结点大，我们只需从根节点开始和两个输入的结点进行
        比较，如果当前节点的值比两个结点的值都大，那么最低的公共祖先结点一定
        在该结点的左子树中，下一步开遍历当前结点的左子树。如果当前节点的值比
        两个结点的值都小，那么最低的公共祖先结点一定在该结点的右子树中，下一
        步开遍历当前结点的右子树。这样从上到下找到第一个在两个输入结点的值之
        间的结点。
    """

    def __init__(self, left=None, right=None, data=None):
        self.data = data
        self.left = left
        self.right = right

    def getCommonAncestor(self, root, node1, node2):
        while root:
            if root.data > node1.data and root.data > node2.data:
                root = root.left
            elif root.data < node1.data and root.data < node2.data:
                root = root.right
            else:
                return root

