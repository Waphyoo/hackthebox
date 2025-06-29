from flask import Flask, request, render_template_string, render_template
import os

app = Flask(__name__)

# Template HTML สำหรับทดสอบ
SAFE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>XSS Test - Safe Version</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; }
        .test-section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; }
        .safe { background-color: #d4edda; }
        .unsafe { background-color: #f8d7da; }
        input[type="text"] { width: 300px; padding: 8px; }
        button { padding: 10px 20px; margin: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 XSS Testing Lab</h1>
        
        <div class="test-section safe">
            <h2>✅ Safe Version (Auto-escaped)</h2>
            <form method="POST" action="/safe">
                <input type="text" name="user_input" placeholder="ลองใส่ <script>alert('XSS')</script>" value="{{ request.form.get('user_input', '') }}">
                <button type="submit">Test Safe</button>
            </form>
            {% if show_safe_result %}
                <h3>ผลลัพธ์ (Safe):</h3>
                <p><strong>Input:</strong> {{ user_input }}</p>
                <p><strong>แสดงผล:</strong> {{ user_input }}</p>
            {% endif %}
        </div>
        
        <div class="test-section unsafe">
            <h2>⚠️ Unsafe Version (with |safe filter)</h2>
            <form method="POST" action="/unsafe">
                <input type="text" name="user_input" placeholder="ลองใส่ <b>Bold Text</b> หรือ <script>alert('XSS')</script>" value="{{ request.form.get('user_input', '') }}">
                <button type="submit">Test Unsafe</button>
            </form>
            {% if show_unsafe_result %}
                <h3>ผลลัพธ์ (Unsafe):</h3>
                <p><strong>Input:</strong> {{ user_input }}</p>
                <p><strong>แสดงผล:</strong> {{ user_input | safe }}</p>
            {% endif %}
        </div>
        
        <div class="test-section">
            <h2>📝 ตัวอย่างการทดสอบ</h2>
            <ul>
                <li>&lt;b&gt;ข้อความตัวหนา&lt;/b&gt;</li>
                <li><code>&lt;i&gt;ข้อความตัวเอียง&lt;/i&gt;</code></li>
                <li><code>&lt;script&gt;alert('XSS Test')&lt;/script&gt;</code></li>
                <li><code>&lt;img src="x" onerror="alert('Image XSS')"&gt;</code></li>
                <li><code>&lt;svg onload="alert('SVG XSS')"&gt;&lt;/svg&gt;</code></li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(SAFE_TEMPLATE, 
                                show_safe_result=False, 
                                show_unsafe_result=False)

@app.route('/safe', methods=['POST'])
def safe_test():
    user_input = request.form.get('user_input', '')
    return render_template_string(SAFE_TEMPLATE, 
                                user_input=user_input,
                                show_safe_result=True, 
                                show_unsafe_result=False)

@app.route('/unsafe', methods=['POST'])
def unsafe_test():
    user_input = request.form.get('user_input', '')
    return render_template_string(SAFE_TEMPLATE, 
                                user_input=user_input,
                                show_safe_result=False, 
                                show_unsafe_result=True)

if __name__ == '__main__':
    print("🚀 เริ่มต้น XSS Testing Lab")
    print("📖 เปิดเบราว์เซอร์ไปที่: http://localhost:5000")
    print("⚠️  นี่เป็นการทดสอบในเครื่องเท่านั้น!")
    app.run(debug=True, host='127.0.0.1', port=5000)