import math
class Vec2D:
    x=0
    y=0

    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def __sub__(self,other):
        return Vec2D(self.x-other.x,self.y-other.y)
    
    def __add__(self,other):
        return Vec2D(self.x+other.x,self.y+other.y)
    
    def __mul__(self,other):
        return Vec2D(self.x*other.x, self.y*other.y)
    
    def __repr__(self):
        return f'({self.x},{self.y})'
    
    def norma(self):
        return (self.x**2+self.y**2)**(1/2)
    
    def angulo(self):
        return math.atan(self.y/self.x)*(180/math.pi)
    
    def angulo_vec(self,other):
        m1=self.y/self.x
        m2=other.y/other.x
        return math.atan((m2-m1)/(1+m1*m2))*(180/math.pi)
    
    def multScalar(self,k):
        return Vec2D(self.x*k,self.y*k)



a = Vec2D(1,1)
b = Vec2D(2,2)
print(a.angulo())
print(a.angulo_vec(b))