$("input").change(function(){
  keyupfunction($(this).attr('name'),$(this).attr('class'), $(this).val(),$(this).is(':checked'))
});

$("textarea").change(function(){
  keyupfunction2($(this).attr('name'),$(this).attr('class'), $(this).val())
});

$("select").change(function(){
  keyupfunction3($(this).attr('name'),$(this).attr('class'), $(this).val())
});


function addDash(input) {
  var val = input.value;
  if ((val.length == 2 || val.length == 5) & ! (val.indexOf("/") == 1) ) {
    val = val + '/';
    input.value = val;
  }
}

// تمام ورودی‌های مربوطه را به دست آورید
var inputs = document.getElementsByName('play_date');

// برای هر ورودی، یک رویداد `oninput` تعریف کنید تا هنگامی که کاربر مقدار را تغییر می‌دهد، تابع `addDash` را صدا بزند.
for (var i = 0; i < inputs.length; i++) {
  inputs[i].onkeyup = function() {
    addDash(this);
  };
}


function addDash3(input) {
  var val = input.value;
  if ((val.length == 2 || val.length == 5) & ! (val.indexOf("/") == 1) ) {
    val = val + '/';
    input.value = val;
  }
}

// تمام ورودی‌های مربوطه را به دست آورید
var inputs = document.getElementsByName('presentesion_date');

// برای هر ورودی، یک رویداد `oninput` تعریف کنید تا هنگامی که کاربر مقدار را تغییر می‌دهد، تابع `addDash` را صدا بزند.
for (var i = 0; i < inputs.length; i++) {
  inputs[i].onkeyup = function() {
    addDash3(this);
  };
}


function addDash2(input) {
  var val = input.value;
  if ((val.length == 2 || val.length == 5) & ! (val.indexOf("/") == 1) ) {
    val = val + "/";
    input.value = val;
  }
  if ((val.length == 10) & ! (val.indexOf("/") == 1) ) {
    val = val + "-";
    input.value = val;
  }
  if ((val.length == 13) & ! (val.indexOf("/") == 1) ) {
    val = val + ":";
    input.value = val;
  }
  
}

// تمام ورودی‌های مربوطه را به دست آورید
var inputs = document.getElementsByName('record_date');

// برای هر ورودی، یک رویداد `oninput` تعریف کنید تا هنگامی که کاربر مقدار را تغییر می‌دهد، تابع `addDash` را صدا بزند.
for (var i = 0; i < inputs.length; i++) {
  inputs[i].onkeyup = function() {
    addDash2(this);
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


