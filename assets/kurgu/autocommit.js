$("input").change(function(){
  keyupfunction($(this).attr('name'),$(this).attr('id'), $(this).val(),$(this).is(':checked'))
});

$("textarea").change(function(){
  keyupfunction2($(this).attr('name'),$(this).attr('id'), $(this).val())
});

function keyupfunction(name, id, value,check) {
  var timeout = null;
  var minlength = 0;

  // clear last timeout check
  clearTimeout(timeout);

  if (check) {
    value="true";
  };

  if (value.length > minlength) {

    timeout = setTimeout(function() {
      $.ajax({
        type: "POST",
        url: "/kurgu/kj_kurgu",
        data: {
          [name] : value,
          id : id
        },
        dataType: "text",
      });
    }, 500); 
}

}


function keyupfunction2(name, id, value) {
  var timeout = null;
  var minlength = 0;

  // clear last timeout check
  clearTimeout(timeout);

  if (value.length > minlength) {
    // console.log(name, id, value)

    timeout = setTimeout(function() {
      $.ajax({
        type: "POST",
        url: "/kurgu/kj_kurgu",
        data: {
          [name] : value,
          id : id
        },
        dataType: "text",
      });
    }, 500); 
}

}


