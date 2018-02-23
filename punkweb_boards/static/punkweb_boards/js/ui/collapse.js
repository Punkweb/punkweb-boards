// This script saves collapsed items in local storage,
// so collapsing an item will persist.

$(function() {
  $(document).ready(function() {
    var storageKey = 'collapsed';

    var collapsed = JSON.parse(localStorage.getItem(storageKey)) || {
      keys: []
    };
    var toggles = $('[data-role="collapsible-toggle"]');
    var items = $('[data-role="collapsible"]');

    function getToggle(key) {
      return toggles.filter('[data-key=' + key + ']');
    }

    function getItem(key) {
      return items.filter('[data-key=' + key + ']');
    }

    function setPointer(toggle) {
      toggle.css({
        'cursor': 'pointer',
      });
    }

    function setHidden(item) {
      item.css({
        'display': 'none',
      });
    }

    function addToCollapsed(key) {
      var objIndex = _.findIndex(collapsed.keys, function(o) {
        return o.key === key;
      });
      if (objIndex === -1) {
        collapsed.keys.push({'key': key});
        localStorage.setItem(storageKey, JSON.stringify(collapsed));
      }
    }

    function removeFromCollapsed(key) {
      var objIndex = _.findIndex(collapsed.keys, function(o) {
        return o.key === key;
      });
      if (objIndex !== -1) {
        collapsed.keys.splice(objIndex, 1);
        localStorage.setItem(storageKey, JSON.stringify(collapsed));
      }
    }

    function toggle(key) {
      var item = getItem(key).toggle('100', 'swing', function() {
        $(this).is(':visible') ? removeFromCollapsed(key) : addToCollapsed(key);
      });
    }

    toggles.each(function() {
      var self = $(this);
      setPointer(self);
      self.click(function() {
        toggle(self.attr('data-key'));
      });
    });

    items.each(function() {
      var self = $(this);
      var index = _.findIndex(collapsed.keys, function(o) {
        return o.key === self.attr('data-key');
      });
      if (index !== -1) {
        setHidden(self);
      }
    });
  });
});
