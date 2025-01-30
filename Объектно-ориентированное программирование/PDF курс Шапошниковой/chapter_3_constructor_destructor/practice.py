"""
Напишите программу по следующему описанию:

1. Есть класс Person, конструктор которого принимает три параметра (не учитывая self) –
имя, фамилию и квалификацию специалиста. Квалификация имеет значение заданное по
умолчанию, равное единице.

2. У класса Person есть метод, который возвращает строку, включающую в себя всю
информацию о сотруднике.

3. Класс Person содержит деструктор, который выводит на экран фразу "До свидания,
мистер …" (вместо троеточия должны выводиться имя и фамилия объекта).

4. В основной ветке программы создайте три объекта класса Person. Посмотрите
информацию о сотрудниках и увольте самое слабое звено.

5. В конце программы добавьте функцию input(), чтобы скрипт не завершился сам, пока
не будет нажат Enter. Иначе вы сразу увидите как удаляются все объекты при
завершении работы программы.
"""


class Person:
    def __init__(self, name, surname, qualification=1):
        self.name, self.surname, self.qualification = name, surname, qualification

    def get_person_info(self):
        return f"До свидания, мистер {self.name} {self.surname}"

    def __del__(self):
        print(self.get_person_info())


p1, p2, p3 = Person('name1', 'surname1'), Person('name2', 'surname2', 2), Person('name3', 'surname3', 3)
print(dir(Person))
weakest_p = [p for p in [p1, p2, p3] if p.qualification == min([p1.qualification, p2.qualification, p3.qualification])][0]
del weakest_p
input()
