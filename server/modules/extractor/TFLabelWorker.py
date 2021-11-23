import os
# from multiprocessing import Process, Value
#
# from text_extraction.extractor.TFBase import TFBase
# from text_extraction.TFFile import TFFile
# from text_extraction.extractor.TFWebDoc import TFWebDoc
#
#
# def get_docs_count(target_channel_type, target_ext_type):
#     tfb = TFBase()
#     tff = TFFile()
#
#     target_path = tfb.get_target_path(target_channel_type, target_ext_type)
#     file_list = tff.get_file_list(target_path)
#
#     return len(file_list)
#
#
# def iter_docs(target_channel_type, target_ext_type, si, ei):
    # tfb = TFBase()
    # tff = TFFile()
    #
    # target_path = tfb.get_target_path(target_channel_type, target_ext_type)
    # file_list = tff.get_file_list(target_path)[si:ei]
    #
    # # file_list = ["nav_web_doc_1773.csv", "nav_web_doc_3554.csv"]
    # # print(file_list)
    #
    # # ir_count = 0
    # __web_doc_list = []
    # for filename in file_list:  # file_list[132:133]:
    #     wd = TFWebDoc()
    #     # print(filename)
    #     if ".csv" in filename:
    #         wd.load_text_blocks(target_path, filename)
    #         __web_doc_list.append(wd)
    #
    #     # ir_count = ir_count + 1
    #     # if ir_count == 100:
    #     #     break
    #
    # return __web_doc_list


