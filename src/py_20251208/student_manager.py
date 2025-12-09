import os
import re
import sqlite3
import sys
import time

from dbutils.pooled_db import PooledDB

from src.py_20251208.student import Student, Score


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
        self.db_file = os.path.abspath("data/student.db")
        if not os.path.exists("data/"):
            os.mkdir("data/")

        self.pool = PooledDB(
            creator=sqlite3,  # 使用 sqlite3 模块
            maxconnections=5,  # 最大连接数
            maxusage=10,  # 每个🔗最多使用次数
            database=self.db_file  # SQLite 数据库文件路径
        )

        self.__create_table()

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
        sid = int(round(time.time() * 1000000))  # 取微妙作为ID
        if re.match(stu_no_patten, student.no) is None:
            raise ValueError(f"学生{student.name}的学号 {student.no} 格式错误.")

        if re.match(stu_phone_patten, student.phone) is None:
            raise ValueError(f"学生{student.name}的学号 {student.no} 格式错误.")

        exists = self.query_student_exists(student.name)
        if exists:
            raise Exception(f"已存在名为 {student.name} 的学生信息.")

        exists = self.query_student_exists(no=student.no)
        if exists:
            raise Exception(f"已存在学号为 {student.no} 的学生信息.")

        insert_sql = """
                     INSERT INTO Student_Info (Id, Name, Age, Height, No, Phone, CreateTime, ModifiedTime)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        insert_params = (sid, student.name, student.age, student.height, student.no, student.phone, student.create_time,
                         student.modified_time)

        success = self.__execute(insert_sql, insert_params)
        if not success:
            print(f"Insert student failed: {student.name}")
            return success, f"Insert student failed: {student.name}"

        score_states = []
        score_msg = ""
        score_id = int(round(time.time() * 1000000))
        for key, value in student.scores.items():
            insert_score_sql = """INSERT INTO Student_Score (Id, StudentId, Subject, Score)
                                  VALUES (?, ?, ?, ?)"""
            insert_score_params = (score_id, sid, key, value)
            success = self.__execute(insert_score_sql, insert_score_params)
            score_states.append(success)
            if not success:
                print(f"Insert student score failed: {student.name}")
                score_msg += f"Insert student score failed: {student.name}\n"
            else:
                print(f"Insert student score success: {student.name}")

            score_id += 1

        if all(score_states):
            return True, f"Insert student and score success"
        else:
            return False, score_msg

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
        stu = self.query_student(name)
        if stu is None:
            raise Exception(f"未找到名为 {name} 的学生信息.")

        del_sql = "DELETE FROM Student_Info WHERE Name = ?"
        del_params = (name,)
        success = self.__execute(del_sql, del_params)
        if not success:
            print(f"Delete student failed: {name}")
            return success, f"Delete student failed: {name}"

        del_score_sql = "DELETE FROM Student_Score WHERE StudentId = ?"
        del_score_params = (stu.id,)
        success = self.__execute(del_score_sql, del_score_params)
        if not success:
            print(f"Delete student score failed: {name}")
            return success, f"Delete student score failed: {name}"

        return success, f"Delete student success: {name}"

    def update(self, name: str, values: dict, scores: dict = None):
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
        score_states = []
        score_msg = ""
        stu = self.query_student(name)
        if stu is None:
            raise Exception(f"未找到名为 {name} 的学生信息.")

        spilt_sql = ""
        for key, value in values.items():
            spilt_sql += f",{key} = ?"

        update_sql = f"UPDATE Student_Info SET ModifiedTime = datetime('now', 'localtime'){spilt_sql} WHERE Name = ?"
        update_params = tuple(values.values()) + (name,)
        success = self.__execute(update_sql, update_params)
        if not success:
            print(f"Update student failed: {name}")
            return success, f"Update student failed: {name}"

        if scores is not None:
            for key, value in scores.items():
                update_score_sql = f"UPDATE Student_Score SET Score = ? WHERE Subject = ? AND StudentId = ?"
                update_score_params = (value, key, stu.id)
                score_states.append(self.__execute(update_score_sql, update_score_params))
                if not score_states[-1]:
                    score_msg += f"Update student score failed: {name}\n"
                    print(f"Update student score failed: {name}")

        succcess = all(score_states)
        msg = f"Update student and score success: {name}" if succcess else score_msg
        return succcess, msg

    def query_student(self, name: str):
        """
        查询指定名称的学生信息。
        通过学生的姓名在现有数据中查找相关信息并返回。
        :param name: 学生的姓名，用于查询
        :type name: str
        :return: 若学生存在，返回对应的学生信息；否则返回 None
        :rtype: Any
        """
        try:
            query_stu_sql = "SELECT * FROM Student_Info WHERE Name = ?"
            query_stu = self.__query_one(query_stu_sql, (name,))
            stu = self.__to_student(query_stu)

            if stu is not None:
                query_stu_score_sql = "SELECT * FROM Student_Score WHERE StudentId = ? "
                scores = self.__query_all(query_stu_score_sql, (stu.id,))
                stu.scores = self.__to_score(scores)

            return stu
        except Exception as e:
            print(e, file=sys.stderr)
            return None

    def query_all_students(self, args: dict = None):
        try:
            query_stu_params = None
            query_stu_sql = """SELECT *
                               FROM Student_Info
                               WHERE 1 = 1"""

            if args is not None:
                query_stu_params = tuple(args.values())
                for key, value in args.items():
                    query_stu_sql += f" AND {key} = ? "

            query_stu = self.__query_all(query_stu_sql, query_stu_params)
            students = self.__to_students(query_stu)

            if students is not None:
                query_stu_score = ", ".join(["?"] * len(students))
                query_stu_score_sql = f"SELECT * FROM Student_Score WHERE StudentId in ({query_stu_score})"
                query_stu_score_params = [stu.id for stu in students]
                score_rows = self.__query_all(query_stu_score_sql, query_stu_score_params)
                scores = self.__to_Scores(score_rows)
                if scores is not None:
                    self.__with_stu_score(students, scores)

            return students
        except Exception as e:
            print(e, file=sys.stderr)
            return None

    def query_student_exists(self, name: str = None, no: str = None) -> bool:
        """
        检查学生是否存在于数据库中。
        通过指定的姓名或学号查询学生信息表，判断是否存在满足条件的学生记录。
        :param name: 学生姓名，可选
        :param no: 学生学号，可选
        :return: 如果查询到学生记录，返回 True，否则返回 False
        :rtype: bool
        """
        args = {}
        if name is not None:
            args["Name"] = name
        if no is not None:
            args["No"] = no

        result = self.__query_count("Student_Info", args)
        return result > 0

    def __query_count(self, table: str, args: dict = None):
        query_sql = f"SELECT COUNT(*) FROM {table} WHERE 1=1"
        for key, value in args.items():
            query_sql += f" AND {key} = ? "

        query_params = tuple(args.values())
        result = self.__query_one(query_sql, query_params)
        return result[0]

    def __query_one(self, sql: str, params: tuple = None):
        """
        执行单条SQL查询语句并返回第一条查询结果。
        此方法通过数据库连接池获取连接，执行指定的SQL语句，并返回查询结果的第一条记录。
        若发生异常，将输出错误信息，且正确释放数据库连接和游标资源。
        :param sql: 要执行的SQL查询语句的字符串
        :type sql: str
        :param params: SQL查询中的参数，用于防止SQL注入攻击，默认为 None
        :type params: tuple, optional
        :return: 查询结果的第一条记录，通常为元组类型；若无记录或发生异常，则返回 None
        :rtype: Any
        """
        # 初始化资源变量（避免finally中引用未定义的变量）
        conn = None
        cursor = None
        result = None  # 初始化返回值，避免异常时无返回
        try:
            conn = self.pool.connection()
            #conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
            result = cursor.fetchone()
            conn.close()
        except Exception as e:
            print(e, file=sys.stderr)
        finally:
            # 优先关闭游标，再关闭连接（顺序不能反）
            if cursor:  # 判空：避免cursor未创建时调用close()报错
                try:
                    cursor.close()
                except Exception as e:
                    print(f"关闭游标失败：{e}", file=sys.stderr)
            if conn:  # 判空：避免conn未创建时调用close()报错
                try:
                    conn.close()
                except Exception as e:
                    print(f"关闭连接失败：{e}", file=sys.stderr)

        return result

    def __query_all(self, sql: str, params: tuple = None):
        """
        执行 SQL 查询语句并返回所有查询结果。
        该方法用于执行提供的 SQL 查询，并返回对应的结果集。
        通过连接池获取数据库连接，确保数据库资源的高效使用。
        资源释放遵循游标优先关闭、连接后关闭的顺序，确保过程安全。
        :param sql: SQL 查询字符串，用于指定查询的具体内容。
        :param params: 可选的参数化查询参数，用于提供 SQL 中的动态参数值。
        :return: 查询结果集，返回值类型为查询结果的列表。如果查询发生异常，返回 None。
        :rtype: list | None
        """
        # 初始化资源变量（避免finally中引用未定义的变量）
        conn = None
        cursor = None
        result = None  # 初始化返回值，避免异常时无返回
        try:
            conn = self.pool.connection()
            cursor = conn.cursor()
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
            result = cursor.fetchall()
            conn.close()
        except Exception as e:
            print(e, file=sys.stderr)
        finally:
            # 优先关闭游标，再关闭连接（顺序不能反）
            if cursor:  # 判空：避免cursor未创建时调用close()报错
                cursor.close()
            if conn:  # 判空：避免conn未创建时调用close()报错
                conn.close()

        return result

    def __execute(self, sql: str, params: tuple = None):
        """
        执行给定的 SQL 查询并根据结果返回执行状态。
        此方法使用连接池获取数据库连接并执行参数化的 SQL 查询。执行完成后，
        自动提交事务。如果在执行过程中发生异常，会回滚事务，同时确保
        关闭游标和连接，避免资源泄漏。

        :param sql: 要执行的 SQL 查询字符串。
        :type sql: str
        :param params: SQL 查询的参数，可选，默认为 None。
        :type params: tuple, optional
        :return: 表示 SQL 查询执行成功或失败的布尔值。
        :rtype: bool
        """
        conn = None
        cursor = None
        success = False

        try:
            conn = self.pool.connection()
            cursor = conn.cursor()

            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)

            conn.commit()
            success = True
        except Exception as e:
            success = False
            if conn:
                conn.rollback()
            print(e, file=sys.stderr)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return success

    def __create_table(self):
        create_score_sql = "CREATE TABLE IF NOT EXISTS Student_Score (Id INTEGER PRIMARY KEY, StudentId INTEGER NOT NULL, Subject TEXT NOT NULL, Score REAL)"
        create_student_sql = "CREATE TABLE IF NOT EXISTS Student_Info (Id INTEGER PRIMARY KEY,Name TEXT NOT NULL,Age INTEGER,Height REAL,NO TEXT UNIQUE,Phone TEXT,CreateTime DATETIME DEFAULT (datetime('now', 'localtime')),ModifiedTime DATETIME DEFAULT (datetime('now', 'localtime')))"

        success = self.__execute(create_student_sql)
        if not success:
            print(f"Create table failed: {create_student_sql}")
        success = self.__execute(create_score_sql)
        if not success:
            print(f"Create table failed: {create_score_sql}")

    def __to_student(self, row):
        stu = Student()
        stu.id = row[0]
        stu.no = row[4]
        stu.name = row[1]
        stu.age = row[2]
        stu.height = row[3]
        stu.phone = row[5]
        stu.create_time = row[6]
        stu.modified_time = row[7]
        return stu

    def __to_score(self, rows):
        scores = {}
        for row in rows:
            scores[row[2]] = row[3]
        return scores

    def __to_Scores(self, rows):
        scores = []
        for row in rows:
            score = Score()
            score.id = row[0]
            score.student_id = row[1]
            score.subject = row[2]
            score.score = row[3]
            scores.append(score)
        return scores

    def __to_students(self, rows):
        students = []
        for row in rows:
            student = self.__to_student(row)

        return students

    def __with_stu_score(self, students: list[Student], scores: list[Score]):
        for stu in students:
            for score in [s for s in scores if s.student_id == stu.id]:
                stu.scores[score.subject] = score.score
