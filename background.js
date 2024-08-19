chrome.browserAction.onClicked.addListener(function(tab) {
  // Aktif sekmede content script'i çalıştır
  chrome.tabs.executeScript(tab.id, {
      file: 'content.js'
  });
});
