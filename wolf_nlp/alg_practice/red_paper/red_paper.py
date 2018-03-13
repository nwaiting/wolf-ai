#coding=utf-8

import random

def red_paper(coins, people):
    if coins < people or coins <= 0 or people <= 0:
        print("data error")
        return
    if coins == people:
        return [1 for i in range(people)]

    first_gain = [1 for i in range(people)]
    coins = coins - people
    last_coins = coins
    rand_list = [random.randint(10,100) for _ in range(people)]
    rand_sum = sum(rand_list)
    print(rand_list, rand_sum)
    for i in range(people):
        tmp_gain = int(float(rand_list[i] / rand_sum) * coins)
        first_gain[i] = first_gain[i] + tmp_gain
        last_coins -= tmp_gain
    if last_coins > 0:
        first_gain[0] += last_coins
    print(first_gain)
    random.shuffle(first_gain)
    return first_gain


if __name__ == '__main__':
    result_list = red_paper(100, 5)
    print(result_list, sum(result_list))
