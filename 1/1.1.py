import urllib.request
import re
url="https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.78b13727dl7gbT&id=598724949790&skuId=4185713437361&areaId=320500&user_id=880734502&cat_id=2&is_b=1&rn=8c61077a198717d0afd1a0298a02dfaf"
data=urllib.request.urlopen(url).read().decode('gbk').replace('&nbsp;',' ')
pat='''<li title=.*?>(.*?)</li>'''
result=re.compile(pat).findall(data)
for i in result:
    print(i)