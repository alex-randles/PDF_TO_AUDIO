import pdftotext
import sys
import os 
import time
from gtts import gTTS



def read_paper(file_name, start_page, end_page, filename):
	with open(file_name, "rb") as f:
		pdf = pdftotext.PDF(f)

	# checking page boundaries
	if not start_page and not end_page:
		start_page = 0
		end_page = len(pdf)
	else:
		start_page = int(start_page)
		end_page = int(end_page)
		if start_page <= 1:
			start_page = 0
		if end_page >= len(pdf):
			end_page = len(pdf)
			print("tooo high")
		print(start_page, end_page, len(pdf), "try clause")
	sliced_pdf = [pdf[i] for i in range(start_page, end_page)]
	text_to_speak = " ".join(sliced_pdf)
	text_to_speak = text_to_speak.replace('"',"'")
	print(filename, "*************")
	# tts = gTTS(text_to_speak, "en")
	# tts.save('/home/alex/PycharmProjects/Summer-Projects/research_paper_reader/static/audio_files/' + filename)
	# audio_file_name = "speakText{}.wav".format(file_counter)
	os.system('./speakText.sh "{}" "{}"'.format(filename, text_to_speak))
	return filename

if __name__ == "__main__":
	read_paper(sys.argv[1]) 
