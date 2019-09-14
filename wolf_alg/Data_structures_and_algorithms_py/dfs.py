#coding=utf-8

def dfs(row):
    stack_list.append(row)
    print(stack_list)
    for clon in range(len(dl[row])):
        if dl[row][clon] > 0 and clon not in stack_list: #顶点是否已经在当前路径中
            dfs(clon)
            stack_list.pop()

visited_set = set()
def dfs(node):
    if not node:
        return
    visited_set.add(node)
    for i in node:
        if i not in visited_set:
            dfs(i)


void DFS(int root,Node* nodes){// 深度优先遍历
    stack<int> s;
    s.push(root);
    while(!s.empty()){
        int now = s.top();
        s.pop();
        printf("%d ",now); // 出栈访问
        vector<int> children = nodes[now].children;
        for(int i=children.size()-1;i>=0;--i){
            int post = children[i];
            s.push(post);
        }
    }
}

void BFS(int root,Node* nodes){// 广度优先遍历
    queue<int> s;
    s.push(root);
    printf("%d ",root); // 入队访问
    while(!s.empty()){
        int now = s.front();
        s.pop();
        vector<int> children = nodes[now].children;
        for(int i= 0;i<children.size();++i){
            int post = children[i];
            s.push(post);
            printf("%d ",post); // 入队访问
        }
    }
}


if __name__ == '__main__':
    dl = [
    [0, 1, 1, 0, 0, 0],
    [1, 0, 0, 1, 1, 0],
    [1, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0]]
    stack_list = list()
    dfs(0)
