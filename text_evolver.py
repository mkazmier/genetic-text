import random
import string

class GeneticEvolver:

   """Evolve a given template string from a random initial population 
      using genetic algorithm with tounament selection."""
       
   char_pool = string.ascii_letters + string.digits + string.punctuation + ' '
 
   def __init__(self, template, population_size=100, mutation_chance=.1, tournament_size=2):
      self.template = template
      self.population_size = population_size
      self.population = self.generate_initial_population()
      self.mutation_chance = mutation_chance
      self.tournament_size = tournament_size
     
   def generate_initial_population(self):
      """Generates random initial population containing letters, digits, punctuation and whitespace."""
      length = len(self.template)
      population = []
      for i in range(self.population_size):
      # initialise population with <size> random specimen
         rand_str = ''.join(random.choice(self.char_pool) for _ in range(length))
         population.append(rand_str)
      return population

   def fitness(self, specimen):
      """Assess the fitness of a specimen as the number of characters that need to be changed
         in order to arrive at the template"""
      correct = 0
      for i in range(len(self.template)): 
         if specimen[i] == self.template[i]:
            correct += 1
      return len(self.template) - correct   

   def crossover(self, parent_1, parent_2):
      """Create a child string as a crossover between two parents, i.e split one parent at random position
         and fill up to the length of the template with characters from the other parents, e.g:
            abcd x efgh -> abgh"""

      position = random.randint(0, len(parent_1))
      child = parent_1[:len(parent_1)-position] + parent_2[len(parent_1)-position:]
      return self.mutate(child)      

   def mutate(self, specimen):
      """Mutate the specimen based on the mutation chance. Mutation simply means replacing one randomly selected 
         character from the given string with a randomly selected character from the pool."""
      if random.random() < self.mutation_chance:
         return specimen.replace(random.choice(specimen), random.choice(self.char_pool))
      else:
         return specimen
  
   def select_parent(self):
      """Select a parent for the next generation using tournament selection - taking a random sample
         of size self.tournament_size and select the best within the sample. If more than one specimen
         have equal fitness, return a randomly selected one."""
      compete = random.sample(self.population, self.tournament_size)
      best = None
      for specimen in compete:
          if best == None or self.fitness(specimen) < self.fitness(best):
             best = specimen
          elif self.fitness(specimen) == self.fitness(best):
             best = random.choice(list((specimen, best)))
      return best

   def evolve(self):
      """Evolve the initial population into the template string and record the number of generations."""
      i = 0
      template = self.template
      match = False
      while not match:
         i += 1
         for specimen in self.population:
            if specimen == template:
               match = True

         best = None
         for specimen in self.population:
            if best == None or self.fitness(specimen) < self.fitness(best):
               best = specimen
         print("Generation %d\t| %d |\t%s" % (i, self.fitness(best), best))
              
         new_population = []
         while len(new_population) < self.population_size:
            parent_1 = self.select_parent()
            parent_2 = self.select_parent()
            new_population.append(self.crossover(parent_1, parent_2)) 
          
         self.population = new_population 

      print('\n'+'-'*25)    
      print("\nGenerations: %d" % i)
            
def main():
   import time

   print("Template:")
   template = input()

   print("Population size (d for default = 100):")
   population_size = input()
   if population_size == 'd':
      population_size = 100

   print("Mutation chance (d for default = 0.1):") 
   mutation_chance = input()
   if mutation_chance == 'd':
      mutation_chance = .1
   
   print("Tournament size (d for default = 2):")
   tournament_size = input()
   if tournament_size == 'd':
      tournament_size = 2

   evolver = GeneticEvolver(template, int(population_size), float(mutation_chance), int(tournament_size))
   start = time.time()
   evolver.evolve()
   end = time.time()
   elapsed = end - start
   print("Elapsed time: %4fs" % elapsed) 
   print('\n'+'-'*25)
 
if __name__ == "__main__":
   main()
