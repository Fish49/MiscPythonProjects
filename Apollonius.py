import math

class Vector2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        else:
            raise TypeError

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(self.x / other, self.y / other)
        else:
            raise TypeError

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            raise TypeError

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise TypeError

    def __iter__(self):
        return (self.x, self.y)

    def dot(self, other):
        if isinstance(other, Vector2):
            return (self.x * other.x) + (self.y * other.y)
        else:
            raise TypeError()

    def distance(self):
        return math.sqrt((self.x**2) + (self.y**2))

    def normalizeIP(self):
        distance = self.distance()
        self.x /= distance
        self.y /= distance

class Line():
    def __init__(self, originVector, directionVector):
        self.origin = originVector
        self.direction = directionVector

    @staticmethod
    def fromTwoPoints(p1, p2):
        origin = Vector2(*p1)
        direction = Vector2(*p2) - Vector2(*p1)
        direction.normalizeIP()
        return Line(origin, direction)

class Circle():
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    @staticmethod
    def line2circle1(line1, line2, circle):
        # (newCenter - line1.origin).dot(rv1) = newRadius
        # (newCenter - line2.origin).dot(rv2) = newRadius
        # (circle.center - newCenter).distance() = circle.radius + newRadius

        # newCenter.dot(rv1) - line1.origin.dot(rv1) = newRadius
        # newCenter.dot(rv2) - line2.origin.dot(rv2) = newRadius
        # (circle.center - newCenter).distance() - circle.radius = newRadius
        # sqrt((circle.center.x - newCenter.x)**2 + (circle.center.y - newCenter.y)**2) - circle.radius = newRadius

        # (newCenter.x * rv1.x) + (newCenter.y * rv1.y) - line1.origin.dot(rv1) = newRadius
        # (newCenter.x * rv2.x) + (newCenter.y * rv2.y) - line2.origin.dot(rv2) = newRadius

        # (newCenter.x * rv1.x) + (newCenter.y * rv1.y) - line1.origin.dot(rv1) = (newCenter.x * rv2.x) + (newCenter.y * rv2.y) - line2.origin.dot(rv2)

        # newCenter.x = ((newCenter.y * rv2.y) - line2.origin.dot(rv2) - (newCenter.y * rv1.y) + line1.origin.dot(rv1)) / (rv1.x - rv2.x)

        # (newCenter.x * rv1.x) + (newCenter.y * rv1.y) - line1.origin.dot(rv1) = sqrt((circle.center.x - newCenter.x)**2 + (circle.center.y - newCenter.y)**2) - circle.radius
        # ((newCenter.x * rv1.x) + (newCenter.y * rv1.y) - line1.origin.dot(rv1) + circle.radius)**2 = (circle.center.x - newCenter.x)**2 + (circle.center.y - newCenter.y)**2
        # (newCenter.y * rv1.y)**2 + 2(newCenter.y * rv1)((newCenter.x * rv1.x) - line1.origin.dot(rv1) + circle.radius)) + ((newCenter.x * rv1.x) - line1.origin.dot(rv1) + circle.radius))**2 = (circle.center.x - newCenter.x)**2 + (circle.center.y - newCenter.y)**2
        pass