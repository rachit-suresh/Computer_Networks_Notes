import socket,sys,datetime

import os

resources_dir = "resources"

def get_file_path(url_path):
    if url_path == "/":
        return os.path.join(resources_dir, "index.html")
    # Remove leading slash
    file_name = url_path.lstrip("/")
    return os.path.join(resources_dir, file_name)
# os.path.join() automatically adds the correct slash between path components if needed.
#If you join "resources" and "/page.html", it will ignore "resources" and return "/page.html" (because a leading slash makes it absolute

'''
The "r" parameter in open(file_path, "r", encoding="utf-8") means open the file for reading (read-only mode).

"r" = read mode (default)
"w" = write mode (creates/truncates file)
"a" = append mode
"rb" = read binary mode

Here are the main file reading commands in Python:

Syntax
Open a file for reading:
f = open("filename.txt", "r", encoding="utf-8")

Read the entire file as a string:
content = f.read()

Read one line at a time:
line = f.readline()

Read all lines into a list:
lines = f.readlines()

Close the file:
f.close()

Recommended: Use with statement (auto-closes file):
with open("filename.txt", "r", encoding="utf-8") as f:
    content = f.read()

Example Implementation
# Read entire file
with open("resources/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Read lines into a list
with open("resources/index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Read file line by line
with open("resources/index.html", "r", encoding="utf-8") as f:
    for line in f:
        print(line)

A more technical explanation

1. open()
Purpose: Opens a file and returns a file object.
Syntax:
f = open("filename.txt", "r", encoding="utf-8")
Parameters:
"filename.txt": Path to the file.
"r": Mode ("r" for read, "w" for write, "a" for append, "rb" for binary read, etc.).
encoding="utf-8": Specifies character encoding (important for text files).

2. .read()
Purpose: Reads the entire file content as a single string.
Syntax:
content = f.read()
Behavior:
Reads from the current file pointer position to the end.
If the file is large, this can consume a lot of memory.

3. .readline()
Purpose: Reads one line from the file.
Syntax:
line = f.readline()
Behavior:
Each list element is a line from the file (including newline characters).

5. Iterating Over File Object
Purpose: Efficiently reads lines one by one.
Syntax:
for line in f:
    print(line)
Behavior:
Reads each line sequentially.
Memory efficient for large files.

6. .close()
Purpose: Closes the file and releases system resources.
Syntax:
f.close()
Behavior:
Always close files when done to avoid resource leaks.

7. with Statement (Context Manager)
Purpose: Automatically closes the file when the block ends.
Syntax:
with open("filename.txt", "r", encoding="utf-8") as f:
    content = f.read()
Behavior:
Ensures the file is closed even if an error occurs.
'''

def serve_file(conn, file_path, http_version):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        response = response_body(http_version, 200, "OK", len(content), content)
        conn.send(response.encode())
        filename = os.path.basename(file_path)
        print(f"  -> 200 OK: {filename}")
    except FileNotFoundError:
        response = response_body(http_version, 404, "Not Found", 0, "<h1>404 Not Found</h1>")
        conn.send(response.encode())
        print(f"  -> 404 Not Found")
