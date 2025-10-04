# UI and Control Flow
# Purpose:
# The front-end brain — everything the user sees and interacts with.
# Runs on Streamlit to provide a fast, interactive, and responsive app.
# Responsibilities:
# Create the sidebar inputs and main layout.
# Allow users to:

    # Select an asteroid or use live data.
    # Adjust size, speed, density, and angle.
    # Pick impact coordinates and target type.
    # Choose mitigation strategies.
# Dynamically call:
    # utils for physics.
    # ai_core for predictions.
    # visuals for rendering.
# Render summary text and tooltips.
# Handle fallback (offline mode).

# Key functions:

# def main():
#     """Streamlit entrypoint: builds UI, handles state, updates outputs."""


# Used by: main.py