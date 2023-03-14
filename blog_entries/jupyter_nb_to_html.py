# Creating and formatting the HTML file
import os
from bs4 import BeautifulSoup as bs

def convert_jupyter_notebook_to_html(jupyter_notebook_path:str, background_img_path:str=None):
     
     if background_img_path is None:
        background_img_path = os.path.join(
            r"../../images/my_pictures/", r"blackboard_PI.jpg"
        )
     saving_directory = r'blog_entries/blog_html_results'
     
     os.system(
          "jupyter nbconvert" 
          + f" --output-dir={saving_directory}"
          + " --to html"
          + " --execute --template basic"
          + f" {jupyter_notebook_path}"
     )

     html_path = os.path.join(saving_directory, os.path.splitext(os.path.basename(jupyter_notebook_path))[0] + '.html')
     formatting(html_path)


def formatting(html_path:str):

     with open(html_path,  encoding="utf8") as html:
          
          nb_body = bs(html, 'html.parser').prettify()
          title_name = ' '.join(os.path.splitext(os.path.basename(html_path))[0].split()).capitalize()
          subtitle=None
          keywords=None
          _image_background = "<style>.main-single-post {background: url('../../images/my_pictures/blackboard_PI.jpg') no-repeat;}}</style>"
          _mathjax_lines = """<!-- mathjax --> <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script> <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script> <script> MathJax = { tex: { inlineMath: [['$', '$'], ['\\(', '\\)']] }, svg: { fontCache: 'global' } }; </script>"""
          
          html_as_string = f"""
          <!DOCTYPE html>
          <html lang="en">

          <head>

               <meta charset="UTF-8">
               <meta http-equiv="X-UA-Compatible">
               <meta name="description" content="None">
               <meta name="keywords" content="">
               <meta name="author" content="Leopoldo Cuspinera">
               <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">

               <title>Blog entry</title>
               <link rel="icon" type="image/x-icon" href="../../images/favicon.ico">
               <link rel="stylesheet" href="../../css/bootstrap.min.css">
               <link rel="stylesheet" href="../../css/font-awesome.min.css">

               <!-- Main css -->
               <link rel="stylesheet" href="../../css/style.css">
               <link href="https://fonts.googleapis.com/css?family=Lora|Merriweather:300,400" rel="stylesheet">
               <link href="../../css/notebook.css" rel="stylesheet">
               <link href="../../css\python_pygments.css" rel="stylesheet">
               
               {_image_background}


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
                                   <h1>{title_name}</h1>
                              </div>

                         </div>
                    </div>
               </section>

               <!-- Blog Single Post Section -->

               <section id="blog-single-post">
                    <div class="row">
                         <div class="column left"> </div>
                         <div class="column middle">
                              {nb_body}
                         </div>
                         <div class="column right"></div>
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
               {_mathjax_lines}

          </body>

          </html>
          """

          with open(html_path, mode="wb") as f_output:
               f_output.write(bs(html_as_string, 'html.parser').prettify("utf-8"))


if __name__ == '__main__':
     # jupyter_notebook_path = r'blog_entries/blog_jupyter_nb/simple_example.ipynb'
     # convert_jupyter_notebook_to_html(jupyter_notebook_path)