'''
 there are other ways to implement path traversal protection in a file server.
You chose the absolute path comparison method because it is:

Simple
Reliable
Cross-platform
Other Methods
Manual String Checks

Example: Block any path containing .. or starting with ...
Problem: Attackers can bypass with encoded or nested traversal (/foo/../../bar, /..\\file.txt, etc.).
Regular Expressions

Use regex to detect suspicious patterns.
Problem: Hard to cover all edge cases and encoding tricks.
Canonicalization

Use os.path.normpath() to normalize the path, then check for traversal.
Better, but: Still need to compare with the base directory.
Chroot/Jail

Run the server in a restricted environment where it cannot access files outside a directory.
Complex: Requires OS-level configuration.
Why Absolute Path Comparison?
Covers all traversal tricks: Works even if attackers use /foo/../../bar, backslashes, or URL encoding.
Easy to implement: Just compare os.path.abspath() of the requested file and the resources directory.
No need for complex parsing: No regex or manual string manipulation.
Portable: Works on Windows, Linux, macOS.

1. os.path.abspath()
Purpose: Converts a relative file path to an absolute path.
How it works:
Takes a path like "resources/page.html" and returns its full path, e.g., "C:\\Users\\vangs\\cursor\\ComputerNetworks\\5_internet_applications-http\\hw\\resources\\page.html" on Windows.
Resolves . (current directory) and .. (parent directory) in the path.
Why use it:
Ensures you're working with the actual location on disk, not a relative or ambiguous path.
Used for security checks (like path traversal protection) because you can compare absolute paths reliably.
Example:
import os
print(os.path.abspath("resources/page.html"))
# Output: C:\\Users\\vangs\\cursor\\ComputerNetworks\\5_internet_applications-http\\hw\\resources\\page.html

2. Canonicalization
Purpose: Converts a file path to its canonical (standardized) form.
How it works:
Removes redundant separators, resolves . and .., and normalizes the path.
In Python, os.path.normpath() is used for canonicalization.
Why use it:
Prevents tricks like /foo/../bar or /./bar from bypassing security checks.
Ensures that different representations of the same path are treated identically.
Example:
import os
print(os.path.normpath("resources/../resources/page.html"))
# Output: resources/page.html

3. Chroot/Jail
Purpose: Restricts a process to a specific directory tree, so it cannot access files outside that directory.
How it works:
On Unix/Linux, chroot("/home/user/resources") changes the root directory for the process.
The process sees /home/user/resources as / and cannot access files outside it.
Why use it:
Provides strong OS-level isolation for security.
Even if an attacker exploits path traversal, they cannot escape the jail.
Example (Linux):
sudo chroot /home/user/resources
# Now, /etc/passwd refers to /home/user/resources/etc/passwd

Note:

Chroot is not available natively on Windows.
Requires root/admin privileges and careful setup.

'''
def is_safe_path(base_dir, path):
    abs_base = os.path.abspath(base_dir)
    abs_path = os.path.abspath(path)
    try:
        return os.path.commonpath([abs_base, abs_path]) == abs_base
    except ValueError:
        return False

'''
    # Normalize and get absolute paths
    abs_base = os.path.abspath(base_dir)
    abs_path = os.path.abspath(path)
    # Check if abs_path starts with abs_base
    return abs_path.startswith(abs_base)

    The original code used abs_path.startswith(abs_base) to verify that a user was accessing a file within a designated directory. The problem is that this is just a simple text comparison. It can be easily fooled.

Let's use an example:

    Your allowed directory (base_dir) is /srv/resources.

    A hacker creates a directory named /srv/resources_evil and puts a malicious file in it.

Now, a request comes in for the file /srv/resources_evil/malicious_file.sh.

Old Code's Logic:

    abs_base becomes /srv/resources.

    abs_path becomes /srv/resources_evil/malicious_file.sh.

    The check is: Does "/srv/resources_evil/malicious_file.sh" start with "/srv/resources"?

    Result: True. The check passes, and the server might execute or serve a file from a completely different and unauthorized directory! 😱

This is the classic bypass: the attacker uses a directory name that shares a prefix with the legitimate one.

The Solution: How the New Code Works 🛡️

The new code uses os.path.commonpath(), which is much smarter. It doesn't just compare the beginning of the strings; it finds the actual, deepest directory that both paths share.

Let's re-run the same malicious scenario:

New Code's Logic:

    abs_base is still /srv/resources.

    abs_path is still /srv/resources_evil/malicious_file.sh.

    The check calculates os.path.commonpath(['/srv/resources', '/srv/resources_evil/malicious_file.sh']).

        The common path between these two is just /srv.

    It then compares the result: Is /srv equal to /srv/resources?

    Result: False. Access is correctly denied.

For a valid file request, like /srv/resources/images/cat.jpg, os.path.commonpath() would return /srv/resources, the check would pass ('/srv/resources' == '/srv/resources'), and the file would be served as intended.

The try...except ValueError block is added because os.path.commonpath can raise an error if the paths are on different drives (e.g., C:\ and D:\ on Windows), making the code more robust.

    '''

def error_page(status_code, status_message,brief_desc="cant be asked"):
   return f'''
  <!DOCTYPE html>
<html>
<head>
    <title>{status_code} {status_message}</title>
</head>
<body>
    <h1>{status_code} {status_message}</h1>
    <p>{brief_desc}</p>
    <hr>
    <p><em>Simple HTTP Server</em></p>
</body>
</html>
'''

