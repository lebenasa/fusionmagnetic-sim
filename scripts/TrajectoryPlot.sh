if [ $1 = '-h' -o $1 = "--help" ]; then
  echo "TrajectoryPlot.sh : Plot trajectory from file"
  echo "    USAGE :"
  echo "    TrajectoryPlot.sh <ion/electron> <filename>"
  exit
fi

if [ $1 = 'deuterium' ]; then
  echo "Plotting deuterium's trajectory. . ."
  X=11
elif [ $1 = 'tritium' ]; then
  echo "Plotting tritium's trajectory. . ."
  X=14
else
  echo "Plotting electron's trajectory. . ."
  X=17
fi

Y=$X+1

gnuplot << END_INPUT
plot for [i=$X:$Y] $2 using i title "Title ".columnhead(i)
END_INPUT
