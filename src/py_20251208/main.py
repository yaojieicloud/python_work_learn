import sys

import student

from src.py_20251208.student_vm import StudentViewModel

stu_vm = StudentViewModel()

while True:
    try:
        cmd = int(input("请输入命令(1-录入,2-查询,3-修改,4-删除):").strip())
        match cmd:
            case 1:
                stu_vm.add()
            case 2:
                stu_vm.query()
            case 3:
                stu_vm.update()
            case 4:
                stu_vm.delete()
            case __:
                continue
    except Exception as e:
        print(e, file=sys.stderr)
    finally:
        print("-----------------------------------------------------------")
