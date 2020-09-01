# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
from newcar_new.items import NewcarNewItem


class AutohomeSeriesSpider(scrapy.Spider):
    name = 'autohome_series'
    # allowed_domains = ['autohome.com']
    # start_urls = ['http://autohome.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeSeriesSpider, self).__init__(**kwargs)
        self.counts = 0
        self.brand_list = [{"id":33,"name":"奥迪","letter":"A"},{"id":35,"name":"阿斯顿·马丁","letter":"A"},{"id":34,"name":"阿尔法·罗密欧","letter":"A"},{"id":410,"name":"APEX","letter":"A"},{"id":397,"name":"Aspark","letter":"A"},{"id":378,"name":"AUXUN傲旋","letter":"A"},{"id":117,"name":"AC Schnitzer","letter":"A"},{"id":340,"name":"Aurus","letter":"A"},{"id":134,"name":"ABT","letter":"A"},{"id":327,"name":"爱驰","letter":"A"},{"id":310,"name":"Aria","letter":"A"},{"id":221,"name":"安凯客车","letter":"A"},{"id":303,"name":"ATS","letter":"A"},{"id":251,"name":"Arash","letter":"A"},{"id":253,"name":"Apollo","letter":"A"},{"id":272,"name":"ARCFOX","letter":"A"},{"id":273,"name":"艾康尼克","letter":"A"},{"id":276,"name":"ALPINA","letter":"A"},{"id":292,"name":"Agile Automotive","letter":"A"},{"id":14,"name":"本田","letter":"B"},{"id":38,"name":"别克","letter":"B"},{"id":15,"name":"宝马","letter":"B"},{"id":36,"name":"奔驰","letter":"B"},{"id":75,"name":"比亚迪","letter":"B"},{"id":13,"name":"标致","letter":"B"},{"id":40,"name":"保时捷","letter":"B"},{"id":120,"name":"宝骏","letter":"B"},{"id":39,"name":"宾利","letter":"B"},{"id":95,"name":"奔腾","letter":"B"},{"id":27,"name":"北京","letter":"B"},{"id":154,"name":"北汽制造","letter":"B"},{"id":173,"name":"北京汽车","letter":"B"},{"id":231,"name":"宝沃","letter":"B"},{"id":208,"name":"北汽新能源","letter":"B"},{"id":79,"name":"北汽昌河","letter":"B"},{"id":203,"name":"北汽幻速","letter":"B"},{"id":143,"name":"北汽威旺","letter":"B"},{"id":392,"name":"铂驰","letter":"B"},{"id":390,"name":"Bollinger Motors","letter":"B"},{"id":387,"name":"比德文汽车","letter":"B"},{"id":37,"name":"布加迪","letter":"B"},{"id":362,"name":"博郡汽车","letter":"B"},{"id":140,"name":"巴博斯","letter":"B"},{"id":333,"name":"北京清行","letter":"B"},{"id":172,"name":"保斐利","letter":"B"},{"id":180,"name":"BAC","letter":"B"},{"id":302,"name":"拜腾","letter":"B"},{"id":301,"name":"北汽道达","letter":"B"},{"id":257,"name":"宾尼法利纳","letter":"B"},{"id":271,"name":"比速汽车","letter":"B"},{"id":76,"name":"长安","letter":"C"},{"id":163,"name":"长安欧尚","letter":"C"},{"id":77,"name":"长城","letter":"C"},{"id":294,"name":"长安凯程","letter":"C"},{"id":299,"name":"长安跨越","letter":"C"},{"id":293,"name":"昶洧","letter":"C"},{"id":411,"name":"Czinger","letter":"C"},{"id":389,"name":"Canoo","letter":"C"},{"id":366,"name":"车驰汽车","letter":"C"},{"id":171,"name":"Conquest","letter":"C"},{"id":322,"name":"Cupra","letter":"C"},{"id":189,"name":"Caterham","letter":"C"},{"id":196,"name":"成功汽车","letter":"C"},{"id":264,"name":"长江EV","letter":"C"},{"id":1,"name":"大众","letter":"D"},{"id":113,"name":"东风风神","letter":"D"},{"id":165,"name":"东风风行","letter":"D"},{"id":259,"name":"东风风光","letter":"D"},{"id":41,"name":"道奇","letter":"D"},{"id":169,"name":"DS","letter":"D"},{"id":32,"name":"东风","letter":"D"},{"id":142,"name":"东风小康","letter":"D"},{"id":81,"name":"东南","letter":"D"},{"id":341,"name":"大乘汽车","letter":"D"},{"id":187,"name":"东风风度","letter":"D"},{"id":406,"name":"东风富康","letter":"D"},{"id":405,"name":"大运","letter":"D"},{"id":380,"name":"De Tomaso","letter":"D"},{"id":92,"name":"大发","letter":"D"},{"id":157,"name":"Dacia","letter":"D"},{"id":326,"name":"东风·瑞泰特","letter":"D"},{"id":198,"name":"DMC","letter":"D"},{"id":217,"name":"Datsun","letter":"D"},{"id":234,"name":"Donkervoort","letter":"D"},{"id":280,"name":"电咖","letter":"D"},{"id":211,"name":"Elemental","letter":"E"},{"id":3,"name":"丰田","letter":"F"},{"id":8,"name":"福特","letter":"F"},{"id":42,"name":"法拉利","letter":"F"},{"id":96,"name":"福田","letter":"F"},{"id":11,"name":"菲亚特","letter":"F"},{"id":141,"name":"福迪","letter":"F"},{"id":132,"name":"Fisker","letter":"F"},{"id":176,"name":"弗那萨利","letter":"F"},{"id":177,"name":"FM Auto","letter":"F"},{"id":197,"name":"福汽启腾","letter":"F"},{"id":248,"name":"Faraday Future","letter":"F"},{"id":82,"name":"广汽传祺","letter":"G"},{"id":313,"name":"广汽新能源","letter":"G"},{"id":112,"name":"GMC","letter":"G"},{"id":329,"name":"广汽集团","letter":"G"},{"id":383,"name":"高合HiPhi","letter":"G"},{"id":372,"name":"格罗夫","letter":"G"},{"id":370,"name":"GYON","letter":"G"},{"id":369,"name":"国机智骏","letter":"G"},{"id":365,"name":"Ginetta","letter":"G"},{"id":361,"name":"GFG Style","letter":"G"},{"id":108,"name":"广汽吉奥","letter":"G"},{"id":115,"name":"Gumpert","letter":"G"},{"id":116,"name":"光冈","letter":"G"},{"id":152,"name":"观致","letter":"G"},{"id":190,"name":"GAZ","letter":"G"},{"id":230,"name":"GTA","letter":"G"},{"id":304,"name":"国金汽车","letter":"G"},{"id":277,"name":"GLM","letter":"G"},{"id":278,"name":"广通客车","letter":"G"},{"id":181,"name":"哈弗","letter":"H"},{"id":91,"name":"红旗","letter":"H"},{"id":86,"name":"海马","letter":"H"},{"id":267,"name":"汉腾汽车","letter":"H"},{"id":386,"name":"汉龙汽车","letter":"H"},{"id":87,"name":"华泰","letter":"H"},{"id":220,"name":"华颂","letter":"H"},{"id":415,"name":"Hudson","letter":"H"},{"id":24,"name":"哈飞","letter":"H"},{"id":376,"name":"HYCAN合创","letter":"H"},{"id":43,"name":"悍马","letter":"H"},{"id":85,"name":"华普","letter":"H"},{"id":357,"name":"Hispano Suiza","letter":"H"},{"id":97,"name":"黄海","letter":"H"},{"id":348,"name":"华人运通","letter":"H"},{"id":336,"name":"红星汽车","letter":"H"},{"id":150,"name":"海格","letter":"H"},{"id":164,"name":"恒天","letter":"H"},{"id":170,"name":"Hennessey","letter":"H"},{"id":184,"name":"华骐","letter":"H"},{"id":237,"name":"华利","letter":"H"},{"id":240,"name":"霍顿","letter":"H"},{"id":245,"name":"华凯","letter":"H"},{"id":260,"name":"华泰新能源","letter":"H"},{"id":414,"name":"INKAS","letter":"I"},{"id":188,"name":"Icona","letter":"I"},{"id":274,"name":"Inferno","letter":"I"},{"id":288,"name":"Italdesign","letter":"I"},{"id":25,"name":"吉利汽车","letter":"J"},{"id":46,"name":"Jeep","letter":"J"},{"id":44,"name":"捷豹","letter":"J"},{"id":358,"name":"捷达","letter":"J"},{"id":84,"name":"江淮","letter":"J"},{"id":319,"name":"捷途","letter":"J"},{"id":119,"name":"江铃","letter":"J"},{"id":83,"name":"金杯","letter":"J"},{"id":373,"name":"几何汽车","letter":"J"},{"id":270,"name":"江铃集团新能源","letter":"J"},{"id":297,"name":"君马汽车","letter":"J"},{"id":356,"name":"钧天","letter":"J"},{"id":371,"name":"捷尼赛思","letter":"J"},{"id":145,"name":"金龙","letter":"J"},{"id":151,"name":"九龙","letter":"J"},{"id":175,"name":"金旅","letter":"J"},{"id":281,"name":"奇点汽车","letter":"J"},{"id":47,"name":"凯迪拉克","letter":"K"},{"id":9,"name":"克莱斯勒","letter":"K"},{"id":101,"name":"开瑞","letter":"K"},{"id":214,"name":"凯翼","letter":"K"},{"id":109,"name":"KTM","letter":"K"},{"id":353,"name":"Karma","letter":"K"},{"id":100,"name":"科尼赛克","letter":"K"},{"id":139,"name":"凯佰赫","letter":"K"},{"id":156,"name":"卡尔森","letter":"K"},{"id":199,"name":"卡威","letter":"K"},{"id":213,"name":"开沃汽车","letter":"K"},{"id":224,"name":"卡升","letter":"K"},{"id":52,"name":"雷克萨斯","letter":"L"},{"id":279,"name":"领克","letter":"L"},{"id":49,"name":"路虎","letter":"L"},{"id":51,"name":"林肯","letter":"L"},{"id":48,"name":"兰博基尼","letter":"L"},{"id":10,"name":"雷诺","letter":"L"},{"id":53,"name":"铃木","letter":"L"},{"id":54,"name":"劳斯莱斯","letter":"L"},{"id":318,"name":"零跑汽车","letter":"L"},{"id":345,"name":"理想汽车","letter":"L"},{"id":50,"name":"路特斯","letter":"L"},{"id":78,"name":"猎豹汽车","letter":"L"},{"id":80,"name":"力帆汽车","letter":"L"},{"id":124,"name":"理念","letter":"L"},{"id":335,"name":"LITE","letter":"L"},{"id":118,"name":"Lorinser","letter":"L"},{"id":88,"name":"陆风","letter":"L"},{"id":89,"name":"莲花汽车","letter":"L"},{"id":346,"name":"罗夫哈特","letter":"L"},{"id":343,"name":"领途汽车","letter":"L"},{"id":121,"name":"蓝旗亚","letter":"L"},{"id":323,"name":"拉共达","letter":"L"},{"id":320,"name":"LEVC","letter":"L"},{"id":183,"name":"朗世","letter":"L"},{"id":316,"name":"绿驰","letter":"L"},{"id":204,"name":"陆地方舟","letter":"L"},{"id":225,"name":"领志","letter":"L"},{"id":241,"name":"LOCAL MOTORS","letter":"L"},{"id":244,"name":"拉达","letter":"L"},{"id":261,"name":"雷诺三星","letter":"L"},{"id":265,"name":"LeSEE","letter":"L"},{"id":285,"name":"Lucid","letter":"L"},{"id":58,"name":"马自达","letter":"M"},{"id":20,"name":"名爵","letter":"M"},{"id":57,"name":"玛莎拉蒂","letter":"M"},{"id":56,"name":"MINI","letter":"M"},{"id":129,"name":"迈凯伦","letter":"M"},{"id":381,"name":"迈迈","letter":"M"},{"id":374,"name":"迈莎锐","letter":"M"},{"id":55,"name":"迈巴赫","letter":"M"},{"id":364,"name":"Mole","letter":"M"},{"id":126,"name":"MELKUS","letter":"M"},{"id":338,"name":"Micro","letter":"M"},{"id":168,"name":"摩根","letter":"M"},{"id":229,"name":"MAGNA","letter":"M"},{"id":250,"name":"Mahindra","letter":"M"},{"id":268,"name":"Mazzanti","letter":"M"},{"id":309,"name":"哪吒汽车","letter":"N"},{"id":130,"name":"纳智捷","letter":"N"},{"id":413,"name":"Nikola","letter":"N"},{"id":395,"name":"Neuron EV","letter":"N"},{"id":136,"name":"Noble","letter":"N"},{"id":228,"name":"nanoFLOWCELL","letter":"N"},{"id":295,"name":"NEVS国能汽车","letter":"N"},{"id":60,"name":"讴歌","letter":"O"},{"id":331,"name":"欧拉","letter":"O"},{"id":59,"name":"欧宝","letter":"O"},{"id":146,"name":"欧朗","letter":"O"},{"id":308,"name":"Polestar极星","letter":"P"},{"id":61,"name":"帕加尼","letter":"P"},{"id":363,"name":"Pi&#235;ch Automotive","letter":"P"},{"id":360,"name":"Puritalia","letter":"P"},{"id":186,"name":"佩奇奥","letter":"P"},{"id":62,"name":"起亚","letter":"Q"},{"id":26,"name":"奇瑞","letter":"Q"},{"id":122,"name":"启辰","letter":"Q"},{"id":210,"name":"骐铃汽车","letter":"Q"},{"id":368,"name":"清源汽车","letter":"Q"},{"id":312,"name":"庆铃汽车","letter":"Q"},{"id":219,"name":"全球鹰","letter":"Q"},{"id":222,"name":"乔治·巴顿","letter":"Q"},{"id":235,"name":"前途","letter":"Q"},{"id":63,"name":"日产","letter":"R"},{"id":19,"name":"荣威","letter":"R"},{"id":296,"name":"瑞驰新能源","letter":"R"},{"id":352,"name":"RIVIAN","letter":"R"},{"id":103,"name":"瑞麒","letter":"R"},{"id":337,"name":"容大智造","letter":"R"},{"id":174,"name":"如虎","letter":"R"},{"id":193,"name":"Rinspeed","letter":"R"},{"id":227,"name":"RENOVO","letter":"R"},{"id":239,"name":"Rezvani","letter":"R"},{"id":252,"name":"Rimac","letter":"R"},{"id":67,"name":"斯柯达","letter":"S"},{"id":68,"name":"三菱","letter":"S"},{"id":65,"name":"斯巴鲁","letter":"S"},{"id":155,"name":"上汽MAXUS","letter":"S"},{"id":45,"name":"smart","letter":"S"},{"id":269,"name":"SWM斯威汽车","letter":"S"},{"id":162,"name":"思铭","letter":"S"},{"id":306,"name":"SRM鑫源","letter":"S"},{"id":330,"name":"思皓","letter":"S"},{"id":404,"name":"SONY","letter":"S"},{"id":402,"name":"上喆","letter":"S"},{"id":388,"name":"SHELBY","letter":"S"},{"id":377,"name":"Sono Motors","letter":"S"},{"id":64,"name":"萨博","letter":"S"},{"id":66,"name":"世爵","letter":"S"},{"id":69,"name":"双龙","letter":"S"},{"id":90,"name":"双环","letter":"S"},{"id":127,"name":"SPIRRA","letter":"S"},{"id":137,"name":"Scion","letter":"S"},{"id":138,"name":"SSC","letter":"S"},{"id":147,"name":"首望","letter":"S"},{"id":149,"name":"陕汽通家","letter":"S"},{"id":325,"name":"SERES赛力斯","letter":"S"},{"id":178,"name":"上海","letter":"S"},{"id":205,"name":"赛麟","letter":"S"},{"id":226,"name":"斯太尔","letter":"S"},{"id":238,"name":"斯达泰克","letter":"S"},{"id":133,"name":"特斯拉","letter":"T"},{"id":161,"name":"腾势","letter":"T"},{"id":407,"name":"Troller","letter":"T"},{"id":403,"name":"TOGG","letter":"T"},{"id":125,"name":"Tramontana","letter":"T"},{"id":339,"name":"天际汽车","letter":"T"},{"id":135,"name":"TVR","letter":"T"},{"id":200,"name":"塔塔","letter":"T"},{"id":202,"name":"泰卡特","letter":"T"},{"id":255,"name":"泰克鲁斯·腾风","letter":"T"},{"id":400,"name":"天美汽车","letter":"T"},{"id":379,"name":"Ultima","letter":"U"},{"id":412,"name":"Vega Innovations","letter":"V"},{"id":342,"name":"Vinfast","letter":"V"},{"id":223,"name":"Venturi","letter":"V"},{"id":249,"name":"VLF Automotive","letter":"V"},{"id":70,"name":"沃尔沃","letter":"W"},{"id":114,"name":"五菱汽车","letter":"W"},{"id":283,"name":"WEY","letter":"W"},{"id":284,"name":"蔚来","letter":"W"},{"id":167,"name":"五十铃","letter":"W"},{"id":291,"name":"威马汽车","letter":"W"},{"id":408,"name":"瓦滋","letter":"W"},{"id":393,"name":"潍柴汽车","letter":"W"},{"id":99,"name":"威兹曼","letter":"W"},{"id":102,"name":"威麟","letter":"W"},{"id":159,"name":"沃克斯豪尔","letter":"W"},{"id":192,"name":"潍柴英致","letter":"W"},{"id":233,"name":"W Motors","letter":"W"},{"id":71,"name":"雪佛兰","letter":"X"},{"id":12,"name":"现代","letter":"X"},{"id":396,"name":"新宝骏","letter":"X"},{"id":72,"name":"雪铁龙","letter":"X"},{"id":275,"name":"小鹏汽车","letter":"X"},{"id":350,"name":"星途","letter":"X"},{"id":98,"name":"西雅特","letter":"X"},{"id":324,"name":"新特汽车","letter":"X"},{"id":185,"name":"新凯","letter":"X"},{"id":73,"name":"英菲尼迪","letter":"Y"},{"id":111,"name":"野马汽车","letter":"Y"},{"id":144,"name":"依维柯","letter":"Y"},{"id":263,"name":"驭胜","letter":"Y"},{"id":399,"name":"一汽凌河","letter":"Y"},{"id":382,"name":"远程汽车","letter":"Y"},{"id":375,"name":"银隆新能源","letter":"Y"},{"id":93,"name":"永源","letter":"Y"},{"id":110,"name":"一汽","letter":"Y"},{"id":317,"name":"云雀汽车","letter":"Y"},{"id":307,"name":"裕路","letter":"Y"},{"id":232,"name":"御捷","letter":"Y"},{"id":243,"name":"游侠","letter":"Y"},{"id":247,"name":"YAMAHA","letter":"Y"},{"id":298,"name":"宇通客车","letter":"Y"},{"id":286,"name":"云度","letter":"Y"},{"id":94,"name":"众泰","letter":"Z"},{"id":22,"name":"中华","letter":"Z"},{"id":74,"name":"中兴","letter":"Z"},{"id":182,"name":"之诺","letter":"Z"},{"id":153,"name":"Zenvo","letter":"Z"},{"id":206,"name":"知豆","letter":"Z"},{"id":290,"name":"正道汽车","letter":"Z"}]

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'residual_value',
        'MYSQL_TABLE': 'autohome_series',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'residual_value',
        'MONGODB_COLLECTION': 'autohome_series',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        for brand in self.brand_list:
            brandid = brand["id"]
            brandname = brand["name"]
            meta = {
                "brandname": brandname,
                "brandid": brandid
            }
            url = f"https://www.autohome.com.cn/ashx/index/GetHomeFindCar.ashx?type=1&v=1&brandid={brandid}"
            yield scrapy.Request(
                url=url,
                meta=meta
            )

    def parse(self, response):
        item = NewcarNewItem()
        json_data = json.loads(response.text)["result"]
        item["brandid"] = json_data["brandid"]
        item["brandname"] = json_data["brandname"]
        fctlist = json_data["fctlist"]
        for fct in fctlist:
            item["fctid"] = fct["fctid"]
            item["fctname"] = fct["fctname"]
            item["seriesplace"] = fct["seriesplace"]
            series_list = fct["serieslist"]
            for series in series_list:
                item["seriesid"] = series["seriesid"]
                item["seriesName"] = series["seriesName"]
                item["levelName"] = series["levelName"]
                state = series["seriesState"]
                if state == 20:
                    item["seriesState"] = "在售"
                elif state == 40:
                    item["seriesState"] = "停售"
                elif state == 0:
                    item["seriesState"] = "未售"
                else:
                    item["seriesState"] = "在售"
                # print(item)
                item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
                item["url"] = response.url
                item["status"] = item["seriesName"]+'-'+str(item["seriesid"])+'-'+item["seriesState"]
                yield item
                # print(item)


