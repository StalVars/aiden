# bash /home/svaranasi/run_docker.sh --mem 150G  -p V100-32GB bash scripts/whisper.sh
python=/netscratch/butt/miniconda3/envs/aiden_whisper/bin/python
echo "In shell script"

$python whisper_try.py /netscratch/butt/aiden/data "base"