# Audio-Based Melody Generation
By: Aaron Basch, Lucas Bastos, and Chris Carson
Course: IS 485/698 Machine Listening at New Jersey Insitute of Technology
Instructor: Professor Mark Cartwright

### Background
Audio-Based Melody Generation is an end-to-end program written by Aaron Basch, Lucas Bastos, and Chris Carson for our IS-485/698 Machine Listening final project. The goal was to create a program that takes in one or more audio files in a .wav format and output a uniquely generated audio file that is inspired by the melodies and different styles. We do this by first converting each of the .wav files into .mid MIDI files, and using MusicVAE we blend the melodies into a final single audio track.
![Graph Image](./AudioMixerGraph.png)
_After a user provides two audio files, we extract the notes and convert them into MIDI format to then use as input for the melody mixer component._

One of the most frustrating situations that a music producer can run into is a creative block. Whether it just be trying to start a new project or build upon an established idea, a creative block can completely ruin your workflow and affect your inspiration for an extended period of time. This can be even worse for people who make music as their primary source of income. There are plenty of websites, programs, and plug-ins that will randomly generate melodies, but there are few, if any, that can take in an audio input to produce new, but similar, results. 

By creating the Audio-Based Melody Generation project, we give users a more accurate result of what they are looking for than other programs. Also, by giving them MIDI files, they can easily be edited in any DAW so they are not stuck with the melody we provide. Doing this provides the producer with absolute freedom to do whatever they want with the melody. If implemented well, this could be a great tool to help music producers get inspired and get over their creative blocks. 

One of the most frustrating situations that a music producer can run into is a creative block. Whether it just be trying to start a new project or build upon an established idea, a creative block can completely ruin your workflow and affect your inspiration for an extended period of time. This can be even worse for people who make music as their primary source of income. There are plenty of websites, programs, and plug-ins that will randomly generate melodies, but there are few, if any, that can take in an audio input to produce new, but similar, results. 

By creating the Audio-Based Melody Generation project, we give users a more accurate result of what they are looking for than other programs. Also, by giving them MIDI files, they can easily be edited in any DAW so they are not stuck with the melody we provide. Doing this provides the producer with absolute freedom to do whatever they want with the melody. If implemented well, this could be a great tool to help music producers get inspired and get over their creative blocks. 
### Set up
Our program can be used simply through the command line with the Python main.py program, or it can be deployed with a web interface by running the Node application via localhost. First, you must have git, Python 3, pip3, and Node.js installed. You can check if these are installed by running these commands:
```dotnetcli
git --version
python3 --version
pip3 --version
node --version
```
If you see version numbers for all of the above, you're ready to move on! If not, you must install what you're missing with your desired method (package manager, web, etc.). Now, clone this repo with git by running ```git clone https://github.com/lucaspbastos/Audio-Based-Melody-Generation.git``` and navigate to the /Audio-Based-Melody-Generation folder. Now you will need to run ```pip3 install -r requirements.txt``` to install the Python dependencies and ```npm i``` to install the Node.js dependencies.

### Run the Program
- **Command Line**:
In the base directory, you can run the main.py program by running `python3 src/main.py /INPUT_DIRECTORY [/OUTPUT_DIRECTORY]`, where _INPUT_DIRECTORY_ is a required parameter that specifies the directory containing the .wav files, and _OUTPUT_DIRECTORY_ is an optional parameter specifying the desired output directory for the final audio file. If no output directory is specified, the program defaults to /MIDI, and will create the directory if it does not exist.

- **Web Interface**:
In the base directory, you can run `npm start` to start the web application at localhost:3000. You can specify a different port by exporting an environment variable named PORT to your desired port number. For example, in bash you would simply run `PORT=4000` to set the variable into the current shell, or `$PORT=4000` in PowerShell.

### Demo without installing
We have hosted an instance of our web application via Heroku for those who would like to demo the application before installing! You can access the website [here](https://melodygeneration.herokuapp.com/).

### Contact
- Aaron Basch ab2496@njit.edu
- Lucas Bastos lpb6@njit.edu
- Chris Carson cec36@njit.edu
