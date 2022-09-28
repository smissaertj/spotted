import firebase from "firebase/app";
import "firebase/auth";
import "firebase/firestore";
import "firebase/storage";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAJQkdcRAjPXDeqyQaTymoR_N8Yq7j9F6I",
  authDomain: "spotted-a3667.firebaseapp.com",
  projectId: "spotted-a3667",
  storageBucket: "spotted-a3667.appspot.com",
  messagingSenderId: "778934144630",
  appId: "1:778934144630:web:9770bfed1d93861a3d1957",
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();
const storage = firebase.storage();
const usersCollection = db.collection("users");
const mapMarkerCollection = db.collection("mapMarkers");
const photoCollection = db.collection("markerPhotos");

export {
  auth,
  db,
  storage,
  usersCollection,
  mapMarkerCollection,
  photoCollection,
};
