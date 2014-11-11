function processRegistrationForm(e) {
  e.preventDefault();
  var $form = $('#registrationForm'),
    url = flask_util.url_for('register');

  var posting = $.post(url, {
    'email': $form.find("input[name='email']").val(),
    'password': $form.find("input[name='password']").val()
  });

  posting.done(function(data) {
    data = JSON.parse(data);
    if (data['success']) {
      alert = '<div class="alert alert-success alert-dismissable fade in" role="alert"><button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>Thanks for signing up. Please login to begin.</div>';
      $form.trigger('reset');
    }

    else {
      alert = '<div class="alert alert-danger alert-dismissable fade in" role="alert"><button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>Uh oh - someone\'s already registered that email address. Please use another.</div>';
    }
    $('.alert-location').append(alert);
  });
}

function processLoginForm() {
  var $form = $('#loginForm'),
    url = flask_util.url_for('login');

  var posting = $.post(url, {
    'email': $form.find("input[name='email']").val(),
    'password': $form.find("input[name='password']").val()
  });

  posting.done(function(data) {
    data = JSON.parse(data);
    if (data['success']) {
      $('#navbar').load(location.href + ' #navbar > *');
      $('#registration').load(location.href + ' #registration > *');
    }

    else {
      alert = '<div class="alert alert-danger alert-dismissable fade in" role="alert"><button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>Uh oh - Check your username and password and try again.</div>';
      $('.alert-location').append(alert);
    }

  });

  return false;
}

function validateRegistrationForm() {
  $('#registrationForm').bootstrapValidator({
      feedbackIcons: {
          valid: 'glyphicon glyphicon-ok',
          invalid: 'glyphicon glyphicon-remove',
          validating: 'glyphicon glyphicon-refresh'
      }
  });
}

function logout() {
  var getting = $.get(flask_util.url_for('logout'));
  
  getting.done(function(data) {
    data = JSON.parse(data);
    if (data['success'])
      $('#navbar').load(location.href + ' #navbar');
      $('#registration').load(location.href + ' #registration > *');
  });
}