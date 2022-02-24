$(function() {
  $(document).ready(function() {
    sceditor.formats.bbcode.set(
      'shadow',
      {
        tags: {
          span: null
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
          return '<span style="text-shadow: 0px 0px 1em ' + attrs.defaultattr + '">' + content + '</span>';
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
  });
});
