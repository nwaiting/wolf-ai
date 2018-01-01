#coding=utf-8

from tkinter import *

def main(paperfile, teacherfile):
    paper_index = list()
    teacher_index = dict()
    with open(paperfile, 'rb') as fd:
        for line in fd.readlines():
            if line:
                paper_index.append(line.strip().decode())

    with open(teacherfile, 'rb') as fd:
        for line in fd.readlines():
            if line:
                line = line.strip()
                find_index = line.decode().find(':')
                if find_index != -1:
                    res = line.decode().split(':')
                    if len(res) == 2:
                        teacher_index[res[0].strip()] = {res[1].strip():list()}

    for item in paper_index:
        res = sorted(teacher_index.items(), key=lambda x:len(list(x[1].values())[0]), reverse=False)
        for i in range(len(teacher_index)):
            if res[i][0][:5] == item[:5]:
                continue
            print(res[i][0][:5],item[:5])
            flag = False
            for itemi,itemj in res[i][1].items():
                if len(itemj) > 0:
                    tmp_list = itemj[:]
                    tmp_list.append(item)
                    teacher_index[res[i][0]] = {itemi:tmp_list}
                else:
                    teacher_index[res[i][0]] = {itemi:[item]}
                flag = True
            if flag:
                break

        print(teacher_index)

    root = Tk()
    root.title('研究生论文评阅')
    list_one = Listbox(root, height=20, width=30)
    list_two = Listbox(root, height=20, width=30)
    list_one.grid(row=1,column=1,padx=(10,5),pady=10)
    list_two.grid(row=1,column=2,padx=(5,10),pady=10)

    for i,j in teacher_index.items():
        first_list = i + '--'
        second_list = ''
        for m,n in j.items():
            first_list += m
            second_list += m + ':'
            list_two.insert(END, second_list)
            for nn in n:
                list_two.insert(END, nn)
        list_one.insert(END, first_list)

    root.mainloop()

if __name__ == '__main__':
    paper_path = 'outer/home_work_lunwen/paper.txt'
    teacher_path = 'outer/home_work_lunwen/teacher.txt'
    main(paper_path, teacher_path)
