import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy


class Particle :
    def __init__(self, _type, _mass, _radius, _pos, _vel) :
        self.type = _type
        self.mass = _mass
        self.radius = _radius
        self.pos = _pos
        self.vel = _vel
    
    def is_in(self) :
        if abs(self.pos[0]) < HALF_LENGTH and abs(self.pos[1]) < HALF_LENGTH :
            return True
        else :
            return False

    def update(self) :
        self.pos += self.vel

    def wall_collide(self, vent_left, vent_right) :
        if self.is_in() :
            nx, ny = self.pos + self.vel
            if vent_left < nx < vent_right and ny > HALF_LENGTH :
                return
            if abs(nx) >= HALF_LENGTH :
                self.vel[0] *= -1
            if abs(ny) >= HALF_LENGTH :
                self.vel[1] *= -1


def collide(particle1, particle2) :
    m1, m2 = particle1.mass, particle2.mass
    r1, r2 = particle1.radius, particle2.radius
    p1, p2 = particle1.pos, particle2.pos
    v1, v2 = particle1.vel, particle2.vel

    disp = (p1 - p2) ** 2
    dist = disp.sum()
    u1, u2 = v1, v2
    if dist <= r1 + r2 :
        u1 = (m1 - m2) / (m1 + m2) * v1 + 2 * m2 / (m1 + m2) * v2
        u2 = 2 * m1 / (m1 + m2) * v1 + (m2 - m1) / (m1 + m2) * v2
    
    return u1, u2


##### main #####
MAXFRAME = 5000
PARTICLE_NUM = 10000
HALF_LENGTH, VENT_SIZE = 10.0, 1.0
MASS, RADIUS, SPEED_STDDEF = 1.0, 0.1, 1.0
RACORD_NUM = 100

for try_cnt in range(1, 11) :
    in_count = [[] for i in range(9)]

    particles_list = list()
    for i in range(PARTICLE_NUM) :
        particles_list.append(Particle('GAS', MASS, RADIUS, 2 * HALF_LENGTH * np.random.rand(2) - HALF_LENGTH, np.random.normal(0, SPEED_STDDEF, 2)))

    for vent_loc in range(-4, 5) :
        vent_left, vent_right = (HALF_LENGTH / 5) * vent_loc - VENT_SIZE / 2, (HALF_LENGTH / 5) * vent_loc + VENT_SIZE / 2

        particles = copy.deepcopy(particles_list)
        px = [[] for i in range(RACORD_NUM)]
        py = [[] for i in range(RACORD_NUM)]

        for frame in range(1, MAXFRAME + 1) : 
            if frame % 100 == 0 :
                print("try:", try_cnt, "\tvent_loc:", vent_loc ,"\tFrame:", frame)

            for i in range(len(particles)) :
                for j in range(i) :
                    p1, p2 = particles[i], particles[j]
                    p1.vel, p2.vel = collide(p1, p2)
                
            for p in particles :
                p.wall_collide(vent_left, vent_right)
                p.update()

            in_cnt = 0
            for p in particles :
                if p.is_in() :
                    in_cnt += 1
            in_count[vent_loc + 4].append(in_cnt)

            for i in range(RACORD_NUM) :
                px[i].append(particles[i].pos[0])
                py[i].append(particles[i].pos[1])
        
        ### Record Particles' movement ###
        plt.xlim(-HALF_LENGTH - 5, HALF_LENGTH + 5)
        plt.ylim(-HALF_LENGTH - 5, HALF_LENGTH + 5)
        for i in range(RACORD_NUM) :
            plt.plot(px[i], py[i], linewidth = 3)
        plt.savefig('Particle Exercise' + ' MAXFRAME' + str(MAXFRAME) + ' RACORD_NUM' + str(RACORD_NUM) + ' VENT_LOC' + str((HALF_LENGTH / 5) * vent_loc) + '.png')

    df = pd.DataFrame(in_count, index = [(HALF_LENGTH / 5) * i for i in range(-4, 5)])
    df = df.T

    df.to_csv('Particle Count' + ' MAXFRAME' + str(MAXFRAME) + ' NUM' + str(PARTICLE_NUM) + ' LENGTH' + str(HALF_LENGTH) + ' VENT_SIZE' + str(VENT_SIZE) + '_' + str(try_cnt) + '.csv')

    df.plot()
    plt.legend(loc = 'best')
    plt.savefig('Particle Count' + ' MAXFRAME' + str(MAXFRAME) + ' NUM' + str(PARTICLE_NUM) + ' LENGTH' + str(HALF_LENGTH) + ' VENT_SIZE' + str(VENT_SIZE) + '_' + str(try_cnt) + '.png')
