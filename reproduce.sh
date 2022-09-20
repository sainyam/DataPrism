a="on"
while getopts a: flag
do
    case "${flag}" in
        a) a=${OPTARG};;
    esac
done

python cleanup.py
sh Figure6.sh -a "${a}" 
sh Figures_8_and_9.sh -a "${a}" 
