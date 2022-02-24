$(function() {
  $(document).ready(function() {
    $('.post-editor').sceditor({
      format: 'bbcode',
      icons: 'material',
      toolbar: 'bold,italic,underline,strike|bulletlist,orderedlist,center,horizontalrule|font,size,color,quote,code,link,image|date,time|source,maximize,removeformat',
      style: '/static/punkweb_boards/scss/editor.css',
      fonts: 'Arial,Arial Black,Comic Sans MS,Inconsolata,Courier New,Georgia,Impact,Open Sans,Montserrat,Sans-serif,Serif,Times New Roman,Trebuchet MS,Verdana',
      autoExpand: true,
      emoticonsEnabled: false,
      emoticonsCompat: true,
      emoticonsRoot: '/media/precise_bbcode/smilies/'
    });

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
