#!/usr/bin/python
import requests
import csv
import re
import os
import time
from lxml import etree
from bs4 import BeautifulSoup
import pandas as pd

def get_all_gene():
    response = requests.get("https://www.mycancergenome.org/",verify=False)
    html = response.text
    bs = BeautifulSoup(html,"html.parser")
    data = bs.find_all("option")
    genelist = []
    for each in data:
        gene = each.string.lower()
        if re.search(' ',gene):
            gene = "-".join(gene.split(' '))
        genelist.append(gene)
    print("already get gene list!")
    return genelist

def get_all_geneurl(gene):
    gene_urllist = []
    gene_url = "https://www.mycancergenome.org/content/disease/"+gene+"/"
    response = requests.get(gene_url,verify=False)
    html = response.text
    bs = BeautifulSoup(html,"html.parser")
    data = bs.find_all("a", class_ = "subitem")
    for each in data:
        url = each['href']
        if re.search('.+\d+/',url):
            gene_urllist.append(url)
    return gene_urllist


def get_data(url):
        print("正在抓取网页:"+url)
        response = requests.get(url,verify=False,headers = headers)
        time.sleep(5)
        html = response.text
        bs = BeautifulSoup(html,"html.parser")
        title = bs.title.string
        gene = title.split(" ")[0]
        if re.search('.*(c\..+)\(.*',title):
            cmut = re.search('.*(c\..+)\(.*',title).group(1)
            pmut = re.search('.*\((.*)\).*',title).group(1)
        elif re.search('.* Fusions *',title):
            cmut = 'fusion'
            pmut = '/'
        elif re.search('\S+\s(.*)\sin.*',title):
            cmut = re.search('\S+\s(.*)\sin.*',title).group(1)
            pmut = '/'
        else:
            cmut = 'mutations'
            pmut = '/'


        if re.search('.* in (.*) -.*',title):
            cancer = re.search('.* in (.*) -.*',title).group(1)
        else:
            cancer = '/'

        tables = bs.select('table')
        for index,each in enumerate(tables):
            each = each.prettify()
            if re.search('Properties',each) or re.search('Implications',each):
                table1 = tables[index].prettify()
            else:
                next
        text = pd.concat(pd.read_html(table1))
        print(text)
        anno = []
        for index,row in text.iterrows():
            if re.search('.*Properties.*',str(row[0])) or re.search('.*Implications.*',str(row[0])):
                next
            else:
                list1 = (str(row[0]),str(row[1]))
                item = ":".join(list1)
                if re.search('.*\s+[a-z]$',item):
                    item = re.sub('\s+[a-z]$','',item)
                anno.append(item)
        anno_info = ";".join(anno).strip()
        all_data = gene+"\t"+cmut+"\t"+pmut+"\t"+cancer+"\t"+anno_info
        print(all_data)
        return all_data

def towrite():
    csvfile = open("mycancer.csv",'w')
    with open('mycancerurl.csv','r') as f:
        for line in f.readlines():
            line = line.strip()
            print("开始抓取"+line)
            item = get_data(line)
            print("正在抓取"+line)
            csvfile.write(item+"\n")
            print("已经将该条信息写入文件....")

def write_urlfile():
    genelist = get_all_gene()
    all_url = []
    for each in genelist:
        gene_urllist = get_all_geneurl(each)
        for url in gene_urllist:
            if url not in all_url:
                all_url.append(url)
    with open('mycancerurl.csv','w') as url_file:
        for url in all_url:
            url_file.write(url+"\n")
    return url_file

if __name__ == '__main__':
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    proxies = {"http":"http://117.86.15.90:18118","http": "http://61.135.217.7:80","https": "https://119.10.67.144:808","http": "http://222.171.83.213:63000","https":"https://123.58.251.183:3128"}
    if os.path.isfile('mycancerurl.csv'):
        towrite()
    else:
        url_file = write_urlfile()
        towrite()
