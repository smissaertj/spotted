import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import VeeValidatePlugin from "@/includes/validation.js";

import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faMapLocationDot,
  faMagnifyingGlassLocation,
  faSplotch,
  faSpinner,
} from "@fortawesome/free-solid-svg-icons";

import { faSlideshare, faGithub } from "@fortawesome/free-brands-svg-icons";

/* add icons to the library */
library.add(
  faMapLocationDot,
  faMagnifyingGlassLocation,
  faSplotch,
  faSpinner,
  faSlideshare,
  faGithub
);
import "./assets/main.css";

const app = createApp(App).component("font-awesome-icon", FontAwesomeIcon);

app.use(createPinia());
app.use(router);
app.use(VeeValidatePlugin);

app.mount("#app");
