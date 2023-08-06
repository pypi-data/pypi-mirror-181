## Takes inputs from user and prints number students


class School:
    def __init__(self):
        self.name= ''
        self.regno=int(0)
        self.marks=int(0)
        #self.list2=list2
        

    def get_student_information(self):
        try:
            self.name = input("Enter student Name: \n")
            self.regno= int(input("Enter stduent Rego: \n"))
            self.marks= int(input("Enter students Marks: \n"))
            return self.name,self.regno,self.marks
        except Exception as e:
            print("Please call numberofstudents class \n",e)

    def numberofstudents(self):
        self.No_of_students = int(input('Enter number of stduents:\n'))
        self.list1=[]
        for _ in range(0,self.No_of_students):

            
            obj1= School()
            self.list1.append(obj1.get_student_information())
            #print(list1)
            #list1=[]
            obj1=''
        return self.list1



