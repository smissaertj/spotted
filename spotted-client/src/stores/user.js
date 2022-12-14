import { defineStore } from "pinia";
import { auth, usersCollection } from "@/includes/firebase";

export default defineStore("user", {
  state: () => ({
    userLoggedIn: false,
    userIsAdmin: false,
    displayName: "",
    email: "",
    photoUrl: "",
    idToken: "",
    uid: "",
  }),
  actions: {
    async checkUsername(username) {
      const user = await auth.currentUser;
      if (user && user.displayName.toLowerCase() === username.toLowerCase()) {
        return true;
      } else {
        const results = [];
        const docsRef = await usersCollection
          .where("username", "==", username.toLowerCase())
          .get()
          .then((querySnapshot) => {
            querySnapshot.forEach((doc) => {
              results.push(doc.data());
            });
          });

        return results.length <= 0;
      }
    },
    async register(values) {
      const userCred = await auth.createUserWithEmailAndPassword(
        values.email,
        values.password
      );
      await usersCollection.doc(userCred.user.uid).set({
        username: values.username.toLowerCase(),
        email: values.email,
        isAdmin: false,
        isActive: true,
      });
      await userCred.user.updateProfile({
        displayName: values.username.toLowerCase(),
      });
      this.userLoggedIn = true;
      this.displayName = userCred.user.displayName;
      this.email = userCred.user.email;
      this.photoUrl = userCred.user.photoUrl;
    },
    async authenticate(values) {
      await auth.signInWithEmailAndPassword(values.email, values.password);
      this.userLoggedIn = true;

      const user = auth.currentUser;
      if (user != null) {
        this.idToken = await user.getIdToken(false);
        this.displayName = user.displayName;
        this.email = user.email;
        this.photoUrl = user.photoUrl;
        this.uid = user.uid;
        const docRef = await usersCollection
          .doc(user.uid)
          .get()
          .then((doc) => {
            if (doc.exists) {
              this.userIsAdmin = doc.data().isAdmin;
            }
          });
      }
    },
    async signOut() {
      await auth.signOut();
      this.userLoggedIn = false;
    },
    async update(values) {
      const user = await auth.currentUser;
      if (user.displayName != values.username) {
        user.updateProfile({ displayName: values.username });
        this.displayName = values.username;
        const docRef = usersCollection.doc(this.uid);
        docRef.update({ username: this.displayName });
      }
      if (user.email != values.email) {
        user.updateEmail(values.email);
        this.email = values.email;
      }
      if (values.password && values.confirmPassword) {
        user.updatePassword(values.confirmPassword);
      }
    },
  },
});
