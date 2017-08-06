<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" >
	<head>
		<title>Photomaton</title>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<style type="text/css">
			h1 { color: red; }
			h1 { text-align: center; }
			h1 { font-size: 70px; }
			a img { border:0; }
			p { border: solid black 2px; }
			.containerBox {
			    position: relative;
			    display: inline-block;
			}
			.text-box {
			    position: absolute;    
			    height: 100%;
			    text-align: center;    
			    width: 100%;
			}
			.text-box:before {
			   content: '';
			   display: inline-block;
			   height: 100%;
			   vertical-align: top;
			}
			h4 {
			   display: inline-block;
			   font-size: 15px; /*or whatever you want*/
			   color: #FFF;
			   background-color: #000;   
			}
			img {
			  display: block;
			  max-width: 100%;
			  height: auto;
			}
		</style>
	</head>
	<header>
		<h1>Galerie photo</h1>
	</header>
	<body>
		<p>
			<?php 
                        foreach (glob("*.png") as $image){
                            echo 	"<a href=\"$image\" download>
					<div class=\"containerBox\">
					    <div class=\"text-box\">
						<h4>$image</h4>
					    </div>
					    <img class=\"img-responsive\" src=\"mini/$image\"/>
					</div>";
                        }
                        ?>
		</p>
	</body>
</html>
