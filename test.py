#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _zipcodetw import Address

def test_address_init():

    expected_tokens = ((u'', u'', u'臺北', u'市'), (u'', u'', u'大安', u'區'), (u'', u'', u'市府', u'路'), (u'1', u'', u'', u'號'))
    assert Address(u'臺北市大安區市府路1號').tokens == expected_tokens
    assert Address('臺北市大安區市府路1號').tokens == expected_tokens

def test_address_init_subno():

    expected_tokens = ((u'', u'', u'臺北', u'市'), (u'', u'', u'大安', u'區'), (u'', u'', u'市府', u'路'), (u'1', u'1', u'', u'號'))
    assert Address(u'臺北市大安區市府路1之1號').tokens == expected_tokens
    assert Address('臺北市大安區市府路1之1號').tokens == expected_tokens

def test_address_init_tricky_input():

    assert Address(u'桃園縣中壢市普義').tokens == ((u'', u'', u'桃園', u'縣'), (u'', u'', u'中壢', u'市'), (u'', u'', u'普義', u''))
    assert Address(u'桃園縣中壢市普義10號').tokens == ((u'', u'', u'桃園', u'縣'), (u'', u'', u'中壢', u'市'), (u'', u'', u'普義', u''), (u'10', u'', u'', u'號'))

    assert Address(u'臺北市中山區敬業1路').tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中山', u'區'), (u'', u'', u'敬業1', u'路'))
    assert Address(u'臺北市中山區敬業1路10號').tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中山', u'區'), (u'', u'', u'敬業1', u'路'), (u'10', u'', u'', u'號'))

def test_address_init_normalization():

    expected_tokens = ((u'', u'', u'臺北', u'市'), (u'', u'', u'大安', u'區'), (u'', u'', u'市府', u'路'), (u'1', u'1', u'', u'號'))
    assert Address(u'臺北市大安區市府路1之1號').tokens == expected_tokens
    assert Address(u'台北市大安區市府路1之1號').tokens == expected_tokens
    assert Address(u'臺北市大安區市府路１之１號').tokens == expected_tokens
    assert Address(u'臺北市　大安區　市府路 1 之 1 號').tokens == expected_tokens
    assert Address(u'臺北市，大安區，市府路 1 之 1 號').tokens == expected_tokens
    assert Address(u'臺北市, 大安區, 市府路 1 之 1 號').tokens == expected_tokens

def test_address_flat():

    addr = Address('臺北市大安區市府路1號')
    assert addr.flat(1) == addr.flat(-3) == u'臺北市'
    assert addr.flat(2) == addr.flat(-2) == u'臺北市大安區'
    assert addr.flat(3) == addr.flat(-1) == u'臺北市大安區市府路'
    assert addr.flat() == u'臺北市大安區市府路1號'

def test_address_repr():

    repr_str = "Address(u'\u81fa\u5317\u5e02\u5927\u5b89\u5340\u5e02\u5e9c\u8def1\u865f')"
    assert repr(Address('臺北市大安區市府路1號')) == repr_str
    assert repr(eval(repr_str)) == repr_str

from _zipcodetw import Rule

