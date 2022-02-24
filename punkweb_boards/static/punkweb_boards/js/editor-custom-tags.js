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
          console.log(element);
          console.log(content);
          var textShadow = element.style.textShadow;
          if (!textShadow) {
            return content;
          }
          var shadowColor = textShadow.split(" 0px")[0];
          return '[shadow=' + shadowColor + ']' + content + '[/shadow]';
        },
        html: function(token, attrs, content) {
          console.log('token', token);
          console.log('attrs', attrs);
          console.log('content', content);
          return '<span style="text-shadow: 0px 0px 1em ' + attrs.defaultattr + '">' + content + '</span>';
        }
      }
    );
  });
});
