class Node:
    def __init__(self, data, index):
        self.data = data
        self.index = index
        self.next = None


class LinkedList:
    def __init__(self):
        self.__head = None
        self.__tail = None
        self.__size = 0

    def append(self, node):
        if self.__head is None:
            self.__head = node
            self.__tail = node
        else:
            self.__tail.next = node
            self.__tail = self.__tail.next
        self.__size += 1

    def __len__(self):
        return self.__size

    def __str__(self):
        text = ""
        pointer = self.__head
        while pointer is not None:
            text = f"{text}, {pointer}"
            pointer = pointer.next

        return f"Size: {self.__size}: {text}"

    @property
    def head(self):
        return self.__head