def test_rule_init():

    rule = Rule('臺北市,中正區,八德路１段,全')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'八德', u'路'), (u'', u'', u'1', u'段'))
    assert rule.rule_tokens == set([u'全'])

    rule = Rule('臺北市,中正區,三元街,單全')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'三元', u'街'))
    assert rule.rule_tokens == set([u'單', u'全'])

    rule = Rule('臺北市,中正區,三元街,雙  48號以下')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'三元', u'街'), (u'48', u'', u'', u'號'))
    assert rule.rule_tokens == set([u'雙', u'以下'])

    rule = Rule('臺北市,中正區,大埔街,單  15號以上')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'大埔', u'街'), (u'15', u'', u'', u'號'))
    assert rule.rule_tokens == set([u'單', u'以上'])

    rule = Rule('臺北市,中正區,中華路１段,單  25之   3號以下')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'中華', u'路'), (u'', u'', u'1', u'段'), (u'25', u'3', u'', u'號'))
    assert rule.rule_tokens == set([u'單', u'以下'])

    rule = Rule('臺北市,中正區,中華路１段,單  27號至  47號')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'中華', u'路'), (u'', u'', u'1', u'段'), (u'27', u'', u'', u'號'), (u'47', u'', u'', u'號'))
    assert rule.rule_tokens == set([u'單', u'至'])

    rule = Rule('臺北市,中正區,仁愛路１段,連   2之   4號以上')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'仁愛', u'路'), (u'', u'', u'1', u'段'), (u'2', u'4', u'', u'號'))
    assert rule.rule_tokens == set([ u'以上'])

    rule = Rule('臺北市,中正區,杭州南路１段,　  14號含附號')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'中正', u'區'), (u'', u'', u'杭州南', u'路'), (u'', u'', u'1', u'段'), (u'14', u'', u'', u'號'))
    assert rule.rule_tokens == set([u'含附號'])

    rule = Rule('臺北市,大同區,哈密街,　  47附號全')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'大同', u'區'), (u'', u'', u'哈密', u'街'), (u'47', u'', u'', u'號'))
    assert rule.rule_tokens == set([u'附號全'])

    rule = Rule('臺北市,大同區,哈密街,雙  68巷至  70號含附號全')
    assert rule.tokens == ((u'', u'', u'臺北', u'市'), (u'', u'', u'大同', u'區'), (u'', u'', u'哈密', u'街'), (u'68', u'', u'', u'巷'), (u'70', u'', u'', u'號'))
    assert rule.rule_tokens == set([u'雙', u'至', u'含附號全'])

    rule = Rule('桃園縣,中壢市,普義,連  49號含附號以下')
    assert rule.tokens == ((u'', u'', u'桃園', u'縣'), (u'', u'', u'中壢', u'市'), (u'', u'', u'普義', u''), (u'49', u'', u'', u'號'))
    assert rule.rule_tokens == set([u'含附號以下'])

    rule = Rule('臺中市,西屯區,西屯路３段西平南巷,　   1之   3號及以上附號')
    assert rule.tokens == ((u'', u'', u'臺中', u'市'), (u'', u'', u'西屯', u'區'), (u'', u'', u'西屯', u'路'), (u'', u'', u'3', u'段'), (u'', u'', u'西平南', u'巷'), (u'1', u'3', u'', u'號'))
    assert rule.rule_tokens == set([u'及以上附號'])

def test_rule_init_tricky_input():

    rule = Rule('新北市,中和區,連城路,雙 268之   1號以下')
    assert rule.tokens == ((u'', u'', u'新北', u'市'), (u'', u'', u'中和', u'區'), (u'', u'', u'連城', u'路'), (u'268', u'1', u'', u'號'))
    assert rule.rule_tokens == set([u'雙', u'以下'])

    rule = Rule('新北市,泰山區,全興路,全')
    assert rule.tokens == ((u'', u'', u'新北', u'市'), (u'', u'', u'泰山', u'區'), (u'', u'', u'全興', u'路'))
    assert rule.rule_tokens == set([u'全'])

def test_rule_repr():

    repr_str = "Rule(u'\u81fa\u5317\u5e02\u5927\u5b89\u5340\u5e02\u5e9c\u8def1\u865f\u4ee5\u4e0a')"
    assert repr(Rule('臺北市大安區市府路1號以上')) == repr_str
    assert repr(eval(repr_str)) == repr_str

