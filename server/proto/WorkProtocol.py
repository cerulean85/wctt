import os

import proto.WorkProtocolService_pb2
import proto.WorkProtocolService_pb2_grpc
from multiprocessing import Process
import text_preprocessor as tp
# import modules.Divider


# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./proto/WorkProtocolService.proto

# from url_collector import Collector


class WorkProtocol(proto.WorkProtocolService_pb2_grpc.WorkProtocolServiceServicer):

    def echo(self, request, context):
        for i in range(len(request.workList)):
            work = request.workList[i]
            print("ECHO:", work.requestType)

        reponseList = [
            {
                "message": "111"
            },
            {
                "message": "222"
            }

        ]
        return proto.WorkProtocolService_pb2.Works(workList=reponseList)

    def request(self, request, context):
        reponseList = []
        for i in range(len(request.workList)):
            work = request.workList[i]
            if work.requestType == "open_directory":
                directory = work.message
                os.startfile(directory)
                reponseList.append({ "state": "OK" })

            elif work.requestType == "execute_file":
                directory = work.message
                if not os.path.isfile(directory):
                    reponseList.append({"state": "No "})
                os.system("notepad {}".format(directory))
                reponseList.append({"state": "OK"})

            elif work.requestType == "extract_morphs":
                paramArr = work.message.split(',')
                id, data_directory = paramArr[0], paramArr[1]
                reqData = {
                    "id": id,
                    "data_directory": data_directory
                }

                p = Process(target=tp.preprocess, args=(reqData,))
                p.start()
                reponseList.append({ "state": "OK" })

            elif work.requestType == "create_tables":
                paramArr = work.message.split(',')
                id, data_directory, kindsOf = paramArr[0], paramArr[1], paramArr[2]
                reqData = {
                    "id": id,
                    "data_directory": data_directory,
                    "table_tf": (True if int(kindsOf[0]) == 1 else False),
                    "table_tfidf": (True if int(kindsOf[1]) == 1 else False),
                    "table_tcoo": (True if int(kindsOf[2]) == 1 else False),
                }

                p = Process(target=tp.create_table, args=(reqData,))
                p.start()

                reponseList.append({ "state": "OK" })


        return proto.WorkProtocolService_pb2.Works(workList=reponseList)

    def collectUrls(self, request, context):
        # work_list = []
        # for i in range(len(request.workList)):
        #     work = request.workList[i]
        #     work_list.append({
        #         "channel": work.channels[0],
        #         "keyword": work.keywords[0],
        #         "start_dt": work.collectionDates[0][0:10],
        #         "end_dt": work.collectionDates[1][0:10],
        #         "work_type": "collect_url",
        #         "work_group_no": work.groupNo,
        #         "work_no": work.no
        #     })
        # collect = Collector()
        # collect.collect_urls(work_list)
        return proto.WorkProtocolService_pb2.WorkResponse(message="requested")

    def collectDocs(self, request, context):
        # work_list = []
        # for i in range(len(request.workList)):
        #     work = request.workList[i]
        #     work_list.append({
        #         "channel": work.channels[0],
        #         "keyword": work.keywords[0],
        #         "start_dt": work.collectionDates[0][0:10],
        #         "end_dt": work.collectionDates[1][0:10],
        #         "work_type": "collect_doc",
        #         "work_group_no": work.groupNo,
        #         "work_no": work.no
        #     })
        # collect = Collector()
        # collect.collect_docs(work_list)
        return proto.WorkProtocolService_pb2.WorkResponse(state="requested")

    def extractTexts(self, request, context):
        # work_list = []
        # for i in range(len(request.workList)):
        #     work = request.workList[i]
        #     work_list.append({
        #         "channel": work.channels[0],
        #         "keyword": work.keywords[0],
        #         "start_dt": work.collectionDates[0][0:10],
        #         "end_dt": work.collectionDates[1][0:10],
        #         "work_type": "extract_text",
        #         "work_group_no": work.groupNo,
        #         "work_no": work.no
        #     })
        # collect = Collector()
        # collect.extract_texts(work_list)
        return proto.WorkProtocolService_pb2.WorkResponse(state="requested")

    def extractContents(self, request, context):
        # work_list = []
        # for i in range(len(request.workList)):
        #     work = request.workList[i]
        #     work_list.append({
        #         "channel": work.channels[0],
        #         "keyword": work.keywords[0],
        #         "start_dt": work.collectionDates[0][0:10],
        #         "end_dt": work.collectionDates[1][0:10],
        #         "work_type": "extract_content",
        #         "work_group_no": work.groupNo,
        #         "work_no": work.no
        #     })
        # collect = Collector()
        # collect.extract_contents(work_list)
        return proto.WorkProtocolService_pb2.WorkResponse(state="requested")