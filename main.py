import time
import os
import requests
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# 搜索API：https://music.163.com/#/search/m/?s=处处吻&type=1
# 歌单API：https://music.163.com/#/song?id=1444071945
# 歌曲API：http://music.163.com/song/media/outer/url?id=316686.mp3

class DownLoadMusic(object):
	def __init__(self, url, name):
		# 初始URL
		self.url = url
		# 初始化歌曲名称
		self.name = name
		# 设置浏览器user-agent
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
		}
		# 配置selenium请求
		self.options = webdriver.ChromeOptions()
		# 设置浏览器屏幕大小
		self.options.add_argument('--window-size=1920,1080')
		# 设置无头模式
		self.options.add_argument('--headless')
		# 设置user-agent
		self.options.add_argument(
			'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36')
		# 创建浏览器对象
		self.driver = webdriver.Chrome(options=self.options)

	# 存储cookies
	def save_cookies(self):
		# 获取cookies
		cookies = self.driver.get_cookies()
		# 遍历cookies字典集合,转换为requests格式的cookie
		self.cookies = {}
		for cookie in cookies:
			self.cookies[cookie['name']] = cookie['value']

	# 使用selenium打开网页
	def get_data(self):
		# 定位搜索框并发送歌名
		self.driver.find_element(by=By.XPATH, value='//input[@id="srch"]').send_keys(self.name)
		self.driver.find_element(by=By.XPATH, value='//input[@id="srch"]').send_keys(Keys.ENTER)
		# 等待页面加载
		time.sleep(2)

	# 解析搜索结果页面数据
	def parse_data(self):
		# 定位包含歌曲信息的frame
		el_frame = self.driver.find_element(by=By.XPATH, value='//*[@id="g_iframe"]')
		# 切换到frame
		self.driver.switch_to.frame(el_frame)
		# 获取div集合
		div_list = self.driver.find_elements(by=By.XPATH, value='//div[@class="srchsongst"]/div')
		# 遍历获取每一条歌曲信息并存储到list集合中
		self.music_list = []
		for div in div_list:
			temp = {}
			try:
				id = div.find_element(by=By.XPATH, value='./div[2]/div/div/a').get_attribute('href')
				temp['id'] = str(id).split('?id=')[-1]
				temp['title'] = div.find_element(by=By.XPATH, value='./div[2]/div/div/a/b').get_attribute('title')
				temp['name'] = div.find_element(by=By.XPATH, value='./div[4]/div/a').text
				temp['album'] = div.find_element(by=By.XPATH, value='./div[5]/div/a').text
				temp['duration'] = div.find_element(by=By.XPATH, value='./div[6]').text
				self.music_list.append(temp)
			except selenium.common.exceptions.NoSuchElementException as NoSuchElementException:
				continue

	# 构建下载链接
	def download_url(self):
		self.download_desc = []
		for music in self.music_list:
			temp = {}
			temp['title'] = music['title']
			temp['name'] = music['name']
			temp['album'] = music['album']
			temp['duration'] = music['duration']
			id = music['id']
			temp['url'] = f'http://music.163.com/song/media/outer/url?id={id}.mp3'
			self.download_desc.append(temp)

	# 展示抓取到的歌曲信息
	def show_music(self):
		index = 0
		for music in self.download_desc:
			title = music['title']
			name = music['name']
			album = music['album']
			duration = music['duration']
			url = music['url']
			print('{0:^70}'.format('∨' * 70))
			print('索引:{0:^70}'.format(index))
			print('歌名:{0:^70}'.format(title))
			print('歌手:{0:^70}'.format(name))
			print('专辑:{0:^70}'.format(album))
			print('时长:{0:^70}'.format(duration))
			print('链接:{0:^70}'.format(url))
			index += 1

	# 使用requests下载音乐并保存到本地
	def download_music(self, index):
		name = self.download_desc[index]['name']
		title = self.download_desc[index]['title']
		url = self.download_desc[index]['url']
		print(f'即将下载\t{name}的\t{title}')
		# requests获取响应
		response = requests.get(url=url, headers=self.headers, cookies=self.cookies)
		# 构建保存路径
		path = './' + self.name + '/'
		# 判断路径是否存在
		if not os.path.exists(path):
			os.makedirs(path)
		file = path + title + '-' + name + '.mp3'
		print(f'正在下载\t{name}的\t{title}\t保存路径为：{file}')
		# 保存选择的歌曲
		with open(file, 'wb') as f:
			f.write(response.content)
		print(f'下载完成\t{name}的\t{title}\t保存路径为：{file}')

	def run(self):
		# 获取起始url页面请求数据
		self.driver.get(self.url)
		# 使用selenium打开网页,在搜索框输入要下载的歌曲
		self.get_data()
		# 保存cookie
		self.save_cookies()
		# 解析搜索结果获取歌曲名称、歌手、专辑、时长、歌曲id
		self.parse_data()
		# 构建单曲下载url
		self.download_url()
		# 显示列表在控制台,通过键盘录入选择要下载的歌曲
		self.show_music()
		# requests下载歌曲
		print('▮' * 41)
		print('！！下载前先点击链接试听！！')
		print('！！下载前先点击链接试听！！')
		print('！！下载前先点击链接试听！！')
		index = int(input('请输入【索引值】下载相应歌曲:'))
		# 保存到本地
		self.download_music(index)


if __name__ == '__main__':
	name = input('请输入要下载的歌名、歌手、专辑：')
	music = DownLoadMusic(url='http://music.163.com', name=name)
	music.run()
