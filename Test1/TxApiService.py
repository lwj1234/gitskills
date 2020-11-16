import base64
import requests

class TxApiService:
    def __init__(self):
        self.appkey = '4db20ab9223b5f34f27dc415ac1ed17c'  # 在天行数据(www.tianapi.com)注册，获取自己的key
        self.text_cls_url_root = 'https://api.tianapi.com/txapi/lajifenlei/index?key=%s&word=%s'
        self.img_cls_url_root = 'https://api.tianapi.com/txapi/imglajifenlei/index'

    def get_text_cls_res(self, garbage_name):
        url = self.text_cls_url_root % (self.appkey, garbage_name)
        response = requests.get(url)

        res = []
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get('newslist'):
                new_list_json = res_json['newslist']
                for item in new_list_json:
                    name = item.get('name')
                    cat = self.garbage_id_to_name(item.get('type'))
                    tip = item.get('tip')
                    ai_pre = item.get('aipre')
                    pre_type = 'None'
                    if ai_pre == 0:
                        pre_type = '正常结果'
                    if ai_pre == 1:
                        pre_type = '预判结果'
                    item_dict = {'name': name, 'type': cat, 'tip': tip, 'pre_type': pre_type}
                    res.append(item_dict)
                return res
            else:
                return None
        return None

    def get_img_cls_res(self, img_base64):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'key': self.appkey,
            "img": img_base64,
        }
        response = requests.post(self.img_cls_url_root, headers=headers, data=body)

        res = []
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get('newslist'):
                new_list_json = res_json['newslist']
                for item in new_list_json:
                    name = item.get('name')
                    cat = self.garbage_id_to_name(item.get('lajitype'))
                    tip = item.get('lajitip')
                    trust = item.get('trust')
                    if trust <= 80:
                        continue
                    item_dict = {'name': name, 'type': cat, 'tip': tip, 'pre_score': trust}
                    res.append(item_dict)
                return res
            else:
                return None
        return None

    def garbage_id_to_name(self, id):
        if id == 0:
            return '可回收物'
        if id == 1:
            return '有害垃圾'
        if id == 2:
            return '厨余垃圾'
        if id == 3:
            return '其他垃圾'
        return None

if __name__ == '__main__':
    tx_api_service = TxApiService()

    res = tx_api_service.get_text_cls_res('苹果')
    print(res)

    with open("apple.jpg", 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
    res = tx_api_service.get_img_cls_res(s)
    print(res)