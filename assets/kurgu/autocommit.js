$("input").change(function(){
  keyupfunction($(this).attr('name'),$(this).attr('id'), $(this).val())
});

function keyupfunction(name, id, value) {
  var timeout = null;
  var minlength = 0;

  // clear last timeout check
  clearTimeout(timeout);

  if (value.length > minlength) {
    console.log(name, id, value)

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