function construct() {
    document.getElementById("aboutUs_title").innerHTML = about_us.title;
    document.getElementById("aboutUs_des").innerHTML = about_us.description;
}
if (!String.prototype.format) {
    String.prototype.format = function() {
      var args = arguments;
      return this.replace(/{(\d+)}/g, function(match, number) { 
        return typeof args[number] != 'undefined'
          ? args[number]
          : match
        ;
      });
    };
  }
$(function () {       
    $('.menu-home').click(function (e) { 
        e.preventDefault();        
        pos = 0;
        $('html').animate({scrollTop: pos}, 1500, "easeOutBack");
    });
    $('.menu-news').click(function (e) { 
        e.preventDefault();   
        pos = $('.news').offset().top;     
        $('html').animate({scrollTop: pos}, 1500, "easeOutBack");
    });
    $('.menu-menu').click(function (e) { 
        e.preventDefault();   
        pos = $('.menu').offset().top;     
        $('html').animate({scrollTop: pos}, 1500, "easeOutBack");
    });
    $('.menu-about').click(function (e) { 
        e.preventDefault();   
        pos = $('.about-us').offset().top;     
        $('html').animate({scrollTop: pos}, 1500, "easeOutBack");
    });
    construct();
    show_menu();
    
});

var about_us = {
    title: "About Us",
    description: "On her way she met a copy. The copy warned the Little Blind Text, that where it came from it would have been rewritten a thousand times and everything that was left from its origin would be the word \"and\" and the Little Blind Text should turn around and return to its own, safe country. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth.",
}

// show menu
function show_menu() {
  var rows = document.getElementsByClassName('menu-content')[0];
  for (var c = 0; c < 2; c ++) {
    var row = document.createElement('div');
    row.setAttribute('class', 'row stage');
    for (var i = 0; i < 4; i ++) {
      // create col
      var col = document.createElement("div");
      col.setAttribute('class', 'col-lg-3 col-sm-5 item');

      // create bouding a tag to col
      var a_tag = document.createElement("a");
      setAttributes(a_tag, {
        'href': "#",
        'class': 'block w-100'
      });

      // create img tag
      img_tag = document.createElement('img');
      setAttributes(img_tag, {
        'src': "./assets/food/food1.jpg",
        'class': 'img-fluid'
      });

      // create content for the food
      info_tag = document.createElement("div");
      info_tag.setAttribute('class', "info");

      h4_tag = document.createElement('h4');
      h4_tag.innerHTML = 'Title';

      p_tag = document.createElement('p');
      p_tag.innerHTML = 'On her way she met a copy. The copy warned the Little Blind Text, that where it came';

      info_tag.innerHTML = h4_tag.outerHTML + p_tag.outerHTML;
      a_tag.innerHTML = img_tag.outerHTML + info_tag.outerHTML;
      col.appendChild(a_tag);
      row.appendChild(col);
    }
    rows.appendChild(row);
  }
  console.log(rows[0])
}

function setAttributes(el, attrs) {
  for(var key in attrs) {
    el.setAttribute(key, attrs[key]);
  }
}