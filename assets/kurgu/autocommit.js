$("input").change(function(){
  keyupfunction($(this).attr('name'),$(this).attr('id'), $(this).val(),$(this).is(':checked'))
});

$("textarea").change(function(){
  keyupfunction2($(this).attr('name'),$(this).attr('id'), $(this).val())
});

$("select").change(function(){
  keyupfunction3($(this).attr('name'),$(this).attr('id'), $(this).val())
});

function keyupfunction(name, id, value,check) {
  var timeout = null;

  // clear last timeout check
  clearTimeout(timeout);

  if (check) {
    value="true";
  };

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


function keyupfunction2(name, id, value) {
  var timeout = null;

  // clear last timeout check
  clearTimeout(timeout);

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

function keyupfunction3(name, id, value) {
  var timeout = null;

  // clear last timeout check
  clearTimeout(timeout);

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