# def write_web_doc(target_path, wdoc, new_tb_arr):
#     if len(new_tb_arr) > 0:
#         tff = TFFile()
#         tff.write_web_doc(target_path, wdoc.get_filename(), new_tb_arr)
#
#
# def get_target_path(channel_type, ext_type):
#     tfb = TFBase()
#     target_path = tfb.get_target_path(channel_type, ext_type)
#     return target_path
#
#
# def labeling_tweeter(start_index, end_index, total_doc_count, finished_doc_count):
#     pp_tags = [
#         "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/article/div/div/div/div/div/div/div/div/div/div/a/div/div/div/span",
#         # "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/article/div/div/div/div/div/div/div/div/div/a",
#         "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/article/div/div/div/div/div/div/div/div/span",
#         "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/article/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/span",
#         "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/article/div/div/div/div/div/div/div/div/div/div/div/span",
#         "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/article/div/div/div/div/div/div/div/div/div/div/div/div/div/div/span",
#         "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/article/div/div/div/div/div/div/div/div/div/div/div/article/div/div/div/div/div/div/div/div/div/a",
#         "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/article/div/div/div/div/div/div/div/div/div/div/div/article/div/div/div/div/div/div/div/div/div/div/span",
#         "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/div/h1",
#         "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/div/div",
#         "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/div/div/a/div/span",
#         "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/div/div/div/div",
#         "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/div/div/div",
#         "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/article/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div",
#     ]
#
#     pp_dict = {
#         "코로나 백신트위터 검색트위터": "html/head",
#         "자바스크립트를 사용할 수 없습니다": "html/body/noscript/div",
#         "이 브라우저에서 자바스크립트를 사용할 수 없는 것으로 감지되었습니다 을 계속 사용하려면 자바스크립트를 사용 설정하거나 지원되는 브라우저로 전환하세요 트위터 고객센터에서 지원되는 브라우저 목록을 확인할 수 있습니다": "html/body/noscript/div",
#         "고객센터": "html/body/noscript/div/p",
#         "이용약관": "html/body/noscript/div/p",
#         "개인정보 처리방침": "html/body/noscript/div/p",
#         "쿠키 정책": "html/body/noscript/div/p",
#         "광고 정보": "html/body/noscript/div/p",
#         "최신 소식을 놓치지 마세요": "html/body/div/div/div/div/div/div/div/div/div/div/div/div",
#         "트위터를 사용하면 가장 먼저 알게 됩니다": "html/body/div/div/div/div/div/div/div/div/div/div/div/div",
#         "로그인": "html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/a/div/span",
#         "가입하기": "html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/a/div/span",
#         "새 트윗 보기": "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/div/div/div",
#         "타임라인 검색": "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section",
#         "이 스레드 보기": "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/article/div/a/div/div/div",
#         "트윗 인용하기": "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/article/div/div/div/div/div/div/div/div/div/div/div",
#         # "영상보기": "html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/section/div/div/div/div/div/article/div/div/div/div/div/div/div/div"
#     }
#
#     no_tag_list = [
#         "html/head",
#         "html/body",
#         "html/body/noscript"
#     ]
#
#     docs = iter_docs("tweeter", "predict", start_index, end_index)
#     target_path = get_target_path("tweeter", "label")
#     print(target_path)
#
#     for wdoc in docs:
#         tb_arr = wdoc.get_tb_arr()
#         new_tb_arr = ["line,text,tags,word_density,lb\n"]
#
#         for tb in tb_arr:
#             line = tb.get_line()
#             text = tb.get_text()
#             tags = tb.get_parent_tags()
#             tags_pattern = tb.get_parent_tags_pattern()
#             word_density = tb.get_word_density()
#
#             pp = False
#
#             ## pp_tags
#             for pt in pp_tags:
#                 if tags == pt.split('/'):
#                     pp = True
#                     break
#
#             ## pp_dict
#             if not pp:
#                 for pd in pp_dict.items():
#
#                     pd_txt, pd_tag = pd[0], pd[1]
#                     if text == pd_txt and tags_pattern == pd_tag:
#                         pp = True
#                         break
#
#             # print(tags_pattern)
#             # if tags in no_tag_list:
#             label = 0 if pp or (tags_pattern in no_tag_list) else 1
#             # (0 if pp else 1)
#
#             tb_data = wdoc.get_tb_data(line, text, tags, word_density, label)
#             new_tb_arr.append(tb_data)
#
#         write_web_doc(target_path, wdoc, new_tb_arr)
#         print("Finished: {:0.2f}% ({}/{})".format((finished_doc_count.value / total_doc_count) * 100,
#                                                   finished_doc_count.value, total_doc_count))
#         finished_doc_count.value += 1
#
#
# def labeling_instagram(web_doc_list):
#     true_pp_tags = [
#         "html/body/div/section/main/div/div/article/div/div/ul/div/li/div/div/div/span",
#         "html/body/div/section/main/div/div/article/div/div/ul/ul/div/li/div/div/div",
#         "html/head",
#         "html/body/div/section/main/div/div/article/div/div/a"
#     ]
#
#     iter_docs("instagram", "predict")
#     target_path = get_target_path("instagram", "label")
#     for wdoc in web_doc_list:
#         tb_arr = wdoc.get_tb_arr()
#         new_tb_arr = ["line,text,tags,word_density,lb\n"]
#
#         for tb in tb_arr:
#             line = tb.get_line()
#             text = tb.get_text()
#             tags = tb.get_parent_tags()
#             word_density = tb.get_word_density()
#
#             pp = False
#             ## pp_tags
#             for pt in true_pp_tags:
#                 if tags == pt.split('/'):
#                     pp = True
#                     break
#
#             tb_data = wdoc.get_tb_data(line, text, tags, word_density, (1 if pp else 0), )
#             new_tb_arr.append(tb_data)
#
#         write_web_doc(target_path, wdoc, new_tb_arr)
#
#
# def labeling_naver_blog(start_index, end_index, total_doc_count, finished_doc_count):
#
#     print(start_index, end_index)
#
#     docs = iter_docs("naver_blog", "predict", start_index, end_index)
#     target_path = get_target_path("naver_blog", "label")
#     print(target_path)
#     top_list = [
#         "C 상품",
#         "스마트에디터3 타이틀 제거 임시 적용"
#     ]
#     bot_list = [
#         "이 글에 공감한 블로거 열고 닫기",
#         "스마트에디터3 타이틀 제거 임시 적용",
#         "소셜플러그인"
#     ]
#     direct_list = [
#         "다시 보내기",
#         "블로그앱",
#         "모바일에서 작성된 글입니다",
#         "스마트에디터3 타이틀 제거 임시 적용",
#         "번역하기",
#         "이 글에 댓글 단 블로거 열고 닫기",
#         "라이센스",
#         "동영상 인코딩 중입니다",
#         "5분 이상 소요될 수 있으며 영상의 길이에 따라 소요 시간은 달라집니다",
#         "재생 수",
#         "마우스를 드래그 하세요",
#         "360°",
#         "멀티트랙의 트랙별 영상은 우측 관련영상에서 볼 수 있습니다",
#         "선거광고 안내",
#         "화질 선택 옵션",
#         "전체화면",
#         "광고정보 더보기",
#         "광고 후 계속됩니다",
#         "소스 코드",
#         "플레이어",
#         "레이어 닫기",
#         "접기펴기",
#     ]
#     ext_file = ["nav_web_doc_1773.csv"]
#
#     for wdoc in docs:
#         tb_arr = wdoc.get_tb_arr()
#         new_tb_arr = ["line,text,tags,word_density,lb\n"]
#         is_lb = False
#         top_str = ''
#         for tb in tb_arr:
#             line = tb.get_line()
#             text = tb.get_text()
#             p_tags = tb.get_parent_tags()
#             word_density = tb.get_word_density()
#             label = 0
#             tb_data = wdoc.get_tb_data(line, text, p_tags, word_density, label)
#
#             if text in top_list:
#                 new_tb_arr.append(tb_data)
#                 if text == top_str:
#                     for i in range(len(new_tb_arr) - 1, 0, -1):
#                         contents = new_tb_arr[i]
#                         new_tb_arr[i] = contents[0:len(contents) - 2] + "0\n"
#
#                 top_str = text
#                 is_lb = True
#
#             elif text in bot_list:
#                 new_tb_arr.append(tb_data)
#                 is_lb = False
#
#             else:
#                 if text != '':
#                     lb = str(1 if is_lb and text not in direct_list else 0)
#                     tb_data = wdoc.get_tb_data(line, text, p_tags, word_density, lb)
#                     new_tb_arr.append(tb_data)
#         # print(new_tb_arr)
#         write_web_doc(target_path, wdoc, new_tb_arr)
#         print("Finished: {:0.2f}% ({}/{})".format((finished_doc_count.value / total_doc_count) * 100,
#                                                   finished_doc_count.value, total_doc_count))
#         finished_doc_count.value += 1
#
#
# def labeling_joongang(start_index, end_index, total_doc_count, finished_doc_count):
#     docs = iter_docs("joongang", "predict", start_index, end_index)
#     target_path = get_target_path("joongang", "label")
#
#     for doc in docs:
#         tb_arr = doc.get_tb_arr()
#         new_tb_arr = ["line,text,tags,word_density,lb\n"]
#         # title_label_step = 0
#         title_label_work = False
#         title_label_work_enable_count = 2
#         content_label_work = False
#         # content_label_enabled = False
#         for i in range(0, len(tb_arr)):
#             tb = tb_arr[i]
#             line = tb.get_line()
#             text = tb.get_text()
#             p_tags = tb.get_parent_tags()
#
#             tags = ''
#             for k in range(0, len(p_tags)):
#                 tags += p_tags[k] + ('' if k == (len(p_tags) - 1) else '/')
#
#             word_density = tb.get_word_density()
#             label = 0
#
#             if title_label_work:
#                 label = 1
#
#             if content_label_work:
#                 label = 1
#                 # label = 0 if (i == len(tb_arr) - 1) and (word_density == 0.0001) else 1
#
#             if not content_label_work and text == "아티클 공통기자":
#                 label = 0
#                 content_label_work = True
#
#             # if content_label_work and text == "아티클 ":
#             if content_label_work and text == "아티클 공통태그":
#                 label = 0
#                 content_label_work = False
#
#
#             # if text == "중앙그룹 브랜드 메뉴" and tags == "html/body/div":
#             #     label = 0
#             #     title_label_work_enable_count -= 1
#             #     if title_label_work_enable_count == 0:
#             #         title_label_work = True
#             #
#             # elif text == "아티클 공통기자" and tags == "html/body/div/div/div/div/div":
#             #     label = 0
#             #     title_label_work = False
#             #
#             # elif text == "클릭 수" and tags == "html/body/div/div/div/div/div/div/dl/dd/span":
#             #     label = 0
#             #     content_label_work = True
#             #
#             # elif text == "관련기사" and tags == "html/body/div/div/div/div/div/div/div/div/h2":
#             #     label = 0
#             #     content_label_work = False
#             #
#             # elif text == "아티클 " and tags == "html/body/div/div/div/div/div/div":
#             #     label = 0
#             #     content_label_work = False
#             #
#             # elif text == "9 15 15 15 15" and tags == "html/body":
#             #     label = 0
#             #     content_label_work = True
#
#             # elif text == "중앙그룹 브랜드 메뉴":
#             #     title_label_step += 1
#             #     if title_label_step == 2:
#             #         title_label_work = True
#             #
#             # patterns = "^(입력) [0-9]{8,} [0-9]{4,}$"
#             # m = re.match(patterns, text)
#             # if m is not None:
#             #     label = 1
#
#             # elif
#
#             tb_data = doc.get_tb_data(line, text, p_tags, word_density, label)
#
#
#             new_tb_arr.append(tb_data)
#
#         write_web_doc(target_path, doc, new_tb_arr)
#         print("Finished: {:0.2f}% ({}/{})".format((finished_doc_count.value / total_doc_count) * 100,
#                                                   finished_doc_count.value, total_doc_count))
#         finished_doc_count.value += 1
#
#         # title_label_work = True
#         # label = 0
#         # tb_data = doc.get_tb_data(line, text, p_tags, word_density, label)
#         # new_tb_arr.append(tb_data)


