from flask import Flask
import subprocess
import os

app = Flask(__name__)

@app.route('/run-orchestrator')
def run_orchestrator():
    """Endpoint to trigger the orchestrator script."""
    try:
        subprocess.run(['python', 'orchestrator.py'], check=True)
        return "Orchestrator script executed successfully!", 200
    except subprocess.CalledProcessError as e:
        return f"Error executing orchestrator script: {e}", 500
    except FileNotFoundError:
        return "Error: orchestrator.py not found.", 404

if __name__ == '__main__':
    # Não execute o orquestrador diretamente aqui, ele será chamado pelo endpoint
    pass
