<template>
  <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-300 m-auto">
    <div class="card-body bg-base-300">
      <vee-form
        class="form-control"
        :validation-schema="loginSchema"
        @submit="login"
      >
        <div class="form-control mt-2">
          <vee-field
            type="email"
            placeholder="Email"
            class="input input-bordered"
            name="email"
            v-model="formData.email"
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
            v-model="formData.password"
            required
          />
          <ErrorMessage class="text-red-600" name="password" />
        </div>
        <div class="form-control mt-2">
          <button
            class="btn btn-primary"
            type="submit"
            :disabled="loginAction || !formData.email || !formData.password"
          >
            Login
          </button>
          <div
            class="alert alert-error shadow-lg mt-2 justify-center font-bold"
            v-if="loginResponse.status === 'error'"
          >
            <div>
              <span>{{ loginResponse.message }}</span>
            </div>
          </div>
        </div>
      </vee-form>
      <div class="form-control mt-2">
        <div
          class="alert alert-success shadow-lg mt-2 justify-center font-bold"
          v-if="loginResponse.status === 'success'"
        >
          <div>
            <span>{{ loginResponse.message }}</span>
          </div>
        </div>
      </div>
      <div
        class="alert alert-warning shadow-lg mt-2 justify-center font-bold"
        v-if="loginAction"
      >
        <div>
          <font-awesome-icon icon="fa-solid fa-spinner" class="fa-spin" />
          <span>We're logging you in...</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "appLogin",
  data() {
    return {
      loginSchema: {
        email: "required|email",
        password: "required",
      },
      userLoggedIn: false,
      loginAction: false,
      loginResponse: "",
      formData: {
        email: "",
        password: "",
      },
    };
  },
  methods: {
    async login(values) {
      try {
        console.log(values);
        this.loginAction = true;
        this.loginResponse = "";
        const response = await axios.post(
          import.meta.env.VITE_API_URL + "/login",
          {
            email: values.email,
            password: values.password,
          }
        );
        this.loginAction = false;
        this.loginResponse = response.data;
      } catch (error) {
        console.log(error);
        this.loginAction = false;
        this.loginResponse = error.response.data;
      }
    },
  },
};
</script>

<style scoped></style>
