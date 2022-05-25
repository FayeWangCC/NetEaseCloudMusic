import requests
from selenium import webdriver


# 搜索API：https://music.163.com/#/search/m/?s=处处吻&type=1
# 歌单API：https://music.163.com/#/song?id=1444071945
# 歌曲API：http://music.163.com/song/media/outer/url?id=316686.mp3

class DownLoadMusic(object):
    def __init__(self):
        # 初始URL
        self.url =
        pass

    def run(self):
        # 使用selenium打开网页
        # 在搜索框输入要下载的歌曲
        # 解析搜索结果获取歌曲名称、歌手、专辑、时长、歌曲id
        # 构建单曲下载url
        # requests下载歌曲
        # 保存到本地
        pass


if __name__ == '__main__':
    music = DownLoadMusic()
    music.run()
