'''
3d object renderer
-PaiShoFish49
'''

from PIL import Image
from pygame import Vector3, Vector2
import math
from copy import deepcopy
import colorsys
import time
import random

starttime = time.time()

def inBBox(point, ppp, nnn):
    if not nnn[0] <= point[0] <= ppp[0]:
        return False
    if not nnn[1] <= point[1] <= ppp[1]:
        return False
    if not nnn[2] <= point[2] <= ppp[2]:
        return False
    return True

def normalizeAngle(x):
    return ((x+180) % 360) - 180

class TransformableV3(Vector3):
    def __init__(self, *args) -> None:
        super().__init__(*args)

    def translateT(self, vect):
        return self + vect

    def rotateT(self, center, angle, axis):
        temp: Vector3 = self - center
        temp.rotate_ip(angle, axis)

        return temp + center

    def scaleT(self, factor, center):
        temp: Vector3 = self - center
        temp = temp * factor

        return temp + center

    def translateT_ip(self, vect):
        self.update(self + vect)

    def rotateT_ip(self, center, angle, axis):
        temp: Vector3 = self - center
        temp.rotate_ip(angle, axis)

        self.update(temp + center)

    def scaleT_ip(self, factor, center):
        temp: Vector3 = self - center
        temp = temp * factor

        self.update(temp + center)

    def getDiffAngle(self):
        vect2 = self.copy()
        m = min(tuple(map(lambda x: abs(x), vect2)))
        for i in range(len(vect2)):
            if abs(vect2[i]) == m:
                axis = [0] * len(vect2)
                axis[i] = 1
                vect2.rotate_ip(90, axis)
                break
        return vect2

class Ray():
    def __init__(self, position, rotation) -> None:
        self.position: TransformableV3 = position.copy()
        self.rotation: TransformableV3 = rotation.copy()

    def translate(self, vect):
        return self.position.translateT(vect)

    def rotate(self, angle, axis):
        return self.rotation.rotateT(self.position, angle, axis)

    def scale(self, factor):
        return self.rotation.scaleT(factor)

    def translate_ip(self, vect):
        self.position.translateT_ip(vect)

    def rotate_ip(self, angle, axis):
        self.rotation.rotateT_ip(self.position, angle, axis)

    def scale_ip(self, factor):
        self.rotation.scaleT_ip(factor)

    def getDestination(self):
        return self.position + self.rotation

class Plane(Ray):
    def __init__(self, position, rotation) -> None:
        super().__init__(position, rotation)

    def projectTo2D(self, points: list[TransformableV3]):
        self.rotation.normalize_ip()
        temp = self.rotation.getDiffAngle()
        xAxis = self.rotation.cross(temp)
        yAxis = self.rotation.cross(xAxis)

        xAxis.normalize_ip()
        yAxis.normalize_ip()

        newPoints: list[Vector2] = []
        for i in points:
            x = (i - self.position).dot(xAxis)
            y = (i - self.position).dot(yAxis)

            newPoints.append(Vector2(x, y))

        return newPoints

    def getIntersection(self, ray: Ray, clipDistance = 100000000):
        nray = Ray(ray.position, ray.rotation)
        nray.rotation.normalize_ip()
        if nray.rotation.dot(self.rotation) == 0:
            return

        sval = ((self.position-nray.position).dot(self.rotation)) / nray.rotation.dot(self.rotation)

        if sval < 0:
            return
        if sval > clipDistance:
            return

        nray.rotation = nray.rotation * sval
        return (sval, nray.getDestination())

class Vertex():
    def __init__(self, *args) -> None:
        self.vector = TransformableV3(*args)

