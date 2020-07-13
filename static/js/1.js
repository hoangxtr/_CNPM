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
    show_menu(1);
    $('.page-item').click(function(e) {
      $('.page-item').removeClass('active');
      $(this).addClass('active');
      pos = $('.menu').offset().top;
      $('html').animate({scrollTop: pos}, 1500, "easeOutBack");
    });

    // new functionality


});

function updatedUser(id, action) {
  var url = '/page/updatedItem/';
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({'productID': id, 'action': action})
  })

  .then((response) => {
    return response.json()
  })

  .then((data) => {
    console.log('data', data)
    document.getElementById("_cart").setAttribute("value", data.total)
  })


}

var about_us = {
    title: "About Us",
    description:"Smart Food Court located at the campus of Ho Chi Minh City University Of Technology. We have many stall is local brand now. Many beautiful food from everywhere VietNam's food, Asian's food, being in class, why you don't come here. Smart Food Court confident that one of the smart restaurant systems will give to you the most convenient and convenient service., which helps customers save time to buy, diversify payment methods and above all professional service style Smart Food Court, Why?  Sure that, Smart Food Court has everything you need and always ready to welcome you",
}

// show menu
const menu_size = 12;
function show_menu(tab) {
  var rows = document.getElementsByClassName('menu-content')[0];
  rows.innerHTML = '';
  for (var r = 0; r < 3; r ++) {
    var row = document.createElement('div');
    row.setAttribute('class', 'row stage');
    for (var i = 0; i < 4; i ++) {
      // create col
      var pos = menu_size * (tab - 1) + 4 * r + i;
      if (pos >= Foods.length) break;
      food = Foods[pos]
      var col = document.createElement("div");
      col.setAttribute('class', 'col-lg-3 col-sm-5 item');
      col.setAttribute('data-id', food.id);
      col.setAttribute('data-action', "add");

      // create bouding a tag to col
      var a_tag = document.createElement("span");
      setAttributes(a_tag, {
        'href': food.link,
        'class': 'block w-100'
      });

      // create img tag
      img_tag = document.createElement('img');
      setAttributes(img_tag, {
        'src': food.avatar,
        'class': 'img-fluid'
      });

      // create content for the food
      info_tag = document.createElement("div");
      info_tag.setAttribute('style', "overflow-y: auto")
      info_tag.setAttribute('class', "info");


      h4_tag = document.createElement('h4');
      h4_tag.innerHTML = food.title;

      p_tag = document.createElement('p');
      p_tag.setAttribute('style', "white-space: normal; word-break: break-all;")
      p_tag.innerHTML = food.description;

      span_tag = document.createElement("span")
      span_tag.setAttribute("class", "buy")
      i_tag = document.createElement("i");
      i_tag.setAttribute("class", "fa fa-cart-plus")
      i_tag.setAttribute("area-hidden", "true")
      span_tag.appendChild(i_tag)

      info_tag.innerHTML = h4_tag.outerHTML + p_tag.outerHTML + span_tag.outerHTML;
      a_tag.innerHTML = img_tag.outerHTML + info_tag.outerHTML;
      col.appendChild(a_tag);
      row.appendChild(col);
    }
    rows.appendChild(row);

    var foods = document.getElementsByClassName("item");
    for (var i = 0; i < foods.length; i ++) {

      $(foods[i]).on('click', function (e) {
        // event handler for dynamically added children
        e.stopImmediatePropagation();
        console.log("hello world");
        var id = this.dataset.id;
        action = this.dataset.action;
        console.log(id);

        if (my_user === 'AnonymousUser') {
          console.log("Login before order");
        } else {
          updatedUser(id, action);
        }
    });

    }
  }
}

function setAttributes(el, attrs) {
  for(var key in attrs) {
    el.setAttribute(key, attrs[key]);
  }
}


