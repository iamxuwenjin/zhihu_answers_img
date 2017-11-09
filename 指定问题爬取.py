# coding=utf-8
from bs4 import BeautifulSoup
import requests
import re
import json

class OneQueestionImg(object):
    def __init__(self):
        self.session = requests.session()
        self.base_url = 'https://www.zhihu.com/question/'
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
                      "Cookie": 'q_c1=b1fb249e4f43497da44b7f9641e14909|1509620047000|1509620047000; _zap=3fb2e4a8-e34a-400d-bc37-b07f6f885dd3; d_c0="ACACIErwnwyPTuJSOV62smk97TnBnJBbPG4=|1509671730"; capsion_ticket="2|1:0|10:1509765646|14:capsion_ticket|44:MDMwOWQyYjA4OTY2NDE4MWFlMWJiOWUzODM4ZTc1NjI=|a062cb606959395d814452989eb174812fc5ed204b8941fde5e11a6fb2c1124e"; aliyungf_tc=AQAAANJ/hT0ZowkAAnCCDopvCr0s+IEX; _xsrf=b091908365d1081adc075f0a095e3cbd; r_cap_id="YWNlZThlOGMwZWMwNDBlMGEzODgyZDY2MjJkZTI4YTU=|1510036499|6bf98dc2abb2da7146e13da293c3c1feee641869"; cap_id="YzMyNjk4NTZiZTUwNDc1ZmFhNmEyNjhmMGE1NzBhYTI=|1510036498|e62be63daad620eab6eb4bd72d7c9fb3c555f5be"; z_c0=Mi4xOGRtZEFBQUFBQUFBSUFJZ1N2Q2ZEQmNBQUFCaEFsVk5HS0x1V2dEVXFZalQ5SlRUeW82WXZyX0x5TVY1ck0yS1VR|1510036504|afa0b6b5f15b88a82d14148bad7497371f15f93e; s-q=%E9%A2%9C%E5%80%BC%E9%AB%98; s-i=12; sid=jtv34bbg; __utma=51854390.545928740.1510036501.1510036501.1510036501.1; __utmc=51854390; __utmz=51854390.1510036501.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100-1|2=registration_date=20141108=1^3=entry_date=20141108=1; _xsrf=b091908365d1081adc075f0a095e3cbd'}
        self.pattern = re.compile('\d+')
        self.num = self.pattern.search(self.base_url).group()
        self.pattern_img = re.compile(r'https://.{50,55}?hd.jpg')

    def load_page(self,url):
        html = self.session.get(url=url, headers=self.headers).content
        return html

    def saveimg(self,img, filename):
        with open('./image/'+filename, 'wb') as f:
            f.write(img)

    def get_json(self, num):
        json_url = "https://www.zhihu.com/api/v4/questions/"+self.num+"/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset="+str(num)+"&limit=20&sort_by=default"
        print json_url
        html = self.session.get(json_url,headers=self.headers).content
        html = json.loads(html)
        answers = html['data']
        i = 0
        for index,answer in enumerate(answers):
            content = answer['content']
            url_list = self.pattern_img.findall(content)
            url_set = set(url_list)
            for num, url in enumerate(url_set):
                print '正在请求第%d个答案中的第%d个图片'%(index+1, num+1)
                html = self.load_page(url)
                filename = url[-10:]
                self.saveimg(html, filename)

    def handle_content(self，url):
        html = self.load_page(url=url)
        soup = BeautifulSoup(html,'lxml')
        # list = soup.select('span[class="RichText CopyrightRichText-richText"] img')
        con_num = soup.select('h4')[0].get_text()
        con_num = self.pattern.search(con_num).group()
        num = (int(con_num)//20)+1
        list = soup.find_all('span',{'class':'RichText CopyrightRichText-richText'})
        list_str = str(list)
        i_list = self.pattern_img.findall(list_str)
        i_set = set(i_list)
        print '正在请求首页答案'
        for num, url in enumerate(i_set):
            html = self.load_page(url)
            filename = url[-10:]
            self.saveimg(html, filename)
        return num

    def start_work(self):
        question_num = raw_input('请输入问题代码')
        url = self.base_url+question_num
        nums = self.handle_content(url)
        for num in range(0,int(nums)):
            print '正在请求第%d组'%(int(num)+1)
            num_page = num*10+3
            self.get_json(num_page)

if __name__ == '__main__':
    img = OneQueestionImg()
    img.start_work()

