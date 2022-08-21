class HashTable:
    __size: int
    __collision_number: int

    def __init__(self, size, initial_element=None):
        self.__size = size
        self.__collision_number = 0
        self.__is_linkedlist = -1  # Flag pra saber se é list ou lista ligada

        if initial_element is None:
            self.__structure = [[] for i in range(size)]
            self.__is_linkedlist = 0
        else:
            self.__structure = [initial_element() for i in range(size)]
            self.__is_linkedlist = 1

    def push(self, index, data):
        position = self.hash_function(index)

        if len(self.__structure[position]) != 0:
            self.__collision_number += 1

        self.__structure[position].append(data)

    def hash_function(self, index):
        return index % self.__size

    @property
    def hash_structure(self):
        return self.__structure

    def find(self, index):
        position = self.hash_function(index)

        if self.__is_linkedlist == 0: # Lista
            for i in self.__structure[position]:
                if index == i.index:
                    return i.data
        elif self.__is_linkedlist == 1: # Lista ligada
            pointer = self.__structure[position].head
            while pointer is not None:
                if index == pointer.index:
                    return pointer.data
                else:
                    pointer = pointer.next

    @property
    def collisions_number(self):
        return self.__collision_number

    @property
    def occupation(self):
        occupation = []
        for i in self.__structure:
            occupation.append(len(i))
        return occupation
