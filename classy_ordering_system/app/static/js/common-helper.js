/**
 *
 * Restricts input for the given textbox to the given inputFilter function.
 *
 */

function setInputFilter(textbox, inputFilter) {
  [
    "input",
    "keydown",
    "keyup",
    "mousedown",
    "mouseup",
    "select",
    "contextmenu",
    "drop",
  ].forEach(function (event) {
    if (textbox) {
      textbox.addEventListener(event, function () {
        if (inputFilter(this.value)) {
          this.oldValue = this.value;
          this.oldSelectionStart = this.selectionStart;
          this.oldSelectionEnd = this.selectionEnd;
        } else if (this.hasOwnProperty("oldValue")) {
          this.value = this.oldValue;
          this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
        } else {
          this.value = "";
        }
      });
    }
  });
}

/**
 *
 * Functions for input validation
 *
 */

//only number
document.querySelectorAll(".onlyNumber").forEach((ele) => {
  setInputFilter(ele, function (value) {
    return /^[0-9]*$/.test(value);
  });
});

//number min 0
document.querySelectorAll(".numberMin0").forEach((ele) => {
  setInputFilter(ele, function (value) {
    return /^\d*$/.test(value);
  });
});

//number with min max value

document.querySelectorAll(".intLimitTextBox").forEach((ele) => {
  setInputFilter(ele, function (value) {
    return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 500);
  });
});

//number with float value

document.querySelectorAll(".numberWithFloat").forEach((ele) => {
  setInputFilter(ele, function (value) {
    return /^-?\d*[.,]?\d*$/.test(value);
  });
});
//number with 2 deicimal

document.querySelectorAll(".numberWith2Decimal").forEach((ele) => {
  setInputFilter(ele, function (value) {
    return /^-?\d*[.,]?\d{0,2}$/.test(value);
  });
});
//only A-z char

document.querySelectorAll(".onlyChar").forEach((ele) => {
  setInputFilter(ele, function (value) {
    return /^[a-z]*$/i.test(value);
  });
});
//only hexadecimal value
document.querySelectorAll(".hexadecimal").forEach((ele) => {
  setInputFilter(ele, function (value) {
    return /^[0-9a-f]*$/i.test(value);
  });
});
/**
 *
 * Function for check given object is empty.
 *
 */
const isEmpty = (obj) => {
  return Object.keys(obj).length === 0 && obj.constructor === Object;
};

/*
 *
 *Function for displat default image where image not loded currently
 *
 */

const imgReplace = (src) => {
  let image = document.querySelector("img");
  image.forEach((ele) => {
    if (ele.complete && ele.naturalHeight !== 0) {
      ele.src = src;
    }
  });
};

function getProductBasedOnCategoryId(categoryId, subCategoryId = 0, selected_tag = true, selectedProducts = "") {
  var productIds = [];
  if (selectedProducts != "")
    productIds = selectedProducts.split(",");

  $.ajax({
    type: "GET",
    url: url + "/admin/product/list/" + categoryId + '/' + subCategoryId,
  }).done(function (data) {
    var options = '<option value="">-- Select product list --</option>';

    $.map(data, function (val, i) {
      var selected = "";
      if (selectedProducts != "") {
        selected = (productIds.includes(val.id.toString())) ? 'selected="selected"' : '';
      }
      else if (subCategoryId != 0)
        selected = (subCategoryId == val.sub_category_id && selected_tag == true) ? 'selected="selected"' : '';
      else
        selected = (categoryId == val.category_id && selected_tag == true) ? 'selected="selected"' : '';

      options = options + '<option value="' + val.id + '" ' + selected + '>' + val.name + '</option>';
    });
    $('#product_select_box').html(options);
  }).fail(function (data) { });
}



