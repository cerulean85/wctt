import re
import copy
import html5lib
from bs4 import BeautifulSoup
from modules.extractor import ExtractorConfig as tfg
from modules.extractor.TextNode import TextNode

class ExtractorTextNode:
    def __init__(self):
        super().__init__()
        self.__text_node_list = []
        self.__file_name = ''
        self.ENABLED_TEXT_COUNT = 3

    def __explore_node(self, depth, parent_path_tags, prev_node_name, current_node):
        def get_tag_name(__node):
            tag = str(__node.tag).replace('{http://www.w3.org/1999/xhtml}', '')
            tag = tag.replace('{http://www.w3.org/2000/xhtml}', '')
            tag = tag.replace('{http://www.w3.org/2000/svg}', '')
            return tag

        depth = depth + 1
        pts = parent_path_tags
        pts.append(prev_node_name)

        for i in range(0, len(current_node)):
            node = current_node[i]
            tagname = get_tag_name(node)

            tail_text = str(node.tail).replace('\n', '')  # 중앙일보의 경우의 조건
            if len(node) == 0 or (tail_text != "None" and len(tail_text) > 0):
                target_text = str(node.text) + ' ' + str(node.tail)
                target_text = self.__replace_words_prev(target_text)
                target_text = self.__clean_stopwords(target_text)
                target_text = self.__replace_words_post(target_text)

                if target_text != 'None' and len(target_text) > self.ENABLED_TEXT_COUNT:
                    target_text = re.sub('\n', '', target_text, 0)
                    tb = TextNode(target_text, copy.deepcopy(pts), 0)
                    self.__text_node_list.append(tb)

                continue

            self.__explore_node(depth, copy.deepcopy(pts), tagname, node)

    def create_text_node_list(self, target_path, filename):

        dom, s_text = self.__dom_create(target_path + filename)
        self.__explore_node(0, [], 'html', list(dom))
        result_text_nodes = []
        for tb in self.__text_node_list:
            text = tb.get_text()
            if text != '':
                result_text_nodes.append({
                    "text": text,
                    "ptp": tb.get_parent_tag_path()
                })
                # result_text_nodes += text + ',' + tb.get_parent_tag_path() + ',1\n'
        return result_text_nodes

    def get_tb_arr(self):
        return self.__text_node_list

    def __dom_create(self, filename):
        f = open(filename, 'rb')
        html = f.read()
        f.close()

        html = html.decode('utf-8')
        html = re.sub('<', '\n<', html)
        soup = BeautifulSoup(html, "html.parser")
        return html5lib.parse(str(soup)), soup.get_text()

    def __replace_words_prev(self, text):
        for r_word in tfg.PRE_PROC_REPLACE_DICT.items():
            text = text.replace(r_word[0], r_word[1])
        return text

    def __replace_words_post(self, text):
        for r_word in tfg.POST_PROC_REPLACE_DICT.items():
            text = text.replace(r_word[0], r_word[1])
        return text

    def __clean_stopwords(self, text):
        for stopword in tfg.PRE_PROC_STOPWORD_DICT.items():
            from_word, to_word = stopword[0], stopword[1]
            try:
                text = re.sub(from_word, to_word, text)
            except Exception as e:
                print(e)
        return text

    def __evil_text(self, text):
        for etxt in tfg.PRE_PROC_EVIL_TEXT:
            if etxt in text:
                return True

        return False