# def labeling_donga(start_index, end_index, total_doc_count, finished_doc_count):
from modules.zhbase.ZHPandas import ZHPandas

def labeling_donga():

    path = "D:/__programming/__data3/dna/nodes"
    save_path = "D:/__programming/__data3/dna/label"
    if not os.path.isdir(save_path):
        os.makedirs(save_path, exist_ok=True)

    content_tp_list = ["html/body/div/div/div/div"]

    zhp = ZHPandas()
    file_list = os.listdir(path)
    for file in file_list:
        if ".csv" in file:
            file_path = path + '/' + file
            result = zhp.read_csv(file_path)
            for index in range(0, len(result)):
                tp = result.tags.values[index]
                result.lb.values[index] = 1 if tp in content_tp_list else 0
            zhp.save_csv(result, save_path + '/' + file)











    # channel_type, ext_type = "donga", "predict"
    # for file

    # docs = iter_docs("donga", "predict", start_index, end_index)
    # target_path = get_target_path("donga", "label")

    # ext_tag_list = [
    #     "html/body", "html/body/div/div/div/dl/dd", "html/body/div/div/div/dl/dt"
    # ]
    # ext_text_list = [
    #     "다국어뉴스", "에서도 동아일보의 기사를 보실 수 있습니다", "더보기메뉴", "최대 폰트 사이즈입니다",
    #     "최소 폰트 사이즈입니다", "60 00", "a l0 e", "ee 8e", " b q l"
    # ]
    #
    # for doc in docs:
    #     tb_arr = doc.get_tb_arr()
    #     new_tb_arr = ["line,text,tags,word_density,lb\n"]
    #
    #     content_label_work = False
    #     for tb in tb_arr:
    #
    #         line = tb.get_line()
    #         text = tb.get_text()
    #         p_tags = tb.get_parent_tags()
    #         word_density = 0  # tb.get_word_density()
    #
    #         tags = ''
    #         label = 0
    #         for i in range(0, len(p_tags)):
    #             tags += p_tags[i] + ('' if i == (len(p_tags) - 1) else '/')
    #
    #         if tags == "undefined" and text == "최대 폰트 사이즈입니다":
    #             content_label_work = True
    #             tb_data = doc.get_tb_data(line, text, p_tags, word_density, label)
    #             new_tb_arr.append(tb_data)
    #             continue
    #
    #         if tags == "undefined" and text == "기사를 추천 하셨습니다":
    #             content_label_work = False
    #             tb_data = doc.get_tb_data(line, text, p_tags, word_density, label)
    #             new_tb_arr.append(tb_data)
    #             continue
    #
    #         if tags == "undefined" and content_label_work:
    #             label = 1
    #
    #         tb_data = doc.get_tb_data(line, text, p_tags, word_density, label)
    #         new_tb_arr.append(tb_data)
    #
    #     write_web_doc(target_path, doc, new_tb_arr)
    #     print("Finished: {:0.2f}% ({}/{})".format((finished_doc_count.value / total_doc_count) * 100,
    #                                               finished_doc_count.value, total_doc_count))
    #     finished_doc_count.value += 1


