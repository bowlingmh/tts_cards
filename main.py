from PIL import Image, ImageFont, ImageDraw
import io
import flask

app = flask.Flask(__name__)

def draw_text(img, text, textcolor, fontsize, padding=50):
    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', fontsize)
    draw = ImageDraw.Draw(img)

    lines = text.split('\n')

    _, line_height = draw.textsize(lines[0], font=font)
    height = line_height * len(lines)

    for i, line in enumerate(lines):
        w, h = draw.textsize(line, font=font)
        pos = ((img.width - w)//2, (img.height - height)//2 + line_height * i)
        print(pos, textcolor, line)
        draw.text(pos,line,textcolor,font=font)

@app.route('/card')
def card():
    bgcolor = flask.request.args.get('bgcolor', 'white')
    textcolor = flask.request.args.get('textcolor', 'black')
    text = flask.request.args.get('text', '')
    fontsize = flask.request.args.get('fontsize', 48)

    img = Image.new('RGB', (500, 720), color=bgcolor)
    draw_text(img, text, 'white', fontsize)

    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return flask.send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run()
    
