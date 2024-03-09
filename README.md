# Bracheistochrone solved with Abaqus
Python script for the Linkedin video: \
https://www.linkedin.com/feed/update/urn:li:activity:7010578968194023424/

# AUTHOR
Name: Youngbin LIM \
E-mail: lyb0684@naver.com

# Graphical abstract
![Optimized_Side](https://github.com/YB-LIM/Brachistochrone/assets/105615106/580ffa30-79f1-4be8-8330-2c0c2f37ac9e)

# Run command
call abaqus cae noGUI=Pre_Processing.py\
call abaqus J=Ball_Drop int cpus=(number of cpus) ask_delete=no\
call abaqus viewer noGUI=Post_Processing.py
