from flask import Flask, request, send_from_directory, jsonify, render_template
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from tools.order_meal_statistics import order_meal_statistics
from tools.rd_indicator import rd_indicator
from tools.cancer_management_indicator import cancer_management_indicator
from tools.clinical_indicator import clinical_indicator
from datetime import datetime


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['cancer'] = './static/cancer_management_indicator'
app.config['rd'] = './static/rd_indicator'
app.config['clinical'] = './static/clinical_indicator'
app.config['order'] = './static/order_meal_statistics'
app.config['APPLICATION_ROOT'] = 'nutrition_indicators-api'

# 在檔名前加 timestamp
def add_timestamp(filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    name, ext = os.path.splitext(filename)
    return f"{name}_{timestamp}_{ext}"

# 首頁
@app.route('/')
def index():
    return jsonify({
        'status': 200,
        'message': "nutrition_indicators-api|Test endpoint is working",
        'result': [],
        'success': True
    }), 200

# 上傳 API
@app.route('/upload/<type>', methods=['POST'])
def upload_file(type):
    try:
        if 'file' not in request.files:
            return jsonify({
                'status': 400,
                'error': "沒有找到 file 欄位",
                'success': False
            }), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'status': 400,
                'error': "未選擇檔案",
                'success': False
            }), 400
        if file:
            filename = secure_filename(file.filename)
            if not filename.endswith('.xlsx'):
                    return jsonify({
                        'status': 400,
                        'message': "只可以上傳.xlsx",
                        'success': False
                    }), 400
            
            timestamped_filename = add_timestamp(filename)
            
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], timestamped_filename)
            file.save(filepath)
            if type == 'order':
                try:
                    month = int(request.form.get('month'))
                    output_filepath=order_meal_statistics(filepath, timestamped_filename, month)
                except Exception as e:
                    return jsonify({
                        'status': 400,
                        'message': "請確認檔案及指標是否選錯",
                        'success': False
                    }), 400
            elif type == 'rd':
                try:
                    output_filepath=rd_indicator(filepath, timestamped_filename)
                    if output_filepath == 'Stage0未刪除，請檢查':
                        return jsonify({
                            'status': 400,
                            'message': "Stage0未刪除，請檢查",
                            'success': False
                        }), 400
                    elif output_filepath == 'Stage欄位有空值，請檢查':
                        return jsonify({
                            'status': 400,
                            'message': "Stage欄位有空值，請檢查",
                            'success': False
                        }), 400 
                except Exception as e:
                    return jsonify({
                    'status': 400,
                    'message': "請確認檔案及指標是否選錯",
                    'success': False
                }), 400
            elif type == 'cancer':
                try:
                    output_filepath = cancer_management_indicator(filepath, timestamped_filename)
                except Exception as e:
                    return jsonify({
                        'status': 400,
                        'message': "請確認檔案及指標是否選錯",
                        'success': False
                    }), 400
            elif type == 'clinical':
                try:
                    output_filepath =  clinical_indicator(filepath, timestamped_filename)
                except Exception as e:
                    return jsonify({
                        'status': 400,
                        'message': "請確認檔案及指標是否選錯",
                        'success': False
                    }), 400
            else:
                return jsonify({
                    'status': 400,
                    'message': "未知的指標類型",
                    'success': False
                }), 400
            return jsonify({
                'status': 201,
                "message": "檔案上傳成功",
                "filename": output_filepath.split('/')[-1],
                'success': True
            }), 201
        else:
            return jsonify({
                'status': 400,
                'message': "未選擇檔案",
                'success': False
            }), 400
    except Exception as e:
        return jsonify({
                'status': 500,
                'error': f'檔案上傳錯誤: {str(e)}',
                'success': False
            }), 500

# 下載 API
@app.route('/download/<type>/<filename>', methods=['GET'])
def download_file(type, filename):
    try:
        return send_from_directory(app.config[f'{type}'], filename, as_attachment=True)
    except  Exception as e:
        return jsonify({
                'status': 404,
                'error': "檔案不存在",
                'success': False
            }), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
