import re
from fpdf import FPDF, HTMLMixin

class MyFPDF(FPDF, HTMLMixin):
    pass

def html2pdf(html_text, path):
    pdf = MyFPDF()
    pdf.add_page()
    pdf.write_html(html_text)
    pdf.output(path, 'F')

def clear_text(text):
    lines=[]
    for line in text.split('\n'):
        line=line.strip()
        if len(line)>0:
            lines.append(line)
    return ' '.join(lines)

with open("example.tex","rb") as fr:
    text=fr.read().decode(encoding='utf-8')

# document
pat_doc=re.compile('begin\{document\}(.*?)\\\end\{document\}',re.S)
document=pat_doc.findall(text)[0]

# title
pat_title=re.compile('title\{(.*?)\}',re.S)
title=pat_title.findall(text)[0]

# abstract
pat_abs=re.compile('begin\{abstract\}(.*?)\\\end\{abstract\}',re.S)
abstract=pat_abs.findall(text)[0]

# section1
pat_sec=re.compile('section\{(.*?)\}(.*?)\r\n\t\r\n\t',re.S)
sec_title1,sec_content1=pat_sec.findall(text)[0]
sec_content1=clear_text(sec_content1)

# section2
pat_sec=re.compile('section\{(.*?)\}(.*?)\r\n\t\r\n\t',re.S)
sec_title2,sec_content2=pat_sec.findall(text)[1]
sec_content2=clear_text(sec_content2)

# subsection1
pat_subsec=re.compile('subsection\{(.*?)\}(.*?)\r\n\t\r\n\t',re.S)
subsec_title1,subsec_content1=pat_subsec.findall(text)[0]
subsec_content1=clear_text(subsec_content1)

# subsection2
pat_subsec=re.compile('subsection\{(.*?)\}(.*?)\r\n\t\r\n\t',re.S)
subsec_title2,subsec_content2=pat_subsec.findall(text)[1]
subsec_content2=clear_text(subsec_content2)

# subsection3
pat_subsec=re.compile('subsection\{(.*?)\}(.*?)\r\n\t\r\n\t',re.S)
subsec_title3,subsec_content3=pat_subsec.findall(text)[2]
subsec_content3=clear_text(subsec_content3)

# subsection4
pat_subsec=re.compile('subsection\{(.*?)\}(.*?)\r\n\t\r\n\t',re.S)
subsec_title4,subsec_content4=pat_subsec.findall(text)[3]
subsec_content4=clear_text(subsec_content4)

# itemize1、item、emph
pat_itemize=re.compile('begin\{itemize\}(.*?)\\\end\{itemize\}\r\n\t\r\n\t',re.S)
itemize1=pat_itemize.findall(text)[0]
itemize1 = re.sub('\\\item','<li>',itemize1)
itemize1 = re.sub('\\\emph','<i>',itemize1)
itemize1 = re.sub('\\\\begin\{itemize\}','<ul>',itemize1)#处理嵌套的itemize
itemize1 = re.sub('\\\end\{itemize\}','</ul>',itemize1)

# itemize2、item
pat_itemize=re.compile('begin\{itemize\}(.*?)\\\end\{itemize\}\r\n\t\r\n\t',re.S)
itemize2=pat_itemize.findall(text)[1]
itemize2 = re.sub('\\\item','<li>',itemize2)

# itemize3、item
pat_itemize=re.compile('begin\{itemize\}(.*?)\\\end\{itemize\}\r\n\t\r\n\t',re.S)
itemize3=pat_itemize.findall(text)[2]
itemize3 = re.sub('\\\item','<li>',itemize3)

# tabular
pat_tabular=re.compile('begin\{tabular\}(.*?)\\\end\{tabular\}',re.S)

html_text=''
# title
html_text+='<h1>%s</h1>\n\n' %title
# abstract
html_text+='<p>%s</p>\n\n' %abstract
# section -- 1
html_text+='<h2>%s</h2>\n\n' %sec_title1
html_text+='<p>%s</p>\n\n' %sec_content1
# section -- 2
html_text+='<h2>%s</h2>\n\n' %sec_title2
html_text+='<p>%s</p>\n\n' %sec_content2
# subsection1
html_text+='<h3>%s</h3>\n\n' %subsec_title1
html_text+='<p>%s</p>\n\n' %subsec_content1
# subsection2
html_text+='<h3>%s</h3>\n\n' %subsec_title2
html_text+='<p>%s</p>\n\n' %subsec_content2
# itemize1
html_text+='<ul>%s</ul>\n\n' %itemize1
# subsection3
html_text+='<h3>%s</h3>\n\n' %subsec_title3
html_text+='<p>%s</p>\n\n' %subsec_content3
# itemize2
html_text+='<ul>%s</ul>\n\n' %itemize2
# itemize3
html_text+='<ul>%s</ul>\n\n' %itemize3
# subsection4
html_text+='<h3>%s</h3>\n\n' %subsec_title4
html_text+='<p>%s</p>\n\n' %subsec_content4

print(type(html_text))

print(html_text)
html2pdf(html_text,'2.pdf')