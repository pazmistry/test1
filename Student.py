class Student:
    def __init__(self,name,major,gpa,isMale):
        self.name = name
        self.major=major
        self.gpa=gpa
        self.isMale=isMale

    def isHonourStudent(self):
        if self.gpa > 2:
            return True
        else:
            return False
