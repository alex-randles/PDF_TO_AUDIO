VAR1='/home/alex/PycharmProjects/Summer-Projects/research_paper_reader/static/audio_files/'
VAR2=$1
VAR3="$VAR1$VAR2"
pico2wave -w=$VAR3 "$2"
# aplay $VAR4
# rm $file_name