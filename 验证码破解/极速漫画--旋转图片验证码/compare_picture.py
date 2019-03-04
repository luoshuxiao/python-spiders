# 声明一个图片类，对象属性是图片的PIL库的Image对象
# compare对象方法可以判断两张图片是否一样，但是并不能百分百判断正确，正确率在百分之九十左右

# 设置判断两张图片相匹配的最低匹配度
COMPATIBLE = 70


class PictureHash(object):
    """图片类"""
    def __init__(self, obj):
        """param obj: 图片Image对象"""
        self.obj = obj

    def get_gray(self):
        """
        获取图片灰度集合
        :return: 灰度列表
        """
        a = self.change_size_con()
        tmpls = []
        for h in range(0, a.size[1]):
            for w in range(0, a.size[0]):
                tmpls.append(a.getpixel((w, h)))
        return tmpls

    def change_size_con(self):
        """
        改变图片大小，转255灰度图(0到255的值)
        :return: 新图片Image对象
        """
        return self.obj.resize((12, 12)).convert("L")

    def get_hash(self):
        """生成图片哈希表"""
        bitls = ''
        a = self.change_size_con()
        b = self.get_gray()
        avg = sum(b) / len(b)
        for h in range(1, a.size[1] - 1):
            for w in range(1, a.size[0] - 1):
                if a.getpixel((w, h)) >= avg:
                    bitls = bitls + '1'
                else:
                    bitls = bitls + '0'
        return bitls

    def compare(self, other_picture):
        """
        比较两个图片是否一样
        :param other_picture: 另一张图片的PictureHash对象
        :return: 布尔值（1表示相同，0表示不同）
        """
        dist = 0
        hash_s = self.get_hash()
        hash_o = other_picture.get_hash()
        for i in range(0, len(hash_s)):
            if hash_s[i] == hash_o[i]:
                dist = dist + 1
        if dist >= COMPATIBLE:
            return 1
        else:
            return 0