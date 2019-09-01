import retro
import numpy as np
import cv2
import neat
import pickle
import warnings
import sys
import visualize

warnings.filterwarnings("ignore", category=RuntimeWarning)

env = retro.make('DonkeyKongCountry-Snes')

imgarray = []

resume = False

if len(sys.argv) == 2:
    resume = True
    restore_file = 'neat-checkpoint-{}'.format(sys.argv[1])


def eval_genomes(genomes, config):
    global generation_max_fitness
    for genome_id, genome in genomes:
        ob = env.reset()
        action = env.action_space.sample()

        inx, iny, inc = env.observation_space.shape

        inx = int(inx/8)
        iny = int(iny/8)

        net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)

        current_max_fitness = 0
        fitness_current = 0
        frame = 0
        counter = 0
        xpos = 0
        xpos_max = 0
        
        done = False
        cv2.namedWindow("main", cv2.WINDOW_NORMAL)

        while not done:
            env.render()
            frame += 1
            scaledimg = cv2.cvtColor(ob, cv2.COLOR_BGR2RGB)
            scaledimg = cv2.resize(scaledimg, (iny, inx)) 

            ob = cv2.resize(ob, (inx, iny))
            ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
            ob = np.reshape(ob, (inx, iny))
            cv2.imshow('main', scaledimg)
            cv2.waitKey(1)

            for x in ob:
                for y in x:
                    imgarray.append(y)
            

            nnOutput = net.activate(imgarray)
            
            ob, rew, done, info = env.step(nnOutput)

            imgarray.clear()

            xpos = info['x']

            fitness_current += rew * 5

            if xpos > xpos_max:
                fitness_current += 0.25
                xpos_max = xpos

            if xpos_max >= 5120:
                    fitness_current += 1200
                    done = True
            
            if fitness_current > current_max_fitness:
                current_max_fitness = fitness_current
                counter = 0
            else:
                counter += 1

            if done or counter == 140:
                if fitness_current <= 15:
                    fitness_current = 0
                else:
                    fitness_current -= 15
                done = True
                print('ID:', genome_id, "Fitness:", fitness_current, "Max Position X:", xpos_max)
            
            genome.fitness = fitness_current


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation, 'config-feedforward')

if resume == True:
    try:
        p = neat.Checkpointer.restore_checkpoint(restore_file)
    except:
        print("ERROR: checkpoint doesn't exist")
        exit()

else:
    p = neat.Population(config)

p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
p.add_reporter(neat.Checkpointer(10))

winner = p.run(eval_genomes)

with open('winner.pkl', 'wb') as output:
    pickle.dump(winner, output, 1)
