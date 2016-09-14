#!/usr/bin/python3
from args import parse_arguments
import controller

if __name__ == '__main__':
  args = parse_arguments()
  controller.run(exchange_after=args.exchange, stop_after=args.stop,
    generations=args.generations, cities=args.cities, population_size=args.chromosomes,
    elite_size=args.elite, mutation_probability=args.mprobability,
    independent_populations=args.populations, number_workers=args.workers,
    verbose=args.verbose, latex=args.latex)

