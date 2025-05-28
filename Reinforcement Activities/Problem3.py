# Evan-Soobin Jeon
# ejeon2@uci.edu
def sequential_search(collection, key):
    collection = iter(collection)

    def helper(it):
        try:
            current = next(it)
        except StopIteration:
            return False
        if current == key:
            return True
        return helper(it)

    return helper(collection)

# Time complexity: O(n)
# Space complexity (extra memory for recursion): O(n)
# If Python had tail call elimination, Space complexity would become O(1)

def binary_search(collection, key):
    def helper(low, high):
        if low > high:
            return False
        mid = (low + high) // 2
        if collection[mid] == key:
            return True
        elif key < collection[mid]:
            return helper(low, mid - 1)
        else:
            return helper(mid + 1, high)

    return helper(0, len(collection) - 1)

# Time complexity: O(log n)
# Space complexity (extra memory for recursion): O(log n)
# If Python had tail call elimination, Space complexity would become O(1)

