import re
import base64
import urllib
import http.cookiejar
import urllib.request
import time
import http.cookiejar
from html.parser import HTMLParser


class Spider:
	'''
		这个类是一个爬虫类  用来自动爬取poj的题解 并 提交  大概这样
	'''

	def __init__(self , page_start , page_end):
		self.page_start = page_start
		self.page_end = page_end
		self.login_url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'#这是hdu的登陆界面地址
		self.login_data = {"username": "Matrixneo",
						"userpass": "314159",
						"login": "Sign In"
						}
		self.question_url_pre = "http://acm.hdu.edu.cn/showproblem.php?pid="
		self.problem_url = ""
		self.problem_id = ""
		self.coding = ""
		self.problem_name = ""
		self.source = ""
		self.submit_data = {"check": "0",
							"problemid": "",
							"language": "0",
							"usercode": ""
							}
		self.submit_url = "http://acm.hdu.edu.cn/submit.php?action=submit"
		self.login_data = urllib.parse.urlencode(self.login_data).encode('utf-8')
		self.headers = {
			"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
		}
		self.pattern_title = 'lang="en-US">(.)*?</div>'

	def login(self):
		requ = urllib.request.Request(url = self.login_url , data = self.login_data , headers = self.headers)
		cjar = http.cookiejar.CookieJar()#创建一个CookieJar对象
		#使用HTTPCookieProcessor创建一个cookie处理器 并且用它当参数构建opener对象
		opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
		#把opener安装为全局
		urllib.request.install_opener(opener)
		file = opener.open(requ)
		#with open("test.html" , "wb") as fhandler:
		#	fhandler.write(file.read())

	def Get_problem_url(self , page):
		'''
			用来获得第page到题的网页url地址
		'''
		fullurl = self.question_url_pre + str(page)
		self.problem_url = fullurl


	def Get_problem_name(self , page):
	#	self.problem_id = page
		requ = urllib.request.Request(url = self.problem_url , headers = self.headers)
		html = urllib.request.urlopen(requ , timeout = 10).read().decode('utf-8')
		pos = re.search(self.pattern_title , str(html)).span()
		self.problem_name = html[pos[0] : pos[1]]
		Pattern = ">(.)*?<"
		pos = re.search(Pattern , self.problem_name).span()
		self.problem_name = self.problem_name[pos[0] + 1: pos[1] - 1]
		print(self.problem_name)



	def submit(self , page):
		self.submit_data["problemid"] = str(page)
		try:
			self.submit_data["usercode"] = self.coding
		except Exception as E:
			print("错误发生在这里 快来看我  line 81 " + str(E))
		self.submit_data = urllib.parse.urlencode(self.submit_data).encode('utf-8')
		#self.headers["Referer"] = "http://poj.org/submit?problem_id=" + str(page)
		requ = urllib.request.Request(url = self.submit_url , data = self.submit_data , headers = self.headers)
		try:
			html = urllib.request.urlopen(requ , timeout = 15)
		except Exception as E:
			print(E)
		#with open("file.html" , "wb") as fhandler:
		#	fhandler.write(html.read())
		#print("submit模块")
		#


	def Get_code_by_page(self , page):
		url_of_list = "http://www.acmsearch.com/article/?ArticleListSearch%5BFoj%5D=hdoj&ArticleListSearch%5BFproblem_id%5D="
		url_of_coding = "http://www.acmsearch.com"
		url_of_list += str(page)
	#	print(url_of_list)
		#print("查询链接为" + url_of_list)
		requ = urllib.request.Request(url = url_of_list , headers = self.headers)
		html = urllib.request.urlopen(requ).read()
		pattern = '"/article/show/\d.*?"'
		string = str(html)
		result = re.search(pattern , string)
		#print(result)
		#print("地址链接为" + url_of_coding)
		try:
			pos = result.span()
			url_of_coding += string[pos[0] + 1 : pos[1] - 1]
			#print(url_of_coding)
			requ = urllib.request.Request(url = url_of_coding , headers = self.headers)
			html = urllib.request.urlopen(requ).read()
		except Exception as e:
			print("错误发生在爬取acmcoding链接部分")
			print(str(e))
		
		
		pattern = 'important;">.*</textarea>'
		string = str(html)
		result = re.search(pattern , string)
	#	print("地址链接为" + url_of_coding)
		try:
			pos = result.span()
			coding = string[pos[0] + 12: pos[1] - 11]
			self.coding = coding
			#print(coding)
		except Exception as e:
			print("错误发生在爬取代码部分")
			print(str(e))
		html = self.coding
		h = HTMLParser()
		html = h.unescape(html)
		k = 0
		stringofcoding = ""

		while k < len(html) :
			if html[k] == "\\" and html[k + 1] == "\\" and html[k + 2] == "n":
				stringofcoding += "\\n"
				k += 3
			elif html[k] == "\\" and html[k + 1] == "n":
				stringofcoding += "\n"
				k += 2
			elif html[k] == "\\" and html[k + 1] == "t":
				stringofcoding += "    "
				k += 2
			elif html[k] == "\\" and html[k + 1] == "r":
				stringofcoding += ""
				k += 2	
			elif html[k] == "\\" and html[k + 1] == "'":
				stringofcoding += "'"
				k += 2	
			else:
				stringofcoding += html[k]
				k += 1
		self.coding = stringofcoding
		#with open("hdu" + str(page) + ".txt" , "w") as fhandler:
		#	fhandler.write(stringofcoding)
		return 


	def urlpostiontrans(self):
		k = 0
		stringofcoding = ""
		h = HTMLParser()
		self.coding = h.unescape(self.coding)
		while k < len(self.coding) :
			if self.coding[k] == "\\" and self.coding[k + 1] == "\\" and self.coding[k + 2] == "n":
				stringofcoding += "\\n"
				k += 3
			elif self.coding[k] == "\\" and self.coding[k + 1] == "n":
				stringofcoding += "\n"
				k += 2
			elif self.coding[k] == "\\" and self.coding[k + 1] == "t":
				stringofcoding += "    "
				k += 2
			else:
				stringofcoding += self.coding[k]
				k += 1
		self.coding = stringofcoding
		bytestring = self.coding.encode(encoding = 'utf-8')
		self.coding = base64.encodestring(bytestring)
		self.coding = self.coding.decode('utf-8')
		self.source = self.coding
		print(self.coding)

	def start(self):
		for it in range(self.page_start , self.page_end):
			ss = Spider(1020 , 1000)
			try:
				ss.Get_problem_url(it)
				#spider.Get_problem_name(it)
				ss.Get_code_by_page(it)
				#spider.urlpostiontrans()
				ss.submit(it)
				print(str(it) + "提交成功")
				time.sleep(2)
			except Exception as E:
				print(E)



if __name__ == "__main__":
	spider = Spider(1000, 1010)
	spider.login()
	spider.start()
'''
user_id1: Matrixneo
password1: 314159
B1: login
url: /problem?id=1000


'''
