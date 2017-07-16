/**
 * Created by joseret on 7/13/17.
 */



'use strict';

// Initializes FriendlyChat.
function FriendlyChat() {this.checkSetup();

  // Shortcuts to DOM Elements.
  this.userIdToken = '';
  this.userInfo = {}
  this.messageList = document.getElementById('messages');
  this.messageForm = document.getElementById('message-form');
  this.messageInput = document.getElementById('message');
  this.submitButton = document.getElementById('submit');
  this.submitImageButton = document.getElementById('submitImage');
  this.imageForm = document.getElementById('image-form');
  this.mediaCapture = document.getElementById('mediaCapture');
  this.userPic = document.getElementById('user-pic');
  this.userName = document.getElementById('user-name');
  this.signInButton = document.getElementById('sign-in');
  this.signOutButton = document.getElementById('sign-out');
  this.signInSnackbar = document.getElementById('must-signin-snackbar');
  this.pingPrivate = document.getElementById('ping-private');
  // Saves message on form submit.
  // this.messageForm.addEventListener('submit', this.saveMessage.bind(this));
  this.signOutButton.addEventListener('click', this.signOut.bind(this));
  this.signInButton.addEventListener('click', this.signInWithPopup.bind(this));
  this.pingPrivate.addEventListener('click', this.pingPrivateAction.bind(this));
  // Toggle for the button.
  var buttonTogglingHandler = this.toggleButton.bind(this);
  this.messageInput.addEventListener('keyup', buttonTogglingHandler);
  this.messageInput.addEventListener('change', buttonTogglingHandler);

  // Events for image upload.
  this.submitImageButton.addEventListener('click', function(e) {
    e.preventDefault();
    this.mediaCapture.click();
  }.bind(this));
 // this.mediaCapture.addEventListener('change', this.saveImageMessage.bind(this));
  this.initFirebase();
}


FriendlyChat.prototype.signInWithPopup = function() {
  window.open(this.getWidgetUrl(), 'Sign In', 'width=985,height=735');
};


/**
 * @return {string} The URL of the FirebaseUI standalone widget.
 */
FriendlyChat.prototype.getWidgetUrl = function()  {
  return 'widget.html';
};

// Sets up shortcuts to Firebase features and initiate firebase auth.
FriendlyChat.prototype.initFirebase = function() {
  // Shortcuts to Firebase SDK features.
  this.auth = firebase.auth();
  // this.database = firebase.database();
  // this.storage = firebase.storage();
  // Initiates Firebase auth and listen to auth state changes.
  this.auth.onAuthStateChanged(this.onAuthStateChanged.bind(this));
};

FriendlyChat.prototype.onAuthStateChanged = function(user) {
  console.log('user', user);

  if (user) { // User is signed in!
    console.log('user', user);
    // Get profile pic and user's name from the Firebase user object.
    var profilePicUrl = user.photoURL; // Only change these two lines!
    var userName = user.displayName;
    var self = this;
    user.getToken().then(function(idToken) {
      console.log('getToken', idToken, user);
      self.userIdToken = idToken;
    });
    // Set the user's profile pic and name.
    this.userPic.style.backgroundImage = 'url(' + profilePicUrl + ')';
    this.userName.textContent = userName;

    // Show user's profile and sign-out button.
    this.userName.removeAttribute('hidden');
    this.userPic.removeAttribute('hidden');
    this.signOutButton.removeAttribute('hidden');
    this.pingPrivate.removeAttribute('hidden');
    this.pingPrivate.removeAttribute('disabled')
    // Hide sign-in button.
    this.signInButton.setAttribute('hidden', 'true');

    // We load currently existing chant messages.
    //this.loadMessages();

    // We save the Firebase Messaging Device token and enable notifications.
    // this.saveMessagingDeviceToken();
  } else { // User is signed out!
    // Hide user's profile and sign-out button.
    this.idUserToken = null;
    this.userName.setAttribute('hidden', 'true');
    this.userPic.setAttribute('hidden', 'true');
    this.signOutButton.setAttribute('hidden', 'true');

    // Show sign-in button.
    this.signInButton.removeAttribute('hidden');
    this.pingPrivate.removeAttribute('disabled')
  }
};


FriendlyChat.prototype.checkSetup = function() {
  if (!window.firebase || !(firebase.app instanceof Function) || !firebase.app().options) {
    window.alert('You have not configured and imported the Firebase SDK. ' +
        'Make sure you go through the codelab setup instructions and make ' +
        'sure you are running the codelab using `firebase serve`');
  }
};

// // Signs-in Friendly Chat.
// FriendlyChat.prototype.signIn = function() {
//   // Sign in Firebase using popup auth and Google as the identity provider.
//   console.log('signIn');
//   var provider = new firebase.auth.GoogleAuthProvider();
//   this.auth.signInWithPopup(provider);
// };

// Signs-out of Friendly Chat.
FriendlyChat.prototype.signOut = function() {
  // Sign out of Firebase.
  this.auth.signOut();
};

// Returns true if user is signed-in. Otherwise false and displays a message.
FriendlyChat.prototype.checkSignedInWithMessage = function() {
  // Return true if the user is signed in Firebase
  if (this.auth.currentUser) {
    return true;
  }
};

// Enables or disables the submit button depending on the values of the input
// fields.
FriendlyChat.prototype.toggleButton = function() {
  if (this.messageInput.value) {
    this.submitButton.removeAttribute('disabled');
  } else {
    this.submitButton.setAttribute('disabled', 'true');
  }
};

FriendlyChat.prototype.pingPrivateAction = function() {
    var userIdToken = this.userIdToken;
    console.log('pingPrivateAction', userIdToken);
    $.ajax('/private', {
    /* Set header for the XMLHttpRequest to get data from the web server
    associated with userIdToken */
    headers: {
      'Authorization': 'Bearer ' + userIdToken
    }
  });
};

$(function(){
  window.friendlyChat = new FriendlyChat();
});
