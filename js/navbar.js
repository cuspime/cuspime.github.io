let navBar = `
<div class="navbar navbar-default navbar-static-top" role="navigation">
<div class="container">

    <div class="navbar-header">
        <button class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                 <span class="icon icon-bar"></span>
                 <span class="icon icon-bar"></span>
                 <span class="icon icon-bar"></span>
            </button>
        <a href="index.html" class="navbar-brand">Leopoldo Cuspinera</a>
    </div>
    <div class="collapse navbar-collapse">
        <ul class="nav navbar-nav navbar-right">
            <li id="navbar-leopoldo cuspinera"><a href="index.html">Home</a></li>
            <li id="navbar-about"><a href="about.html">About</a></li>
            <li id="navbar-projects"><a href="projects.html">Projects</a></li>
            <li id="navbar-gallery"><a href="gallery.html">Gallery</a></li>
            <li id="navbar-blog"><a href="blog.html">Blog</a></li>
            <li id="navbar-contact"><a href="contact.html">Contact</a></li>
        </ul>
    </div>

</div>
</div>
`;

document.getElementById("app-navbar").innerHTML = navBar;
document.getElementById('navbar-' + document.title.toLowerCase()).classList.add("active");