import sys

students = {}
subjects = ["语文", "数学", "英语", "化学", "物理"]

while True:
    try:
        print("-----------------------------------------------------------", file=sys.stdout)
        user_name = input("请输入学生姓名：").strip()
        if user_name == "":
            print("您输入的学生姓名有误，请重新录入学生信息！", file=sys.stderr)
            continue

        user_age = int(input("请输入学生年龄：").strip())
        user_height = float(input("请输入学生身高(cm)：").strip())
        score_txt = input("请输入学生 语文,数学,英语,化学,物理 的成绩(逗号分隔):")
        scores = list(map(float, score_txt.split(",")))
        student_info = (user_name, user_age, user_height)
        student_dict_scores = dict(zip(subjects, scores))
        students[user_name] = (student_info, student_dict_scores)

        print(f"学生 [{user_name}] 的详细信息: \n{students[user_name]}")
        print("")

        txt = input("输入任意键继续录入, 输入 exit 退出学生信息录入.")
        if txt.strip().lower() == "exit":
            break
    except Exception as e:
        print(f"出现错误,请重新录入学生信息:{e}", file=sys.stderr)

while True:
    command = int(input(f"请输入您需要的操作 (1-修改, 2-删除, 3-查询) :").strip())
    match command:
        case 1:
            user_name = input(f"请输入您要修改的学生姓名:")
            if user_name == "":
                print("您输入的学生姓名有误，请重新录入学生信息！", file=sys.stderr)
                continue

            user_age = int(input("请输入学生年龄：").strip())
            user_height = int(input("请输入学生身高(cm)：").strip())
            score_txt = input("请输入学生 语文,数学,英语,化学,物理 的成绩(逗号分隔):")
            scores = list(map(float, score_txt.split(",")))
            student_info = (user_name, user_age, user_height)
            student_dict_scores = dict(zip(subjects, scores))
            students[user_name] = (student_info, student_dict_scores)
        case 2:
            user_name = input(f"请输入您要删除的学生姓名:")
            if user_name in students:
                del students[user_name]
                print(f"学生[{user_name}]的数据已删除.")
            else:
                print(f"未找到学生[{user_name}]的数据")
        case 3:
            user_name = input(f"请输入您要查询的学生姓名:")
            if user_name not in students:
                print(f"未找到学生[{user_name}]的数据")
                continue

            (student_info,student_score) = students[user_name]
            # 平均成绩
            all_score = student_score.values()
            sum_score = sum(all_score)
            avg_sore = sum_score / len(subjects)
            # 总体评价
            composite_assess = None
            if avg_sore >= 90:
                composite_assess = "优秀"
            elif 75 <= avg_sore < 90:
                composite_assess = "良好"
            elif 60 <= avg_sore < 75:
                composite_assess = "及格"
            else:
                composite_assess = "不及格"
            print(f"学生：{user_name} | 年龄：{student_info[1]} | 身高：{student_info[2]}cm\n"
                  f"成绩：语文 {student_score["语文"]}, 数学 {student_score["数学"]}, 英语 {student_score["英语"]}, 化学 {student_score["化学"]}, 物理 {student_score["物理"]}\n"
                  f"平均分：{avg_sore} | 等级：{composite_assess}")
        case 999:
            print(f"程序结束!")
            exit(0)
        case _:
            print(f"命令输入错误,请重新输入!")

