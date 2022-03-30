# A simple script to calculate BMI
from functools import partial
import makeTex as mt
import pywebio
from pywebio.input import *
from pywebio.output import *
from zipfile import ZipFile


class APP:

    def __init__(self):
        self.ALIVE = False

    def processImage(self, null, imgs):
        zip = ZipFile('figures.zip', mode='w')
        # writing each file one by one
        for i in imgs:
            f = open(i['filename'], 'wb')
            f.write(i['content'])
            zip.write(i['filename'])
            put_file(i['filename'], i['content'], 'download ' + i['filename'])
        zip.close()
        zip = open('figures.zip', 'rb').read()
        put_file('figures.zip', zip, 'download figures.zip')

    def processLatex(self, null, file):
        mt.make(file)
        file = open("outTexFile.tex", 'rb').read()
        put_file("outTexFile.tex", file, 'download outTexFile.tex')

    def process(self, content, isImg):
        self.START()
        if isImg:
            count = 1
            imgs = []
            for img in content:
                img['filename'] = "figure" + str(count) + ".png"
                put_html('<br>')
                put_image(img['content'], width="400xp")
                put_text(img['filename'])
                count += 1
                imgs.append(img)
            buttonTxt = "Save and rename images for latex"
            onclick = partial(self.processImage, imgs=imgs)
        else:
            file = content['content'].decode("utf-8")
            put_text(file)
            buttonTxt = "Convert txt raw to latex instructions"
            onclick = partial(self.processLatex, file=file)

        put_html('<br>')
        put_buttons([buttonTxt], onclick=onclick)

    def fileUpload(self):
        self.process(file_upload("Choose your input base file:", accept="text/*", required=True, multiple=False), False)

    def textArea(self):
        self.process(textarea('Raw text:', placeholder="Please input your text", required=True), False)

    def uploadImg(self):
        self.process(file_upload("Choose your input images:", accept="image/*", required=True, multiple=True), True)

    def initNav(self):
        url1 = "https://www.bing.com/videos/search?q=overleaf&&view=detail&mid" \
               "=2DC76EBCD6D5943620AF2DC76EBCD6D5943620AF&&FORM=VRDGAR&ru=%2Fvideos%2Fsearch%3Fq%3Doverleaf%26%26FORM" \
               "%3DVDVVXX/ "
        url2 = "https://www.bing.com/search?q=overleaf/ "
        put_markdown('# **_Latex Converter, From Plain Text_**')
        put_link(name="Overleaf Latex Compiler", url="https://www.overleaf.com/project", new_window=True)
        put_html('<br>')
        put_tabs([
            {'title': 'Intro to OverLeaf',
             'content': put_html('<iframe width=810xp height=350xp src=%s></iframe>' % url1)},
            {'title': 'OverLeaf Compiler',
             'content': put_html('<iframe width=810xp height=350xp src=%s></iframe>' % url2)}
        ])
        put_markdown('This is a LaTex converter, the input is plain text formatted by the parsing rules '
                     'indicated blow.\n\nIf the tab "OverLeaf Compiler does not open please click on the '
                     'blue highlighted hyperlink, placed above the picture in picture.')
        put_html('<br>')
        put_markdown('### *Raw text rules*')
        put_text("Below are 3 buttons, the first button and the second button converts a plain text to a '.tex' file "
                 "download.\n"
                 "The second button server the same purpose a the first but instead of uploading a '.txt' file you may "
                 "edit within.\n"
                 "The third button will take all the image prep them and return them to a zip file.\n"
                 "With both the latex file and the photo zip we can copy it into overleaf and compiler it to a "
                 "professional formatted pdf.")
        put_html('<hr>')
        put_markdown('These are the flags to indicate all the formmating componets')
        put_markdown('Your Section Header: `~`[XXXX]')
        put_markdown('Your SubSection Header: `~~`[XXXX]')
        put_markdown('Your Figures Identifier: `@@`[XXXX]')
        put_markdown('The order of content is perverse from the plain text, so text in plain text without flags '
                     'belongs to the figure below it.')
        put_html('<hr>')
        put_buttons(['Upload file', 'Type text', 'Upload image'],
                    onclick=[self.fileUpload, self.textArea, self.uploadImg])
        put_html('<hr>')

    def START(self):
        if not self.ALIVE:
            self.ALIVE = True
            clear()
            self.initNav()
            self.fileUpload()
        else:
            clear()
            self.initNav()


if __name__ == '__main__':
    app = APP()
    pywebio.start_server(app.START(), port=51)
