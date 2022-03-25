import turtle
import random as rd

wn = turtle.Screen()
wn.title("Charged Particle Animation")
wn.bgcolor("white")


class Particle(turtle.Turtle):
    def __init__(self, walls, prob_negative, mass):
        self.walls = walls #all particles are bound by the same walls
        self.prob_negative = prob_negative
        turtle.Turtle.__init__(self)
        self.penup()
        self.setposition(rd.uniform(-walls[0], walls[0]), rd.uniform(-walls[1], walls[1])) #x, y coord
        self.shape("circle")
        self.mass = mass
        self.velocity = [0, 0]
        if rd.random() < self.prob_negative: # probability of a negative
            self.color("blue")
            self.charge = -1
        else:
            self.color("red")
            self.charge = 1
        
    def move(self, velocity): #velocity is a list, walls flag can be set for collisions
        if abs(list(self.position())[0] + velocity[0]) > self.walls[0]: #if you're about to step outside horizontally
            velocity[0] *= -1 #bounce
        if abs(list(self.position())[1] + velocity[1]) > self.walls[1]: #if you're about to step outside vertically
            velocity[1] *= -1 #bounce
        self.goto(list(self.position())[0] + velocity[0], list(self.position())[1] + velocity[1])
        
def update_velocity(particles, k):
    for particle in particles:
        for other_particle in particles:
            if particle != other_particle:
                r_squared = ((list(other_particle.position())[0] - list(particle.position())[0])**2) + ((list(other_particle.position())[1] - list(particle.position())[1])**2)
                force = k*particle.charge*other_particle.charge/r_squared
                unit_vector = [(list(particle.position())[0] - list(other_particle.position())[0])/(r_squared**0.5), (list(particle.position())[1] - list(other_particle.position())[1])/(r_squared**0.5)]
                particle.velocity = [particle.velocity[0] + (1/(particle.mass))*force*unit_vector[0], particle.velocity[1] + (1/(particle.mass))*force*unit_vector[1]]


def watch_n_particles_go(n, walls = [100, 100], prob_negative = 0, mass = 1, k = 20):
    t = turtle.Turtle() #draw walls
    t.penup()
    l = walls[0]*2
    w = walls[1]*2
    t.forward(walls[0]) 
    t.left(90) 
    t.pendown()
    t.forward(walls[1])
    t.left(90) 
    t.forward(l) 
    t.left(90) 
    t.forward(w) 
    t.left(90) 
    t.forward(l)
    t.left(90)
    t.forward(walls[1])
    t.left(90)
    particles = [Particle(walls, prob_negative, mass) for _ in range(n)]
    while True:
        update_velocity(particles, k)
        for particle in particles:
            particle.move(particle.velocity)
            
watch_n_particles_go(10)