class Face():
    def __init__(self, vertecies, HS = (0, 0)) -> None:
        self.flipNormal = False
        self.vertecies: list[Vertex] = vertecies
        self.HS = HS

    def getNormal(self):
        edge1: TransformableV3 = self.vertecies[2].vector - self.vertecies[1].vector
        edge2: TransformableV3 = self.vertecies[0].vector - self.vertecies[1].vector

        N = edge1.cross(edge2)

        if self.flipNormal:
            return (N * -1).normalize()
        return N.normalize()

    def getCenter(self):
        return (self.vertecies[0].vector+self.vertecies[1].vector+self.vertecies[2].vector) / 3

    def getPlane(self):
        return Plane(self.getCenter(), self.getNormal())

    def getBBox(self):
        ppp = [-math.inf] * 3
        nnn = [math.inf] * 3

        for i in self.vertecies:
            ppp[0] = max(i.vector.x, ppp[0])
            ppp[1] = max(i.vector.y, ppp[1])
            ppp[2] = max(i.vector.z, ppp[2])
            nnn[0] = min(i.vector.x, nnn[0])
            nnn[1] = min(i.vector.y, nnn[1])
            nnn[2] = min(i.vector.z, nnn[2])

        pppv = TransformableV3(ppp)
        nnnv = TransformableV3(nnn)

        return (pppv, nnnv)

    def flipNormals(self):
        self.flipNormal = (not self.flipNormal)

    def getCollisionDistance(self, ray: Ray, clipDistance = 100000000):
        plane = self.getPlane()
        colpoint = plane.getIntersection(ray, clipDistance)

        if colpoint == None:
            return

        if not inBBox(colpoint[1], *self.getBBox()):
            return

        points2D = plane.projectTo2D((colpoint[1], *[i.vector for i in self.vertecies]))

        BitoA = points2D[2] - points2D[1]
        XitoA = points2D[0] - points2D[1]
        CitoA = points2D[3] - points2D[1]
        AitoB = points2D[1] - points2D[2]
        XitoB = points2D[0] - points2D[2]
        CitoB = points2D[3] - points2D[2]

        maxVA = normalizeAngle(BitoA.angle_to(CitoA))
        actVA = normalizeAngle(BitoA.angle_to(XitoA))
        maxVB = normalizeAngle(AitoB.angle_to(CitoB))
        actVB = normalizeAngle(AitoB.angle_to(XitoB))

        if actVA < 0:
            maxVA *= -1
            actVA *= -1
        if actVB < 0:
            maxVB *= -1
            actVB *= -1


        conditionA = (0 <= actVA <= maxVA)
        conditionB = (0 <= actVB <= maxVB)

        # if (4 < colpoint[0] < 6)  and (random.randint(1, 100) < 3):
        #     print(f'in terms of a: b: {BitoA}, c: {CitoA}, x: {XitoA}, bigAngle: {maxVA}, littleAngle: {actVA}.')
        #     print(f'in terms of b: a: {AitoB}, c: {CitoB}, x: {XitoB}, bigAngle: {maxVB}, littleAngle: {actVB}.')
        #     nn = (min([i.x for i in points2D])-2, min(i.y for i in points2D)-2)
        #     pp = (max([i.x for i in points2D])+2, max(i.y for i in points2D)+2)
        #     img = Image.new('RGB', (128, 128), (0, 0, 0))
        #     for j, i in enumerate(points2D):
        #         col = [0, 0, 0]
        #         if j > 0:
        #             col[j-1] = 255
        #         else:
        #             col = (255, 255, 255)
        #         img.putpixel((int((i.x - nn[0]) * 128 / (pp[0] - nn[0])), int((i.y - nn[1]) * 128 / (pp[1] - nn[1]))), tuple(col))
        #     print(conditionA and conditionB)
        #     img.show()
        #     exit()

        if not (conditionA and conditionB):
            return
        return colpoint[0]

