ROLL NO : C46
 Web Crawler using BFS and DFS

This is a simple web crawler implemented in Python, which can traverse web pages starting from a given URL using either **Breadth-First Search (BFS)** or **Depth-First Search (DFS)**. The crawler records and displays the order in which pages are visited.

## Features

- Crawls web pages starting from a user-provided URL
- Supports both BFS and DFS traversal methods
- Extracts and follows links on each page (hyperlinks)
- Displays the order of visited pages
- Limits the maximum number of pages to prevent excessive crawling

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AshutoshMore142k4/classproject.git
   cd classproject
   ```

2. **Create and activate a virtual environment (optional but recommended)**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Unix or Mac:
   source .venv/bin/activate
   ```

3. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```
   *Or, if you don’t have a requirements.txt:*
   ```bash
   pip install requests beautifulsoup4
   ```

## Usage

Run the script and follow the prompts, or edit the `start` variable in the script directly to specify your starting URL.

```bash
python bfsdfs.py
```
This will output the order in which pages are crawled using both BFS and DFS.

### Sample Output

```
BFS crawl order:
https://example.com
https://example.com/about
https://example.com/contact

DFS crawl order:
https://example.com
https://example.com/about
https://example.com/contact
```

## Configuration

- **Starting URL:** Change the `start` variable in `bfsdfs.py` to specify a different starting URL.
- **Max Visits:** Change the `max_visits` parameter in the `bfs_web_crawler()` and `dfs_web_crawler()` calls to increase or decrease the number of pages to crawl.

## Project Structure

```
.
├── bfsdfs.py         # Main script for web crawling
├── README.md         # Documentation
├── .gitignore        # Git ignore rules
└── requirements.txt  # Optional - Python dependencies
```

## Notes

- The crawler will only follow HTTP/HTTPS links.
- Basic exception handling is included for network errors.
- This is a demonstration project and does not obey robots.txt or implement politeness policies.

## License

This project is for educational purposes.

