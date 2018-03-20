class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        point = "x: " + str(self.x) + "     y: " + str(self.y)
        return point

    def __add__(self, other):
        if isinstance(other, Point):
            return self.add_point(other)
        elif isinstance(other, tuple):
            t = Point(other[0], other[1])
            return self.add_point(t)
        else:
            return "unsupported addition"

    def add_point(self, other):
        new_point = Point()
        new_point.x = self.x + other.x
        new_point.y = self.y + other.y
        return new_point

class Rect:
    def __init__(self, width, height, corner):
        self.width = width
        self.height = height
        self.corner = Point(corner.x, corner.y)

    def __str__(self):
        rectangle = "W: " + str(self.width) + "  H: " + str(self.height) + \
            "  corner: " + str(self.corner)
        return rectangle

def move_rectangle(rect, dx, dy):
    rect_new = Rect(rect.width, rect.height, rect.corner)
    rect_new.corner.x += dx
    rect_new.corner.y += dy

    return rect_new

corner_point1 = Point(0, 0)
corner_point2 = Point(-15, 2)
rect = Rect(10, 50, corner_point1)
rect_new = move_rectangle(rect, -3, -11)

# print (rect_new)
# print (rect_new is rect)

print (corner_point1 + corner_point2)
print (corner_point1 + (5, 2))
print (corner_point1 + "hey")

"""
This operation is called a shallow copy because it copies the object and
any references it contains, but not the embedded objects.
"""
import copy

rect2 = copy.copy(rect)
rect3 = copy.deepcopy(rect)

# print (rect2 is rect)
# print (rect2.corner is rect.corner)
# print (rect3.corner is rect.corner)
#
# rect.corner = Point(-9, 0)
#
# print (rect.corner, rect2.corner)
# print (rect2.corner is rect.corner)
