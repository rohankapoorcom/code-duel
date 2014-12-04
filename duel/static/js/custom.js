/*
 * AJAX submit the registration form
 */
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

/*
 * AJAX submit the login form
 */
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

/*
 * Call bootstrapValidator on the registration form
 */
function validateRegistrationForm() {
  $('#registrationForm').bootstrapValidator({
      feedbackIcons: {
          valid: 'glyphicon glyphicon-ok',
          invalid: 'glyphicon glyphicon-remove',
          validating: 'glyphicon glyphicon-refresh'
      }
  });
}

/*
 * AJAX logout the current user
 */
function logout() {
  var getting = $.get(flask_util.url_for('logout'));
  
  getting.done(function(data) {
    data = JSON.parse(data);
    if (data['success'])
      $('#navbar').load(location.href + ' #navbar');
      $('#registration').load(location.href + ' #registration > *');
  });
}

/*
 * Setup a SocketIO connection to the server and respond to messages
 */
function setupSocketIO() {
  socket = io.connect('http://' + document.domain + ':' + location.port);
  socket.emit('connect', '');
  socket.on('graded_code', function(msg) {
    if (msg['session_id'] != $('#duel_session_id').val()) {
      console.log('ignoring');
      return;
    }

    if (msg['user_id'] != $('#user_id').val()) {
      // Inform the user that the opponent won
      console.log('user_id not equal');
      if (msg['correct']) {
        banner = "<div class='alert alert-danger alert-dismissable fade in' role='alert'><button type='button' class='close' data-dismiss='alert'><span aria-hidden='true'>&times;</span><span class='sr-only'>Close</span></button>You Lose, your opponent submitted the correct answer!</div>";
      }
      else
        return;
    }

    else {
      // Inform the user that they won
      if (msg['correct']) {
        banner = "<div class='alert alert-success alert-dismissable fade in' role='alert'><button type='button' class='close' data-dismiss='alert'><span aria-hidden='true'>&times;</span><span class='sr-only'>Close</span></button>You Win, you submitted the correct answer!</div>";
      }

      else {
        banner = "<div class='alert alert-danger alert-dismissable fade in' role='alert'><button type='button' class='close' data-dismiss='alert'><span aria-hidden='true'>&times;</span><span class='sr-only'>Close</span></button>Your Code Didn't Work. Change it, then try Again!</div>";
      }
    }
    $('#placeholder').html(banner);
    
    window.setTimeout(function() {
          $('.alert').alert('close');
        }, 5000);
  });
}

/*
 * Use SocketIO to submit the code for grading
 */
function submitCode() {
  socket.emit(
    'submit_code',
    {
      'code': codeMirror.getValue(),
      'question_id': $('#question_id').val(),
      'user_id': $('#user_id').val(),
      'session_id': $('#duel_session_id').val()
    }
  );
}