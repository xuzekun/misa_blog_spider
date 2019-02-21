# coding=utf-8
import requests
import json
import os
import re
from lxml import html

base_dir = os.getcwd()+ '/'

def get_blog_list():
    with open('misa.json',encoding='utf-8') as f:
        blog_list = json.load(f)
    return blog_list


def get_html(url):
    part = url.split("/")
    relative_dir = part[3] + "/" + part[4] + "/" + part[5] + "/" + part[6] +"/"
    filename = part[7][:-3] + "html"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

    raw_html = requests.get(url, headers=headers)
    #raw_html = str(raw_html.content,encoding='utf-8')

    raw_html = raw_html.content
    #downloadImage(raw_html)
    downloadEmoji(raw_html)
    #downloadDefaultEmoji()

    html = handle_html(raw_html)

    #if not os.path.exists(base_dir + relative_dir):
     #   os.makedirs(base_dir + relative_dir)

    with open(base_dir + relative_dir + filename,'w',encoding='utf-8') as f:
        f.write(html)




def handle_html(content):

    # content = re.sub("http://blog.nogizaka46.com/", '../../../../',  content)

    # for l in lists:
    tree = html.fromstring(content)
    # lists = tree.xpath('//*[@id="container"]')
    # print(lists)
    # content = ""
    # print(content)
    #
    # for div in lists:
    #     content += str(html.tostring(div, method='html', encoding='utf-8'),encoding='utf-8')
    # head = "<html><head></head><body>"
    # tail = "</body></html>"
    # content = head + content + tail
    #lists = tree.xpath('//*[@id="head"]')
    for l in tree.xpath('//*[@id="head"]'):
        l.getparent().remove(l)
    for l in tree.xpath('//*[@id="comments"]/div[1]/a'):
        l.getparent().remove(l)
    for l in tree.xpath('//*[@id="comments"]/div[22]'):
        l.getparent().remove(l)
    for l in tree.xpath('//*[@id="snsbtns"]'):
        l.getparent().remove(l)
    for l in tree.xpath('// *[ @ id = "menu2"]'):
        l.getparent().remove(l)
    for l in tree.xpath('//*[@id="officialSNS"]'):
        l.getparent().remove(l)
    for l in tree.xpath('/html/body/div[5]'):
        l.getparent().remove(l)
    for l in tree.xpath('/html/body/div[4]'):
        l.getparent().remove(l)
    for l in tree.xpath('//*[@id="comments-open-text"]'):
        l.getparent().remove(l)
    for l in tree.xpath('//*[@id="comments-open"]/h2'):
        l.getparent().remove(l)
    for l in tree.xpath('//*[@id="comment-form-name"]'):
        l.getparent().remove(l)
    for l in tree.xpath('//*[@id="comment-form-email"]'):
        l.getparent().remove(l)
    for l in tree.xpath('//*[@id="comment-form-url"]'):
        l.getparent().remove(l)
    for l in tree.xpath('//*[@id="comment-form-remember-me"]'):
        l.getparent().remove(l)
    for l in tree.xpath('//*[@id="comments-open-footer"]'):
        l.getparent().remove(l)

    content = html.tostring(tree, method='html', encoding='utf-8')

    content = str(content,encoding='utf-8')
    content = re.sub("http://blog.nogizaka46.com/", '../../../../', content)
    content = re.sub('php"', 'html"', content)
    content = re.sub('https://img.nogizaka46.com/blog/','../../../../', content )
    content = re.sub('http://img.nogizaka46.com/blog/', '../../../../', content)
    content = re.sub('misa.eto/smph/"', 'misa.eto/smph/index.html"', content)
    content = re.sub('smph/\\?d=(\d+)', 'smph/index/\\1/1.html', content)
    content = re.sub('//www.google-analytics.com/analytics.js', '', content)
    content = re.sub('//j.wovn.io/1', '', content)
    content = re.sub('//img.nogizaka46.com/www/smph/img/fukidash.png', '', content)
    return content


def downloadImage(content):
    tree = html.fromstring(content)
    imagelist = tree.xpath('//*[@id="sheet"]//a/img/@src')
    print(imagelist)
    for imageUrl in imagelist:
        part = imageUrl.split('/')
        base_dir = '/'.join(part[4:-1])
        imageName = base_dir + '/' + part[-1]
        print(base_dir)
        print(imageName)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        imgStream = requests.get(imageUrl, stream=True)
        with open(imageName, 'wb') as f:
            for chunk in imgStream.iter_content():
                f.write(chunk)

def downloadEmoji(content):
    tree = html.fromstring(content)
    emojiList = tree.xpath('//*[@id="sheet"]/div/div/div/div/img/@src')
    print(emojiList)
    for emoji in emojiList:
        print(emoji)
        part = emoji.split('/')
        base_dir = '/'.join(part[4:-1])
        imageName = base_dir + '/' + part[-1]
        print(base_dir)
        print(imageName)

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        imgStream = requests.get(emoji, stream=True)
        with open(imageName, 'wb') as f:
            for chunk in imgStream.iter_content():
                f.write(chunk)

def downloadDefaultEmoji():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

    with open('emoji.txt') as f:
        emojilist = f.readlines()

    os.system('cd phtots/icon')

    for emoji in emojilist:
        print(emoji)
        os.system('wget {}'.format(emoji))


def get_all_html():
    blog_list = get_blog_list()
    print(len(blog_list))
    for blog in blog_list:
        print(blog['url'])
        get_html(blog['url'])



#downloadDefaultEmoji()

#get_html('http://blog.nogizaka46.com/misa.eto/smph/2013/01/009761.php')

get_all_html()
