import os
import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = '15874295385'
PASSWORD = 'fpdpvx119'

DETECT_POSITION_CENTERS = [
    # 横竖线
    (30, 80), (80, 130), (130, 80), (80, 30),
    # 斜线
    (60, 60), (60, 100), (100, 100), (100, 60),
    # 中心
    (80, 80)
]
DETECT_RADIUS = 4

FILTER_THRESHOLD = 35


class CrackWeiboSlide():
    def __init__(self):
        self.url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://m.weibo.cn/'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = USERNAME
        self.password = PASSWORD
    
    def __del__(self):
        self.browser.close()
    
    def open(self):
        """
        打开网页输入用户名密码并点击
        :return: None
        """
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()
    
    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'patt-shadow')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)
    
    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot
    
    def get_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha
    
    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 20
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False
    
    def same_pixels_count(self, template, image):
        count = 0
        for x in range(image.width):
            for y in range(image.height):
                if self.is_pixel_equal(template, image, x, y):
                    count += 1
        return count
    
    def same_pixels_counts(self, image):
        result = []
        for i in range(8):
            template = Image.open('templates/' + str(i) + '.jpg')
            count = self.same_pixels_count(template, image)
            result.append(count)
        print('Result', result)
    
    def detect_center(self, image, center):
        left, right = center[0] - DETECT_RADIUS, center[0] + DETECT_RADIUS
        top, bottom = center[1] - DETECT_RADIUS, center[1] + DETECT_RADIUS
        print(left, right, top, bottom)
        
        target = image.crop((left, top, right, bottom))
        if not os.path.exists('sss.jpg'):
            target.save('sss.jpg')
        target.show()
        counts = self.same_pixels_counts(target)
        
        return counts
    
    def crop_image(self, image):
        result = []
        dark_index = []
        for index, center in enumerate(DETECT_POSITION_CENTERS):
            line_counts = self.detect_center(image, center)
    
    def get_pixels(self, image):
        pixels = image.load()
        print(pixels)
    
    def crack(self):
        self.open()
        # 获取验证码图片
        image = self.get_image('captcha1.png')
        # image = Image.open('captcha1.png')
        self.crop_image(image)


if __name__ == '__main__':
    crack = CrackWeiboSlide()
    crack.crack()
