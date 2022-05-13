from reportlab.platypus import SimpleDocTemplate, Paragraph,Table,Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.pdfgen import canvas
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Spacer, SimpleDocTemplate
from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg

PAGE_HEIGHT = A4[1]
PAGE_WIDTH = A4[0]

intro = "This report is generated by Teaching Insighter. "
text = "1. Here are the five themes that came up most often in the students' questions."
plot = "2. This is distribution of question topics"

counter = pd.read_csv('counter_topics.csv',header=0)
most_freq = counter.head(6)
list_t = [most_freq.columns[:,].values.astype(str).tolist()] + most_freq.values.tolist()

ts = [('ALIGN', (1,1), (-1,-1), 'CENTER'),
     ('LINEABOVE', (0,0), (-1,0), 1, colors.black),
     ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
     ('FONT', (0,0), (-1,0), 'Times-Bold'),
    #  ('LINEABOVE', (0,-1), (-1,-1), 1, colors.black),
    #  ('LINEBELOW', (0,-1), (-1,-1), 0.5, colors.black, 1, None, None, 4,1),
     ('LINEBELOW', (0,-1), (-1,-1), 1, colors.black),
#     ('FONT', (0,-1), (-1,-1), 'Times-Bold'),
#     ('BACKGROUND',(1,1),(-2,-2),colors.black),
     ('TEXTCOLOR',(0,0),(1,-1),colors.black)]


def scale(drawing, scaling_factor):
    """
    scale a reportlab.graphics.shapes.drawing()
    object while maintaining the aspect ratio
    """
    scaling_x = scaling_factor
    scaling_y = scaling_factor

    drawing.width = drawing.minWidth() * scaling_x
    drawing.height = drawing.height * scaling_y
    drawing.scale(scaling_x, scaling_y)
    return drawing

def myFirstPage(c: Canvas, doc):
    c.saveState()
    # 设置填充色
    c.setFillColor(colors.orange)
    # 设置字体大小
    c.setFont("Helvetica",30)
    # 绘制居中标题文本
    c.drawCentredString(300, PAGE_HEIGHT - 80, "Report")
    drawing = svg2rlg('Distribution of Question Topics.svg')
    scaled_drawing = scale(drawing, scaling_factor=0.4)
    renderPDF.draw(scaled_drawing, c, 0, 20)
    c.restoreState()
def myLaterPages(c: Canvas, doc):
    c.saveState()
    c.restoreState()
# 创建文档
doc = SimpleDocTemplate("report.pdf")
Story = [Spacer(1, 1 * inch)]
#Story = []
# 保存文档
# styles = getSampleStyleSheet()
# normal_style = styles['Normal']
ps = ParagraphStyle('title', fontSize=15, leading=30)
Story.append(Paragraph(intro,ps))
table = Table(list_t, style=ts)
Story.append(Paragraph(text,ps))
Story.append(table)
Story.append(Spacer(1, 0.2 * inch))
Story.append(Paragraph(plot,ps))

doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)