# encoding='utf-8'

# @Time: 2024-09-25
# @File: pdf_summary.py
#!/usr/bin/env python3
from icecream import ic
import os
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

# 下载必要的 NLTK 数据
nltk.download('punkt')
nltk.download('stopwords')

def summarize_pdf(file_path):
    # 打开PDF文件
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        # 提取文本
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # 分词和去除停用词
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text.lower())
        filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
        
        # 计算词频
        freq_dist = FreqDist(filtered_words)
        
        # 获取最常见的10个词
        most_common = freq_dist.most_common(10)
        
        return most_common

# 使用函数
pdf_path = '/mnt/e/ozon/ozonTools/barcodeprint/output.pdf'
summary = summarize_pdf(pdf_path)

ic("PDF文件摘要:")
for word, count in summary:
    ic(f"{word}: {count}")
