from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

@app.route('/trigger_report', methods=['POST'])
def trigger_report():
    # Generate a unique report ID
    report_id = str(uuid.uuid4())
    
    # TODO: Implement the report generation process here
    
    return jsonify({'report_id': report_id})

@app.route('/get_report', methods=['GET'])
def get_report():
    report_id = request.args.get('report_id')
    
    # TODO: Implement the logic to check the report status and retrieve the CSV file
    
    return jsonify({'status': 'Running'})  # Placeholder response

if __name__ == '__main__':
    app.run()
