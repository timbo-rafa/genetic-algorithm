import argparse
import multiprocessing as mp

class Dictionary(dict):
  def __getattr__(self, attr):
    return self.get(attr)
  def __setattr__(self, key, value):
    self.__setitem__(key, value)
  def __delattr__(self, item):
    self.__delitem__(item)

class ArgsStrings(Dictionary):
  def __init__(self):
    self.arglist = [ "populations", "chromosomes", "workers",
      "generations", "elite", "mprobability", "cities",
      "exchange", "latex", "verbose" ]

    for opt in self.arglist:
      self[opt] = Dictionary()
      self[opt].string = "--" + opt
    self["populations"].short  = "-p"
    self["chromosomes"].short  = "-c"
    self["workers"].short      = "-w"
    self["generations"].short  = "-g"
    self["elite"].short        = "-e"
    self["mprobability"].short = "-m"
    self["cities"].short       = "-n"
    self["exchange"].short     = "-x"
    self["latex"].short        = "-l"
    self["verbose"].short      = "-v"

def parse_arguments():
  argstr = ArgsStrings()

  parser = argparse.ArgumentParser(prog="python3 main.py",
    description=
    """A parallel genetic algorithm implementation for the TSP problem.
      This program will generate p independent populations with w workers each.
      It is recommended that p times w equals the number of cpu cores""")
  parser.add_argument(argstr.populations.short, argstr.populations.string,
    type=int, metavar="N", help="""Number of independent populations.
    This will use p processes.
    Recommended 1 <= p <= cpu_count""", default=max(1,mp.cpu_count()//2))
  parser.add_argument(argstr.chromosomes.short, argstr.chromosomes.string,
    type=int, metavar="N",
    help="Population size (number of chromosomes per population)",
    default=420)
  parser.add_argument(argstr.workers.short, argstr.workers.string,
    type=int, metavar="N",
    help="""Number of pool workers.
    This divides population size c into w processes.
    1 <= w <= cpu_count""", default=2)
  parser.add_argument(argstr.generations.short, argstr.generations.string,
    type=int, help="Number of iterations", metavar="N", default=2000)
  parser.add_argument(argstr.elite.short, argstr.elite.string,
    type=int, help="Number of elite individuals", metavar="N", default=20)
  parser.add_argument(argstr.mprobability.short, argstr.mprobability.string,
    type=float, metavar="F",
    help="Probability of mutation occurring", default=0.20)
  parser.add_argument(argstr.cities.short, argstr.cities.string,
    type=int, help="Number of cities (in the graph)",
    metavar="N", default=200)
  parser.add_argument(argstr.exchange.short, argstr.exchange.string,
    type=int, metavar="N",
    help="Number of generations required to exchange individuals",
    default=80)
  parser.add_argument(argstr.latex.short, argstr.latex.string,
    action="store_true", help="Output in latex format")
  parser.add_argument(argstr.verbose.short, argstr.verbose.string,
    action="store_true", help="Verbosity")
  return parser.parse_args()