def test_rule_match():

    # standard address w/ standard rules

    addr = Address(u'臺北市大安區市府路5號')

    # 全單雙
    assert     Rule(u'臺北市大安區市府路全').match(addr)
    assert     Rule(u'臺北市大安區市府路單全').match(addr)
    assert not Rule(u'臺北市大安區市府路雙全').match(addr)

    # 以上 & 以下
    assert not Rule(u'臺北市大安區市府路6號以上').match(addr)
    assert     Rule(u'臺北市大安區市府路6號以下').match(addr)
    assert     Rule(u'臺北市大安區市府路5號以上').match(addr)
    assert     Rule(u'臺北市大安區市府路5號').match(addr)
    assert     Rule(u'臺北市大安區市府路5號以下').match(addr)
    assert     Rule(u'臺北市大安區市府路4號以上').match(addr)
    assert not Rule(u'臺北市大安區市府路4號以下').match(addr)

    # 至
    assert not Rule(u'臺北市大安區市府路1號至4號').match(addr)
    assert     Rule(u'臺北市大安區市府路1號至5號').match(addr)
    assert     Rule(u'臺北市大安區市府路5號至9號').match(addr)
    assert not Rule(u'臺北市大安區市府路6號至9號').match(addr)

    # 附號
    assert not Rule(u'臺北市大安區市府路6號及以上附號').match(addr)
    assert     Rule(u'臺北市大安區市府路6號含附號以下').match(addr)
    assert     Rule(u'臺北市大安區市府路5號及以上附號').match(addr)
    assert     Rule(u'臺北市大安區市府路5號含附號').match(addr)
    assert not Rule(u'臺北市大安區市府路5附號全').match(addr)
    assert     Rule(u'臺北市大安區市府路5號含附號以下').match(addr)
    assert     Rule(u'臺北市大安區市府路4號及以上附號').match(addr)
    assert not Rule(u'臺北市大安區市府路4號含附號以下').match(addr)

    # 單雙 x 以上, 至, 以下
    assert     Rule(u'臺北市大安區市府路單5號以上').match(addr)
    assert not Rule(u'臺北市大安區市府路雙5號以上').match(addr)
    assert     Rule(u'臺北市大安區市府路單1號至5號').match(addr)
    assert not Rule(u'臺北市大安區市府路雙1號至5號').match(addr)
    assert     Rule(u'臺北市大安區市府路單5號至9號').match(addr)
    assert not Rule(u'臺北市大安區市府路雙5號至9號').match(addr)
    assert     Rule(u'臺北市大安區市府路單5號以下').match(addr)
    assert not Rule(u'臺北市大安區市府路雙5號以下').match(addr)

def test_rule_match_tail_rules():

    # standard address w/ tail rules

    addr = Address(u'臺北市大安區市府路5號')

    # 全單雙
    assert     Rule(u'全').match(addr)
    assert     Rule(u'單全').match(addr)
    assert not Rule(u'雙全').match(addr)

    # 以上 & 以下
    assert not Rule(u'6號以上').match(addr)
    assert     Rule(u'6號以下').match(addr)
    assert     Rule(u'5號以上').match(addr)
    assert     Rule(u'5號').match(addr)
    assert     Rule(u'5號以下').match(addr)
    assert     Rule(u'4號以上').match(addr)
    assert not Rule(u'4號以下').match(addr)

    # 至
    assert not Rule(u'1號至4號').match(addr)
    assert     Rule(u'1號至5號').match(addr)
    assert     Rule(u'5號至9號').match(addr)
    assert not Rule(u'6號至9號').match(addr)

    # 附號
    assert not Rule(u'6號及以上附號').match(addr)
    assert     Rule(u'6號含附號以下').match(addr)
    assert     Rule(u'5號及以上附號').match(addr)
    assert     Rule(u'5號含附號').match(addr)
    assert not Rule(u'5附號全').match(addr)
    assert     Rule(u'5號含附號以下').match(addr)
    assert     Rule(u'4號及以上附號').match(addr)
    assert not Rule(u'4號含附號以下').match(addr)

    # 單雙 x 以上, 至, 以下
    assert     Rule(u'單5號以上').match(addr)
    assert not Rule(u'雙5號以上').match(addr)
    assert     Rule(u'單1號至5號').match(addr)
    assert not Rule(u'雙1號至5號').match(addr)
    assert     Rule(u'單5號至9號').match(addr)
    assert not Rule(u'雙5號至9號').match(addr)
    assert     Rule(u'單5號以下').match(addr)
    assert not Rule(u'雙5號以下').match(addr)

def test_rule_match_gradual_address():

    # standard rule w/ gradual addresses

    rule = Rule('臺北市中正區丹陽街全')
    assert not rule.match(Address('臺北市'))
    assert not rule.match(Address('臺北市中正區'))
    assert not rule.match(Address('臺北市中正區仁愛路１段'))
    assert not rule.match(Address('臺北市中正區仁愛路１段1號'))

    rule = Rule('臺北市,中正區,仁愛路１段,　   1號')
    assert not rule.match(Address('臺北市'))
    assert not rule.match(Address('臺北市中正區'))
    assert not rule.match(Address('臺北市中正區仁愛路１段'))
    assert     rule.match(Address('臺北市中正區仁愛路１段1號'))

