import mechanize
from lxml import html
import re

def t(obj): return obj.text_content()


przedmioty = {
    "WMI.II-BCH-BIO1": 1
}

class USOS(mechanize.Browser):
    domain = "https://login.uj.edu.pl/login"

    def __init__(self):
        mechanize.Browser.__init__(self)
        self.set_handle_robots(False)
        #user_agent = 'Mozilla/4.0 (compatible; MSIE 6.0; ' + \
        #'Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
        #self.addheaders += [("User-agent",user_agent)]
        self.addheaders += [("Accept-Language",
                             'pl-PL,pl;q=0.8,en-US;q=0.6,en;q=0.4')]

    def login(self, login, haslo):
        try:
            self.open("https://login.uj.edu.pl/login")
            self.select_form(nr=0)
            self.form['username'] = login
            self.form['password'] = haslo
            self.submit()
        except Exception, e:
            print "Wyjatek w mechanize.Browser().submit(), czyszcze cookies"
            print e
            self._ua_handlers['_cookies'].cookiejar = mechanize.CookieJar()
            self.open('/cas/login')
            self.select_form(nr=0)
            self.form['username'] = login
            self.form['password'] = haslo
            self.submit()

        if self.response().read().find('Udane logowanie') == -1:
            raise Exception('Blad logowania po stronie usos.')
        else:
            print "Udane logowanie"


    def tabela(self, url, typ_zajec):
        tree = html.fromstring(self.open(url).read())
        tabela = tree.xpath('//table [@class="grey" and '
                            + 'contains(.,"' + unicode(typ_zajec) + '")]')

    def kupa(self):
        for link in self.links():
            #print link.text, link.url
            for przedmiot in przedmioty.keys():
                regex = re.compile(r"grupyPrzedmiotu.*"+przedmioty[przedmiot])
                if regex.search(link.url):
                    print link.text
                    #if link.url.find("grupyPrzedmiotu.*WMI.II-BCH-BIO1") != -1:
                    #print link.text, link.url
                    #self.click_link(link)
                    url = link.url.replace("odczyt:1", "odczyt:0")
                    self.open(url)

                    resp = self.response().read()
                    tree = html.fromstring(resp)
                    for ocena in tree.xpath ('//input[@name="zajecia"'):

                    self.form(nr=0)


                    f = open("test.html", "w+")
                    f.writelines(self.response().read())
                    f.close()
                    #if self.response().read().find("Rejestracja na przedmioty") != -1:
                    #    print "zajebiscie kurwa!!!!11111"

    def test(self):
        for link in self.links():
            print link.text, link.url


usos = USOS()
usos.login("piotr.kowenzowski@uj.edu.pl", "qweasd12")
usos.open('https://www.usosweb.uj.edu.pl/kontroler.php?_action=actionx:dla_stud/rejestracja/koszyk()')
if usos.response().read().find('Na tej stronie') == -1:
    raise Exception('Blad logowania po stronie usos.')

#usos.test()
#
usos.kupa()