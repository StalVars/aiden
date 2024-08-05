the whisper main repo branch doesnt have batch transcription. I found a fork which added this and is in process of being merged to the main. https://github.com/Blair-Johnson/batch-whisper. Its a little behind but i didnt find any major release on main branch between its forking and till now



Structure:

    AIDEN
        whisper_try.py
        data
            [audio mp3 files]
        output
            model transcriptions output
        scripts
            script to run whisper_try

Library installation:
pip install whisper
sudo apt-get install ffmpeg

How to run:
    To run python program:
        python whisper_try.py /netscratch/butt/aiden/data "base" (although this 2nd argument of model variant isnt used at the moment as it     tests on all the variants of whisper)

    To run bash script:
        bash /home/svaranasi/run_docker.sh --mem 150G  -p V100-32GB bash scripts/whisper.sh


Output structure:
File name represents the mp3 file it is about.
First filename is mentioned and then each model variant's transcription is written.
The time written with each variant is that variants' time for ALL the files ( AND NOT THAT FILE INDIVIDUALLY ). Thats because we use batch transcription.




~                                                                                                                                                                                                           
~                                                                                                                                                                                                           
~                                                            