if __name__ == '__main__':
    labeling_donga()

    # p_count = 4
    # # channel_type, ext_type = "tweeter", "predict"
    # channel_type, ext_type = "donga", "predict"
    # total_doc_count = get_docs_count(channel_type, ext_type)
    # # print(total_doc_count)
    # finished_doc_count = Value('i', 0)
    # unit_count = int(total_doc_count / p_count)
    # remain_count = total_doc_count % p_count
    #
    # end_index = 0
    # p_list = []
    # for i in range(0, p_count):
    #     start_index = unit_count * i
    #     end_index = unit_count * (i + 1)
    #     p_list.append(
    #         Process(target=labeling_donga, args=(start_index, end_index, total_doc_count, finished_doc_count)))
    #         # Process(target=labeling_naver_blog, args=(start_index, end_index, total_doc_count, finished_doc_count)))
    #         # Process(target=labeling_tweeter, args=(start_index, end_index, total_doc_count, finished_doc_count)))
    #
    # if remain_count > 0:
    #     start_index = end_index
    #     end_index = end_index + remain_count
    #     p_list.append(
    #         Process(target=labeling_donga, args=(start_index, end_index, total_doc_count, finished_doc_count)))
    #         # Process(target=labeling_naver_blog, args=(start_index, end_index, total_doc_count, finished_doc_count)))
    #         # Process(target=labeling_tweeter, args=(start_index, end_index, total_doc_count, finished_doc_count)))
    #
    # for p in p_list:
    #     p.start()