def response_body(http_version, status_code, status_message, content_length="0", data=""):
  headers = (
      f"{http_version} {status_code} {status_message}\r\n"
      "Content-Type: text/html; charset=utf-8\r\n"
      f"Content-Length: {content_length}\r\n"
      f"Date: {datetime.datetime.utcnow():%a, %d %b %Y %H:%M:%S GMT}\r\n"
      "Server: Simple HTTP Server\r\n"
      "Connection: close\r\n"
  )
  return f"{headers}\r\n{data}"

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Socket created")
interface="127.0.0.1"
port=8080

'''
sys.argv is a list of all command-line arguments passed to your script, including the script name itself as the first element.

sys.argv[0] is always the script filename (e.g., server.py)
sys.argv[1] is the first argument (e.g., port)
sys.argv[2] is the second argument (e.g., interface)
So:

len(sys.argv) == 1 means: only the script name, no arguments.
len(sys.argv) > 1 means: at least one argument (port).
len(sys.argv) > 2 means: at least two arguments (port and interface).
'''
if len(sys.argv)>1:
  port = int(sys.argv[1])
if len(sys.argv)>2:
  interface = sys.argv[2]

sock.bind((interface,port))
print(f"HTTP Server started on http://{interface}:{port}")
print(f"Serving files from '{resources_dir}' directory")
print("Press Ctrl+C to stop the server\n")

try:
    sock.listen(5)


    while True:
      conn,addr=sock.accept()
      print(f"Connection from {addr[0]}:{addr[1]}")
      try:
        
        request=conn.recv(4096)

        if not request:
          print("Client closed the connection")
          continue

        '''if not request.startswith("GET"):
          response = response_body("HTTP/1.1", 405, "Method Not Allowed")
          conn.send(response.encode())

        path_index_from = request.find('/')
        path_index_to = request.find(" ",path_index_from)
        path = request[path_index_from,path_index_to+1]
        print(f"Request path : {path}")

        version_index_from = path_index_to+2
        version_index_to = request.find(" ",version_index_from)
        http_version = request[version_index_from,version_index_to+1]
        print(f"Request HTTP version : {http_version}")
        '''
      # instead of all this above code we can just do the below
        # Parse the path from the request
        try:
            request_line = request.decode().splitlines()[0]
            print(f"Request: {request_line}")
            method, url_path, http_version = request_line.split()
            '''for line in request.decode().splitlines()[1:]:
              if line.lower().startswith("host:"):
                host_value = line.split(":", 1)[1].strip()
                break
            '''
            #idk why i did this but i left it causeit teaches about string funcs in python
            '''
            Here’s why this code works for extracting the Host header from an HTTP request:

            request.decode().splitlines()[1:]
            Skips the request line and loops through the header lines.

            if line.lower().startswith("host:"):
            Checks each header line (case-insensitive) to see if it’s the Host header.

            line.split(":", 1)[1].strip()
            Splits the line at the first colon and takes everything after it, removing extra spaces.

            break
            Stops after finding the first Host header.'''
        except ValueError:
            error_html = error_page(400,"Bad request")
            response = response_body("HTTP/1.1", 400, "Bad Request", len(error_html), error_html)
            conn.send(response.encode())
            print(f"  -> 400 Bad Request")
            continue 
        file_path = get_file_path(url_path)
        if method != "GET":
          error_html = error_page(405,"Method Not Allowed")
          response = response_body(http_version, 405, "Method Not Allowed", len(error_html), error_html)
          conn.send(response.encode())
          print(f"  -> 405 Method Not Allowed")
        elif not is_safe_path(resources_dir, file_path):
          error_html = error_page(403,"Forbidden")
          response = response_body(http_version, 403, "Forbidden", len(error_html), error_html)
          conn.send(response.encode())
          print(f"  -> 403 Forbidden")
        else:
          serve_file(conn, file_path, http_version)


        print(f"HTTP request from client = {request.decode()}")
      except Exception as e:
        error_html = error_page(500,"Internal Server Error")
        response = response_body("HTTP/1.1", 500, "Internal Server Error", len(error_html), error_html)
        try:
            conn.send(response.encode())
            print(f"  -> 500 Internal Server Error")
        except Exception:
            pass  # Connection may already be broken
        print(f"error {e} occured")
      finally:
        conn.close()
except KeyboardInterrupt:
    print("\nServer is shutting down...")
    
except Exception as e:
    print(f"error {e} occured")
finally:
    sock.close()

  
