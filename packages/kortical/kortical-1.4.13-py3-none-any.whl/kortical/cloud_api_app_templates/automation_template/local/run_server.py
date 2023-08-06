import os
import module_placeholder.main
from module_placeholder.config import read_config

config = read_config("config.yml")
api_key = config['api_key']

if __name__ == '__main__':
    print(f"Paste the following into your browser to access the app:\n\n[http://127.0.0.1:5000?api_key={api_key}]")
    os.environ['SERVER_RUNNING_LOCALLY'] = "TRUE"
    module_placeholder.main.app.run(debug=True)