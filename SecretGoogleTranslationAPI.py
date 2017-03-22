# coding=utf-8
import json
import re
import sys
import urllib
import urllib2

reload(sys)
sys.setdefaultencoding("utf-8")


class Translate:
    def translate(self, text, target_lang='hi', src_lang='auto'):
        text = text.replace(u'\xa0', u' ')
        text = text.encode('utf-8')
        text = urllib.quote(text)

        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
        request = urllib2.Request("https://translate.googleapis.com/translate_a/single?client=gtx&sl=" + src_lang + "&tl=" +
                                  target_lang + "&dt=t&q=" + text, headers=header)

        data = urllib2.urlopen(request).read()
        data = re.sub(',+', ',', data)
        json_data = json.loads(data)
        final_list = []
        for i in xrange(0, len(json_data[0])):
            final_list.append(json_data[0][i][0].strip() + u"। ")
        result_string = "".join(final_list)

        return result_string.encode('utf-8')
