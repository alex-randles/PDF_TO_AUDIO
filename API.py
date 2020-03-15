from flask import Flask, render_template, request, send_file, send_from_directory
from flask_caching import Cache
from read_paper import read_paper 
from werkzeug import secure_filename
import os 
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# to prevent caching of previous result
file_counter = 0
app.config["allowed_file_extensions"] = ["pdf"]
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["AUDIO_FOLDER"] =  "/home/alex/PycharmProjects/Summer-Projects/research_paper_reader/static/audio_files"


@app.route('/', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      # get file uploaded
      file = request.files['file']

      if file:
         # will default to None
         start_page = request.form.get('start_page', None)
         end_page = request.form.get('end_page', None)

         # save file
         filename = secure_filename(file.filename)
         file_extension = filename.split(".")[1]
         print(file_extension)
         if file_extension in app.config["allowed_file_extensions"]:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print("file path:", file_path)
            saved_file = file.save(file_path)
            global file_counter
            global wav_file_name

            wav_file_name = filename.split(".")[0] + ".wav"
            audio_filename = read_paper(file_path, start_page, end_page, wav_file_name)

            # get path of saved files
            audio_file_path = "audio_files" + "/" + wav_file_name
            uploaded_file_path = app.config['UPLOAD_FOLDER'].split("/")[1] + "/" + filename

            file_counter += 1

            # display files
            print("audio file_path", audio_file_path)
            return render_template('display.html', uploaded_file= uploaded_file_path, audio_file=audio_file_path)
         else:
            return render_template('display.html', error_message="Wrong file type uploaded")
      else:
         return render_template('display.html', error_message = "Please upload a file!")
   else:
      # remove old audio files
      file_list = [f for f in os.listdir(app.config["AUDIO_FOLDER"])]
      for f in file_list:
         file_path = os.path.join(app.config["AUDIO_FOLDER"], f)
         print("removed file:", file_path)
         os.remove(file_path)
      return render_template('upload.html')

@app.route("/download-file/", methods=["GET"])
def return_file():
    download_path = app.config["AUDIO_FOLDER"] + "/" +  wav_file_name
    return send_file(download_path,as_attachment=True, cache_timeout=0)
      
		
if __name__ == '__main__':
   app.cache = {}
   app.run(debug = True, threaded=True)
