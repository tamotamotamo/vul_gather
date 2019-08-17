#!/usr/bin/env python
# coding:utf-8

import os
import codecs
import feedparser
from datetime import datetime


# Main Transaction
class rss:
    def __init__(self, name=None, url=None):
        self.name = name
        self.url = url
        self.dic = feedparser.parse(self.url)
        str_rss_date = self.dic.feed.date[0:19].replace('T', ' ')
        self.rss_date = datetime.strptime(str_rss_date, '%Y-%m-%d %H:%M:%S')


def cleanup(string):
    string = string.replace('\n', ' ').replace('\r', ' ').replace(',', ' ')
    return string


# Extract information from RSS
def rss_extract(name, dic):
    with codecs.open(result_file, 'a', 'utf-8') as f:
        for entry in dic.entries:
            date = entry.updated[0:10].replace('-', '/')
            time = entry.updated[11:16]
            title = cleanup(entry.title)
            desc = cleanup(entry.description)
            link = entry.link
            f.write(name + ',')
            f.write(date + ',')
            f.write(time + ',')
            f.write(title + ',')
            f.write(desc + ',')
            if name == "jvn":
                dcid = entry.dc_identifier
                f.write(dcid + ',')
                f.write('-' + ',')
                f.write('-' + ',')
            elif name == "jvndb":
                sec_id = entry.sec_identifier
                f.write(sec_id + ',')
                if "sec_cvss" in entry:
                    sec_cvss_dict = entry.sec_cvss
                    cvss_sev_v3 = sec_cvss_dict["severity"]
                    cvss_score_v3 = sec_cvss_dict["score"]
                    f.write(cvss_sev_v3 + ',')
                    f.write(cvss_score_v3 + ',')
                else:
                    f.write('-' + ',')
                    f.write('-' + ',')
            elif name == "nistdb":
                f.write('-' + ',')
                f.write('-' + ',')
                f.write('-' + ',')
                #   elif name == "vulmon":
                f.write('-' + ',')
                f.write('-' + ',')
                f.write('-' + ',')
            f.write(link + '\n')


def main():
    if os.path.isfile(result_file):
        # Get result file update time
        file_date = datetime.fromtimestamp(os.stat(result_file).st_mtime)

        if jvn.rss_date > file_date:
            rss_extract(jvn.name, jvn.dic)

        if jvndb.rss_date > file_date:
            rss_extract(jvndb.name, jvndb.dic)

        if nistdb.rss_date > file_date:
            rss_extract(nistdb.name, nistdb.dic)

    else:
        with codecs.open(result_file, 'a', encoding='utf-8') as f:
            f.write('category' + ',')
            f.write('date' + ',')
            f.write('time' + ',')
            f.write('title' + ',')
            f.write('desc' + ',')
            f.write('id' + ',')
            f.write('cvss_v3_sev' + ',')
            f.write('cvss_v3_score' + ',')
            f.write('link' + '\n')

        # Extract for jvn
        rss_extract(jvn.name, jvn.dic)

        # Extract for jvndb(iPedia)
        rss_extract(jvndb.name, jvndb.dic)

        # Extract for NIST National Vulnerability Database
        rss_extract(nistdb.name, nistdb.dic)

        # Extract for Vulmon
        # rss_extract(vulmon.name, vulmon.dic)


if __name__ == "__main__":
    # Create result file
    result_file = 'result.csv'

    # Transaction for jvn
    jvn = rss('jvn', 'http://jvn.jp/rss/jvn.rdf')

    # Transaction for jvndb(iPedia)
    jvndb = rss('jvndb', 'http://jvndb.jvn.jp/rss/ja/jvndb.rdf')

    # Transaction for NIST National Vulnerability Database
    nistdb = rss('nistdb', 'https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml')

    # Transaction for NIST National Vulnerability Database
    # vulmon = rss('vulmon', 'https://vulmon.com/searchfeed?q=*&sortby=bydate&remote=on&local=on&physical=on&nanalyzed=on')

    main()
