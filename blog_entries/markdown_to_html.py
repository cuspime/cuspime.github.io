import os
import re
import markdown
from markdown.extensions.toc import TocExtension


def convert_markdown_to_html(
    source_markdown_file: str,
    background_img_path: str = None,
    subtitle: str = None,
    update_date=None,
    keywords: list = None,
    table_of_contents=False,
):
    """Function that converts any markdown file into html with the template I want.

    Args:
        source_markdown_file (str): path to the markdown file of origin
        background_img_path (str, optional): path to the image to be used in the home band with parallax.
              If None, it takes a default image. Defaults to None.
        subtitle (str, optional): _description_. Defaults to None.
        keywords (list, optional): _description_. Defaults to None.
    """
    if background_img_path is None:
        background_img_path = os.path.join(r"../../images/my_pictures/", r"blackboard_PI.jpg")

    saving_directory = r"blog_entries/blog_html_results"
    saving_file_name_no_extension = "".join(os.path.split(source_markdown_file)[-1].split(".")[:-1])
    saving_file_name = saving_file_name_no_extension + ".html"
    saving_path = os.path.join(saving_directory, saving_file_name)
    main_title = " ".join(re.split(", |_|-|\.", "_".join(saving_file_name.split(".")[:-1]))).capitalize()

    markdown_file = source_markdown_file

    if table_of_contents:
        temporary_copy_filename = os.path.join(saving_directory, saving_file_name_no_extension + "_temp_copy.md")
        os.system(f"cp {markdown_file} {temporary_copy_filename}")
        markdown_file = temporary_copy_filename

    with open(markdown_file, "r") as md_f:
        md_used_lines = md_f.readlines()[2:]  # remove first line with title in markdown
        md_html = markdown.markdown(
            "".join(md_used_lines),
            extensions=[TocExtension(baselevel=1, title="Table of Contents"), "fenced_code", "codehilite"],
            tab_length=4,
        )

    # Start the HTML file
    file_html = open(saving_path, "w")

    __image_including_string = (
        "<style>.main-single-post {background: url('" + background_img_path + "') no-repeat;}</style>"
    )

    _titles_style = """<style>
                    h1 {
                        font-size: 30px;
                    }
                    
                    h2 {
                        font-size: 24px;
                    }
                    
                    h3 {
                        font-size: 20px;
                    }
                </style>
                """

    _date = (
        f"""<div class="blog-post-format"><span><i class="fa fa-date"></i> {date} </span></div>"""
        if update_date
        else ""
    )

    # Adding the input data to the HTML file
    file_html.write(
        f"""
          <!DOCTYPE html>
          <html lang="en">

          <head>

                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible">
                <meta name="description" content="{subtitle}">
                <meta name="keywords" content="{', '.join(keywords) if keywords else ''}">
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
                
                <!-- Color code cells -->
                <link href="../../css/markdown_pygments.css" rel="stylesheet">

                {__image_including_string}
                {_titles_style}
               
                
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
                                   <h1 style="font-size:50px;">{main_title}</h1>
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

                                        {_date}

                                        <div class="blog-markdown">
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
    # codehilite

    # Saving the data into the HTML file
    file_html.close()

    # Remove temporary copy files
    if table_of_contents:
        print("hi")
        # os.system(f"rm {temporary_copy_filename}")


if __name__ == "__main__":
    # Sources
    source_markdown_file = r"blog_entries/blog_markdown/tips.md"
    background_img_path = os.path.join(r"../../images/my_pictures/", r"blackboard_PI.jpg")
    subtitle = None
    update_date = None
    keywords = ['python', 'maps', 'tips', 'terminal', 'bash', 'spark', 'viz', 'plot', 'git']

    convert_markdown_to_html(
        source_markdown_file, background_img_path, subtitle=subtitle, keywords=keywords, table_of_contents=True
    )
