$(function() {
  $(document).ready(function() {
    sceditor.formats.bbcode.set(
      'url',
      {
        allowEmpty: true,
        tags: {
          a: {
            href: null
          }
        },
        quoteType: 2,
        format: function (element, content) {
          var url = sceditor.dom.attr(element, 'href');
          // make sure this link is not an e-mail,
          // if it is return e-mail BBCode
          if (url.substr(0, 7) === 'mailto:') {
            return '[email="' + url.substr(7) + '"]' +
              content + '[/email]';
          }
          // make sure this link is not a user link,
          // if it is return user BBCode
          if (url.substr(0, 15) === '/board/profile/') {
            return '[user]' + url.substr(15).replace(/\//g, '') + '[/user]';
          }
          return '[url=' + url + ']' + content + '[/url]';
        }
      }
    );
    sceditor.formats.bbcode.set(
      'user',
      {
        quoteType: 2,
        html: function(token, attrs, content) {
          return '<a href="/board/profile/' + content + '/"><i class="fa fa-user" aria-hidden="true"></i> ' + content + '</a>';
        }
      }
    );
    sceditor.formats.bbcode.set(
      'code',
      {
        tags: {
          code: null
        },
        isInline: false,
        allowedChildren: ['#', '#newline'],
        format: '[code]{0}[/code]',
        html: '<pre class="prettyprint"><code>{0}</code></pre>'
      }
    );
    sceditor.formats.bbcode.set(
      'shadow',
      {
        tags: {
          span: {
            id: 'bbcode-shadow',
          }
        },
        style: {
          'text-shadow': null
        },
        format: function(element, content) {
          var textShadow = element.style.textShadow;
          if (!textShadow) {
            return content;
          }
          var shadowColor = textShadow.split(" 0px")[0];
          return '[shadow=' + shadowColor + ']' + content + '[/shadow]';
        },
        html: function(token, attrs, content) {
          return '<span id="bbcode-shadow" style="text-shadow: 0px 0px 1em ' + attrs.defaultattr + '">' + content + '</span>';
        }
      }
    );
  });
});
