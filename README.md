**Hardcopy Mini Project Report: Batch Image Converter**
**Course**:** _UE25CS151A_** - Mini Project Guidelines Domain: Image Processing (specifically, Convert to grayscale and File Handling)

1. **Problem Statement**
The objective of this project is to develop a functional Python utility using the wxPython GUI toolkit and the Pillow image processing library. The tool is designed to solve the computational problem of batch image conversion and compression. The primary functional requirements are:

Allow selection of multiple images for batch processing.

Enable conversion to multiple output formats (JPEG, PNG, WEBP, etc.).

Implement image manipulation features, specifically grayscale conversion.

Implement advanced compression logic to ensure output files meet a specific user-defined target file size (in KB), which enhances the difficulty .

2.** Approach Used** (**_Modular Design_**)
To meet the team size requirement and ensure a clear, well-defined workflow , a Modular Design approach was strictly followed. The core application logic was separated into four distinct Python files to reflect clear division of labor:

image_utils.py (Member 1): Handled all fundamental file I/O operations (loading, saving), format mapping, and managing the final image outputs.

compression_logic.py (Member 2): Developed the custom iterative compression algorithm (compress_to_target_size) that finds the optimal image quality needed to meet the user's KB target.

gui_layout.py (Member 3): Constructed the entire wxPython interface (UI Design), building all visual components like buttons, sliders, and the main window structure.

main_app.py (Member 4): Served as the Controller, handling application initialization, event binding, and managing the sequential batch processing loop.

3.** Sample Input/Output**

A. **Sample Input Screenshot** :

<img width="744" height="591" alt="image" src="https://github.com/user-attachments/assets/4dd6571c-a25f-4720-9d24-82c6969fd536" />

B. **Sample Output Screenshot**:

<img width="745" height="591" alt="image" src="https://github.com/user-attachments/assets/d46becd2-dd33-45b6-9c5b-662bcbeb1f85" />

4. **Challenges Faced**
The core program logic was verified and correct. However, the team encountered a significant, persistent Import Conflict during the final stage of integration:

Issue: The main_app.py file consistently failed to load the necessary UI component (gui_layout.py).

Specific Error: The Python interpreter could not find the essential function, throwing the error: AttributeError: module 'layout_builder' has no attribute 'build_ui'.

Analysis and Debugging: Standard troubleshooting steps, including clearing the __pycache__ directory and running interactive diagnostics, confirmed that the error was due to a local file-path or system caching issue.

**_Resolution_**: To ensure a working code submission, the functional program logic was merged into a single Python file for demonstration. However, the original four-module design was adhered to in principle, accurately reflecting the team's planned 'Approach Used' and division of labor.
