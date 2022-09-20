<template>
  <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
    <div class="card-body bg-base-300">
      <vee-form
        class="form-control"
        :validation-schema="registerSchema"
        @submit="register"
        v-if="
          !registerAction &&
          registerResponse.status !== 'success' &&
          !userLoggedIn
        "
      >
        <div class="form-control">
          <vee-field
            type="text"
            placeholder="Username"
            class="input input-bordered"
            name="username"
            @focusout.prevent="checkUsername"
            v-model="username"
            required
          />
          <ErrorMessage class="text-red-600" name="username" />
        </div>
        <div class="form-control mt-2">
          <vee-field
            type="email"
            placeholder="Email"
            class="input input-bordered"
            name="email"
            required
          />
          <ErrorMessage class="text-red-600" name="email" />
        </div>
        <div class="form-control mt-2">
          <vee-field
            type="password"
            placeholder="Password"
            class="input input-bordered"
            name="password"
            required
          />
          <ErrorMessage class="text-red-600" name="password" />
        </div>
        <div class="form-control mt-2">
          <vee-field
            type="password"
            placeholder="Confirm Password"
            class="input input-bordered"
            name="confirmPassword"
            required
          />
          <ErrorMessage class="text-red-600" name="confirmPassword" />
        </div>

        <div class="form-control mt-2">
          <button
            class="btn btn-primary"
            type="submit"
            v-if="!registerAction"
            :disabled="!usernameAvailable"
          >
            Register
          </button>
          <div
            class="alert alert-error shadow-lg mt-2 justify-center font-bold"
            v-if="registerResponse.status == 'error'"
          >
            <div>
              <span>{{ registerResponse.message }}</span>
            </div>
          </div>
        </div>
      </vee-form>
      <div class="form-control mt-2">
        <div
          class="alert alert-success shadow-lg mt-2 justify-center font-bold"
          v-if="registerResponse.status === 'success' && !registerAction"
        >
          <div>
            <span>{{ registerResponse.message }}</span>
          </div>
        </div>
      </div>
      <div
        class="alert alert-warning shadow-lg mt-2 justify-center font-bold"
        v-if="registerAction"
      >
        <div>
          <font-awesome-icon icon="fa-solid fa-spinner" class="fa-spin" />
          <span>Creating account...</span>
        </div>
      </div>
      <div class="divider">OR</div>
      <a href="/app">
        <button class="btn btn-primary btn-block">Start Exploring</button>
      </a>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "appRegister",
  data() {
    return {
      registerSchema: {
        username: "required",
        email: "required|email",
        password: "required|min:6",
        confirmPassword: "required|confirmed:@password",
      },
      username: "",
      usernameAvailable: true,
      userLoggedIn: false,
      registerAction: false,
      registerResponse: "",
    };
  },
  methods: {
    async register(values) {
      try {
        this.registerAction = true;
        this.registerResponse = "";
        const response = await axios.post(
          import.meta.env.VITE_API_URL + "/signup",
          {
            email: values.email,
            password: values.password,
            username: values.username,
          }
        );
        this.registerAction = false;
        this.registerResponse = response.data;
      } catch (error) {
        this.registerAction = false;
        this.registerResponse = error.response.data;
      }
    },
    async checkUsername() {
      try {
        const response = await axios.post(
          import.meta.env.VITE_API_URL + "/signup/check_username",
          {
            username: this.username,
          }
        );
        this.usernameAvailable = true;
        this.registerResponse = "";
      } catch (error) {
        this.usernameAvailable = false;
        this.registerResponse = error.response.data;
      }
    },
  },
};
</script>