def test_rule_match_rule_all():

    # Be careful of the 全! It will bite you!

    rule = Rule('臺北市,中正區,八德路１段,全')
    assert     rule.match(Address('臺北市中正區八德路１段1號'))
    assert     rule.match(Address('臺北市中正區八德路１段9號'))
    assert not rule.match(Address('臺北市中正區八德路２段1號'))
    assert not rule.match(Address('臺北市中正區八德路２段9號'))

    rule = Rule('臺北市,中正區,三元街,單全')
    assert     rule.match(Address('臺北市中正區三元街1號'))
    assert not rule.match(Address('臺北市中正區三元街2號'))
    assert not rule.match(Address('臺北市中正區大埔街1號'))

    rule = Rule('臺北市,大同區,哈密街,　  45巷全')
    assert     rule.match(Address('臺北市大同區哈密街45巷1號'))
    assert     rule.match(Address('臺北市大同區哈密街45巷9號'))
    assert not rule.match(Address('臺北市大同區哈密街46巷1號'))
    assert not rule.match(Address('臺北市大同區哈密街46巷9號'))

def test_rule_match_tricky_input():

    # The address matched by it must have a even number.
    rule1 = Rule('信義路一段雙全')
    # The address matched by it shall be exactly same.
    rule2 = Rule('信義路一段')

    addr1 = Address('信義路一段')
    addr2 = Address('信義路一段1號')
    addr3 = Address('信義路一段2號')

    assert not rule1.match(addr1)
    assert not rule1.match(addr2)
    assert     rule1.match(addr3)

    assert     rule2.match(addr1)
    assert not rule2.match(addr2)
    assert not rule2.match(addr3)

def test_rule_match_subno():

    rule = Rule('臺北市,中正區,杭州南路１段,　  14號含附號')
    assert not rule.match(Address('臺北市中正區杭州南路1段13號'))
    assert not rule.match(Address('臺北市中正區杭州南路1段13-1號'))
    assert     rule.match(Address('臺北市中正區杭州南路1段14號'))
    assert     rule.match(Address('臺北市中正區杭州南路1段14-1號'))
    assert not rule.match(Address('臺北市中正區杭州南路1段15號'))
    assert not rule.match(Address('臺北市中正區杭州南路1段15-1號'))

    rule = Rule('臺北市,大同區,哈密街,　  47附號全')
    assert not rule.match(Address('臺北市大同區哈密街46號'))
    assert not rule.match(Address('臺北市大同區哈密街46-1號'))
    assert not rule.match(Address('臺北市大同區哈密街47號'))
    assert     rule.match(Address('臺北市大同區哈密街47-1號'))
    assert not rule.match(Address('臺北市大同區哈密街48號'))
    assert not rule.match(Address('臺北市大同區哈密街48-1號'))

    rule = Rule('臺北市,大同區,哈密街,雙  68巷至  70號含附號全')
    assert not rule.match(Address('臺北市大同區哈密街66號'))
    assert not rule.match(Address('臺北市大同區哈密街66-1巷'))
    assert not rule.match(Address('臺北市大同區哈密街67號'))
    assert not rule.match(Address('臺北市大同區哈密街67-1巷'))
    assert     rule.match(Address('臺北市大同區哈密街68巷'))
    assert     rule.match(Address('臺北市大同區哈密街68-1號'))
    assert not rule.match(Address('臺北市大同區哈密街69號'))
    assert not rule.match(Address('臺北市大同區哈密街69-1巷'))
    assert     rule.match(Address('臺北市大同區哈密街70號'))
    assert     rule.match(Address('臺北市大同區哈密街70-1號'))
    assert not rule.match(Address('臺北市大同區哈密街71號'))
    assert not rule.match(Address('臺北市大同區哈密街71-1號'))

    rule = Rule('桃園縣,中壢市,普義,連  49號含附號以下')
    assert     rule.match(Address('桃園縣中壢市普義48號'))
    assert     rule.match(Address('桃園縣中壢市普義48-1號'))
    assert     rule.match(Address('桃園縣中壢市普義49號'))
    assert     rule.match(Address('桃園縣中壢市普義49-1號'))
    assert not rule.match(Address('桃園縣中壢市普義50號'))
    assert not rule.match(Address('桃園縣中壢市普義50-1號'))

    rule = Rule('臺中市,西屯區,西屯路３段西平南巷,　   2之   3號及以上附號')
    assert not rule.match(Address('臺中市西屯區西屯路3段西平南巷1號'))
    assert not rule.match(Address('臺中市西屯區西屯路3段西平南巷1-1號'))
    assert not rule.match(Address('臺中市西屯區西屯路3段西平南巷2號'))
    assert not rule.match(Address('臺中市西屯區西屯路3段西平南巷2-2號'))
    assert     rule.match(Address('臺中市西屯區西屯路3段西平南巷2-3號'))
    assert     rule.match(Address('臺中市西屯區西屯路3段西平南巷3號'))
    assert     rule.match(Address('臺中市西屯區西屯路3段西平南巷3-1號'))
    assert     rule.match(Address('臺中市西屯區西屯路3段西平南巷4號'))
    assert     rule.match(Address('臺中市西屯區西屯路3段西平南巷4-1號'))

