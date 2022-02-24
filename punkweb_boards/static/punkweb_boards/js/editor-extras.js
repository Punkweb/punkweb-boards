$(function() {
  $(document).ready(function() {
    function initFontAwesome() {
      setTimeout(function() {
        $('.sceditor-container').each(function() {
          var editor = $(this);
          var iframe = $(editor).children('iframe')[0];
          var iframeHead = $(iframe).contents().find('head');
          var linkUrl = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css';
          var link = $('<link>', {
            id: 'fontAwesomeLink',
            rel: 'stylesheet',
            href: linkUrl,
            integrity: 'sha512-9usAa10IRO0HhonpyAIVpjrylPvoDwiPUiKdWk5t3PyolY1cOd4DSE0Ga+ri4AuTroPR5aQvXU9xC6qOPnzFeg==',
            crossorigin: 'anonymous',
            referrerpolicy: 'no-referrer'
          });
          $(iframeHead).append(link);
        });
      }, 500);
    }

    function initJQuery() {
      setTimeout(function() {
        $('.sceditor-container').each(function() {
          var editor = $(this);
          var iframe = $(editor).children('iframe')[0];
          var iframeHead = $(iframe).contents().find('head');
          var scriptUrl = '/static/punkweb_boards/js/deps/jquery-3.6.0.min.js';
          $(iframeHead).append($('<script>', { id: 'jqueryScript', src: scriptUrl } ));
        });
      }, 500);
    }

    function initPrettify() {
      setTimeout(function() {
        $('.sceditor-container').each(function() {
          var editor = $(this);
          var iframe = $(editor).children('iframe')[0];
          var iframeHead = $(iframe).contents().find('head');
          var scriptUrl = '/static/punkweb_boards/js/deps/run-prettify.js';

          iframeHead.find('link[href*="prettify.css"]').remove();
          $(iframeHead).find('#prettifyScript').remove();
          $(iframeHead).append($('<script>', { id: 'prettifyScript', src: scriptUrl } ));
        });
      }, 500);
    }

    function initSpoiler() {
      setTimeout(function() {
        $('.sceditor-container').each(function() {
          var editor = $(this);
          var iframe = $(editor).children('iframe')[0];
          var iframeHead = $(iframe).contents().find('head');
          var scriptUrl = '/static/punkweb_boards/js/ui/spoiler.js';
          $(iframeHead).append($('<script>', { id: 'spoilerScript', src: scriptUrl } ));
        });
      }, 500);
    }

    $('.sceditor-button-source').click(function() {
      initPrettify();
    });

    initFontAwesome();
    initJQuery();
    initPrettify();
    initSpoiler();
  });
});
