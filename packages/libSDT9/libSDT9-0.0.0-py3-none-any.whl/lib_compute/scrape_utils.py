import time
import requests
from bs4 import BeautifulSoup
import lib_dsa.byte_array as byte_array
import lib_compute.serialization as serialization
import lib_compute.deserialization as deserialization

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import pandas as pd

import random

def read_website(url):
    resp = requests.get(url)
    return resp.content

def scrape_L1(links):
    return [
        read_website(url)
        for url in links
    ]

def read_iter(file_names, mode='rb'):
    result = []
    for file_name in file_names:
        fp = open(file_name, mode)
        fsource = fp.read()
        fp.close()
        result.append(fsource)
    return result

def scrape_write(link, file_name):
    file_repr = read_website(link)
    fp = open(file_name, 'wb')
    fp.write(file_repr)
    fp.close()

def scrape_write_L1(links, out_files):
    for i in range(0, len(links)):
        print(i)
        scrape_write(links[i], out_files[i])

def fwrite_L1(file_name_L1, file_repr_L1, mode='wb'):
    i = 0
    for file_name, file_repr in zip(file_name_L1, file_repr_L1):
        print( i )
        i += 1
        fp = open(file_name, mode)
        fp.write(file_repr)
        fp.close()


def select_links(html_raw):
    # print(html_raw)
    soup = BeautifulSoup(html_raw, 'html.parser')
    L1 = soup.find_all('a')
    result = []
    for x in L1:
        # print(x)
        # if 'href' in x:
        if 'href' not in x.attrs:
            continue
        result.append( x.attrs['href'] )
    # print( len(result) )
    return result

def vba_write(base_path, str_L1, is_bytes=False):
    vba = byte_array.make_vba(base_path)

    if is_bytes:
        vba.batch_insert_bytes(str_L1)
        return

    target_bytes_L1 = []
    try:
        target_bytes_L1 = [ x.encode('latin-1') for x in str_L1 ]
    except Exception as e:
        target_bytes_L1 = [ x.encode() for x in str_L1 ]
    vba.batch_insert_bytes(target_bytes_L1)

# M: raw html => evaluated js html
def eval_html_srcs(file_name_L1, out_file_L1, time_sleep=1, executable_path=''):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=executable_path)

    for fspath, out_file in zip(file_name_L1, out_file_L1):
        file_name = f'file://{fspath}'
        print(file_name)

        try:
            X = driver.get(file_name)
            time.sleep(time_sleep)
            Y = driver.page_source
        except Exception as e:
            continue

        fp = open(out_file, 'w')
        fp.write(Y)
        fp.close()

    driver.quit()

# soup.find_all(tag_name, class_=[str], attrs=[dict])

# soup element API
# ['__bool__', '__call__', '__class__', '__contains__', '__copy__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', '_all_strings', '_find_all', '_find_one', '_is_xml', '_lastRecursiveChild', '_last_descendant', '_should_pretty_print', 'append', 'attrs', 'can_be_empty_element', 'cdata_list_attributes', 'childGenerator', 'children', 'clear', 'contents', 'decode', 'decode_contents', 'decompose', 'decomposed', 'descendants', 'encode', 'encode_contents', 'extend', 'extract', 'fetchNextSiblings', 'fetchParents', 'fetchPrevious', 'fetchPreviousSiblings', 'find', 'findAll', 'findAllNext', 'findAllPrevious', 'findChild', 'findChildren', 'findNext', 'findNextSibling', 'findNextSiblings', 'findParent', 'findParents', 'findPrevious', 'findPreviousSibling', 'findPreviousSiblings', 'find_all', 'find_all_next', 'find_all_previous', 'find_next', 'find_next_sibling', 'find_next_siblings', 'find_parent', 'find_parents', 'find_previous', 'find_previous_sibling', 'find_previous_siblings', 'format_string', 'formatter_for_name', 'get', 'getText', 'get_attribute_list', 'get_text', 'has_attr', 'has_key', 'hidden', 'index', 'insert', 'insert_after', 'insert_before', 'isSelfClosing', 'is_empty_element', 'known_xml', 'name', 'namespace', 'next', 'nextGenerator', 'nextSibling', 'nextSiblingGenerator', 'next_element', 'next_elements', 'next_sibling', 'next_siblings', 'parent', 'parentGenerator', 'parents', 'parserClass', 'parser_class', 'prefix', 'preserve_whitespace_tags', 'prettify', 'previous', 'previousGenerator', 'previousSibling', 'previousSiblingGenerator', 'previous_element', 'previous_elements', 'previous_sibling', 'previous_siblings', 'recursiveChildGenerator', 'renderContents', 'replaceWith', 'replaceWithChildren', 'replace_with', 'replace_with_children', 'select', 'select_one', 'setup', 'smooth', 'sourceline', 'sourcepos', 'string', 'strings', 'stripped_strings', 'text', 'unwrap', 'wrap']
