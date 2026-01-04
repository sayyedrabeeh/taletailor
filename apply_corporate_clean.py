import os

css_path = r"C:\Users\sayyy\.gemini\antigravity\brain\e0b9bab7-f5d1-4cfa-b20f-62b99dd2c50d\home_corporate_css.css"
html_path = r"d:\project\TaleTailor\Tatetailor\templates\home.html"

try:
    with open(css_path, 'r', encoding='utf-8') as f:
        new_css = f.read()

    with open(html_path, 'r', encoding='utf-8') as f:
        html_lines = f.readlines()

    # Find Style Block
    start_index = -1
    end_index = -1
    for i, line in enumerate(html_lines):
        if '<style>' in line:
            if start_index == -1: start_index = i
        if '</style>' in line:
            if start_index != -1: 
                end_index = i
                break # Just get the first large block

    # Apply CSS
    if start_index != -1 and end_index != -1:
        print(f"Replacing style block lines {start_index+1}-{end_index+1}")
        final_lines = html_lines[:start_index]
        final_lines.append('  <style>\n')
        final_lines.append(new_css)
        final_lines.append('\n  </style>\n')
        
        # Adding the rest of the HTML
        rest_of_html = html_lines[end_index+1:]
        
        # Filter out Spline scripts if present in the rest
        cleaned_html = []
        skip_line = False
        for line in rest_of_html:
             # Basic filter for spline script tags if they are simple
             if 'spline-viewer' in line or 'spline.design' in line:
                 continue
             cleaned_html.append(line)
             
        final_lines.extend(cleaned_html)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.writelines(final_lines)
        print("Success: Corporate CSS applied and HTML cleaned.")
    else:
        print("Error: Style block not found.")

except Exception as e:
    print(f"Exception: {e}")
