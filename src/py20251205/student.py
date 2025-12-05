class Student:
    """
    学生基本信息类
    """

    def __init__(self, name: str = None, age: int = None, height: float = None, no: str = None, phone: str = None,
                 scores: dict = None):
        """
        表示一个包含个人基本信息及学科分数的类。
        该类对象用于存储一个人的姓名、年龄、身高、多个科目的分数以及其学号和手机号等信息。
        Attributes:
            name (str): 姓名，标识个人信息。
            age (int): 年龄，表示个人的年龄。
            height (float): 身高，以米为单位表示。
            scores (dict): 学科分数，以字典形式存储，每个键为学科名称，每个值为对应学科分数。
            no (str): 学号，用于标识每个学生的唯一编号。
            phone (str): 手机号，用于联系个人的联系方式。
        """
        self.name = name
        self.age = age
        self.height = height
        self.scores = scores
        self.no = no
        self.phone = phone

    def __str__(self):
        """
        生成对象的字符串表示形式。
        该方法遍历对象属性及其对应值，并将它们输出到标准输出中。
        :return: 无返回值
        :rtype: None
        """
        for key, value in self.__dict__.items():
            print(f"{key}: {value}")
