a="off"
while getopts a: flag
do
    case "${flag}" in
        a) a=${OPTARG};;
    esac
done


cd flights/
pip install -e DataInsights

cd ../adult/
python Ouralgo.py
cd ../tweets
python Ouralgo.py
cd ../bmi
python Ouralgo.py
cd ../flights
python Ouralgo.py
cd ../amazon
python Ouralgo.py
cd ../opendata
python Ouralgo.py
cd ../physicians
python Ouralgo.py
cd ../
bash Figure7.sh


mv datasets/adult/*.csv Examples/adult/
mv datasets/adult/*.txt Examples/adult/


mv datasets/amazon/*.csv Examples/amazon/

mv datasets/bmi/*.csv Examples/bmi/

mv datasets/flights/*.csv Examples/flights/

mv datasets/opendata/*.csv Examples/opendata/


mv datasets/physicians/*.csv Examples/physicians/

mv datasets/tweets/* Examples/tweets/


python run_baselines_fig6.py "${a}"
python read_output_fig6.py
