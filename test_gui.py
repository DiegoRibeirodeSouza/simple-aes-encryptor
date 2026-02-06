
import tkinter as tk
import sys
import threading
import time

# Add the installation path if not in path (usually /usr/lib/python3/dist-packages or similar)
# But since it's a script in /usr/bin, we might need to import it by path or just run it.
# The .deb installs the script to /usr/bin/simple-encryptor.
# Let's try to import the module if possible, or just load the source.
# Since the script has no .py extension in /usr/bin, imports might be tricky without manipulating sys.path.
# We will read the file and exec it, patching main to just init and exit.

APP_PATH = "/usr/bin/simple-encryptor"

def test_app():
    print("Loading application source...")
    with open(APP_PATH, "r") as f:
        code = f.read()

    # We need to run the code but intercept main loop
    # We will inject a modified main
    
    global_scope = {}
    
    # We want to run the class definitions but not the "if __name__ == '__main__': main()" part
    # Actually, we can just exec the code and then instantiate the class manually.
    
    print("Executing application code definition...")
    try:
        exec(code, global_scope)
    except Exception as e:
        print(f"FAILED to define application: {e}")
        sys.exit(1)
        
    print("Application code loaded. Instantiating App...")
    
    try:
        ModernEncryptorApp = global_scope.get("ModernEncryptorApp")
        if not ModernEncryptorApp:
            print("FAILED: ModernEncryptorApp class not found in source.")
            sys.exit(1)
            
        root = tk.Tk()
        app = ModernEncryptorApp(root)
        
        print("App instantiated successfully.")
        
        # Simulate some update loops
        for i in range(10):
            root.update()
            time.sleep(0.1)
            
        print("GUI update loop ran for 1 second without crash.")
        root.destroy()
        print("SUCCESS: Test Passed.")
        sys.exit(0)
        
    except Exception as e:
        print(f"FAILED during runtime: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_app()
