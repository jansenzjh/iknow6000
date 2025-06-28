import requests
import json
import os
import re

# List to store generated HTML file paths for index.html
generated_html_files = []
output_dir = "iknow_html_output" # Define output_dir globally

def fetch_and_process_goal(goal_id):
    """
    Fetches data for a given goal ID from the iKnow.jp API and generates an HTML file.
    """
    api_url = f"https://iknow.jp/api/v2/goals/{goal_id}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for goal ID {goal_id}: {e}")
        return

    # Create a directory to store the HTML files if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate HTML content
    html_content = generate_html(data)

    # Sanitize the title to create a valid filename
    title = data.get('title', f'goal_{goal_id}')
    sanitized_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
    if not sanitized_title:
        sanitized_title = f"goal_{goal_id}"
    file_name = os.path.join(output_dir, f"{sanitized_title}.html")

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Successfully created {file_name}")
    generated_html_files.append(os.path.basename(file_name)) # Store only the filename

def generate_html(data):
    """
    Generates the HTML content for a given iKnow.jp goal JSON data.
    """
    html = f"""
    <!DOCTYPE html>
    <html lang="{data.get('cue_language', 'en')}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{data.get('title', 'iKnow! Goal')}</title>
        <link rel="stylesheet" href="style.css">
        <script src="script.js" defer></script>
    </head>
    <body>
        <div><a href="index.html" class="home-button">Home</a></div>
        <div class="container">
            <h1>{data.get('title', 'iKnow! Goal')}</h1>
            <div class="goal-info">
                <p><strong>Description:</strong> {data.get('description', 'N/A')}</p>
                <p><strong>Difficulty Level:</strong> {data.get('difficulty_level', 'N/A')}</p>
                <p><strong>Items Count:</strong> {data.get('items_count', 'N/A')}</p>
                <p><strong>Sentences Count:</strong> {data.get('sentences_count', 'N/A')}</p>
            </div>
    """

    for goal_item in data.get('goal_items', []):
        item = goal_item.get('item', {})
        cue = item.get('cue', {})
        response_text = item.get('response', {}).get('text', 'N/A')
        item_sound = goal_item.get('sound')
        sentences = goal_item.get('sentences', [])

        item_text = cue.get('text', 'N/A')
        part_of_speech = cue.get('part_of_speech')
        part_of_speech_display = f'<span class="part-of-speech">({part_of_speech})</span>' if part_of_speech else ''

        html += f"""
            <div class="item-section">
                <div class="item-header">
                    <h2>{item_text} {part_of_speech_display}</h2>
                </div>
                <div class="item-details">
                    <p><strong>Response Text:</strong> {response_text}</p>
                    <p><strong>Transliterations:</strong></p>
                    <ul class="transliterations-list">
        """
        transliterations = cue.get('transliterations', {})
        for key, value in transliterations.items():
            html += f"<li>{key}: {value}</li>"
        html += f"""
                    </ul>
        """
        if item_sound:
            html += f"""
                    <p class="audio-player">
                        <audio controls preload="none">
                            <source src="{item_sound}" type="audio/mpeg">
                            Your browser does not support the audio element.
                        </audio>
                    </p>
            """
        html += f"""
                </div>
                <div class="sentences-section">
                    <h3>Example Sentences:</h3>
        """
        if not sentences:
            html += "<p>No example sentences available for this item.</p>"

        for sentence in sentences:
            cue_sentence = sentence.get('cue', {})
            response_sentence = sentence.get('response', {})
            sentence_sound = sentence.get('sound')

            html += f"""
                    <div class="sentence">
                        <p class="cue-text"><strong>Text:</strong> {cue_sentence.get('text', 'N/A')}</p>
                        <p class="response-text"><strong>Response:</strong> {response_sentence.get('text', 'N/A')}</p>
                        <p class="transliterations"><strong>Transliterations:</strong></p>
                        <ul class="transliterations-list">
            """
            sentence_transliterations = cue_sentence.get('transliterations', {})
            for key, value in sentence_transliterations.items():
                html += f"<li>{key}: {value}</li>"
            html += f"""
                        </ul>
            """
            if sentence_sound:
                html += f"""
                        <p class="audio-player">
                            <audio controls preload="none">
                                <source src="{sentence_sound}" type="audio/mpeg">
                                Your browser does not support the audio element.
                            </audio>
                        </p>
                """
            html += """
                    </div>
            """
        html += """
                </div>
            </div>
        """

    html += """
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    # List of goal IDs you want to process
    # You can extend this list with more goal IDs
    # All article from https://iknow.jp/content/japanese
    goal_ids_to_process = [24666,24667,566921,566922,566924,566925,566926,566927,566928,566929,566930,566932,594768,594770,594771,594772,594773,594774,594775,594777,594778,594780,615865,615866,615867,615869,615871,615872,615873,615874,615876,615877,615947,615949,615950,615951,615953,615954,615955,615957,615958,615959,616077,616078,616079,616080,616081,616082,616083,616084,616085,616086,598434,598432,598431,598430,598427,598426,598425,598424,598423,598422]

    for goal_id in goal_ids_to_process:
        fetch_and_process_goal(goal_id)

    # Generate index.html
    index_html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>iKnow! Goals Index</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="container">
            <h1>iKnow! Goals Index</h1>
    """

    # Group files by the first 18 characters of their display title
    grouped_files = {}
    for filename in sorted(generated_html_files):
        display_title = os.path.splitext(filename)[0].replace('_', ' ')
        group_key = display_title[:18].strip()
        if group_key not in grouped_files:
            grouped_files[group_key] = []
        grouped_files[group_key].append((display_title, filename))

    for group_key in sorted(grouped_files.keys()):
        index_html_content += f'            <h2 class="group-title">{group_key}</h2>\n'
        index_html_content += '            <ul class="index-list">\n'
        for display_title, filename in sorted(grouped_files[group_key]):
            index_html_content += f'                <li><a href="{filename}">{display_title}</a></li>\n'
        index_html_content += '            </ul>\n'

    index_html_content += """
        </div>
    </body>
    </html>
    """
    index_file_path = os.path.join(output_dir, "index.html")
    with open(index_file_path, "w", encoding="utf-8") as f:
        f.write(index_html_content)
    print(f"Successfully created {index_file_path}")

    print("\nProcessing complete. Check the 'iknow_html_output' directory for the generated HTML files and index.html.")
