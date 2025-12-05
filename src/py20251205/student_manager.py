from src.py20251205.student import Student
import re


class StudentManager:
    """
    用于管理学生的类。
    该类主要负责添加、删除、更新和查询学生信息。使用此类可以有效地组织和管理学生数据。
    :ivar students: 存储学生信息的字典，其中键为学生ID，值为学生对象。
    :type students: dict
    """

    def __init__(self):
        """
        班级管理系统的初始化。
        该类用于创建一个简单的学生管理系统，负责存储学生信息。
        :param self: 初始化类实例
        :return: 无返回值
        """
        self.students = {}
        self.subjects = ["语文", "数学", "英语", "化学", "物理"]
        pass

    def add(self, student: Student):
        """
        将学生添加到某集合或结构中的方法。
        :param self: 当前类的实例。
        :param student: 每次添加的学生对象。
        :type student: Student
        :return: 无返回值。
        """
        stu_no_patten = r'^202\d{3}$'  # 学号正则表达式
        stu_phone_patten = r'^1[3-9]\d{9}$'  # 手机号正则表达式
        if re.match(stu_no_patten, student.no) is None:
            raise ValueError(f"学生{student.name}的学号 {student.no} 格式错误.")

        if re.match(stu_phone_patten, student.phone) is None:
            raise ValueError(f"学生{student.name}的学号 {student.no} 格式错误.")

        if student.no in [stu.no for stu in self.students.values()]:
            raise Exception(f"学生{student.name}的学号 {student.no}已存在.")

        self.students[student.name] = student

    def delete(self, name: str):
        """
        删除指定名称的学生信息。
        在学生记录中查找与指定名称匹配的学生信息。如果找到，将其从记录中删除。
        如果未找到，将抛出异常。
        :param self: 当前实例的引用。
        :param name: 要删除的学生名称。
        :type name: str
        :return: None
        :raises Exception: 当学生记录中未找到指定名称时抛出。
        """
        if name in self.students:
            del self.students[name]
        else:
            raise Exception(f"未找到名为 {name} 的学生信息.")

    def update(self, name: str, values: dict):
        """
        更新指定学生的信息。
        本方法用于根据提供的字典更新指定学生的属性。当学生名称不存在时抛出异常。
        更新过程中将覆盖提供属性名对应的现有属性值。
        :param name: 指定更新的学生名称
        :type name: str
        :param values: 包含要更新的属性及新值的字典
        :type values: dict
        :raises Exception: 当指定的学生名称不存在于系统中时抛出异常
        """
        if not name in self.students:
            raise Exception(f"未找到名为 {name} 的学生信息.")

        stu = self.students[name]
        for key, value in values.items():
            setattr(stu, key, value)

    def query(self, name: str):
        """
        查询指定名称的学生信息。
        通过学生的姓名在现有数据中查找相关信息并返回。
        :param name: 学生的姓名，用于查询
        :type name: str
        :return: 若学生存在，返回对应的学生信息；否则返回 None
        :rtype: Any
        """
        query_stu = self.students.get(name)
        return query_stu
