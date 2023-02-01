$("input").change(function(){
  keyupfunction($(this).attr('name'),$(this).attr('class'), $(this).val(),$(this).is(':checked'))
});

$("textarea").change(function(){
  keyupfunction2($(this).attr('name'),$(this).attr('class'), $(this).val())
});

$("select").change(function(){
  keyupfunction3($(this).attr('name'),$(this).attr('class'), $(this).val())
});

$('input[id=datefield]').keyup(function(){
  autodate($(this).val())
});

$('input[id=datetimefield]').keyup(function(){
  autodatetime($(this).val())
});

function autodate(value) {
  if ((value.length == 2 || value.length == 5) & ! (value.indexOf("/") == 1) ) {
    document.getElementById("datefield").value = value+"/"
  };
}

function autodatetime(value) {
  if ((value.length == 2 || value.length == 5) & ! (value.indexOf("/") == 1) ) {
    document.getElementById("datetimefield").value = value+"/"
  };
  if ((value.length == 10) & ! (value.indexOf("/") == 1) ) {
    document.getElementById("datetimefield").value = value+"-"
  };
  if ((value.length == 13) & ! (value.indexOf("/") == 1) ) {
    document.getElementById("datetimefield").value = value+":"
  };
}


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


