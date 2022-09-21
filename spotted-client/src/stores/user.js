import { defineStore } from "pinia";
import { auth, usersCollection } from "@/includes/firebase";

export default defineStore("user", {
  state: () => ({
    userLoggedIn: false,
  }),
  actions: {
    async checkUsername(username) {
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
    },
    async register(values) {
      const userCred = await auth.createUserWithEmailAndPassword(
        values.email,
        values.password
      );
      await usersCollection.doc(userCred.user.uid).set({
        username: values.username.toLowerCase(),
        email: values.email,
      });
      await userCred.user.updateProfile({
        displayName: values.username,
      });
      this.userLoggedIn = true;
    },
    async authenticate(values) {
      await auth.signInWithEmailAndPassword(values.email, values.password);
      this.userLoggedIn = true;
    },
    async signOut() {
      await auth.signOut();
      this.userLoggedIn = false;
    },
  },
});
