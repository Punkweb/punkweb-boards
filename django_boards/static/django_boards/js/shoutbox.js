$(function() {
  $(document).ready(function() {
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
      // test that a given url is a same-origin URL
      // url could be relative or scheme relative or absolute
      var host = document.location.host; // host + port
      var protocol = document.location.protocol;
      var sr_origin = '//' + host;
      var origin = protocol + sr_origin;
      // Allow absolute or scheme relative URLs to same origin
      return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
          // Send the token to same-origin, relative URLs only.
          // Send the token only if the method warrants CSRF protection
          // Using the CSRFToken value acquired earlier
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    var editor = $('#shoutEditor').sceditor({
      format: 'bbcode',
      toolbar: 'bold,italic,underline,strike|font,size,color,link,emoticon|date,time|source,removeformat',
      style: '/static/django_boards/scss/editor.css',
      fonts: 'Arial,Arial Black,Comic Sans MS,Courier New,Georgia,Impact,Sans-serif,Serif,Storybook,Times New Roman,Trebuchet MS,Truckin,Verdana',
      autoExpand: true,
      emoticonsEnabled: true,
      emoticonsCompat: true,
      emoticonsRoot: '/media/precise_bbcode/smilies/',
      emoticons: {
        dropdown: {
          ":gd:": "gd.png",
          ":gimli:": "gimli.jpg"
        },
        hidden: {}
      }
    });

    $('#submitShout').click(function($event) {
      var editorContent = editor.sceditor('instance').val();
      editor.sceditor('instance').val('');
      postShout(editorContent);
    });

    $('#reloadShouts').click(function($event) {
      getShouts();
    });

    var shoutList = [];

    function clearShoutList() {
      shoutList = [];
      $('#shoutBox').html('');
    }

    function shoutLine(shout) {
      var date = new Date(shout.created);
      var dateStr = new Date(date.getTime()).toLocaleTimeString();
      return $.parseHTML('<p class="shout">' + dateStr + ' <a href="/board/profile/' + shout.username + '">' + shout.rendered_username + '</a>: ' + shout._content_rendered + '</p>');
    }

    function getShouts() {
      $.get('/board/api/shouts/', function(data) {
        clearShoutList();
        shoutList = data.results;

        shoutList.forEach(function(shout) {
          $('#shoutBox').append(shoutLine(shout));
        });
      });
    }

    function postShout(shout) {
      if (!shout) {
        return;
      }
      $.ajax({
        type: 'POST',
        url: '/board/api/shouts/',
        data: {
          content: shout
        },
        success: function(data) {
          getShouts();
        },
        error: function(err) {
          var errMsg = err.responseJSON;
          if (errMsg.notAllowed) {
            $('#shoutboxError').text(errMsg.notAllowed).css('color', 'red');
          }
        }
      });
    }

    getShouts();
  });
});
