scores = [] # 成绩列表
username = input("请输入学生姓名：")
chinese_grades = float(input("请录入语文成绩："))
maths_score = float(input("请录入数学成绩："))
english_score = float(input("请输入英语成绩："))
chemistry_score = float(input("请输入化学成绩："))

# 将成绩添加到列表中
scores.append(chinese_grades)
scores.append(maths_score)
scores.append(english_score)
scores.append(chemistry_score)

# 总成绩
sum_socre = chinese_grades + maths_score + english_score + chemistry_score
# 平均成绩
avg_socre = sum_socre / 4
# 星级评价
star_rating = int(avg_socre / 20)
# 总体评价
composite_assess = None

if avg_socre >= 90:
    composite_assess = "优秀"
elif 75 <= avg_socre < 90:
    composite_assess = "良好"
elif 60 <= avg_socre < 75:
    composite_assess = "及格"
else:
    composite_assess = "不及格"

print(f"学生[{username}]的各科成绩：[{chinese_grades},{maths_score},{english_score},{chemistry_score}]")
print(f"学生[{username}]的总分：{sum_socre} ")
print(f"学生[{username}]的平均分：{avg_socre} ")
print(f"学生[{username}]的总体评价：{composite_assess} ")

if chinese_grades < 60:
    print(f"学生[{username}]的语文不及格，请注意。")

if maths_score < 60:
    print(f"学生[{username}]的数学不及格，请注意。")

if english_score < 60:
    print(f"学生[{username}]的英语不及格，请注意。")

if chemistry_score < 60:
    print(f"学生[{username}]的化学不及格，请注意。")

print(f"学生[{username}]的星级评价：", end="")
for i in range(star_rating):
    print("⭐",end="")


