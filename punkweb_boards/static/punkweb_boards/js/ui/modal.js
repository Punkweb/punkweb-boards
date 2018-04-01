$(function() {
  $(document).ready(function() {
    // This script adds functionality to elements with data-role="modal" and data-role="modal-open" attributes.
    // Elements with these roles should also have a data-modal-id attribute that match.

    var openers = $('[data-role="modal-open"]');
    var modals = $('[data-role="modal"]');

    function getOpener(modalId) {
      return openers.filter('[data-modal-id=' + modalId + ']');
    }

    function getModal(modalId) {
      return modals.filter('[data-modal-id=' + modalId + ']');
    }

    function openModal(modalId) {
      getModal(modalId).show(100, 'swing', function() {});
    }

    function closeModal(modalId) {
      getModal(modalId).hide(100, 'swing', function() {});
    }

    function setPointer(opener) {
      opener.css({
        'cursor': 'pointer',
      });
    }

    // Close modal if backdrop with valid id is clicked.
    $(window).click(function(e) {
      var roleAttr = e.target.attributes['data-role'];
      var hasRoleAttr = !!roleAttr;
      var roleValue = hasRoleAttr ? roleAttr.value : undefined;
      if (roleValue == 'modal') {
        var modalIdAttr = e.target.attributes['data-modal-id'];
        var hasModalIdAttr = !!modalIdAttr;
        var modalIdValue = hasModalIdAttr ? modalIdAttr.value : undefined;
        closeModal(modalIdValue);
      }
    });

    // Open modal with the corresponding "data-modal-id" attribute.
    openers.each(function() {
      var self = $(this);
      setPointer(self);
      self.click(function() {
        openModal(self.attr('data-modal-id'));
      });
    });

    modals.each(function() {
      var self = $(this);
      if (self.attr('data-init-open') === "true") {
        openModal(self.attr('data-modal-id'));
      }
    });
  });
});
