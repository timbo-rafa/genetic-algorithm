from nose.tools import assert_equal, assert_not_equal
from mock import patch
from itertools import repeat

# please export tsp root folder to PYTHONPATH
# export PYTHONPATH=.
from tsp.ga import GA
from tsp.graph import Graph
from tsp.chromosome import Chromosome
from tsp.args import ArgsStrings, parse_arguments
import sys

_multiprocess_can_split_ = True


def test_parse_arguments_bool():
  with patch.object(sys, "argv", ["./main.py"]):
    args = parse_arguments()
    assert_equal(args.latex  , False)
    assert_equal(args.verbose, False)

def test_parse_arguments_all():
  argstr = ArgsStrings()
  test_args = [ "./main.py"   ,
    argstr.populations.short  , "8"     ,
    argstr.chromosomes.short  , "440"   ,
    argstr.workers.short      , "4"     ,
    argstr.generations.short  , "5555"  ,
    argstr.elite.short        , "40"    ,
    argstr.mprobability.short , "0.123" ,
    argstr.cities.short       , "124"   ,
    argstr.exchange.short     , "66"    ,
    argstr.latex.short        ,
    argstr.verbose.short      ]
  with patch.object(sys, "argv", test_args):
    args = parse_arguments()
    assert_equal(args.populations , 8     )
    assert_equal(args.chromosomes , 440   )
    assert_equal(args.workers     , 4     )
    assert_equal(args.generations , 5555  )
    assert_equal(args.elite       , 40    )
    assert_equal(args.mprobability, 0.123 )
    assert_equal(args.cities      , 124   )
    assert_equal(args.exchange    , 66    )
    assert_equal(args.latex       , True  )
    assert_equal(args.verbose     , True  )
