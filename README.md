# iKnow! Goal HTML Generator 📚✨

This Python script fetches "goal" data from the iKnow.jp API and converts it into static HTML files, making it easy to browse and review iKnow! content offline. It also generates an `index.html` file to navigate through all the generated goal pages.

## Features 🚀

*   **API Integration**: Fetches goal data directly from the iKnow.jp API.
*   **HTML Generation**: Creates individual HTML files for each specified goal, including details like description, difficulty, item counts, and example sentences.
*   **Audio Support**: Embeds audio for items and sentences if available. 🎧
*   **Index Page**: Generates a main `index.html` file for easy navigation to all generated goal pages. 📖
*   **Offline Access**: Once generated, all content can be viewed offline in your browser. 🌐

## How to Use 🛠️

### Prerequisites

*   Python 3.x installed on your system.
*   `requests` library: You can install it using pip:
    ```bash
    pip install requests
    ```

### Running the Script

1.  **Clone this repository** (or download `iknow.py`):
    ```bash
    git clone https://github.com/jansenzjh/iknow6000
    cd iknow6000
    ```
2.  **Run the script**:
    ```bash
    python iknow.py
    ```

The script will fetch data for the predefined `goal_ids_to_process` list. You can modify this list in `iknow.py` to include any iKnow! goal IDs you wish to process.

## Output 📁

After running the script, a new directory named `iknow_html_output` will be created (or updated) in the same directory as `iknow.py`. This directory will contain:

*   Individual HTML files for each processed goal (e.g., `Japanese_Core_6000_Vol_01.html`).
*   `index.html`: A main page listing all generated goal files, grouped for easier navigation.
*   `style.css` and `script.js`: Supporting files for styling and interactivity of the generated HTML pages.

To view the generated content, simply open `iknow_html_output/index.html` in your web browser. 🖥️

You can access to latest version online [here](https://jansenzjh.github.io/iknow6000/iknow_html_output/)

## Contributing 🤝

Feel free to fork this repository, open issues, or submit pull requests if you have suggestions or improvements!
