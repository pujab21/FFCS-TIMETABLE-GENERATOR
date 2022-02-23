# FFCS-TIMETABLE-GENERATOR
This will generate a timetable from course allocation report, based on user's priority.

Problem statement: Parse the document and bring it into JSON form. Then take inputs from the user and create an algorithm to generate a timetable.

The user must first run json_generator.py with a word document courseallocationreport.docx in the same file, and data.json will be generated in the same file.

The user can then run_main__ui__and__algorithm.py in the terminal. Users can add their courses required, and can add the priority of courses - the order they want to fill courses in the timetable. 
Then they can generate a timetable.
Currently default setting id theory slots in the morning, and lab slots in the evening. This can also be changed for theory in the evening and lab in the morning.

NOTE: _ algorithm_alone_.py is just to show the algorithm, it isn't required to run the timetable generator. 




