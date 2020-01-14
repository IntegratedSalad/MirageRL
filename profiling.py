from engine import main
from engine_functions.new_game import init_game
import cProfile
import pstats

init_game()
cProfile.run('main()', 'profiling')

data = pstats.Stats('profiling')

data.sort_stats('calls')
data.print_stats()