class Object():
    def __init__(self, faces) -> None:
        self.faces: list[Face] = faces

    def getVerts(self):
        verts: list[Vertex] = []
        for i in self.faces:
            for j in i.vertecies:
                if not j in verts:
                    verts.append(j)

        return verts

    def getBBox(self):
        if self.faces == []:
            return (0, 0)

        ppp = [-math.inf] * 3
        nnn = [math.inf] * 3

        for i in self.getVerts():
            ppp[0] = max(i.vector.x, ppp[0])
            ppp[1] = max(i.vector.y, ppp[1])
            ppp[2] = max(i.vector.z, ppp[2])
            nnn[0] = min(i.vector.x, nnn[0])
            nnn[1] = min(i.vector.y, nnn[1])
            nnn[2] = min(i.vector.z, nnn[2])

        pppv = TransformableV3(ppp)
        nnnv = TransformableV3(nnn)

        return (pppv, nnnv)

    def translate(self, vect):
        verts = self.getVerts()

        for i in verts:
            i.vector.translateT_ip(vect)

    def rotate(self, angle, axis):
        verts = self.getVerts()

        ppp, nnn = self.getBBox()
        center = nnn + ((ppp - nnn) * 0.5)

        for i in verts:
            i.vector.rotateT_ip(center, angle, axis)

    def scale(self, factor):
        verts = self.getVerts()

        ppp, nnn = self.getBBox()
        center = nnn + ((ppp - nnn) * 0.5)

        for i in verts:
            i.vector.scaleT_ip(factor, center)

    @staticmethod
    def newFromStl(path, HS = (0, 0)):
        allpoints = []
        curverts = []
        allfaces = []
        allverts = []
        with open(path, 'r') as f:
            for i in f.readlines():
                nums = i.lstrip()
                if nums.startswith('vertex'):
                    nums = nums.replace('vertex ', '')
                    nums = nums.split()

                    nums = tuple(map(lambda x: float(x), nums))

                    try:
                        curverts.append(allpoints.index(nums))
                    except ValueError:
                        allpoints.append(nums)
                        allverts.append(Vertex(nums))
                        curverts.append(len(allpoints)-1)

                elif nums.startswith('endfacet'):
                    face = Face([allverts[v] for v in curverts], HS)
                    allfaces.append(face)
                    curverts = []

            return Object(allfaces)

class Light():
    def __init__(self, rotation: TransformableV3, power) -> None:
        self.rotation = rotation
        self.power = power

class Camera(Ray):
    def __init__(self) -> None:
        super().__init__(TransformableV3((0, -5, 0)), TransformableV3((0, 1, 0)))
        self.clipDistance = 100000000
        self.angle = 20
        self.resolution = 128

    def castRay(self, cord):
        angleX = ((cord[0] - (self.resolution / 2)) / (self.resolution / 2)) * self.angle
        angleY = ((cord[1] - (self.resolution / 2)) / (self.resolution / 2)) * self.angle

        ray = Ray(self.position, self.rotation)
        yrotax = TransformableV3((self.rotation.x, self.rotation.y, 0))
        yrotax.rotate_ip(90, (0, 0, 1))
        xrotax = self.rotation.cross(yrotax)
        ray.rotation.rotate_ip(angleX, xrotax)
        ray.rotation.rotate_ip(angleY, yrotax)

        return ray

class Scene():
    def __init__(self, activeCamera, shapes, light) -> None:
        self.activeCamera: Camera = activeCamera
        self.shapes: list[Object] = shapes
        self.light: Light = light

    def render(self):
        res = self.activeCamera.resolution
        renderResult = Image.new('RGB', (res, res), (0, 0, 0))
        for x in range(res):
            for y in range(res):
                closestdist = math.inf
                closestFace = None
                renderRay = self.activeCamera.castRay((x, y))
                for i in self.shapes:
                    for j in i.faces:

                        collisiondist = j.getCollisionDistance(renderRay, self.activeCamera.clipDistance)
                        if collisiondist != None:
                            #print(collisiondist)
                            # print(j)
                            if collisiondist < closestdist:
                                closestFace = j
                                closestdist = collisiondist

                if closestFace != None:
                    pixelValue = abs(self.light.rotation.normalize().dot(closestFace.getNormal().normalize()))*(self.light.power / 255)
                    pixelColor = colorsys.hsv_to_rgb((closestFace.HS[0] / 255), (closestFace.HS[1] / 255), pixelValue)
                    pixelColor = tuple(map(lambda x: int(x*255), pixelColor))

                    renderResult.putpixel((x, y), pixelColor)

        return renderResult

camera = Camera()
light = Light(TransformableV3((0.152, 0.161, -0.181)), 255)
shape = Object.newFromStl("C:/Users/beebf/Downloads/untitled.stl")
scene = Scene(camera, [shape], light)
print(scene.shapes[0].faces[0].vertecies[0].vector)
print(scene.shapes[0].faces[1].vertecies[0])
scene.shapes[0].rotate(36, TransformableV3(1, 0, 0))
print(scene.shapes[0].faces[0].vertecies[0].vector)

# print(camera.castRay((14, 2)).getDestination())

result = scene.render()
print(time.time() - starttime)
result.show()
