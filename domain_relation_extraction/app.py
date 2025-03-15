from flask import Flask, render_template, request, jsonify
from models.healthcare_model import HealthcareModel
from models.finance_model import FinanceModel

app = Flask(__name__)

# Initialize models
healthcare_model = HealthcareModel()
finance_model = FinanceModel()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_relations():
    # Get data from request
    text = request.form['text']
    domain = request.form['domain']
    
    # Process based on selected domain
    if domain == 'healthcare':
        entities, relations = healthcare_model.extract(text)
    elif domain == 'finance':
        entities, relations = finance_model.extract(text)
    else:
        return jsonify({'error': 'Invalid domain selected'})
    
    # Return results
    return jsonify({
        'entities': entities,
        'relations': relations
    })

if __name__ == '__main__':
    app.run(debug=True)