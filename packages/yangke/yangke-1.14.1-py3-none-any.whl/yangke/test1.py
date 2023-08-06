from flask import Flask, request, jsonify, make_response, send_from_directory, Response
from yangke.base import name_transfer
from flask_cors import *
# from yangke.common.config import logger
# import traceback
# import os
#
# app = Flask("flask")
# app.logger = logger
# app.config['JSON_AS_ASCII'] = False  # 让Flask返回的字符串可以正确显示中文，默认显示的是utf-8编码
# CORS(app)
#
#
# @app.route('/', methods=['GET', 'POST'])
# @cross_origin(origins="*", methods=['GET', 'POST'])
# def download_file():
#     """
#         下载文件功能
#
#         前段通过 ip/download/<下载参数>进行下载，这里的下载参数一般是文件名。
#         @download
#         def deal(args_str):
#             return os.path.join("C:/users", args_str)
#
#         :param file_name: 前段传入的下载参数，一般为文件名
#         :return:
#         """
#     directory = os.path.join(os.getcwd(), 'static')
#     try:
#         directory = os.path.dirname(f"E:/test.xlsx")
#         file_name = os.path.basename(f"E:/test.xlsx")
#         response = make_response(send_from_directory(directory, file_name, as_attachment=True))
#         return response
#     except Exception as e:
#         return jsonify({"Info": f"文件下载失败！{file_name}"})
#
#
# if __name__ == "__main__":
#     app.run(host='127.0.0.1', port='5000', use_reloader=False)


from yangke.web.flaskserver import start_server_app


def deal(args):
    action = args.get("Action")
    result = eval("{}(args)".format(action))
    return result


start_server_app(deal=deal)
