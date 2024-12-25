import random
from random import randint
from copy import deepcopy


def get_ans(data, num=2):
    A, B, C, instructions = format_data(data)

    def getValue(A, B, C, instructions):
        operandMap = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: A,
            5: B,
            6: C,
            7: 'err'
        }
        index = 0
        output = []
        while index + 1 < len(instructions):
            opcode = instructions[index]
            comboOperand = operandMap[instructions[index + 1]]
            literalOperand = instructions[index + 1]
            if opcode == 0:
                operandMap[4] = operandMap[4] // (2 ** comboOperand)
            elif opcode == 1:
                operandMap[5] = operandMap[5] ^ literalOperand
            elif opcode == 2:
                operandMap[5] = comboOperand % 8
            elif opcode == 3:
                if not operandMap[4] == 0:
                    index = literalOperand - 2
            elif opcode == 4:
                operandMap[5] = operandMap[5] ^ operandMap[6]
            elif opcode == 5:
                output.append(comboOperand % 8)
            elif opcode == 6:
                operandMap[5] = operandMap[4] // (2 ** comboOperand)
            elif opcode == 7:
                operandMap[6] = operandMap[4] // (2 ** comboOperand)
            index = index + 2

        return output

    if num == 1:
        output = getValue(A, B, C, instructions)
        return ','.join([str(i) for i in output])
    else:

        class Genome:
            def __init__(self, genome=None):
                if genome is None:
                    self.__genome = []
                    for i in range(16):
                        self.__genome.append(randint(0, 7))
                else:
                    self.__genome = genome

            def getArrNum(self):
                ret = 0
                for i in range(len(self.__genome)):
                    ret = ret + self.__genome[i] * 8 ** i
                return ret

            def getGenome(self):
                return deepcopy(self.__genome)

        def getValueWrapper(A):
            return getValue(A, B, C, instructions)

        def getFitness(genome):
            if genome.getArrNum() >= 266932601928721:
                return -(8 ** 16)
            value = getValueWrapper(genome.getArrNum())
            fitness = 0
            for i in range(len(instructions)):
                if i >= len(value):
                    fitness = fitness - 8 ** (i + 1)
                else:
                    fitness = fitness - (abs(value[i] - instructions[i])) * 8 ** i
            return fitness

        def geneticAlgorithm(popSize=1000, mutationChance=(1, 10)):
            population = []
            for i in range(popSize):
                population.append((Genome(), 1))

            while not population[0][1] == 0:
                for i in range(len(population)):
                    genome, fitness = population[i]
                    if fitness == 1:
                        population[i] = (genome, getFitness(genome))
                population.sort(key=lambda x: x[1], reverse=True)
                best, bestFitness = population[0]
                print(best.getGenome(), bestFitness)
                print(getValueWrapper(best.getArrNum()))
                print(instructions)
                print()
                while len(population) > popSize / 2:
                    population.pop()

                def createNewGenome(genome1, genome2):
                    dna1 = genome1.getGenome()
                    dna2 = genome2.getGenome()
                    newDNA = []
                    for i in range(len(dna1)):
                        prob = randint(1, 2)
                        if prob == 1:
                            newDNA.append(dna1[i])
                        else:
                            newDNA.append((dna2[i]))
                    a, b = mutationChance
                    if a <= randint(1, b):
                        index = randint(0, len(newDNA) - 1)
                        newDNA[index] = randint(0, 7)
                    return Genome(newDNA)

                newPop = []
                while len(population) + len(newPop) < popSize:
                    p1 = population[randint(0, len(population) - 1)][0]
                    p2 = population[randint(0, len(population)) - 1][0]
                    newPop.append(createNewGenome(p1, p2))

                for i in newPop:
                    population.append((i, 1))
            return population[0][0]

        return geneticAlgorithm().getArrNum()


def format_data(data):
    data = data.split('\n\n')

    def getRegisterValue(reg):
        return int(reg[reg.find(':') + 1:])

    registers = data[0].split('\n')
    A = getRegisterValue(registers[0])
    B = getRegisterValue(registers[1])
    C = getRegisterValue(registers[2])
    instructions = [int(i) for i in data[1][data[1].find(':') + 1:].split(',')]
    return A, B, C, instructions
