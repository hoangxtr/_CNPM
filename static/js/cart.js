$(function() {
    var arrown_ups = document.getElementsByClassName("__arrow")
    for (var i = 0; i < arrown_ups.length; i ++) {
        arrown_ups[i].addEventListener('click', function() {
            console.log("clicked")
            var id = this.dataset.id;
            var action = this.dataset.action;
            updatedUser(id, action);
        })
    }
    
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
      food_id = "food" + data['id']
      item = document.getElementById(food_id)
      item.getElementsByClassName("output_quantity")[0].innerHTML = data.quantity
    //   console.log(quan)
      
      item.children[5].innerHTML = item.children[3].innerHTML * data.quantity
      if (data.quantity <= 0)
        item.remove()
    
      document.getElementById("all_total").innerHTML = data.total_bill
      

      document.getElementById("_cart").setAttribute("value", data.total)
    })
  
  
  }