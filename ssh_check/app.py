from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Enables CORS if AJAX requests are made from different origins.

# In-memory storage for credentials
credentials_list = []

@app.route('/api/update_creds', methods=['POST'])
def update_creds():
    content = request.json
    found = False
    for cred in credentials_list:
        if cred['team'] == content.get('team') and cred['ip'] == content.get('ip'):
            cred.update({
                'user': content.get('user'),
                'password': content.get('password'),
                'last_updated': datetime.now().isoformat()
            })
            found = True
            break
    if not found:
        credentials_list.append({
            'team': content.get('team'),
            'ip': content.get('ip'),
            'user': content.get('user'),
            'password': content.get('password'),
            'last_updated': datetime.now().isoformat()
        })
    return {"message": "Credentials updated successfully"}, 200

@app.route('/api/clear_creds', methods=['POST'])
def clear_creds():
    global credentials_list
    threshold = datetime.now() - timedelta(minutes=1)  # Adjust the threshold as needed
    credentials_list = [cred for cred in credentials_list if datetime.fromisoformat(cred['last_updated']) > threshold]
    return {"message": "Outdated credentials cleared successfully"}, 200

@app.route('/api/creds', methods=['GET'])
def get_creds():
    return jsonify(credentials_list)

@app.route('/')
def show_creds():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Credentials Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100">
        <div class="container mx-auto px-4 py-8">
            <h1 class="text-2xl font-bold text-gray-800 mb-4">Credentials Dashboard</h1>
            <div id="credentials-table" class="overflow-hidden rounded-lg shadow-xs">
                <!-- Dynamic content will be loaded here -->
            </div>
        </div>
        <script>
            function fetchCredentials() {
                fetch('/api/creds')
                .then(response => response.json())
                .then(data => {
                    let tableHtml = `<table class="w-full whitespace-no-wrap">
                        <thead>
                            <tr class="text-xs font-semibold tracking-wide text-left text-gray-500 uppercase border-b bg-gray-50">
                                <th class="px-4 py-3">Team</th>
                                <th class="px-4 py-3">IP Address</th>
                                <th class="px-4 py-3">Username</th>
                                <th class="px-4 py-3">Password</th>
                                <th class="px-4 py-3">SSH Command</th>
                                <th class="px-4 py-3">Last Updated</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y">`;
                    data.forEach(cred => {
                        tableHtml += `<tr class="text-gray-700">
                            <td class="px-4 py-3">${cred.team}</td>
                            <td class="px-4 py-3">${cred.ip}</td>
                            <td class="px-4 py-3">${cred.user}</td>
                            <td class="px-4 py-3">${cred.password}</td>
                            <td class="px-4 py-3"><input type="text" readonly class="bg-gray-200" value='ssh ${cred.user}@${cred.ip}' onclick="this.select();"></td>
                            <td class="px-4 py-3">${cred.last_updated}</td>
                        </tr>`;
                    });
                    tableHtml += `</tbody></table>`;
                    document.getElementById('credentials-table').innerHTML = tableHtml;
                })
                .catch(error => console.error('Error fetching credentials:', error));
            }
            
            // Fetch credentials every 5 seconds
            setInterval(fetchCredentials, 5000);
            fetchCredentials(); // Initial fetch
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')