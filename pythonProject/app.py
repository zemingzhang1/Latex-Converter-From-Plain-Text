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
        self.figureID = 1
        self.content = None
        self.imgs = []
        self.imgsNames = []

    def processImage(self, null):
        remove('order')
        remove('processImageView')
        remove('1stScrolable')
        remove('ImgBtn1')
        imgs = self.imgs
        zip = ZipFile('images/figures.zip', mode='w')
        put_scope('processImageView')
        put_scrollable(put_scope('scrollableResult'), height=650, keep_bottom=False, scope='processImageView')
        for i in imgs:
            i['filename'] = "figure" + str(self.figureID) + ".png"
            f = open("images/" + i['filename'], 'wb')
            f.write(i['content'])
            zip.write("images/" + i['filename'])
            put_image(i['content'], width="200xp", scope='scrollableResult')
            put_file('images/' + i['filename'], i['content'], 'download ' + i['filename'], scope='scrollableResult')
            self.figureID += 1
        zip.close()
        zip = open('images/figures.zip', 'rb').read()
        put_file('figures.zip', zip, 'download figures.zip', scope='processImageView')

    def processLatex(self, null, file):
        remove('showtxt')
        mt.make(file)
        file = open("latex/outTexFile.tex", 'rb').read()
        put_file("latex/outTexFile.tex", file, 'download outTexFile.tex')

    def showOrder(self, null):
        remove('order')
        remove('processImageView')
        put_scope('order')
        fig = 1
        put_scrollable(put_scope('scrollableShowImgOdr'), height=650, keep_bottom=False, scope='order')
        for i in self.imgs:
            put_image(i['content'], width="200xp", scope='scrollableShowImgOdr')
            put_text(str(fig), scope='scrollableShowImgOdr')
            fig += 1

    def reName(self, img, scope):
        clear(scope + 'in')
        if img in self.imgs:
            self.imgsNames.remove(img['filename'])
            self.imgs.remove(img)
            put_button('ReName', onclick=partial(self.reName, img=img, scope=scope), scope=scope + "in",
                       color='danger', outline=True)
        else:
            self.imgsNames.append(img['filename'])
            self.imgs.append(img)
            put_button(img['filename'], onclick=partial(self.reName, img=img, scope=scope), scope=scope + "in",
                       color='success', outline=True)

    def process(self, content, isImg, flag):
        self.START()
        onclick = None
        if isImg:
            put_scope('1stScrolable')
            put_scrollable(put_scope('scrollable'), height=650, keep_bottom=False, scope='1stScrolable')
            scopeN = 0
            scope = lambda num: 'scope' + str(scopeN)
            for img in content:
                # put_html('<br>')
                put_scope(scope(scopeN), scope='scrollable')
                put_image(img['content'], width="200xp", scope=scope(scopeN))
                put_scope(scope(scopeN) + "in", scope=scope(scopeN))
                put_button('Rename', onclick=partial(self.reName, img=img, scope=scope(scopeN)),
                           scope=scope(scopeN) + "in", color='danger', outline=True)
                scopeN += 1
            buttonTxt = "Save and rename images for latex"
            onclick = partial(self.processImage)
            put_scope('ImgBtn1')
            put_buttons(["Show image order"], onclick=self.showOrder, scope='ImgBtn1')
        else:
            put_scope('showtxt')
            file = content['content'].decode("utf-8")
            put_text(file, scope='showtxt')
            buttonTxt = "Convert txt raw to latex instructions"
            onclick = partial(self.processLatex, file=file)
        put_buttons([buttonTxt], onclick=onclick)
        put_html('<hr>')

    def fileUpload(self):
        self.process(file_upload("Choose your input base file:", accept="text/*", required=True, multiple=False), False,
                     flag=0)
        self.uploadImg()

    def textArea(self):
        self.process(textarea('Raw text:', placeholder="Please input your text", required=True), False, flag=1)
        self.textArea()

    def uploadImg(self):
        self.process(file_upload("Choose your input images:", accept="image/*", required=True, multiple=True), True,
                     flag=2)
        self.uploadImg()

    def initNav(self):
        url1 = "https://www.bing.com/videos/search?q=overleaf&&view=detail&mid" \
               "=2DC76EBCD6D5943620AF2DC76EBCD6D5943620AF&&FORM=VRDGAR&ru=%2Fvideos%2Fsearch%3Fq%3Doverleaf%26%26FORM" \
               "%3DVDVVXX/ "
        url2 = "https://www.bing.com/search?q=overleaf/ "
        put_markdown('# **_Latex Converter, From Plain Text_**')
        put_link(name="Overleaf Latex Compiler", url="https://www.overleaf.com/project", new_window=True)
        put_html('<br>')
        put_tabs([
            {'title': 'Intro to O verLeaf',
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
    pywebio.start_server(app.START, port=581)
