#!/usr/bin/python

#from matplotlib.backends.backend_svg import FigureCanvasSVG as FigureCanvas
from matplotlib.backends.backend_cairo import FigureCanvasCairo as FigureCanvas

from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import sys
from pprint import pformat

import insulaudit
import logging
logging.basicConfig( stream=sys.stdout )
log = logging.getLogger( 'data.timseries.hacking' )
log.setLevel( logging.DEBUG )

log.debug( 'hello world' )
data = {}

def get_opt_parser( ):
  from optparse import OptionParser
  usage = """usage = "usage: %prog [options] input output"""
  parser = OptionParser(usage=usage)
  parser.add_option("-q", "--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="don't print status messages to stdout")

  return parser

def get_series( name ):
  from insulaudit.data import glucose
  return glucose.load_file( name )

def giant_timeseries( ts ):
  PREFER = ( 120, 135 )
  SAFE = ( 70, 140 )

  fig = Figure( ( 20.3, 3.5 ), 300 )
  canvas = FigureCanvas(fig)

  ax = fig.add_subplot(111)


  preferspan = ax.axhspan( SAFE[0], SAFE[1],
                           facecolor='g', alpha=0.2,
                           edgecolor = '#003333',
                           linewidth=1
                         )

  # visualize glucose using stems
  markers, stems, baselines = ax.stem( ts.time, ts.value,
           linefmt='b:' )
  plt.setp( markers, color='red', linewidth=.5,
            marker='o'
          )
  plt.setp( baselines, marker='None' ) 
  fig.autofmt_xdate( )

  ax.set_title('glucose history')
  ax.grid(True)
  ax.set_xlabel('time')
  ax.set_ylabel('glucose mm/dL')
  return canvas

if __name__ == '__main__':
  print "Generate a chart of a timeseries."

  parser = get_opt_parser( )
  options, args = parser.parse_args( sys.argv )
  infile, outfile = args[ 1 ], args[ 2 ]
  if infile == '-':
    infile = sys.stdout

  data = get_series( infile )

  canvas = giant_timeseries( data )
  canvas.print_figure(outfile)




#####
# EOF
