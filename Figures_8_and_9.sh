a="on"
while getopts a: flag
do
    case "${flag}" in
        a) a=${OPTARG};;
    esac
done

mv datasets/*SIGMOD* .

python ouralgo_experiments_synth.py
python ouralgo_experimentsgrptest.py
python run_baselines.py "${a}"
python figure9.py