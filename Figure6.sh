a="on"
while getopts a: flag
do
    case "${flag}" in
        a) a=${OPTARG};;
    esac
done


#cd adult/
#python Ouralgo_new.py
#cd ../tweets
#python Ouralgo.py
#cd ../bmi
#python Ouralgo.py
#cd ../flights
#python Ouralgo_new.py
cd amazon
python Ouralgo.py
cd ../opendata
python Ouralgo.py
cd ../physicians
python Ouralgo.py
cd ../
python run_baselines_fig6.py "${a}"
python read_output_fig6.py