from _zipcodetw import Directory

class TestDirectory(object):

    def setup(self):

        chp_csv_lines = '''郵遞區號,縣市名稱,鄉鎮市區,原始路名,投遞範圍
10058,臺北市,中正區,八德路１段,全
10079,臺北市,中正區,三元街,單全
10070,臺北市,中正區,三元街,雙  48號以下
10079,臺北市,中正區,三元街,雙  50號以上
10068,臺北市,中正區,大埔街,單  15號以上
10068,臺北市,中正區,大埔街,雙  36號以上
10051,臺北市,中正區,中山北路１段,單   3號以下
10041,臺北市,中正區,中山北路１段,雙  48號以下
10051,臺北市,中正區,中山南路,單   5號以下
10041,臺北市,中正區,中山南路,雙  18號以下
10002,臺北市,中正區,中山南路,　   7號
10051,臺北市,中正區,中山南路,　   9號
10048,臺北市,中正區,中山南路,單  11號以上
10001,臺北市,中正區,中山南路,　  20號
10043,臺北市,中正區,中華路１段,單  25之   3號以下
10042,臺北市,中正區,中華路１段,單  27號至  47號
10010,臺北市,中正區,中華路１段,　  49號
10042,臺北市,中正區,中華路１段,單  51號以上
10065,臺北市,中正區,中華路２段,單  79號以下
10066,臺北市,中正區,中華路２段,單  81號至 101號
10068,臺北市,中正區,中華路２段,單 103號至 193號
10069,臺北市,中正區,中華路２段,單 195號至 315號
10067,臺北市,中正區,中華路２段,單 317號至 417號
10072,臺北市,中正區,中華路２段,單 419號以上
10055,臺北市,中正區,丹陽街,全
10051,臺北市,中正區,仁愛路１段,　   1號
10052,臺北市,中正區,仁愛路１段,連   2之   4號以上
10055,臺北市,中正區,仁愛路２段,單  37號以下
10060,臺北市,中正區,仁愛路２段,雙  48號以下
10056,臺北市,中正區,仁愛路２段,單  39號至  49號
10056,臺北市,中正區,仁愛路２段,雙  48之   1號至  64號
10062,臺北市,中正區,仁愛路２段,單  51號以上
10063,臺北市,中正區,仁愛路２段,雙  66號以上'''.split('\n')

        self.dir_ = Directory()
        self.dir_.load_chp_csv(chp_csv_lines)

    def test_find_zipcodes(self):

        assert self.dir_.find_zipcodes('臺北市') == set(['10048', '10062', '10060', '10066', '10001', '10002', '10065', '10041', '10068', '10069', '10072', '10067', '10042', '10070', '10043', '10058', '10079', '10056', '10055', '10052', '10051', '10010', '10063'])
        assert self.dir_.find_zipcodes('臺北市中正區') == set(['10048', '10062', '10060', '10066', '10001', '10002', '10065', '10041', '10068', '10069', '10072', '10067', '10042', '10070', '10043', '10058', '10079', '10056', '10055', '10052', '10051', '10010', '10063'])
        assert self.dir_.find_zipcodes('臺北市中正區仁愛路１段') == set(['10052', '10051'])
        assert self.dir_.find_zipcodes('臺北市中正區仁愛路１段1號') == set(['10051'])

    def test_find(self):

        assert self.dir_.find('臺北市') == '100'
        assert self.dir_.find('臺北市中正區') == '100'
        assert self.dir_.find('臺北市中正區仁愛路１段') == '1005'
        assert self.dir_.find('臺北市中正區仁愛路１段1號') == '10051'

if __name__ == '__main__':
    import uniout
    test_rule_match_subno()
