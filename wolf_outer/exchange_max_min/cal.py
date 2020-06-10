

total_num = 0
all_nums = None
i = 1
while True:
    s1 = input()
    if i == 1:
        if not s1.isdigit():
            print("请重新输入！")
            continue
        total_num = int(s1)
    if i == 2:
        s1_items = s1.split()
        all_nums = [int(item) for item in s1_items]
        break
    i += 1

min_index = 0
min_val = all_nums[0]
max_index = len(all_nums) - 1
max_val = all_nums[max_index]
for i in range(len(all_nums)):
    if all_nums[i] < min_val:
        min_val = all_nums[i]
        min_index = i
    if all_nums[i] > max_val:
        max_val = all_nums[i]
        max_index = i

if max_index != len(all_nums) - 1:
    all_nums[max_index], all_nums[len(all_nums) - 1] = all_nums[len(all_nums) - 1], all_nums[max_index]
if min_index != 0:
    all_nums[min_index],all_nums[0] = all_nums[0],all_nums[min_index]
print(' '.join(["{}".format(item) for item in all_nums]))
