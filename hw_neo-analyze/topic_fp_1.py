class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def print_list(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")


    ### Початок виконання завдань фінального проєкту

    # Функція для реверсування однозв'язного списку
    def reverse(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    # Сортування вставками
    def insertion_sort(self):
        sorted_list = None
        current = self.head
        while current:
            next_node = current.next
            sorted_list = self._sorted_insert(sorted_list, current)
            current = next_node
        self.head = sorted_list

    def _sorted_insert(self, sorted_list, node):
        if sorted_list is None or node.data < sorted_list.data:
            node.next = sorted_list
            sorted_list = node
        else:
            current = sorted_list
            while current.next and current.next.data < node.data:
                current = current.next
            node.next = current.next
            current.next = node
        return sorted_list

    # Функція для злиття двох відсортованих однозв'язних списків
    @staticmethod
    def merge_sorted_lists(head1, head2):
        dummy = Node()
        tail = dummy

        while head1 and head2:
            if head1.data <= head2.data:
                tail.next = head1
                head1 = head1.next
            else:
                tail.next = head2
                head2 = head2.next
            tail = tail.next

        tail.next = head1 if head1 else head2
        return dummy.next


# Приклад використання
if __name__ == "__main__":
    # Створення першого списку
    llist1 = LinkedList()
    llist1.insert_at_end(5)
    llist1.insert_at_end(44)
    llist1.insert_at_end(10)
    print("Перший список:")
    llist1.print_list()

    # Сортування списку
    llist1.insertion_sort()
    print("Перший список після сортування вставками:")
    llist1.print_list()

    # Створення другого списку
    llist2 = LinkedList()
    llist2.insert_at_end(2)
    llist2.insert_at_end(88)
    llist2.insert_at_end(14)
    print("Другий список:")
    llist2.print_list()

    # Сортування другого списку
    llist2.insertion_sort()
    print("Другий список після сортування вставками:")
    llist2.print_list()

    # Злиття двох відсортованих списків
    merged_head = LinkedList.merge_sorted_lists(llist1.head, llist2.head)
    
    # Створення нового списку з результату злиття
    merged_list = LinkedList()
    merged_list.head = merged_head
    print("Злитий список:")
    merged_list.print_list()

