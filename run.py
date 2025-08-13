"""
Simple runner script for the Blockchain Research AI Agent
"""
import subprocess
import sys
import os

def main():
    """Run the Streamlit application"""
    
    # Change to the application directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run the Streamlit app
    cmd = [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"]
    
    print("Starting Blockchain Research AI Agent...")
    print("Application will be available at: http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    print("-" * 60)
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    main()