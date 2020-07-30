from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from datetime import timedelta
import os
import predict

# PATH_TO_PIC = 'This is default value'

app = Flask(__name__)

# 输出
@app.route('/')
def hello_world():
    return 'Hello World!'

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

# 添加路由
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    # global PATH_TO_PIC
    if request.method == 'POST':
        # 通过file标签获取文件
        f = request.files['file']
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "图片类型：png、PNG、jpg、JPG、bmp"})
        # 当前文件所在路径
        basepath = os.path.dirname(__file__)
        # 一定要先创建该文件夹，不然会提示没有该路径
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))
        # 保存文件
        f.save(upload_path)
        # # 保存到全局变量
        # PATH_TO_PIC = upload_path
        # 进行预测
        preValue = predict.application(upload_path)
        print(preValue)
        # 返回上传成功界面
        return render_template('predict.html', var=preValue)
    # 重新返回上传界面
    return render_template('upload.html')


# @app.route('/predict', methods=['POST', 'GET'])
# def predict():
#     global PATH_TO_PIC
#     # 检验路径是否正确
#     print("In predict, the path to image is: " + PATH_TO_PIC)
#     preValue = predict.application(PATH_TO_PIC)



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8848, debug=True)
