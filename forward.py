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
    <title>fw.mearie.org</title> 
</head>
<body>
    <h1>fw.<a href="http://mearie.org/">mearie.org</a></h1>
    <p>이 도메인의 사용법:</p>
    <ul>
        <li>링크는 해야 하지만 레퍼러를 보여 주지 않아야 할 주소가 있다고 하면</li>
        <li>그런 주소가 <code>http://example.com/path/to/filename</code>라 하면</li>
        <li>링크 주소를 <code>http://fw.mearie.org/example.com/path/to/filename</code>로 고친다</li>
        <li>URL 스킴이 <code>https</code>라면 <code>http://fw.mearie.org/*example.com/path/to/filename</code> 식으로 쓴다</li>
        <li>끗</li>
    </ul>
    <p>HTML5 <a href="http://www.w3.org/TR/html5/interactive-elements.html#link-type-noreferrer"><code>rel="noreferrer"</code></a> 속성이 하루속히 지원되었으면 좋겠지만 안 되는 사람들을 위하여 시험 전날에 뚝딱 만들었음</p>
    <h2 lang="en">Disclaimers</h2>
    <p lang="en">The owner of this domain, Kang Seonghoon, don't have any responsibility on the generated URL. The URL "generated" from this domain is actually transparent, compared to the most URL shortening services, so I don't have any plan to add a feature to track users. In fact, this server doesn't collect any log for this particular domain at all. If you have to trace a malicious activity using this domain, it would be better to <a href="http://google.com/">google</a> it.</p>
</body>
</html>
'''

class forward(app.page):
    path = '/(\*?)((?:[a-zA-Z0-9-]+\.)+[a-zA-Z0-9-]{2,}/.*)'
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

