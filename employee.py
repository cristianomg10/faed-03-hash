class Employee:
    def __init__(self, matricula, salario, setor):
        self.__matricula = matricula
        self.__salario = salario
        self.__setor = setor

    @property
    def matricula(self):
        return self.__matricula

    @property
    def salario(self):
        return self.__salario

    @property
    def setor(self):
        return self.__setor

    def __str__(self):
        return f"{self.__matricula} - {self.__setor}"