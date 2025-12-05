from _ast import While

from src.py20251205.student import Student
import re

from src.py20251205.student_manager import StudentManager


class StudentViewModel:
    """
    学生管理视图模型类。
    该类用于创建一个简单的学生管理系统，负责存储、更新、查询和删除学生信息。
    :ivar students: 存储学生信息的字典，其中键为学生的姓名，值为学生对象。
    :type students: dict
    """

    def __init__(self):
        """
        初始化方法，用于创建类实例。
        :raises ValueError: 如果初始化参数不符合要求。
        :raises TypeError: 如果参数类型不符合预期。
        """
        self.stu_mananger = StudentManager()

    def add(self):
        """
        将学生添加到某集合或结构中的方法。
        :param self: 当前类的实例。
        :return: 无返回值。
        """
        stu = Student()
        stu.name = input("请输入学生姓名:").strip()
        stu.no = input("请输入学号:").strip()
        stu.age = int(input("请输入学生年龄：").strip())
        stu.height = float(input("请输入学生身高(cm)：").strip())
        stu.phone = input("请输入学生手机号码:").strip()
        score_txt = input("请输入学生 语文,数学,英语,化学,物理 的成绩(逗号分隔):")
        score_arry = list(map(float, score_txt.split(",")))
        stu.scores = dict(zip(self.stu_mananger.subjects, score_arry))
        self.stu_mananger.add(stu)
        print(f"学生{stu.name}数据已添加")

    def delete(self):
        """
        删除学生信息。
        该方法通过用户输入获取需要删除的学生姓名，并调用学生管理系统的删除方法完成对学生信息的删除。
        """
        stu_name = input("请输入需要删除的学生姓名:").strip()
        is_del = bool(input(f"是否确认删除学生 {stu_name} ? (1-确认, 其他-取消)"))
        if is_del:
            self.stu_mananger.delete(stu_name)
            print(f"学生 {stu_name} 相关数据已删除.")

    def update(self):
        """
        更新学生信息。
        此方法允许用户输入学生姓名以及需要修改的信息名称和值，并将其更新到学生管理模块中。
        :raises ValueError: 当输入的信息值为空时可能引发。
        """
        stu_value_dict = {}
        stu_name = input("请输入需要修改的学生姓名:").strip()
        while True:
            pro_name = input("请输入需要修改的信息名称:").strip()
            if pro_name == "" or pro_name == "exit":
                break

            pro_value = input("请输入需要修改的信息值:").strip()
            stu_value_dict[pro_name] = pro_value

        if stu_value_dict :
            self.stu_mananger.update(stu_name,stu_value_dict)
            print(f"学生 {stu_name} 相关数据已更新\n{stu_value_dict}")


    def query(self):
        """
        根据用户输入的姓名查询对应的学生信息。
        :raises ValueError: 当输入的姓名为空字符串时可能引发错误。
        """
        stu_name = input("请输入需要查找的学生姓名:").strip()
        stu = self.stu_mananger.query(stu_name)
        print(stu)
