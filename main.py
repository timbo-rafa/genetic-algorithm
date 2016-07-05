import controller
import argparse

def parse_arguments():
  parser = argparse.ArgumentParser(prog="python3 main.py",
    description="A parallel genetic algorithm implementation for the TSP problem")
  parser.add_argument("-i", "--independent", type=int, metavar="N",
    help="Number of independent populations", required=True)
  parser.add_argument("-p", "--populations", type=int, metavar="N",
    help="Population size (number of chromosomes per population)", required=True)
  parser.add_argument("-w", "--workers", type=int, metavar="N",
    help="Number of pool workers (parallelism)", required=True)
  parser.add_argument("-g", "--generations", type=int, help="Number of iterations", metavar="N",
    required=True)
  parser.add_argument("-e", "--elite", type=int, help="Number of elite individuals",
    metavar="N", required=True)
  parser.add_argument("-m", "--mprobability", type=float, metavar="F",
    help="Probability of mutation occurring", required=True)
  parser.add_argument("-n", "--cities", type=int, help="Number of cities (in the graph)",
    metavar="N", default=200)
  parser.add_argument("-x", "--exchange", type=int, metavar="N",
    help="Number of generations required to exchange individuals", default=50)
  parser.add_argument("-s", "--stop", type=int, metavar="N",
    help="Number of idle generations required to stop algorithm", default=999999)
  parser.add_argument("-l", "--latex", action="store_true", help="Output in latex format")
  parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity")
  return parser.parse_args()

if __name__ == '__main__':
  args = parse_arguments()
  controller.run(exchange_after=args.exchange, stop_after=args.generations,
    generations=args.generations, cities=args.cities, population_size=args.populations,
    elite_size=args.elite, mutation_probability=args.mprobability)
  controller.run(exchange_after=20, stop_after=1000, generations=900, cities=200,
    population_size=220, elite_size=20, mutation_probability=0.20)

