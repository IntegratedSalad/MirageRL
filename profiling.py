from engine import main
import cProfile
import pstats


cProfile.run('main()', 'profiling')

data = pstats.Stats('profiling')

data.sort_stats('calls')
data.print_stats()
