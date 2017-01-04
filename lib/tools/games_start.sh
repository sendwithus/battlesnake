:<<__

Run this from the root of the project

__

number_of_games=64
echo `pwd`

for x in `eval echo {1..${number_of_games}}`; do
  echo $x python ./lib/tools/create_games.py;
  (python ./lib/tools/create_games.py) &
done
