# -*- coding:utf8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString


def translate_html(html_data, text_dict):
    soup = BeautifulSoup(html_data)
    html_texts = soup.findAll(text=True)
    for html_text in html_texts:
        if type(html_text) == NavigableString:
            text_key = unicode(html_text.strip())
            if text_key:
                print text_key.encode('utf8')
                print '-' * 10
                text_value = text_dict.get(text_key, None)
                if text_value:
                    html_text.replaceWith(text_value)
    return soup

if __name__ == '__main__':
    def main():
        # import urllib
        # html_data = urllib.urlopen(
        # 'https://github.com/liks79/flask/'
        # 'blob/docs-korean/docs/en/advanced_foreword.rst').read()
        # open('test.html', 'wb').write(html_data)
        html_data = open('test.html', 'rb').read()
        translate_html(html_data, {u'Sign up': u'가입하기'})

    main()
