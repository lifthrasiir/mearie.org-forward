#!/usr/bin/env python
# coding=utf-8

import web

app = web.auto_application()

################################################################################

class index(app.page):
    path = '/'
    def GET(self):
        web.header('Content-type', 'text/html')
        return '''\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ko"> 
<head> 
    <meta http-equiv="Content-Language" content="ko" /> 
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
    <style type="text/css">/*<![CDATA[*/
        body { font-family: "Helvetica Neue", "Helvetica Neue Light", "HelveticaNeue-Light", "Arial", "Helvetica", "나눔고딕", "NanumGothic", "Nanum Gothic", sans-serif; font-size: 0.9em; font-weight: 200; width: 480px; margin: 3em auto; color: white; background: #397; }
        strong { font-weight: 700; }
        h1 { text-align: center; font-size: 250%; line-height: 0.8; }
        h1 img { display: block; margin: 0 auto; }
        h2 { font-size: 150%; }
        p { color: white; line-height: 1.5; }
        a { color: #adc; text-decoration: underline; }
        a:visited { text-decoration: none; }
        ul { list-style: square; line-height: 1.5; padding-left: 1.5em; margin-left: 0; }
    /*]]>*/</style>
    <title>fw.mearie.org</title> 
</head>
<body>
    <h1><img src="http://selene.mearie.org/logo.png" width="117" height="117" alt="" />fw.<a href="http://mearie.org/">mearie.org</a></h1>
    <p>이 도메인은 어디서 왔는지 리퍼러 정보를 남기지 않고 링크를 할 때 씁니당. 물론 서버 로그도 남기지 않습니다.</p>
    <h2>사용법</h2>
    <ul>
        <li>링크는 해야 하지만 레퍼러를 보여 주지 않아야 할 주소가 있다고 하면</li>
        <li>그런 주소가 <code>http://example.com/foo/bar/blah</code>라 하면</li>
        <li>링크 주소를 <code>http://fw.mearie.org/example.com/foo/bar/blah</code>로 고친다</li>
        <li>URL 스킴이 <code>https</code>라면 <code>http://fw.mearie.org/*example.com/foo/bar/blah</code> 식으로 쓴다</li>
        <li>끗</li>
    </ul>
    <p>주의: 자바스크립트를 쓰므로 이미지 링크에는 효과가 없습니다. 이보세요! 여긴 지금 중환자실입니다. 전화는 없어요.</p>
    <h2>좀 더 편한 방법</h2>
    <p>HTML5 <a href="http://www.w3.org/TR/html5/interactive-elements.html#link-type-noreferrer"><code>rel="noreferrer"</code></a>을 이미 쓰고 있다면 <code>&lt;/body&gt;</code> 앞에 이런 코드를 넣어도 됩니다.</p>
    <pre>&lt;script type="<a href="script">http://fw.mearie.org/script</a>"&gt;&lt;/script&gt;</pre>
    <p><a href="http://dahlia.kr/">홍민희</a> 님께서 만드신 코드를 적절히 뜯어 고쳤습니다 ㄱㅅㄱㅅ</p>
    <h2 lang="en">Disclaimers</h2>
    <p lang="en">The owner of this domain, Kang Seonghoon, don't have any responsibility on the generated URL. The URL "generated" from this domain is actually transparent, compared to the most URL shortening services, so I don't have any plan to add a feature to track users. In fact, this server doesn't collect any log for this particular domain at all. If you have to trace a malicious activity using this domain, it would be better to <a href="http://google.com/">google</a> it.</p>
</body>
</html>
'''

class script(app.page):
    path = '/script'
    def GET(self):
        web.header('Content-type', 'application/javascript')
        return '''\
(function(){
    var apply = function(e) {
        if (e.getAttribute('rel') != 'noreferrer') return;
        var href = e.getAttribute('href');
        if (!href || href.match(/^http:\/\/fw\.mearie\.org\/./)) {
            return;
        } else if (href.match(/^http:/)) {
            href = href.substr(7);
        } else if (href.match(/^https:/)) {
            href = '*' + href.substr(8);
        } else {
            return;
        }
        if (href.match(/^[^\/]+$/)) href += '/';
        e.setAttribute('href', 'http://fw.mearie.org/' + href);
    };

    if (document.querySelectorAll) {
        var ee = document.querySelectorAll('a[rel=noreferrer]'), l = ee.length;
        for (var i = 0; i < l; ++i) apply(ee[i]);
    } else if (document.evaluate) {
        var ee = document.evaluate('//a[@rel="noreferrer"]', document, null, XPathResult.UNORDERED_NODE_ITERATOR_TYPE, null), e;
        while (e = ee.iterateNext) apply(e);
    } else {
        var ee = document.getElementsByTagName('a'), l = ee.length;
        for (var i = 0; i < l; ++i) {
            if (ee[i].getAttribute('rel') == 'noreferrer') apply(ee[i]);
        }
    }
}());
'''

class forward(app.page):
    path = '/(\*?)((?:(?:[a-zA-Z0-9-]+\.)+[a-zA-Z0-9-]{2,}|(?:[0-9]+\.){3}[0-9]+)(?::[0-9]+)?/.*)'
    def GET(self, scheme, url):
        if scheme == '':
            scheme = 'http'
        elif scheme == '*':
            scheme = 'https'
        else:
            raise RuntimeError
        url = '%s://%s%s' % (scheme, url, web.ctx.query)
        web.header('Content-type', 'text/html')
        return '''\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"> 
<head> 
    <meta http-equiv="Content-Language" content="en" /> 
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
    <title>fw.mearie.org</title> 
    <script type="text/javascript">/*<![CDATA[*/
        window.onload = function() { location.replace('%(jsurl)s' + location.hash); }
    /*]]>*/</script>
</head>
<body>
    <noscript><p>You will be redirected to <a id="url" href="%(url)s"><code>%(url)s</code></a> soon, or please refer this link if you have disabled Javascript. This mechanism exists for avoiding the unneeded referrer exposure only.</p></noscript>
</body>
</html>
''' % {
            'url': url.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;'),
            'jsurl': url.replace('\\', '\\\\').replace("'", "\\\'").replace('/', '\\/'),
        }

################################################################################

if __name__ == '__main__': app.run()

