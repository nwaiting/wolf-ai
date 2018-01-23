#coding=utf-8

"""
astar
"""

class Point(object):
    def __init__(self,x=None,y=None):
        self.x_ = x
        self.y_ = y

class Params(object):
    def __init__(self,start_x,start_y,end_x,end_y,t_height,t_weith,t_step):
        self.corner_ = None #允许拐角
        self.step_ = t_step
        self.height_ = t_height
        self.weith_ = t_weith
        self.start_point_ = Point(start_x, start_y)
        self.end_point_ = Point(end_x, end_y)

class Node(object):
    def __init__(self,x=None,y=None):
        self.point_ = Point(x,y)
        self.actual_ = None
        self.estimate_ = None
        self.father_ = None

"""
enum Direct    // 8 方向
{
    Up,
    Right_Up,
    Right,
    Right_Down,
    Down,
    Left_Down,
    Left,
    Left_Up
};
"""
trans_states_max = 8
trans_points = [[-1,-1],
            [-1,0],
            [-1,1],
            [0,-1],
            [0,1],
            [1,-1],
            [1,0],
            [1,1]]
slant_value = 1.4
strait_value = 1

#预估值计算  H 表示从指定的方格移动到终点方格的预计耗费 (H启发函数)
def calc_estimate(curr_p, end_p):
    x = abs(curr_p.x_ - end_p.x_)
    y = abs(curr_p.y_ - end_p.y_)
    return x + y
    """
    网上有一种参考方法 
    return min(x,y) * strait_value + (max(x,y)-min(x,y)) * slant_value
    """

#曼哈顿距离 G 表示从起点方格移动到网格上指定方格的移动耗费 (可沿斜方向移动)
def calc_actual(t_i):
    if t_i % 2 == 0:
        return strait_value
    return slant_value

class Astar(object):
    def __init__(self,start_x,start_y,end_x,end_y,t_height,t_weith,t_step):
        self.params_ = Params(start_x,start_y,end_x,end_y,t_height,t_weith,t_step)
        self.opens_ = list()
        self.closes_ = list()

    def find_best_node(self):
        best_node = self.opens_[0]
        tmp_index = 0
        for i in xrange(1,len(self.opens_)):
            item = self.opens_[i]
            if item.actual_ + item.estimate_ < best_node.actual_ + best_node.estimate_:
                best_node = item
                tmp_index = i
        self.closes_.append(best_node)
        self.opens_.pop(tmp_index)
        return best_node

    #检测碰撞或者是否在close列表里
    def check_point(self, t_point):
        if t_point.x_ < 0 or t_point.x_ >= self.params_.weith_ or t_point.y_ < 0 or t_point.y_ >= self.params_.height_ or data[t_point.x_][t_point.y_] <= 0:
            return False
        for tmp_item in self.closes_:
            if tmp_item.point_.x_ == t_point.x_ and tmp_item.point_.y_ == t_point.y_:
                return False
        return True

    def find(self):
        node = Node(self.params_.start_point_.x_, self.params_.start_point_.y_)
        node.actual_ = 0
        node.estimate_ = calc_estimate(self.params_.start_point_, self.params_.end_point_)
        self.opens_.append(node)

        while len(self.opens_) > 0:
            best_node = self.find_best_node()
            print 'x,y:',best_node.point_.x_,best_node.point_.y_,best_node.actual_+best_node.estimate_
            if abs(best_node.point_.x_ + self.params_.step_) >= self.params_.end_point_.x_ and abs(best_node.point_.y_ + self.params_.step_) >= self.params_.end_point_.y_:
                #成功找到
                print "find it"
                self.opens_ = list()
                return
            #开始遍历
            for i in xrange(trans_states_max):
                p = Point(best_node.point_.x_ + trans_points[i][0] * self.params_.step_, best_node.point_.y_ + trans_points[i][1] * self.params_.step_)
                if not self.check_point(p):
                    continue
                #更新open list 数据
                tmp_actual = best_node.actual_ + calc_actual(i)
                inlist_flag = False
                for item in self.opens_:
                    if item.point_.x_ == p.x_ and item.point_.y_ == p.y_:
                        if item.actual_ > tmp_actual:
                            item.actual_ = tmp_actual
                            item.father_ = best_node
                        inlist_flag = True
                        break

                if not inlist_flag:
                    t_n = Node(p.x_, p.y_)
                    #print "add:",p.x_,p.y_
                    t_n.actual_ = tmp_actual
                    t_n.estimate_ = calc_estimate(t_n.point_, self.params_.end_point_)
                    t_n.father_ = best_node
                    self.opens_.append(t_n)


if __name__ == '__main__':
    data = [[0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [1, 1, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 1, 0]]
    astar = Astar(0,0,9,9,10,10,1)
    astar.find()
