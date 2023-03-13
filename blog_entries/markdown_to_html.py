# Creating the HTML file
import os

file_name = r'demo.html'
file_directory = r"C:\Users\cuspi\Dropbox\Website\neuron\blog_entries\blog_html_results"
file_entire_path = os.path.join(file_directory, file_name)

file_html = open(file_entire_path, "w")

# Adding the input data to the HTML file
file_html.write(f"""
//js
<html>
<head>
<title>HTML File</title>
</head> 
<body>
<h1>Welcome Finxters</h1>           
<p>Example demonstrating How to generate HTML Files in Python</p> 
</body>
</html>
;//
""")

# Saving the data into the HTML file
file_html.close()