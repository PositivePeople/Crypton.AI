from flask import Flask, render_template, request
from openai import OpenAI
client = OpenAI()
from pdfquery import PDFQuery
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import shutil

pdf = PDFQuery('linac.pdf')
pdf.load()

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET"])
def index():
    print("Hello World")
    return render_template("index.html")


@app.route("/quiz", methods=["GET", "POST"])
def register():
    """Register user"""
    app.run(debug=True)
    if request.method == "GET":
        print("Get Request Quiz Page")
        return render_template("quiz.html")
    else:
        # Use CSS-like selectors to locate the elements
        text_elements = pdf.pq('LTTextLineHorizontal')

        # Extract the text from the elements
        list = [t.text for t in text_elements]
        text = ' '.join(list)

        # The following block of code shows how to summarize the prompt
        # {"role": "user", "content": "Extract definition for this keyword"}
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": text},
            {"role": "user", "content": "Extract 5 scientific keywords from the text and separate them with commas"}
            ]
        )
        keywords = completion.choices[0].message.content
        keywords = keywords.split(",")

        one = request.form.get("one")
        two = request.form.get("two")
        three = request.form.get("three")
        four = request.form.get("four")

        results = [one, two, three, four]
        visualcount = results.count("visual")
        auditorycount = results.count("auditory")
        readwritecount = results.count("read-write")
        kinestheticcount = results.count("kinesthetic")

        highest = visualcount
        style = "Visual"
        if auditorycount > highest:
            style = "Auditory"
        if readwritecount > highest:
            style = "Read/Write"
        if kinestheticcount > highest:
            style = "Kinesthetic"

        img1 = ""
        img2 = ""
        img3 = ""
        img4 = ""
        img5 = ""
        key1 = keywords[0]
        key2 = keywords[1]
        key3 = keywords[2]
        key4 = keywords[3]
        key5 = keywords[4]
        audio1 = ""
        audio2 = ""
        audio3 = ""
        audio4 = ""
        audio5 = ""
        read1 = ""
        read2 = ""
        read3 = ""
        read4 = ""
        read5 = ""
        define1 = ""
        define2 = ""
        define3 = ""
        define4 = ""
        define5 = ""

        if style == "Visual":
            urls = ['', '', '', '', '']
            for x in range(0,5):
                word = keywords[x]
                url = 'https://www.google.com/search?q={0}&tbm=isch'.format(word)
                content = requests.get(url).content
                soup = BeautifulSoup(content,'lxml')
                images = soup.findAll('img')

                image = images[2]
                image = image['src']
                urls[x] = image
            img1 = urls[0]
            img2 = urls[1]
            img3 = urls[2]
            img4 = urls[3]
            img5 = urls[4]
            

        if style == "Auditory":
            speech_file_path = Path(__file__).parent / "audio1.mp3"
            response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=keywords[0]
            )
            response.stream_to_file(speech_file_path)
            
            speech_file_path = Path(__file__).parent / "audio2.mp3"
            response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=keywords[1]
            )
            response.stream_to_file(speech_file_path)
            speech_file_path = Path(__file__).parent / "audio3.mp3"
            response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=keywords[2]
            )
            response.stream_to_file(speech_file_path)
            speech_file_path = Path(__file__).parent / "audio4.mp3"
            response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=keywords[3]
            )
            response.stream_to_file(speech_file_path)
            speech_file_path = Path(__file__).parent / "audio5.mp3"
            response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=keywords[4]
            )
            response.stream_to_file(speech_file_path)
            audio1 = "audio1.mp3"
            audio2 = "audio1.mp3"
            audio3 = "audio1.mp3"
            audio4 = "audio1.mp3"
            audio5 = "audio1.mp3"
            shutil.move('audio1.mp3', 'static/audio1.mp3')
            shutil.move('audio2.mp3', 'static/audio2.mp3')
            shutil.move('audio3.mp3', 'static/audio3.mp3')
            shutil.move('audio4.mp3', 'static/audio4.mp3')
            shutil.move('audio5.mp3', 'static/audio5.mp3')
        
        #if style == "Read/Write":
            #completion = client.chat.completions.create(
            #model="gpt-3.5-turbo",
            #messages=[
            #{"role": "system", "content": keywords},
            #{"role": "user", "content": "Explain each keyword briefly, separate explanations with comma"}
            #]
            #)
            #define = completion.choices[0].message.content
            #define = keywords.split(",")
            #define1 = define[0]
            #define2 = define[1]
            #define3 = define[2]
            #define4 = define[3]
            #define5 = define[4]

        #if style == "Kinesthetic":
            #Web scrape GIF, animation, simulation URL, experiment URL
    
                                      
        string = "Your Learning Style is {style}".format(style = style)

        return render_template("quiz.html", mycontent = string, type = style, img1 = img1, img2 = img2, img3 = img3, img4 = img4, img5 = img5, key1 = key1, key2 = key2, key3 = key3, key4 = key4, key5 = key5, audio1 = audio1, audio2 = audio2, audio3 = audio3, audio4 = audio4, audio5 = audio5, define1 = define1, define2 = define2, define3 = define3, define4 = define4, define5 = define5 )


