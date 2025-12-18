from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 데이터 구조 (사장님 기존 데이터 유지)
sections = {
    "2층좌석": {"price": 80000, "seats": [{"token": f"f2_{i}", "status": "available"} for i in range(1, 61)]},
    "무대앞스탠딩": {"price": 150000, "seats": [{"token": f"std_{i}", "status": "available"} for i in range(1, 49)]},
    "사이드석L": {"price": 110000, "seats": [{"token": f"sl_{i}", "status": "available"} for i in range(1, 31)]},
    "사이드석R": {"price": 110000, "seats": [{"token": f"sr_{i}", "status": "available"} for i in range(1, 31)]}
}

@app.route('/')
def index():
    # 'booked'(선택중)와 'sold'(판매완료) 상태인 좌석의 금액을 모두 합산합니다.
    current_total = 0
    for section_data in sections.values():
        for seat in section_data['seats']:
            if seat['status'] in ['booked', 'sold']:
                current_total += section_data['price']
    
    return render_template('index.html', sections=sections, total=current_total)

@app.route('/reserve', methods=['POST'])
def reserve():
    token = request.form.get('token')
    for section_data in sections.values():
        for seat in section_data['seats']:
            # 💡 이미 판매된(sold) 좌석은 건드리지 못하게 보호합니다.
            if seat['token'] == token and seat['status'] != 'sold':
                seat['status'] = 'booked' if seat['status'] == 'available' else 'available'
                break
    return redirect(url_for('index'))

@app.route('/checkout', methods=['POST'])
def checkout():
    # 💡 [최종 결제 확정] 버튼을 누르면 'booked'를 'sold'로 바꿉니다.
    for section_data in sections.values():
        for seat in section_data['seats']:
            if seat['status'] == 'booked':
                seat['status'] = 'sold'
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)