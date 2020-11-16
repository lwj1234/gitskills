from wordcloud import WordCloud
import matplotlib.pyplot as plt #绘制图像的模块
import jieba     #jieba分词

path_txt = 'E:\\cy\\word.txt'
f = open(path_txt,'r',encoding='UTF-8').read()

# 结巴分词，生成字符串，wordcloud无法直接生成正确的中文词云
cut_text = " ".join(jieba.cut(f))

wordcloud = WordCloud(
 #设置字体，不然会出现口字乱码，文字的路径是电脑的字体一般路径，可以换成别的
 font_path="C:/Windows/Fonts/ARIALUNI.TTF",
 #设置了背景，宽高
 background_color="black", width=1000, height=880).generate(cut_text)

plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()