# Creating the HTML file
import os
import re
import markdown

source_markdown_file = r"blog_entries/blog_markdown/example_1.md"
saving_directory = r"blog_entries/blog_html_results"

saving_file_name = "".join(os.path.split(source_markdown_file)[-1].split(".")[:-1]) + ".html"
saving_path = os.path.join(saving_directory, saving_file_name)

main_title = " ".join(re.split(", |_|-|\.", "_".join(saving_file_name.split(".")[:-1]))).capitalize()
subtitle = None
keywords = []

with open(source_markdown_file, "r") as md_f:
    md_used_lines = md_f.readlines()[2:] # remove first line with title in markdown
    md_html = markdown.markdown("".join(md_used_lines), extensions=['fenced_code', 'codehilite'])

# Start the HTML file
file_html = open(saving_path, "w")

# Adding the input data to the HTML file
file_html.write(
    f"""
<!DOCTYPE html>
<html lang="en">

<head>

     <meta charset="UTF-8">
     <meta http-equiv="X-UA-Compatible">
     <meta name="description" content="{subtitle}">
     <meta name="keywords" content="{', '.join(keywords)}">
     <meta name="author" content="Leopoldo Cuspinera">
     <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
     <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

     <title>{main_title}</title>
     <link rel="icon" type="image/x-icon" href="../../images/favicon.ico">
     <link rel="stylesheet" href="../../css/bootstrap.min.css">
     <link rel="stylesheet" href="../../css/font-awesome.min.css">

     <!-- Main css -->
     <link rel="stylesheet" href="../../css/style.css">
     <link href="https://fonts.googleapis.com/css?family=Lora|Merriweather:300,400" rel="stylesheet">

</head>

<body>

     <!-- Navigation section  -->

     <div class="navbar navbar-default navbar-static-top" role="navigation">
          <div class="container">

               <div class="navbar-header">
                    <button class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                         <span class="icon icon-bar"></span>
                         <span class="icon icon-bar"></span>
                         <span class="icon icon-bar"></span>
                    </button>
                    <a href="../../index.html" class="navbar-brand">Leopoldo Cuspinera</a>
               </div>
               <div class="collapse navbar-collapse">
                    <ul class="nav navbar-nav navbar-right">
                         <li><a href="../../index.html">Home</a></li>
                         <li><a href="../../about.html">About</a></li>
                         <li><a href="../../gallery.html">Gallery</a></li>
                         <li><a href="../../blog.html">Blog</a></li>
                         <li><a href="../../contact.html">Contact</a></li>
                    </ul>
               </div>

          </div>
     </div>

     <!-- Main title of blog section -->

     <section id="home" class="main-single-post parallax-section">
          <div class="overlay"></div>
          <div class="container">
               <div class="row">

                    <div class="col-md-12 col-sm-12">
                         <h1>{main_title}</h1>
                    </div>

               </div>
          </div>
     </section>

     <!-- Blog Single Post Section -->

     <section id="blog-single-post">
          <div class="container">
               <div class="row">

                    <div class="col-md-offset-1 col-md-10 col-sm-12">
                         <div class="blog-single-post-thumb">


                              <div class="blog-post-title">
                                   {'<h2>' + subtitle + '</h2>' if subtitle else ''}
                              </div>

                              <div class="blog-post-format">
                                   <span><i class="fa fa-date"></i> January, 2023 </span>
                              </div>

                              <div class="blog-post-des">
                              {md_html}
                              </div>

                         </div>
                    </div>
               </div>
     </section>

     <!-- Footer Section -->

     <footer id="app-footer"></footer>
     <script async src="../../js/footer.js"></script>

     <!-- Back top -->
     <a href="#back-top" class="go-top"><i class="fa fa-angle-up"></i></a>

     <!-- SCRIPTS -->
     <script src="./js/jquery.js"></script>
     <script src="./js/bootstrap.min.js"></script>
     <script src="./js/jquery.parallax.js"></script>
     <script src="./js/custom.js"></script>
     <script type="module" src="https://md-block.verou.me/md-block.js"></script>

</body>

</html>
"""
)

# Saving the data into the HTML file
file_html.close()
