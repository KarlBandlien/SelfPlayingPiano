Piano and Marbles MIDI Project

Overview

This project is a unique combination of 3D modeling and programming, designed to take MIDI files and translate them into a dynamic piano performance complete with marbles interacting in sync with the music. The piano and scenery were completely modeled in Blender, while the core functionality is driven by a custom Python script that converts any MIDI file into executable code, triggering the piano keys and marbles. The project also features a reset function to ensure the scene remains in proper order.

This project highlights my learning journey, including the challenges I faced in making the MIDI-to-Python conversion accurate and efficient, as well as refining the synchronization between the piano and the marbles.

Features
Custom 3D Piano Model and Scenery:

The entire piano and environment, from keys to background, were modeled by me in Blender, giving me full control over the aesthetics of the scene.
I spent considerable time perfecting the textures, lighting, and camera angles to create an immersive experience.

MIDI to Python Conversion Script:

I developed a script that converts any MIDI file into a Python file, which then drives the animation of the piano keys and marbles.
The Python file generated contains exact timing data and key/marble movement instructions, ensuring synchronization with the music.
Marble Interactivity:

Marbles roll in time with the piano keys, making this an interactive visual experience. The marbles are dynamically controlled based on the MIDI notes, moving in sync with the piano.
Reset Mechanism:

A reset function allows you to re-align the piano keys and marbles if they become misaligned, or if you need to change songs. This ensures that no matter how many times you run the script, the scene stays consistent.
Development Journey: Challenges and Learnings
This project taught me a great deal about both Blender 3D modeling and Python programming. However, it wasn't without its challenges:

1. MIDI to Python Conversion
Initial Struggles: The most difficult aspect was ensuring that the MIDI file data was correctly parsed and mapped to piano key movements. The challenge lay in converting the note-on and note-off events from the MIDI file into precise timing intervals for the keys and marbles.

Solution: After several attempts, I decided to create a custom function to read the MIDI file and extract note information. Initially, I struggled with syncing the events with the correct key presses and delays, but by leveraging the mido library, I was able to parse the MIDI data more effectively. I wrote a parser that maps each note to the respective key and adjusts the timing based on the tempo.

Efficiency Issues: The first few versions of the script were inefficient, especially with large MIDI files, as it would take a long time to process the data. I had to optimize the loop that handles the timing between notes by using a more efficient method of storing and accessing MIDI events.

Final Approach: Now, the script efficiently processes the MIDI file by caching the MIDI events and generating a Python file that triggers animations using a simplified approach that reduces unnecessary overhead.

2. Synchronizing Piano and Marbles
Initial Errors: Initially, the marbles and piano keys were not in sync. The marbles would sometimes fall too early or too late, disrupting the visual harmony.

Solution: I carefully adjusted the timing logic so that both the piano key presses and marble movements are synchronized. By breaking down the MIDI timing events and converting them into real-time animation frames, I was able to create a smoother experience.

3. Resetting Keys and Marbles
Problem: When testing multiple songs, I encountered issues with the keys and marbles getting misaligned. This would often happen when I ran the script multiple times without resetting the positions first.

Solution: To solve this, I implemented a reset function that re-aligns the keys and marbles back to their original positions every time the script is run. This was crucial for ensuring that the environment stayed consistent, regardless of the number of iterations.

Installation
Prerequisites
Python 3.x
Blender (for the 3D assets and environment)
MIDI file to test the functionality

Clone this repository or download the project files.
Open the Blender file to view or modify the piano model and environment.


Import MIDI:

Use the provided interface to select and load a MIDI file.
The script will automatically convert the MIDI file to a Python file containing the instructions for animating the piano and marbles.
Play the Song:

Run the generated Python file in blender to watch the piano and marbles play the song in sync.
Reset the Scene:

If you encounter any misalignment of the keys or marbles, simply run the reset function to realign everything back to the initial state.
This can also be used to ensure a clean slate when switching songs.


Optimizing the MIDI Parser: Although the MIDI-to-Python script is functional, I plan to optimize it further to handle larger and more complex MIDI files efficiently.
Enhancing Interaction: In the future, I’d like to expand the marble behavior, adding more dynamic interactions, such as bouncing or rolling along different paths.
Visual Effects: I also hope to improve the visuals with special effects like lighting changes or particle effects to make the performance more engaging.
I’m excited to continue developing this project and to explore more advanced features in the future.
