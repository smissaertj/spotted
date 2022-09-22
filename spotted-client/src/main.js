import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import VeeValidatePlugin from "@/includes/validation.js";
import { auth } from "./includes/firebase";

import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faMapLocationDot,
  faMagnifyingGlassLocation,
  faSplotch,
  faSpinner,
  faUser,
  faComments,
  faCirclePlus,
  faRectangleList,
  faWrench,
} from "@fortawesome/free-solid-svg-icons";

import { faSlideshare, faGithub } from "@fortawesome/free-brands-svg-icons";

/* add icons to the library */
library.add(
  faMapLocationDot,
  faMagnifyingGlassLocation,
  faSplotch,
  faSpinner,
  faSlideshare,
  faGithub,
  faUser,
  faComments,
  faCirclePlus,
  faRectangleList,
  faWrench
);

import VueGoogleMaps from "@fawmi/vue-google-maps";

import "./assets/main.css";

const app = createApp(App).component("font-awesome-icon", FontAwesomeIcon);

app.use(createPinia());
app.use(router);
app.use(VeeValidatePlugin);
app.use(VueGoogleMaps, {
  load: {
    key: import.meta.env.VITE_GMAPS_API_KEY,
  },
});

app.mount("#app");
