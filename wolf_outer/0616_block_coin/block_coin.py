import hashlib
import datetime


class EncryBlock:
    def __init__(self, index, timestamp, data, next_hash):
        # 索引
        self.index = index
        # 时间
        self.timestamp = timestamp
        # 记录
        self.data = data
        # 下个哈希
        self.next_hash = next_hash
        # 自己哈希
        self.self_hash = self.hash_self()

    def hash_self(self):
        sha = hashlib.sha512()
        datastr = str(self.index) + str(self.timestamp) + str(self.data) + str(self.next_hash)
        sha.update(datastr.encode("utf-8"))
        return sha.hexdigest()


def create_first_block():
    return EncryBlock(0, datetime.datetime.now(), "Love", "0")


# 其他块
def create_money_block(last_block):
    this_index = last_block.index + 1  # 索引加1
    this_timestamp = datetime.datetime.now()  # 当前时间
    this_data = "Love" + str(this_index)  # 取得上一块的哈希
    this_hash = last_block.self_hash  # 取得上一块的哈希
    return EncryBlock(this_index, this_timestamp, this_data, this_hash)


# 列表只有一个创世模块
block_coins = [create_first_block()]
nums = 100
# 开始只有一个
head_block = block_coins[0]
print("start ",head_block.index, head_block.timestamp, head_block.self_hash, head_block.next_hash)
for i in range(nums):
    block_item = create_money_block(head_block)
    # 加入区块链
    block_coins.append(block_item)
    # 循环
    head_block = block_item
    print(block_item.index, block_item.timestamp, block_item.self_hash, block_item.next_hash)













