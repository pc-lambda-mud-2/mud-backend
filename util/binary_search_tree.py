from util.dll_queue import Queue
from util.dll_stack import Stack
from util.doubly_linked_list import DoublyLinkedList
import sys


class BinarySearchTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        return f'{self.value}'

    # Insert the given value into the tree
    def insert(self, value):
        # print(value)
        # LEFT CASE
        # check if our new node's value is less than the current node's value
        if value < self.value:
            # does it have a child to the left?
            if not self.left:
                # place our new node here
                self.left = BinarySearchTree(value)
            # otherwise
            else:
                # repeat process for the left
                self.left.insert(value)

        # RIGHT CASE
        # check if the new nodes value is greater than or equal to the current nodes value
        if value >= self.value:
            # does it have a child to the right?
            if not self.right:
                # place our new node here
                self.right = BinarySearchTree(value)
            # otherwise
            else:
                # repeat the process for the right
                self.right.insert(value)

    # Return True if the tree contains the value
    # False if it does not
    def contains(self, target):
        # BASE CASE
        if self.value == target:
            return True
        if self.left is None and self.right is None:
            return False
        # LEFT CASE
        if target < self.value and self.left is not None:
            return self.left.contains(target)
        # RIGHT CASE
        elif self.right is not None:
            return self.right.contains(target)
        #############################
        # check if the value matches the target
        # if self is None or self.value == target:
        #     # return true
        #     return True
        # # LEFT CASE if target less than value
        # if target < self.value:
        #     # check if the left child exists if not
        #     if not self.left:
        #         # return false
        #         return False
        #     # otherwise
        #     else:
        #         # call the contains method of the left child
        #         return self.left.contains(target)
        # # RIGHT CASE otherwise
        # else:
        #     # check if right child exists if not
        #     if not self.right:
        #         # return false
        #         return False
        #     # otherwise
        #     else:
        #         # call the contains method of the right child
        #         return self.right.contains(target)

    # Return the maximum value found in the tree

    def get_max(self):
        # base case
        # if empty tree
        if self is None:
            return None
        # recursive case
        # if there is no right value
        if not self.right:
            # return the root node value
            return self.value
        # otherwise
        else:
            # return get max of the right hand child
            return self.right.get_max()

    # Call the function `cb` on the value of each node
    # You may use a recursive or iterative approach
    def for_each(self, cb):
        cb(self.value)
        # if left exists
        if self.left:
            # run the for each on left
            self.left.for_each(cb)
        # if right exists
        if self.right:
            # run the for each on right
            self.right.for_each(cb)

    def dft_for_each_i(self, cb):
        # create an empty stack
        stack = Stack()
        # push self on to stack
        stack.push(self)

        # iterate over the stack
        while stack.len() > 0:
            # pop the stack off in to current node
            current_node = stack.pop()
            # check if node to left
            if current_node.left:
                # push the current nodes left child on to the stack
                stack.push(current_node.left)

            # check if node to right
            if current_node.right:
                # push the node to the right on to the stack
                stack.push(current_node.right)
            # invoke callback on the value of the current node
            cb(current_node.value)

    def bft_for_each_i(self, cb):
        # create an empty stack
        q = Queue()
        # push self on to stack
        q.enqueue(self)

        # iterate over the stack
        while q.len() > 0:
            # pop the stack off in to current node
            current_node = q.dequeue()
            # check if node to left
            if current_node.left:
                # push the current nodes left child on to the stack
                q.enqueue(current_node.left)

            # check if node to right
            if current_node.right:
                # push the node to the right on to the stack
                q.enqueue(current_node.right)
            # invoke callback on the value of the current node
            cb(current_node.value)

    # DAY 2 Project -----------------------

    # Print all the values in order from low to high
    # Hint:  Use a recursive, depth first traversal
    def in_order_print(self, node):
        if self.left:
            self.left.in_order_print(self.left)
        print(self.value)
        if self.right:
            self.right.in_order_print(self.right)
        # create an empty stack
        # # s = Stack()
        # # # push node to stack
        # # s.push(node)

        # # iterate over the stack
        # while s.size > 0:
        #     # set current stack to head by popping
        #     current_node = s.pop()
        #     # if there is a node to the left of the current_node
        #     if current_node.left:
        #         # set current_node as the left node
        #         current_node = current_node.left
        #         # repeat
        #         self.in_order_print(current_node.left)
        #     # if there is a node to the right of the current_node
        #     if current_node.right:
        #         # set current_node as the left node
        #         current_node = current_node.right
        #         # repeat
        #         self.in_order_print(current_node.right.value)
        #     # print the current value
        #     print(current_node.value)


        

    # Print the value of every node, starting with the given node,
    # in an iterative breadth first traversal
    def bft_print(self, node):
        # create an empty queue
        q = Queue()
        # add the starting node to the queue
        q.enqueue(node)

        # iterate over the queue
        # for n in q.storage:
        #     print(n)
        while q.size > 0:
            # set the current_node to the first item in the q
            current_node = q.dequeue()
            # then print the current value
            print(current_node.value)
            # if the current node has a left child
            if current_node.left:
                # call enqueue on the current left
                q.enqueue(current_node.left)
            # if the current node has a right child
            if current_node.right:
                # call enqueue on the current right
                q.enqueue(current_node.right)
            

    # Print the value of every node, starting with the given node,
    # in an iterative depth first traversal
    def dft_print(self, node):
        # create an empty stack
        s = Stack()
        # # add the starting node to the stack
        s.push(node)

        # # iterate over the stack
        while s.size > 0:
        #     # set the current_node to the first item in the stack
            current_node = s.pop()
        #     # then print the current value
            print(current_node.value)
            # if the current node has a left child
            if current_node.left:
                # call push on the current left
                s.push(current_node.left)
            # if the current node has a right child
            if current_node.right:
                # call push on the current right
                s.push(current_node.right)

    # STRETCH Goals -------------------------
    # Note: Research may be required

    # Print Pre-order recursive DFT
    def pre_order_dft(self, node):
        pass

    # Print Post-order recursive DFT
    def post_order_dft(self, node):
        pass

bst = BinarySearchTree(3)
bst.insert(8)
bst.insert(5)
bst.insert(7)
bst.insert(6)
bst.insert(3)
bst.insert(4)
bst.insert(2)

bst.in_order_print(bst)