// Wait till the browser is ready to render the game (avoids glitches)
window.requestAnimationFrame(function () {
  if((typeof LocalStorageManager !== 'undefined') && (typeof KeyboardInputManager !== 'undefined')) {
    new GameManager(4, KeyboardInputManager, HTMLActuator, LocalStorageManager);
  } else { // replay_manager's GameManager class is being used
    new GameManager(4, HTMLActuator);
  }
});
